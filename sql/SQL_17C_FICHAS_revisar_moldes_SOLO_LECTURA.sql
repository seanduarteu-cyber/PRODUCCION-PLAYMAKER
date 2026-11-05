-- SQL 17C · base de FICHAS (jvgifibnoigpicwklasw) · SOLO REVISA: no cambia nada
-- ¿Están en el panel de fichas todos los moldes del catálogo ordenado? Compara los 85 moldes del catálogo con la tabla
-- moldes (la que lee el panel). SQL Editor → New query → pegar todo → Run. Arriba quedan los que tienen algo.
--   OK                → está, activo, con su código y su sección
--   FALTA             → no está en la base (el panel no lo ofrece)
--   DESACTIVADO       → está, pero no se ofrece en las fichas
--   CÓDIGO DISTINTO   → el N° existe con otro código
--   SECCIÓN DISTINTA  → la base lo tiene en otro deporte (lo corrige el SQL 17A)
--   FUERA DEL CATÁLOGO→ está en la base pero no en el catálogo ordenado (ej: 01 al 10)

with cat(numero, etiqueta, codigo, seccion, orden) as (values
  (11, '11', 'FUTINMUJCC01', 'Fútbol', 1),
  (12, '12', 'FUTINHOMCC01', 'Fútbol', 2),
  (13, '13', 'FUTMUJU01PRO', 'Fútbol', 3),
  (14, '14', 'FUTHOMU01PRO', 'Fútbol', 4),
  (15, '15', 'FUTMUJV01PRO', 'Fútbol', 5),
  (16, '16', 'FUTHOMV01PRO', 'Fútbol', 6),
  (17, '17', 'FUTMUJU02', 'Fútbol', 7),
  (18, '18', 'FUTHOMU02', 'Fútbol', 8),
  (19, '19', 'FUTINMUJU02', 'Fútbol', 9),
  (20, '20', 'FUTINHOMU02', 'Fútbol', 10),
  (21, '21', 'FUTMUJV02', 'Fútbol', 11),
  (22, '22', 'FUTHOMV02', 'Fútbol', 12),
  (23, '23', 'FUTINMUJV02', 'Fútbol', 13),
  (24, '24', 'FUTINHOMV02', 'Fútbol', 14),
  (25, '25', 'FUTMUJU02PRO', 'Fútbol', 15),
  (26, '26', 'FUTHOMU02PRO', 'Fútbol', 16),
  (27, '27', 'FUTMUJV02PRO', 'Fútbol', 17),
  (28, '28', 'FUTHOMV02PRO', 'Fútbol', 18),
  (104, 'E04', 'FUTHOMMA01', 'Fútbol', 19),
  (72, '72', 'FUTMUJCCV02', 'Fútbol', 20),
  (73, '73', 'FUTHOMCCV02', 'Fútbol', 21),
  (74, '74', 'FUTINMUJCCV02', 'Fútbol', 22),
  (75, '75', 'FUTINHOMCCV02', 'Fútbol', 23),
  (69, '69', 'FUT-SH', 'Fútbol', 24),
  (29, '29', 'BKMUJU03', 'Básquetbol', 25),
  (30, '30', 'BKHOMU03', 'Básquetbol', 26),
  (31, '31', 'BKINMUJU03', 'Básquetbol', 27),
  (32, '32', 'BKINHOMU03', 'Básquetbol', 28),
  (33, '33', 'BKMUJV03', 'Básquetbol', 29),
  (34, '34', 'BKHOMV03', 'Básquetbol', 30),
  (35, '35', 'BKINMUJV03', 'Básquetbol', 31),
  (36, '36', 'BKINHOMV03', 'Básquetbol', 32),
  (37, '37', 'BKMUJU03RE', 'Básquetbol', 33),
  (38, '38', 'BKHOMU03RE', 'Básquetbol', 34),
  (39, '39', 'BKINMUJU03', 'Básquetbol', 35),
  (40, '40', 'BKINHOMU03RE', 'Básquetbol', 36),
  (41, '41', 'BKMUJU03PRO', 'Básquetbol', 37),
  (42, '42', 'BKHOMU03PRO', 'Básquetbol', 38),
  (43, '43', 'BKMUJV03PRO', 'Básquetbol', 39),
  (44, '44', 'BKHOMV03PRO', 'Básquetbol', 40),
  (45, '45', 'BKSHMUJ', 'Básquetbol', 41),
  (46, '46', 'BK-SH', 'Básquetbol', 42),
  (47, '47', 'BKINSHMUJ', 'Básquetbol', 43),
  (48, '48', 'BKINSHHOM', 'Básquetbol', 44),
  (49, '49', 'BKSHMUJRE', 'Básquetbol', 45),
  (50, '50', 'BK-SH', 'Básquetbol', 46),
  (51, '51', 'BKINSHMUJRE', 'Básquetbol', 47),
  (52, '52', 'BKINSHHOMRE', 'Básquetbol', 48),
  (53, '53', 'BKSHMUJPRO', 'Básquetbol', 49),
  (54, '54', 'BK-SH PRO', 'Básquetbol', 50),
  (55, '55', 'VOMUJV03', 'Vóleibol', 51),
  (56, '56', 'VOMUJMAV03', 'Vóleibol', 52),
  (57, '57', 'VOMUJVCC03', 'Vóleibol', 53),
  (105, 'E05', 'CA-MUJ', 'Vóleibol', 54),
  (64, '64', 'HO-MUJ03', 'Hockey', 55),
  (65, '65', 'HO-MUJCC03', 'Hockey', 56),
  (106, 'E06', 'C-FALDA TUBO', 'Hockey', 57),
  (107, 'E07', 'C-FALDA CRUZADA', 'Hockey', 58),
  (108, 'E08', 'C-FALDA CON COSTADO', 'Hockey', 59),
  (109, 'E09', 'C-FALDA CON TAJALÍ', 'Hockey', 60),
  (84, '84', 'HO-MUJV02', 'Hockey', 61),
  (58, '58', 'RB-HOMU02', 'Rugby', 62),
  (59, '59', 'RB-MUJU02', 'Rugby', 63),
  (60, '60', 'RBHOMCC02', 'Rugby', 64),
  (61, '61', 'RBMUJCC02', 'Rugby', 65),
  (62, '62', 'RB-HOMCL02', 'Rugby', 66),
  (63, '63', 'RBMUJCL02', 'Rugby', 67),
  (101, 'E01', 'RB-HOMUCC02', 'Rugby', 68),
  (102, 'E02', 'RB-HOMUCC02', 'Rugby', 69),
  (103, 'E03', 'RBHOMMA02', 'Rugby', 70),
  (110, 'E10', 'RB-HOMMA02', 'Rugby', 71),
  (111, 'E11', 'RB-MUJU02', 'Rugby', 72),
  (83, '83', 'RB-MUJV02', 'Rugby', 73),
  (76, '76', 'RB-SHHOM', 'Rugby', 74),
  (78, '78', 'RB-SHMUJ', 'Rugby', 75),
  (79, '79', 'RB-SHIN', 'Rugby', 76),
  (80, '80', 'PE-MUJU03', 'Multideporte', 77),
  (81, '81', 'MUL-HOMU03', 'Multideporte', 78),
  (82, '82', 'MUL-HOMV03', 'Multideporte', 79),
  (66, '66', 'PE-HOM02', 'Salida y entrenamiento', 80),
  (67, '67', 'PE-HOM02', 'Salida y entrenamiento', 81),
  (77, '77', 'PK-HOM02', 'Salida y entrenamiento', 82),
  (70, '70', 'PA-UNI01', 'Salida y entrenamiento', 83),
  (71, '71', 'PA-INUNI01', 'Salida y entrenamiento', 84),
  (68, '68', 'PE-MUJ02', 'Salida y entrenamiento', 85)
),
cruce as (
  select coalesce(c.numero, m.numero) as numero,
         coalesce(c.etiqueta, case when m.numero between 101 and 199 then 'E' || lpad((m.numero - 100)::text, 2, '0') else lpad(m.numero::text, 2, '0') end) as molde,
         c.codigo as codigo_catalogo, m.codigo as codigo_base, c.seccion as seccion_catalogo, m.deporte as deporte_base, m.activo,
         case
           when m.numero is null then 'FALTA'
           when c.numero is null then 'FUERA DEL CATÁLOGO' || case when m.activo is false then ' (desactivado)' else ' (activo)' end
           when m.activo is false then 'DESACTIVADO'
           when upper(trim(m.codigo)) <> upper(c.codigo) then 'CÓDIGO DISTINTO'
           when coalesce(m.deporte, '') <> c.seccion then 'SECCIÓN DISTINTA'
           else 'OK' end as estado,
         coalesce(c.orden, 1000) as orden_catalogo
  from cat c full join public.moldes m on m.numero = c.numero
)
select molde, estado, codigo_catalogo, codigo_base, seccion_catalogo, deporte_base,
       (select count(*) from cruce where estado = 'OK') || ' de 85 OK' as resumen
from cruce
order by case when estado = 'OK' then 2 when estado like 'FUERA%' then 1 else 0 end, orden_catalogo, numero;
