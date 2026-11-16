-- SQL 21A · base de VENTAS (nnisdusdujcpkrbjqnhe) · SQL Editor → New query → pegar todo → Run
-- Clasificación de gastos (Fase 1 del sistema de costeo y rentabilidad SCR-PMK).
--
-- No borra ni cambia ningún gasto. La tabla «gastos» sigue igual y Ventas sigue funcionando aunque no se suba la
-- página nueva. Crea, encima de los gastos:
--   plan_cuentas         el plan de cuentas único (sección 6 del documento), igual para todos los computadores
--   gasto_cuenta_alias   traduce las categorías que existen hoy (TALLER EXTERNO, UBER…) a una cuenta del plan
--   gasto_reglas         reglas que se aplican antes que nada: «estampado» → Jornales de producción, etc.
--   gasto_raw            el DATO CRUDO: copia de cada gasto tal como se ingresó. Nunca se modifica ni se borra:
--                        cada edición o eliminación en Ventas agrega una versión nueva
--   gasto_clasif         la clasificación de cada gasto: cuenta, mes al que corresponde, de dónde salió
--                        (alias / regla / historial / manual / ia), estado (clasificado / revision) y motivo
--   gestion_parametros   inicio del análisis (abril 2026), sueldo de gerencia, prorrateo 80/10/10, umbral de inversión
--   gasto_auditoria      quién cambió qué y cuándo (antes y después)
-- y agrega a «proveedores»: tipo de documento (factura afecta / exenta / honorarios / sin documento), cuenta
-- habitual y si es socio.
--
-- Al final clasifica todos los gastos que ya existen (primero las reglas, después la traducción de su categoría)
-- y muestra la conciliación: total de gastos = total del dato crudo = clasificado + en revisión.
-- Se puede volver a correr: no duplica nada ni pisa lo que se haya cambiado desde Ventas.

-- ── 0. Funciones de apoyo ──────────────────────────────────────────────────────────────────────────────
-- Texto para comparar: mayúsculas, sin tildes, un solo espacio
create or replace function public.pmk_norm(t text) returns text language sql immutable as $$
  select btrim(regexp_replace(upper(translate(coalesce(t, ''), 'ÁÉÍÓÚÜÑÀÈÌÒÙáéíóúüñàèìòù', 'AEIOUUNAEIOUaeiouunaeiou')), '\s+', ' ', 'g'))
$$;
-- La descripción contiene la palabra o frase completa (no «estampadora» cuando se busca «estampado»)
create or replace function public.pmk_palabra(texto text, palabra text) returns boolean language sql immutable as $$
  select coalesce(nullif(public.pmk_norm(palabra), ''), null) is not null
     and public.pmk_norm(texto) ~ ('\m' || regexp_replace(public.pmk_norm(palabra), '([.^$*+?()\[\]{}|\\])', '\\\1', 'g') || '\M')
$$;
-- El proveedor empieza con el nombre de la regla («SEAN DUARTE (» calza con «SEAN DUARTE»)
create or replace function public.pmk_prov(proveedor text, patron text) returns boolean language sql immutable as $$
  select public.pmk_norm(patron) <> '' and left(public.pmk_norm(proveedor), length(public.pmk_norm(patron))) = public.pmk_norm(patron)
$$;
-- Conversiones que nunca fallan (un dato raro no puede impedir guardar un gasto)
create or replace function public.pmk_fecha(t text) returns date language plpgsql immutable as $$
begin return nullif(btrim(t), '')::date; exception when others then return null; end $$;
create or replace function public.pmk_num(t text) returns numeric language plpgsql immutable as $$
begin return nullif(btrim(t), '')::numeric; exception when others then return null; end $$;

-- ── 1. Tablas ──────────────────────────────────────────────────────────────────────────────────────────
create table if not exists public.plan_cuentas (
  codigo text primary key,                         -- '2.01'
  nombre text not null unique,
  nivel text not null check (nivel in ('1', '2', '3', '4', '5', '6', 'F')),
  tipo text not null check (tipo in ('ingreso', 'variable', 'semifijo', 'fijo', 'bajo_ebitda', 'fuera')),
  prorrateo text check (prorrateo in ('local', 'sueldos')),   -- local = 80/10/10 · sueldos = según sueldos por área
  devengo_servicio boolean not null default false, -- sueldos, arriendo, servicios: van al mes al que corresponden
  es_activo boolean not null default false,        -- inversión: bajo el umbral se revisa
  que_entra text,                                  -- qué entra y qué no (lo lee la persona y, en la Fase 1b, Claude)
  supuesto text,                                   -- algo por confirmar
  activa boolean not null default true,
  orden integer not null default 0,
  actualizado_por text,
  updated_at timestamptz not null default now()
);

create table if not exists public.gasto_cuenta_alias (
  categoria text primary key,                      -- categoría tal como existe en los gastos
  cuenta_codigo text references public.plan_cuentas (codigo),   -- vacío = no se puede traducir: va a revisión
  revisar boolean not null default false,          -- se sugiere la cuenta, pero cada gasto se revisa
  nota text,
  actualizado_por text,
  updated_at timestamptz not null default now()
);

create table if not exists public.gasto_reglas (
  id bigserial primary key,
  tipo text not null check (tipo in ('proveedor', 'palabra', 'proveedor_palabra')),
  proveedor text,                                  -- el proveedor empieza con esto
  palabra text,                                    -- la descripción contiene esta palabra o frase
  accion text not null default 'clasificar' check (accion in ('clasificar', 'revisar')),
  cuenta_codigo text references public.plan_cuentas (codigo),
  prioridad integer not null default 100,          -- menor = se evalúa antes
  motivo text,
  creada_por text,
  origen_gasto_id bigint,                          -- el gasto cuya corrección creó la regla
  activa boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint gasto_reglas_completa check (
    (tipo = 'proveedor' and coalesce(proveedor, '') <> '') or
    (tipo = 'palabra' and coalesce(palabra, '') <> '') or
    (tipo = 'proveedor_palabra' and coalesce(proveedor, '') <> '' and coalesce(palabra, '') <> '')),
  constraint gasto_reglas_cuenta check (accion = 'revisar' or cuenta_codigo is not null)
);

create table if not exists public.gestion_parametros (
  clave text primary key,
  valor jsonb not null,
  descripcion text,
  actualizado_por text,
  updated_at timestamptz not null default now()
);

create table if not exists public.gasto_raw (
  id bigserial primary key,
  gasto_id bigint not null,
  version integer not null,
  operacion text not null check (operacion in ('carga_inicial', 'alta', 'edicion', 'baja')),
  fecha_pago date,
  descripcion text,
  proveedor text,
  monto_bruto numeric,
  categoria_original text,
  medio_pago text,
  observaciones text,
  dato jsonb not null,                             -- la fila completa tal como estaba
  hash text not null,                              -- fecha|monto|descripción|proveedor: detecta duplicados
  archivo_origen text,
  fila_origen integer,
  cargado_por text,
  fecha_carga timestamptz not null default now(),
  constraint gasto_raw_version unique (gasto_id, version)
);
create index if not exists gasto_raw_hash on public.gasto_raw (hash);

create table if not exists public.gasto_clasif (
  gasto_id bigint primary key,
  raw_id bigint,
  cuenta_codigo text references public.plan_cuentas (codigo),   -- vacío mientras está en revisión
  periodo_devengo date,                            -- primer día del mes al que corresponde
  origen text check (origen in ('alias', 'regla', 'historial', 'manual', 'ia')),
  regla_id bigint,
  confianza numeric,
  estado text not null default 'revision' check (estado in ('clasificado', 'revision')),
  motivo text,                                     -- por qué quedó así o por qué se revisa
  sugerencia_codigo text references public.plan_cuentas (codigo),
  pedido_cot text,
  notas text,
  actualizado_por text,
  updated_at timestamptz not null default now(),
  constraint gasto_clasif_cuenta check (estado = 'revision' or cuenta_codigo is not null)
);
create index if not exists gasto_clasif_estado on public.gasto_clasif (estado);

create table if not exists public.gasto_auditoria (
  id bigserial primary key,
  tabla text not null,
  registro text,
  accion text not null,
  antes jsonb,
  despues jsonb,
  usuario text,
  at timestamptz not null default now()
);

alter table public.proveedores add column if not exists tipo_documento text;   -- afecta / exenta / honorarios / sin_documento
alter table public.proveedores add column if not exists cuenta_codigo text;    -- cuenta habitual
alter table public.proveedores add column if not exists es_socio boolean not null default false;

-- ── 2. Plan de cuentas (sección 6) · solo agrega las que faltan: no pisa lo que se cambie desde Ventas ────
insert into public.plan_cuentas (codigo, nombre, nivel, tipo, prorrateo, devengo_servicio, es_activo, activa, orden, supuesto, que_entra) values
 ('1.02', 'Devoluciones a clientes', '1', 'ingreso', null, false, false, true, 102, null, 'Dinero devuelto a clientes por pedidos anulados o con problemas. Resta de las ventas: no es gasto.'),
 ('2.01', 'Telas', '2', 'variable', null, false, false, true, 201, null, 'Compra de tela para las prendas (por kilo o por metro); se costea con los kilos cortados de cada pedido. Prendas compradas hechas van a Prendas para reventa.'),
 ('2.02', 'Talleres de confección', '2', 'variable', null, false, false, true, 202, null, 'Pago a talleres externos o al Taller PMK por coser prendas, aunque venga con boleta de honorarios (ej.: «confección de prendas»).'),
 ('2.03', 'Papel y tinta de sublimación', '2', 'variable', null, false, false, true, 203, null, 'Papel de sublimación, tintas (ej.: tintas Mimaki), papel de protección y líquidos del plotter. Son insumos: nunca inversión.'),
 ('2.04', 'Aplicaciones externas', '2', 'variable', null, false, false, true, 204, null, 'DTF, escudos, bordados, transfer y tapacosturas hechos por terceros para un pedido.'),
 ('2.05', 'Avíos y accesorios', '2', 'variable', null, false, false, true, 205, null, 'Etiquetas, cierres, elásticos, hilos, ojales, cuellos, puños y piezas de costura que van en la prenda.'),
 ('2.06', 'Packaging', '2', 'variable', null, false, false, true, 206, null, 'Bolsas, cajas, cintas de embalaje y material para entregar los pedidos.'),
 ('2.07', 'Prendas para reventa', '2', 'variable', null, false, false, true, 207, null, 'Prendas o productos comprados hechos para vender (medias, polerones, parkas, artículos deportivos).'),
 ('2.08', 'Compra de inventario en liquidación', '2', 'variable', null, false, false, true, 208, null, 'Mercadería comprada en liquidación para revender.'),
 ('2.09', 'Comisiones de venta', '2', 'variable', null, false, false, true, 209, null, 'Comisiones pagadas a vendedores por sus ventas (ej.: honorarios de Antonia Hermosilla, que comisiona 5% sin sueldo base).'),
 ('2.10', 'Royalty a clubes', '2', 'variable', null, false, false, false, 210, 'Hoy no existe (respuesta D3).', 'Pago a clubes por uso de su marca.'),
 ('2.11', 'Despachos a clientes', '2', 'variable', null, false, false, true, 211, null, 'Envíos, courier y Uber para entregar pedidos a clientes.'),
 ('3.01', 'Sueldos de producción', '3', 'semifijo', null, true, false, true, 301, null, 'Sueldos del equipo de producción: corte, confección interna, sublimación, revisión y bodega.'),
 ('3.02', 'Sueldos de diseño', '3', 'semifijo', null, true, false, true, 302, 'Confirmar que diseño es costo de producción.', 'Sueldos del equipo de diseño.'),
 ('3.03', 'Leyes sociales', '3', 'semifijo', 'sueldos', true, false, true, 303, null, 'Cotizaciones previsionales y de salud de todos los sueldos; se reparten por área según los sueldos.'),
 ('3.04', 'Jornales de producción', '3', 'semifijo', null, false, false, true, 304, null, 'Pagos por día a personas de producción: estampado, corte, apoyo (ej.: «estampado», «aseo y estampado»).'),
 ('3.05', 'Honorarios de producción', '3', 'semifijo', null, false, false, true, 305, null, 'Boletas de honorarios de moldería, modelista, escalado de moldes e inventario. Si es confección de prendas, va a Talleres de confección.'),
 ('3.06', 'Mantención y repuestos de máquinas', '3', 'semifijo', null, false, false, true, 306, null, 'Técnicos, repuestos y arreglos de plotter, calandra, máquinas de coser y estampadoras.'),
 ('3.07', 'Arriendo', '3', 'semifijo', 'local', true, false, true, 307, null, 'Arriendo del local. Se reparte 80% producción, 10% ventas y 10% administración.'),
 ('3.08', 'Luz, agua y servicios del local', '3', 'semifijo', 'local', true, false, true, 308, null, 'Luz, agua, gas, gastos comunes y basura del local. Se reparte 80/10/10.'),
 ('3.09', 'Aseo', '3', 'semifijo', 'local', false, false, true, 309, null, 'Artículos y servicios de aseo del local. Un pago por estampado va a Jornales de producción. Se reparte 80/10/10.'),
 ('3.10', 'Mantención del local', '3', 'semifijo', 'local', false, false, true, 310, null, 'Arreglos menores del local: gasfitería, pintura, ferretería. Obras grandes y duraderas son Mejoras al local. Se reparte 80/10/10.'),
 ('3.11', 'Traslados a talleres', '3', 'semifijo', null, false, false, true, 311, null, 'Uber o movilización para llevar y traer trabajo de los talleres.'),
 ('4.01', 'Sueldos de ventas y marketing', '4', 'fijo', null, true, false, true, 401, null, 'Sueldos del equipo de ventas y marketing. Las comisiones van en Comisiones de venta.'),
 ('4.02', 'Publicidad Meta', '4', 'fijo', null, false, false, true, 402, null, 'Anuncios en Facebook e Instagram.'),
 ('4.03', 'Publicidad Google', '4', 'fijo', null, false, false, true, 403, null, 'Anuncios en Google.'),
 ('4.04', 'Agencia de marketing', '4', 'fijo', null, false, false, true, 404, null, 'Agencias de publicidad y de gestión de anuncios.'),
 ('4.05', 'Herramientas de marketing', '4', 'fijo', null, false, false, true, 405, null, 'Plataformas de marketing y atención (ej.: Heat Suit, ManyChat).'),
 ('4.06', 'Sitio web y hosting', '4', 'fijo', null, false, false, true, 406, null, 'Dominio, hosting y desarrollo del sitio web.'),
 ('4.07', 'Contenido y fotografía', '4', 'fijo', null, false, false, true, 407, null, 'Fotos, videos y producción de contenido.'),
 ('4.08', 'Eventos y activaciones', '4', 'fijo', null, false, false, true, 408, null, 'Stands, eventos deportivos, activaciones y regalos de marketing.'),
 ('4.09', 'Viajes comerciales', '4', 'fijo', null, false, false, true, 409, null, 'Viajes para vender o visitar clientes.'),
 ('4.10', 'Honorarios de marketing', '4', 'fijo', null, false, false, true, 410, null, 'Boletas de honorarios por trabajos de marketing.'),
 ('5.01', 'Contabilidad y asesorías', '5', 'fijo', null, false, false, true, 501, null, 'Contador, abogados y asesorías (ej.: honorarios del contador).'),
 ('5.02', 'Software e IA', '5', 'fijo', null, false, false, true, 502, null, 'Suscripciones de software, sistemas e inteligencia artificial.'),
 ('5.03', 'Banco y comisiones', '5', 'fijo', null, false, false, true, 503, null, 'Mantención de la cuenta corriente y comisiones bancarias.'),
 ('5.04', 'Insumos de oficina', '5', 'fijo', null, false, false, true, 504, null, 'Papelería y artículos de oficina.'),
 ('5.05', 'Telefonía e internet', '5', 'fijo', null, true, false, true, 505, null, 'Planes de teléfono e internet.'),
 ('5.06', 'Trámites, permisos y prevención', '5', 'fijo', null, false, false, true, 506, null, 'Patentes, permisos, trámites (ej.: INAPI) y prevención de riesgos.'),
 ('5.07', 'Bienestar del personal', '5', 'fijo', null, false, false, true, 507, null, 'Almuerzos, celebraciones, agua y bonos de bienestar del equipo.'),
 ('5.08', 'Alumnos en práctica', '5', 'fijo', null, false, false, true, 508, null, 'Pagos a practicantes.'),
 ('5.09', 'Movilización', '5', 'fijo', null, false, false, true, 509, null, 'Uber, estacionamiento, combustible y traslados del equipo. No incluye despachos a clientes ni traslados a talleres.'),
 ('6.01', 'Intereses de préstamos', '6', 'bajo_ebitda', null, false, false, true, 601, null, 'Intereses de créditos. La parte de capital va fuera del resultado (Cuotas de préstamos).'),
 ('6.02', 'Impuesto a la renta', '6', 'bajo_ebitda', null, false, false, true, 602, null, 'Impuesto anual a la renta y pagos provisionales (PPM).'),
 ('F.01', 'Pago de IVA', 'F', 'fuera', null, false, false, true, 901, null, 'Pago mensual del IVA al SII (F29). No es gasto.'),
 ('F.02', 'Inversión en máquinas y equipos', 'F', 'fuera', null, false, true, true, 902, null, 'Máquinas, computadores y muebles que duran más de 1 año y cuestan $300.000 o más. Bajo ese monto es gasto.'),
 ('F.03', 'Mejoras al local', 'F', 'fuera', null, false, true, true, 903, null, 'Obras duraderas en el local arrendado (ej.: instalación eléctrica del Taller PMK, piso). Activo que se deprecia.'),
 ('F.04', 'Garantía de arriendo', 'F', 'fuera', null, false, false, true, 904, null, 'Garantía del local: se recupera, no es gasto.'),
 ('F.05', 'Cuotas de préstamos', 'F', 'fuera', null, false, false, true, 905, 'Falta separar capital (fuera) e intereses (gasto financiero): Fase 3.', 'Cuotas de créditos.'),
 ('F.06', 'Pagos a socios', 'F', 'fuera', null, false, false, true, 906, null, 'Pagos a Sean Duarte y Silvia Urbina: anticipos, sueldos de socios y retiros. El resultado usa en su lugar un sueldo de gerencia fijo (parámetro).'),
 ('F.07', 'Gastos personales de socios', 'F', 'fuera', null, false, false, true, 907, null, 'Cuentas personales o de la casa pagadas por la empresa, y reembolsos sin respaldo.'),
 ('F.08', 'Ajustes y errores', 'F', 'fuera', null, false, false, true, 908, null, 'Transferencias por error, reversas y movimientos que se compensan.')
on conflict (codigo) do nothing;

-- ── 3. Traducción de las categorías actuales (y de las antiguas de la lista de Ventas) ──────────────────
insert into public.gasto_cuenta_alias (categoria, cuenta_codigo, revisar, nota) values
 ('TELAS', '2.01', false, null), ('TALLERES DE CONFECCIÓN', '2.02', false, null), ('TALLER EXTERNO', '2.02', false, null),
 ('TALLER PMK', '2.02', false, null), ('PAPEL Y TINTA SUBLIMACIÓN', '2.03', false, null), ('APLICACIONES EXTERNAS', '2.04', false, null),
 ('SERVICIO DE BORDADOS', '2.04', false, null), ('AVÍOS Y ACCESORIOS', '2.05', false, null),
 ('INSUMOS PRODUCCION', '2.05', true, 'Insumos de producción: según el detalle es Avíos o Packaging.'),
 ('PACKAGING', '2.06', false, null), ('PRENDAS PARA REVENTA', '2.07', false, null), ('PROVEEDOR DE PRENDAS', '2.07', false, null),
 ('PROVEEDOR INDUMENTARIAS', '2.07', false, null), ('PROVEDOR DE ARTICULOS DEPORTIVOS', '2.07', false, null),
 ('COMPRA DE INVENTARIO EN LIQUIDACIÓN', '2.08', false, null), ('DESPACHOS A CLIENTES', '2.11', false, null), ('ENVIOS', '2.11', false, null),
 ('SUELDOS PRODUCCIÓN', '3.01', false, null), ('SUELDOS DISEÑO', '3.02', false, null), ('LEYES SOCIALES', '3.03', false, null),
 ('JORNALES DE PRODUCCIÓN', '3.04', false, null), ('HONORARIOS DE PRODUCCIÓN', '3.05', false, null),
 ('MANTENCIÓN Y REPUESTOS DE MÁQUINAS', '3.06', false, null), ('ARRIENDO', '3.07', false, null),
 ('LUZ, AGUA Y SERVICIOS DEL LOCAL', '3.08', false, null), ('CONSUMOS BASICOS', '3.08', false, null), ('ASEO', '3.09', false, null),
 ('MANTENCIÓN DEL LOCAL', '3.10', false, null), ('TRASLADOS A TALLERES', '3.11', false, null),
 ('SUELDOS VENTAS Y MARKETING', '4.01', false, null), ('PUBLICIDAD META', '4.02', false, null), ('PUBLICIDAD GOOGLE', '4.03', false, null),
 ('AGENCIA DE MARKETING', '4.04', false, null), ('AGENCIA ADS', '4.04', false, null), ('HERRAMIENTAS DE MARKETING', '4.05', false, null),
 ('SITIO WEB Y HOSTING', '4.06', false, null), ('HOSTING', '4.06', false, null), ('CONTENIDO Y FOTOGRAFÍA', '4.07', false, null),
 ('EVENTOS Y ACTIVACIONES', '4.08', false, null), ('VIAJES COMERCIALES', '4.09', false, null), ('HONORARIOS DE MARKETING', '4.10', false, null),
 ('CONTABILIDAD Y ASESORÍAS', '5.01', false, null), ('SOFTWARE E IA', '5.02', false, null), ('SOFTWARE', '5.02', false, null), ('IA', '5.02', false, null),
 ('BANCO Y COMISIONES', '5.03', false, null), ('MANTENCION CUENTA CORRIENTE EMPRESA', '5.03', false, null),
 ('INSUMOS DE OFICINA', '5.04', false, null), ('TELEFONÍA E INTERNET', '5.05', false, null), ('TRÁMITES, PERMISOS Y PREVENCIÓN', '5.06', false, null),
 ('BIENESTAR DEL PERSONAL', '5.07', false, null), ('ALMUERZO', '5.07', false, null), ('ALUMNOS EN PRÁCTICA', '5.08', false, null),
 ('MOVILIZACIÓN', '5.09', false, null), ('UBER', '5.09', false, null), ('COMBUSTIBLE', '5.09', false, null), ('ASIGNACION MOVILIZACION', '5.09', false, null),
 ('CRÉDITO Y PRÉSTAMOS', 'F.05', false, null), ('IMPUESTOS (IVA)', 'F.01', false, null),
 ('IMPUESTO SII', 'F.01', true, 'Impuesto SII: confirmar si es IVA (F29) o impuesto a la renta.'),
 ('INVERSIÓN EN MÁQUINAS Y EQUIPOS', 'F.02', false, null), ('INVERSION', 'F.02', false, null),
 ('MOBILIARIO', 'F.02', false, null), ('INFRAESTRUCTURA/MOBILIARIO', 'F.02', false, null),
 ('GARANTÍA DE ARRIENDO', 'F.04', false, null), ('REMUNERACIÓN DE SOCIOS', 'F.06', false, null),
 ('GASTOS PERSONALES DE SOCIOS', 'F.07', false, null),
 ('REEMBOLSO SOCIO', 'F.07', true, 'Reembolso a socio: exige boleta o factura; sin respaldo es gasto personal.'),
 ('AJUSTES Y ERRORES', 'F.08', false, null), ('DEVOLUCIONES A CLIENTES', '1.02', false, null), ('DEVOLUCIÓN A CLIENTE', '1.02', false, null),
 ('POR IDENTIFICAR', null, true, 'Por identificar: elegir la cuenta.'),
 ('OTROS', null, true, 'Otros: elegir la cuenta.'),
 ('HONORARIOS', null, true, 'Honorarios: ¿producción, taller, marketing o comisión?'),
 ('REMUNERACIONES', null, true, 'Remuneraciones: ¿de qué área?'),
 ('RRSS', null, true, 'Redes sociales: ¿publicidad, herramienta o contenido?')
on conflict (categoria) do nothing;
-- el nombre de cada cuenta también se traduce a sí mismo (los gastos nuevos guardan el nombre de la cuenta)
insert into public.gasto_cuenta_alias (categoria, cuenta_codigo, revisar)
select pc.nombre, pc.codigo, false from public.plan_cuentas pc
where not exists (select 1 from public.gasto_cuenta_alias a where public.pmk_norm(a.categoria) = public.pmk_norm(pc.nombre));

-- ── 4. Reglas iniciales (sección 8 del documento y respuestas D2 y S3) · solo la primera vez ─────────────
insert into public.gasto_reglas (tipo, proveedor, palabra, accion, cuenta_codigo, prioridad, motivo, creada_por)
select v.* from (values
 ('palabra', null, 'NO SE', 'revisar', null, 5, 'La descripción dice «no sé»: identificar el gasto.', 'sistema'),
 ('palabra', null, 'NO ME ACUERDO', 'revisar', null, 5, 'La descripción dice «no me acuerdo»: identificar el gasto.', 'sistema'),
 ('palabra', null, 'ESTAMPADO', 'clasificar', '3.04', 10, 'El estampado es jornal de producción, en cualquier categoría.', 'sistema'),
 ('palabra', null, 'TINTAS MIMAKI', 'clasificar', '2.03', 10, 'Las tintas son insumo de sublimación, no inversión.', 'sistema'),
 ('palabra', null, 'CONFECCION DE PRENDAS', 'clasificar', '2.02', 10, 'Confección de prendas es taller, aunque venga con boleta de honorarios.', 'sistema'),
 ('palabra', null, 'COMPRA TELA', 'clasificar', '2.01', 10, 'Compra de tela es Telas, aunque esté en otra categoría.', 'sistema'),
 ('palabra', null, 'HONORARIOS CONTADOR', 'clasificar', '5.01', 10, 'Los honorarios del contador son Contabilidad y asesorías.', 'sistema'),
 ('proveedor_palabra', 'ANTONIA HERMOSILLA', 'HONORARIOS', 'clasificar', '2.09', 10, 'Antonia Hermosilla comisiona 5% sin sueldo base: sus honorarios son comisión (D2).', 'sistema'),
 ('proveedor_palabra', 'RODOLFO RIQUELME', 'ELECTRICO', 'clasificar', 'F.03', 10, 'Instalación eléctrica del Taller PMK: activo depreciable (S3).', 'sistema'),
 ('palabra', null, 'REEMBOLSO', 'revisar', null, 50, 'Reembolso: exige boleta o factura; sin respaldo es gasto personal o retiro.', 'sistema'),
 ('proveedor', 'SEAN DUARTE', null, 'revisar', null, 50, 'Pago a socio: ¿gasto de la empresa, reembolso con respaldo o retiro?', 'sistema')
) as v(tipo, proveedor, palabra, accion, cuenta_codigo, prioridad, motivo, creada_por)
where not exists (select 1 from public.gasto_reglas);

-- ── 5. Parámetros (respuestas D5, D7, D8, D9 y S5) · solo los que faltan ─────────────────────────────────────
insert into public.gestion_parametros (clave, valor, descripcion) values
 ('inicio_analisis', '"2026-04-01"', 'Desde qué mes se analizan gastos y ventas (D9: los meses anteriores no estaban ordenados).'),
 ('sueldo_gerencia_mensual', '4500000', 'Sueldo de gerencia a valor de mercado, por mes (D5). Se usa en el resultado en vez de los pagos a socios.'),
 ('prorrateo_local', '{"produccion": 80, "ventas": 10, "administracion": 10}', 'Reparto de arriendo, luz, agua, aseo y mantención del local (D7).'),
 ('umbral_inversion', '300000', 'Desde este monto, y con vida útil de más de 1 año, un bien es activo fijo (D8).'),
 ('tasa_iva', '0.19', 'IVA.'),
 ('regimen_tributario', '"Pro Pyme General (art. 14 D)"', 'Régimen tributario de la empresa (S5). Lo usa la Fase 3 (IVA e impuesto a la renta) junto al contador.')
on conflict (clave) do nothing;

-- ── 6. Clasificación automática: reglas → traducción de la categoría → revisión ─────────────────────────
create or replace function public.gasto_clasificar_auto(j jsonb)
returns table (cuenta text, origen text, regla bigint, estado text, motivo text, sugerencia text)
language plpgsql stable set search_path = public as $$
declare
  d text := pmk_norm(j ->> 'descripcion');
  p text := pmk_norm(j ->> 'proveedor');
  c text := pmk_norm(j ->> 'categoria');
  m numeric := pmk_num(j ->> 'monto');
  r record; a record; umbral numeric;
begin
  select g.* into r from gasto_reglas g
   where g.activa and (
     (g.tipo = 'palabra' and pmk_palabra(d, g.palabra)) or
     (g.tipo = 'proveedor' and pmk_prov(p, g.proveedor)) or
     (g.tipo = 'proveedor_palabra' and pmk_prov(p, g.proveedor) and pmk_palabra(d, g.palabra)))
   order by g.prioridad, g.id limit 1;
  select al.cuenta_codigo, al.revisar, al.nota into a from gasto_cuenta_alias al where pmk_norm(al.categoria) = c limit 1;
  if r.id is not null and r.accion = 'clasificar' then
    cuenta := r.cuenta_codigo; origen := 'regla'; regla := r.id; estado := 'clasificado'; motivo := r.motivo; sugerencia := null;
  elsif r.id is not null then
    cuenta := null; origen := 'regla'; regla := r.id; estado := 'revision'; motivo := r.motivo; sugerencia := coalesce(r.cuenta_codigo, a.cuenta_codigo);
  elsif a.cuenta_codigo is not null and not a.revisar then
    cuenta := a.cuenta_codigo; origen := 'alias'; regla := null; estado := 'clasificado'; motivo := null; sugerencia := null;
  else
    cuenta := null; origen := 'alias'; regla := null; estado := 'revision'; sugerencia := a.cuenta_codigo;
    motivo := coalesce(a.nota, case when c = '' then 'Gasto sin categoría.' else 'Categoría sin traducción: ' || (j ->> 'categoria') || '.' end);
  end if;
  -- inversión bajo el umbral: puede ser gasto (mantención, oficina) o parte de una obra mayor
  if cuenta is not null and exists (select 1 from plan_cuentas pc where pc.codigo = cuenta and pc.es_activo) then
    umbral := coalesce((select pmk_num(gp.valor #>> '{}') from gestion_parametros gp where gp.clave = 'umbral_inversion'), 300000);
    if coalesce(m, 0) < umbral then
      sugerencia := cuenta; cuenta := null; estado := 'revision';
      motivo := 'Bajo el umbral de inversión ($' || replace(to_char(umbral, 'FM999,999,999'), ',', '.') || '): ¿es gasto o parte de una obra mayor?';
    end if;
  end if;
  return next;
end $$;

-- Agrega una versión al dato crudo (nunca modifica las anteriores)
create or replace function public.gasto_raw_agregar(j jsonb, op text, archivo text, usuario text)
returns bigint language plpgsql security definer set search_path = public as $$
declare gid bigint := pmk_num(j ->> 'id')::bigint; v integer; nuevo bigint;
begin
  select coalesce(max(version), 0) + 1 into v from gasto_raw where gasto_id = gid;
  insert into gasto_raw (gasto_id, version, operacion, fecha_pago, descripcion, proveedor, monto_bruto, categoria_original,
                         medio_pago, observaciones, dato, hash, archivo_origen, cargado_por)
  values (gid, v, op, pmk_fecha(j ->> 'fecha'), j ->> 'descripcion', j ->> 'proveedor', pmk_num(j ->> 'monto'), j ->> 'categoria',
          j ->> 'metodo_pago', j ->> 'observaciones', j,
          md5(concat_ws('|', pmk_fecha(j ->> 'fecha'), pmk_num(j ->> 'monto'), pmk_norm(j ->> 'descripcion'), pmk_norm(j ->> 'proveedor'))),
          archivo, usuario)
  returning id into nuevo;
  return nuevo;
end $$;

-- Cada vez que Ventas guarda, edita o elimina un gasto: versión nueva del crudo y clasificación automática si
-- no tiene una. Si algo falla aquí, el gasto se guarda igual (la conciliación muestra lo que quedó sin crudo).
create or replace function public.gasto_registrar() returns trigger
language plpgsql security definer set search_path = public as $$
declare j jsonb; gid bigint; rid bigint; op text; x record; ya record;
begin
  begin
    if tg_op = 'DELETE' then j := to_jsonb(old); op := 'baja';
    else j := to_jsonb(new); op := case when tg_op = 'INSERT' then 'alta' else 'edicion' end; end if;
    if tg_op = 'UPDATE' and to_jsonb(old) = to_jsonb(new) then return null; end if;   -- se guardó igual: nada cambió
    gid := pmk_num(j ->> 'id')::bigint;
    rid := gasto_raw_agregar(j, op, null, null);
    if tg_op = 'DELETE' then
      delete from gasto_clasif where gasto_id = gid;
      return null;
    end if;
    select * into ya from gasto_clasif where gasto_id = gid;
    select * into x from gasto_clasificar_auto(j);
    if ya.gasto_id is null then
      insert into gasto_clasif (gasto_id, raw_id, cuenta_codigo, periodo_devengo, origen, regla_id, estado, motivo, sugerencia_codigo, actualizado_por)
      values (gid, rid, x.cuenta, date_trunc('month', pmk_fecha(j ->> 'fecha'))::date, x.origen, x.regla, x.estado, x.motivo, x.sugerencia, 'automático');
    elsif ya.origen in ('alias', 'regla') then
      -- clasificación automática: se recalcula con el gasto editado
      update gasto_clasif set raw_id = rid, cuenta_codigo = x.cuenta, origen = x.origen, regla_id = x.regla, estado = x.estado,
             motivo = x.motivo, sugerencia_codigo = x.sugerencia, actualizado_por = 'automático', updated_at = now(),
             periodo_devengo = case when date_trunc('month', pmk_fecha(to_jsonb(old) ->> 'fecha'))::date = periodo_devengo
                                    then date_trunc('month', pmk_fecha(j ->> 'fecha'))::date else periodo_devengo end
       where gasto_id = gid;
    else
      update gasto_clasif set raw_id = rid where gasto_id = gid;   -- elegida por una persona: se respeta
    end if;
  exception when others then
    raise warning 'gasto_registrar: %', sqlerrm;
  end;
  return null;
end $$;

drop trigger if exists gastos_registrar on public.gastos;
create trigger gastos_registrar after insert or update or delete on public.gastos
  for each row execute function public.gasto_registrar();

-- El dato crudo y la auditoría no se modifican ni se borran
create or replace function public.pmk_inmutable() returns trigger language plpgsql as $$
begin raise exception 'El registro de % no se modifica ni se borra: es el dato original.', tg_table_name; end $$;
drop trigger if exists gasto_raw_inmutable on public.gasto_raw;
create trigger gasto_raw_inmutable before update or delete on public.gasto_raw for each row execute function public.pmk_inmutable();
drop trigger if exists gasto_raw_sin_truncate on public.gasto_raw;
create trigger gasto_raw_sin_truncate before truncate on public.gasto_raw for each statement execute function public.pmk_inmutable();
drop trigger if exists gasto_auditoria_inmutable on public.gasto_auditoria;
create trigger gasto_auditoria_inmutable before update or delete on public.gasto_auditoria for each row execute function public.pmk_inmutable();
drop trigger if exists gasto_auditoria_sin_truncate on public.gasto_auditoria;
create trigger gasto_auditoria_sin_truncate before truncate on public.gasto_auditoria for each statement execute function public.pmk_inmutable();

-- Auditoría: quién cambió qué, con el antes y el después
create or replace function public.gasto_auditar() returns trigger
language plpgsql security definer set search_path = public as $$
declare n jsonb := case when tg_op = 'DELETE' then null else to_jsonb(new) end;
        o jsonb := case when tg_op = 'INSERT' then null else to_jsonb(old) end;
begin
  if tg_op = 'UPDATE' and (n - 'updated_at') = (o - 'updated_at') then return null; end if;
  insert into gasto_auditoria (tabla, registro, accion, antes, despues, usuario)
  values (tg_table_name, coalesce(n, o) ->> tg_argv[0], tg_op, o, n,
          coalesce(n ->> 'actualizado_por', n ->> 'creada_por', o ->> 'actualizado_por'));
  return null;
end $$;
drop trigger if exists gasto_clasif_auditar on public.gasto_clasif;
create trigger gasto_clasif_auditar after insert or update or delete on public.gasto_clasif for each row execute function public.gasto_auditar('gasto_id');
drop trigger if exists gasto_reglas_auditar on public.gasto_reglas;
create trigger gasto_reglas_auditar after insert or update or delete on public.gasto_reglas for each row execute function public.gasto_auditar('id');
drop trigger if exists plan_cuentas_auditar on public.plan_cuentas;
create trigger plan_cuentas_auditar after insert or update or delete on public.plan_cuentas for each row execute function public.gasto_auditar('codigo');
drop trigger if exists gasto_cuenta_alias_auditar on public.gasto_cuenta_alias;
create trigger gasto_cuenta_alias_auditar after insert or update or delete on public.gasto_cuenta_alias for each row execute function public.gasto_auditar('categoria');
drop trigger if exists gestion_parametros_auditar on public.gestion_parametros;
create trigger gestion_parametros_auditar after insert or update or delete on public.gestion_parametros for each row execute function public.gasto_auditar('clave');

-- Vuelve a aplicar reglas y traducciones a los gastos clasificados automáticamente (nunca a los elegidos por
-- una persona). Ventas lo usa al crear una regla o cambiar una traducción.
create or replace function public.gasto_reclasificar(p_usuario text default null)
returns jsonb language plpgsql security definer set search_path = public as $$
declare n_rev integer; n_cambio integer;
begin
  select count(*) into n_rev from gasto_clasif where origen in ('alias', 'regla');
  with s as (
    select pmk_num(to_jsonb(g) ->> 'id')::bigint as gid, x.*
      from gastos g cross join lateral gasto_clasificar_auto(to_jsonb(g)) x
  )
  update gasto_clasif c
     set cuenta_codigo = s.cuenta, origen = s.origen, regla_id = s.regla, estado = s.estado, motivo = s.motivo,
         sugerencia_codigo = s.sugerencia, actualizado_por = coalesce(p_usuario, 'automático'), updated_at = now()
    from s
   where c.gasto_id = s.gid and c.origen in ('alias', 'regla')
     and (c.cuenta_codigo, c.origen, c.regla_id, c.estado, c.motivo, c.sugerencia_codigo)
         is distinct from (s.cuenta, s.origen, s.regla, s.estado, s.motivo, s.sugerencia);
  get diagnostics n_cambio = row_count;
  return jsonb_build_object('revisados', n_rev, 'cambiados', n_cambio);
end $$;

-- Conciliación: total de gastos = total del dato crudo = clasificado + en revisión (diferencia $0)
create or replace view public.v_gastos_conciliacion as
with g as (select pmk_num(to_jsonb(x) ->> 'id')::bigint as id, coalesce(pmk_num(to_jsonb(x) ->> 'monto'), 0) as monto,
                  pmk_fecha(to_jsonb(x) ->> 'fecha') as fecha from public.gastos x),
     ini as (select coalesce(pmk_fecha((select valor #>> '{}' from public.gestion_parametros where clave = 'inicio_analisis')), date '2026-04-01') as d),
     r as (select distinct on (gasto_id) gasto_id, monto_bruto, operacion from public.gasto_raw order by gasto_id, version desc)
select
  (select count(*) from g) as gastos,
  (select coalesce(sum(monto), 0) from g) as total_gastos,
  (select coalesce(sum(r.monto_bruto), 0) from r where r.operacion <> 'baja') as total_crudo,
  (select count(*) from g where not exists (select 1 from r where r.gasto_id = g.id and r.operacion <> 'baja')) as gastos_sin_crudo,
  (select coalesce(sum(g.monto), 0) from g join public.gasto_clasif c on c.gasto_id = g.id where c.estado = 'clasificado') as total_clasificado,
  (select coalesce(sum(g.monto), 0) from g join public.gasto_clasif c on c.gasto_id = g.id where c.estado = 'revision') as total_en_revision,
  (select count(*) from g join public.gasto_clasif c on c.gasto_id = g.id where c.estado = 'revision') as gastos_en_revision,
  (select count(*) from g join public.gasto_clasif c on c.gasto_id = g.id, ini where c.estado = 'revision' and g.fecha >= ini.d) as en_revision_desde_inicio,
  (select count(*) from g where not exists (select 1 from public.gasto_clasif c where c.gasto_id = g.id)) as gastos_sin_clasificacion,
  (select coalesce(sum(monto), 0) from g) - (select coalesce(sum(g.monto), 0) from g join public.gasto_clasif c on c.gasto_id = g.id) as diferencia;

-- ── 7. Carga inicial: dato crudo y clasificación de los gastos que ya existen ───────────────────────────
select public.gasto_raw_agregar(to_jsonb(g), 'carga_inicial', 'gastos de Ventas al ' || to_char(now(), 'DD-MM-YYYY'), 'SQL 21A')
  from public.gastos g
 where not exists (select 1 from public.gasto_raw r where r.gasto_id = public.pmk_num(to_jsonb(g) ->> 'id')::bigint);

insert into public.gasto_clasif (gasto_id, raw_id, cuenta_codigo, periodo_devengo, origen, regla_id, estado, motivo, sugerencia_codigo, actualizado_por)
select s.gid, (select max(r.id) from public.gasto_raw r where r.gasto_id = s.gid), s.cuenta,
       date_trunc('month', s.fecha)::date, s.origen, s.regla, s.estado, s.motivo, s.sugerencia, 'carga inicial'
  from (select public.pmk_num(to_jsonb(g) ->> 'id')::bigint as gid, public.pmk_fecha(to_jsonb(g) ->> 'fecha') as fecha, x.*
          from public.gastos g cross join lateral public.gasto_clasificar_auto(to_jsonb(g)) x) s
 where not exists (select 1 from public.gasto_clasif c where c.gasto_id = s.gid);

-- ── 8. Acceso (como las demás tablas de Ventas: la app entra con la llave pública) ──────────────────────
alter table public.plan_cuentas enable row level security;
alter table public.gasto_cuenta_alias enable row level security;
alter table public.gasto_reglas enable row level security;
alter table public.gestion_parametros enable row level security;
alter table public.gasto_clasif enable row level security;
alter table public.gasto_raw enable row level security;
alter table public.gasto_auditoria enable row level security;

drop policy if exists plan_cuentas_todo on public.plan_cuentas;
create policy plan_cuentas_todo on public.plan_cuentas for all to anon, authenticated using (true) with check (true);
drop policy if exists gasto_cuenta_alias_todo on public.gasto_cuenta_alias;
create policy gasto_cuenta_alias_todo on public.gasto_cuenta_alias for all to anon, authenticated using (true) with check (true);
drop policy if exists gasto_reglas_todo on public.gasto_reglas;
create policy gasto_reglas_todo on public.gasto_reglas for all to anon, authenticated using (true) with check (true);
drop policy if exists gestion_parametros_todo on public.gestion_parametros;
create policy gestion_parametros_todo on public.gestion_parametros for all to anon, authenticated using (true) with check (true);
drop policy if exists gasto_clasif_todo on public.gasto_clasif;
create policy gasto_clasif_todo on public.gasto_clasif for all to anon, authenticated using (true) with check (true);
drop policy if exists gasto_raw_leer on public.gasto_raw;
create policy gasto_raw_leer on public.gasto_raw for select to anon, authenticated using (true);
drop policy if exists gasto_auditoria_leer on public.gasto_auditoria;
create policy gasto_auditoria_leer on public.gasto_auditoria for select to anon, authenticated using (true);

-- sin «delete»: las reglas y cuentas se desactivan, no se borran; el crudo y la auditoría solo se leen
grant select, insert, update on public.plan_cuentas, public.gasto_cuenta_alias, public.gasto_reglas,
                                public.gestion_parametros, public.gasto_clasif to anon, authenticated;
grant select on public.gasto_raw, public.gasto_auditoria, public.v_gastos_conciliacion to anon, authenticated;
grant usage, select on sequence public.gasto_reglas_id_seq to anon, authenticated;
revoke all on function public.gasto_raw_agregar(jsonb, text, text, text) from public, anon, authenticated;
grant execute on function public.gasto_reclasificar(text) to anon, authenticated;

notify pgrst, 'reload schema';

-- Revisión: debe decir «clasificación lista» y diferencia 0
select 'clasificación lista' as estado, c.gastos, c.total_gastos, c.total_crudo, c.total_clasificado, c.total_en_revision,
       c.en_revision_desde_inicio as en_revision_desde_abril, c.gastos_sin_crudo, c.gastos_sin_clasificacion, c.diferencia
  from public.v_gastos_conciliacion c;
