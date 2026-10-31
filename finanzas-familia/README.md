# Finanzas Familia

App para **registrar a diario los gastos, boletas, deudas y pagos en cuotas** de la familia, compartida entre los miembros (por ejemplo, tú y tu pareja) y con **descarga en Excel o PDF**. Funciona en **Android y iPhone** como aplicación instalable (PWA), sin pasar por las tiendas.

Cada familia es un **centro de costos separado y privado**: cualquier persona se registra con su propia cuenta, crea su familia e invita a los suyos. Nadie fuera de la familia puede ver sus datos, **ni siquiera quien administra la app** (ver [Privacidad](#privacidad)).

La lógica de cálculo replica la planilla `PRESUPUESTO_CASA` (hojas Presupuesto, Registro, Boletas y Deudas), y la app puede **importar esa planilla** para no partir de cero.

**Dónde funciona:** la app se publica en **Netlify** (la página) y guarda los datos en **Supabase** (base de datos y cuentas). Ambos tienen plan gratuito.

---

## Qué hace

| Pantalla | Para qué sirve |
|---|---|
| **Resumen** | Saldo proyectado a fin de mes, ya pagado, por pagar, saldo hoy, estado del mes (superávit / ajustado / déficit), distribución Esencial-Deudas-Prescindible-Ahorro contra metas, avance por categoría, ingresos del mes y alertas de boletas vencidas o cuotas pendientes. |
| **Gastos** | Registro diario: monto, categoría, descripción, fecha, medio de pago y foto de la boleta. Muestra quién registró cada gasto. Búsqueda y filtros por categoría o persona. **"Pagar en cuotas"** convierte una compra con tarjeta en un plan de cuotas futuras. |
| **Boletas** | Cuentas por pagar (luz, agua, gas, colegio…). Pagos parciales, boletas vencidas ("VENCIDA hace N días: pedir monto actualizado"), traspasadas (convenio / boleta nueva). Lo no pagado se arrastra a los meses siguientes. |
| **Cuotas** | Deudas, convenios, préstamos y compras en cuotas. Cuotas del mes con botón "Pagar", deuda restante, % del ingreso (alerta sobre 30%), prioridad por tasa (estrategia avalancha) y **proyección de 12 meses**. Admite cuotas variables por mes y cierre anticipado. |
| **Más** | Presupuesto por categoría, ingresos fijos, metas; familia y miembros (invitar, roles); **Excel y PDF** del mes, del año o de un rango; **importar planilla**; privacidad. |

Los cambios de un miembro aparecen **al instante** en el teléfono de los demás. Además: modo oscuro, montos en pesos chilenos y botón "atrás" de Android. Para registrar se necesita internet.

---

## Privacidad

1. **Familias aisladas.** El [esquema de la base de datos](supabase/esquema.sql) solo permite leer a los miembros de cada familia, y toda escritura pasa por funciones que validan la membresía. No se pueden listar familias ni invitaciones. Las invitaciones son de **un solo uso** y vencen a los 7 días.
2. **Cifrado de extremo a extremo.** Al crear la familia se genera en el teléfono una **clave de la familia** (ej. `K7PD-3MXQ-9TRW-HZ2B-6NVC`). Con ella se cifra (AES-256-GCM) todo el contenido —montos, descripciones, categorías, presupuesto, boletas, deudas y fotos— **antes de subirlo**. La clave nunca llega al servidor: viaja en la invitación (en la parte `#` del enlace, que el navegador no envía) y queda guardada en cada teléfono.
3. **Qué ve el administrador del proyecto Supabase:** correos y nombres de las cuentas, nombre de cada familia, quién es miembro, y el mes y la fecha de creación de cada registro. **No** ve ningún monto ni descripción: solo texto cifrado.

> ⚠️ Guarda la clave de la familia (foto, nota o papel). Si se pierde en todos los teléfonos, los datos no se pueden recuperar. Los archivos Excel/PDF descargados no van cifrados.

---

## Publicarla (≈ 15 minutos, sin instalar nada en tu computador)

### Paso 1 · Supabase (la base de datos)

1. Entra a <https://supabase.com/dashboard> y crea un proyecto nuevo (**New project**), por ejemplo `finanzas-familia`, región **South America (São Paulo)**. Usa un proyecto nuevo y no uno que ya tengas: así sus tablas no se mezclan con otras.
2. Ve a **SQL Editor › New query**, pega **todo** el contenido de [`supabase/esquema.sql`](supabase/esquema.sql) y presiona **Run**. Debe decir *Success*.
3. Ve a **Authentication › Sign In / Providers › Email** y elige cómo se registran las personas:
   - **Desactivar "Confirm email"** (recomendado para empezar): cada persona crea su cuenta y entra de inmediato.
   - Dejarlo activado: cada persona debe abrir un correo de confirmación antes de entrar. El servicio de correo incluido en Supabase permite muy pocos correos por hora; si muchas familias se registran el mismo día, conviene configurar un SMTP propio (Authentication › Emails › SMTP Settings).
4. Ve a **Project Settings › API** (o el botón **Connect**) y copia:
   - **Project URL** (ej. `https://abcd1234.supabase.co`)
   - la llave pública **anon** / **publishable**

   Esta llave es pública por diseño. Lo que protege los datos son las reglas del esquema y el cifrado. **Nunca** uses la llave *service_role* / *secret* en la app.

### Paso 2 · Netlify (la página de la app)

1. Entra a <https://app.netlify.com> › **Add new site › Import an existing project › GitHub** y elige el repositorio **PRODUCCION-PLAYMAKER**.
2. En **Branch to deploy** elige `claude/charming-goldberg-he40po` (o `main`, si ya lo uniste). El resto (carpeta, comando y publicación) Netlify lo lee solo del archivo `netlify.toml`.
3. En **Environment variables** agrega:

   | Key | Value |
   |---|---|
   | `VITE_SUPABASE_URL` | la Project URL del paso 1 |
   | `VITE_SUPABASE_ANON_KEY` | la llave anon / publishable del paso 1 |

4. Presiona **Deploy**. En uno o dos minutos tendrás una dirección como `https://algo-al-azar.netlify.app`. Puedes cambiarla en **Site configuration › Change site name**, por ejemplo `finanzas-dy.netlify.app`.
5. Vuelve a Supabase › **Authentication › URL Configuration**: en **Site URL** pon la dirección de Netlify y agrégala también en **Redirect URLs**. Así los correos (confirmación, olvidé mi contraseña) llevan a tu app.

Cada vez que se suba un cambio a esa rama en GitHub, Netlify vuelve a publicar la app solo, y los teléfonos se actualizan solos. Si cambias las variables, publica de nuevo en **Deploys › Trigger deploy**.

### Paso 3 · Instalar en los teléfonos

- **Android (Chrome):** abre la dirección › menú ⋮ › **Instalar app** (o *Agregar a pantalla principal*).
- **iPhone (Safari):** abre la dirección › botón **Compartir** › **Agregar a inicio**.

Queda un ícono como cualquier app y abre a pantalla completa.

### Paso 4 · Empezar a usarla

1. Crea tu cuenta › **Crear mi familia** (ej. "Casa DY") › **guarda la clave** que aparece.
2. *(Opcional)* **Más › Descargar Excel o PDF › Importar mi planilla**: sube `PRESUPUESTO_CASA_DY_2026-27.xlsx` y se cargan categorías, presupuesto, ingresos, gastos, boletas y la proyección de deudas.
3. Revisa **Más › Presupuesto** (montos por categoría e ingresos fijos).
4. **Más › Familia › Invitar a mi pareja** › *Enviar por WhatsApp*. Ella abre el enlace, crea su cuenta y entra directo a la misma familia.

### Paso 5 · Compartirla con otras familias

Envíales la dirección de la app. Cada una crea su cuenta y **su propia familia**, con su propia clave. Sus datos quedan separados y cifrados: tú no puedes verlos.

### Sobre los planes gratuitos

- **Supabase** pausa los proyectos gratuitos que pasan una semana sin uso. Si se usa a diario no pasa; si llega a pausarse, se reactiva desde el panel sin perder datos.
- **Netlify** alcanza de sobra para una app como esta.

---

## Excel y PDF

En **Más › Descargar Excel o PDF** eliges un mes, un año o un rango:

- **Excel (.xlsx)**: hoja *Presupuesto* (o *Resumen por mes* + una hoja por mes), *Registro*, *Ingresos*, *Boletas* y *Deudas* con la proyección de cuotas, con el mismo formato que la planilla.
- **PDF**: informe con resumen, categorías, distribución, ingresos, gastos, boletas por pagar y proyección de cuotas.

En el teléfono puedes **Descargar** o **Compartir** (WhatsApp, correo, Archivos/Drive).

---

## Para desarrolladores

```text
finanzas-familia/
├── src/
│   ├── lib/          cálculos (calc.ts), cifrado (crypto.ts), Excel/PDF, importador, formatos
│   ├── data/         backends Supabase / Firebase / local (demo), acciones, estado (store.tsx)
│   ├── screens/      pantallas
│   └── components/   componentes de interfaz
├── supabase/esquema.sql   tablas, permisos (RLS) y funciones
├── tests/            pruebas (cálculos, cifrado, importador, seguridad)
└── ../netlify.toml   publicación en Netlify
```

| Comando | Qué hace |
|---|---|
| `npm run dev` | Servidor de desarrollo. Sin variables, abre en **modo demostración** (datos solo en el navegador) |
| `npm test` | Pruebas de cálculos (iguales a la planilla), cifrado e importación |
| `npm run test:supabase` | Pruebas de seguridad del esquema contra Supabase local (`npx supabase start`, aplicar `supabase/esquema.sql`, y definir `SUPABASE_URL` y `SUPABASE_ANON_KEY`) |
| `npm run build` | Compila la app en `dist/` |

La app elige el backend según las variables (`.env.local` o Netlify): **Supabase** si hay `VITE_SUPABASE_*`, **Firebase** si hay `VITE_FIREBASE_*` (alternativa, con `firestore.rules`; pruebas con `npm run test:reglas`), y si no hay ninguna, **modo demostración**.

**Tecnología:** React 19 + TypeScript + Vite, PWA (vite-plugin-pwa), Supabase (Postgres con Row Level Security, Auth y Realtime), Web Crypto (AES-GCM + PBKDF2), ExcelJS y jsPDF.

### ¿Y en Play Store / App Store?

No es necesario, porque la PWA se instala desde el navegador. Si más adelante quieres publicarla en las tiendas, se puede empaquetar la misma app con [PWABuilder](https://www.pwabuilder.com) (Android) o [Capacitor](https://capacitorjs.com) (Android/iPhone; para iPhone se requiere una cuenta de Apple Developer).
