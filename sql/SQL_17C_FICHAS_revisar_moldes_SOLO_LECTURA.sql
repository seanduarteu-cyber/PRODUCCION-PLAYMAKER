-- SQL 17C · base de FICHAS (jvgifibnoigpicwklasw) · SOLO REVISA: no cambia nada
-- ¿Están en el panel de fichas todos los moldes del catálogo ordenado? Compara los 95 moldes del catálogo con la tabla
-- moldes (la que lee el panel). SQL Editor → New query → pegar todo → Run. Arriba quedan los que tienen algo.
--   OK                → está, activo, con su código y su sección
--   FALTA             → no está en la base (el panel no lo ofrece)
--   DESACTIVADO       → está, pero no se ofrece en las fichas
--   CÓDIGO DISTINTO   → el N° existe con otro código
--   SECCIÓN DISTINTA  → la base lo tiene en otro deporte (lo corrige el SQL 17D)
--   FUERA DEL CATÁLOGO→ está en la base pero no en el catálogo ordenado (un molde nuevo, agregado después)

with cat(numero, etiqueta, codigo, seccion, orden) as (values
  (1, '01', 'FUTMUJU01', 'Fútbol', 1),
  (2, '02', 'FUTHOMU01', 'Fútbol', 2),
  (3, '03', 'FUTINMUJU01', 'Fútbol', 3),
  (4, '04', 'FUTINHOMU01', 'Fútbol', 4),
  (5, '05', 'FUTMUJV01', 'Fútbol', 5),
  (6, '06', 'FUTHOMV01', 'Fútbol', 6),
  (7, '07', 'FUTINMUJV01', 'Fútbol', 7),
  (8, '08', 'FUTINHOMV01', 'Fútbol', 8),
  (9, '09', 'FUTMUJCC01', 'Fútbol', 9),
  (10, '10', 'FUTHOMCC01', 'Fútbol', 10),
  (11, '11', 'FUTINMUJCC01', 'Fútbol', 11),
  (12, '12', 'FUTINHOMCC01', 'Fútbol', 12),
  (13, '13', 'FUTMUJU01PRO', 'Fútbol', 13),
  (14, '14', 'FUTHOMU01PRO', 'Fútbol', 14),
  (15, '15', 'FUTMUJV01PRO', 'Fútbol', 15),
  (16, '16', 'FUTHOMV01PRO', 'Fútbol', 16),
  (17, '17', 'FUTMUJU02', 'Fútbol', 17),
  (18, '18', 'FUTHOMU02', 'Fútbol', 18),
  (19, '19', 'FUTINMUJU02', 'Fútbol', 19),
  (20, '20', 'FUTINHOMU02', 'Fútbol', 20),
  (21, '21', 'FUTMUJV02', 'Fútbol', 21),
  (22, '22', 'FUTHOMV02', 'Fútbol', 22),
  (23, '23', 'FUTINMUJV02', 'Fútbol', 23),
  (24, '24', 'FUTINHOMV02', 'Fútbol', 24),
  (25, '25', 'FUTMUJU02PRO', 'Fútbol', 25),
  (26, '26', 'FUTHOMU02PRO', 'Fútbol', 26),
  (27, '27', 'FUTMUJV02PRO', 'Fútbol', 27),
  (28, '28', 'FUTHOMV02PRO', 'Fútbol', 28),
  (104, 'E04', 'FUTHOMMA01', 'Fútbol', 29),
  (72, '72', 'FUTMUJCCV02', 'Fútbol', 30),
  (73, '73', 'FUTHOMCCV02', 'Fútbol', 31),
  (74, '74', 'FUTINMUJCCV02', 'Fútbol', 32),
  (75, '75', 'FUTINHOMCCV02', 'Fútbol', 33),
  (69, '69', 'FUT-SH', 'Fútbol', 34),
  (29, '29', 'BKMUJU03', 'Básquetbol', 35),
  (30, '30', 'BKHOMU03', 'Básquetbol', 36),
  (31, '31', 'BKINMUJU03', 'Básquetbol', 37),
  (32, '32', 'BKINHOMU03', 'Básquetbol', 38),
  (33, '33', 'BKMUJV03', 'Básquetbol', 39),
  (34, '34', 'BKHOMV03', 'Básquetbol', 40),
  (35, '35', 'BKINMUJV03', 'Básquetbol', 41),
  (36, '36', 'BKINHOMV03', 'Básquetbol', 42),
  (37, '37', 'BKMUJU03RE', 'Básquetbol', 43),
  (38, '38', 'BKHOMU03RE', 'Básquetbol', 44),
  (39, '39', 'BKINMUJU03', 'Básquetbol', 45),
  (40, '40', 'BKINHOMU03RE', 'Básquetbol', 46),
  (41, '41', 'BKMUJU03PRO', 'Básquetbol', 47),
  (42, '42', 'BKHOMU03PRO', 'Básquetbol', 48),
  (43, '43', 'BKMUJV03PRO', 'Básquetbol', 49),
  (44, '44', 'BKHOMV03PRO', 'Básquetbol', 50),
  (45, '45', 'BKSHMUJ', 'Básquetbol', 51),
  (46, '46', 'BK-SH', 'Básquetbol', 52),
  (47, '47', 'BKINSHMUJ', 'Básquetbol', 53),
  (48, '48', 'BKINSHHOM', 'Básquetbol', 54),
  (49, '49', 'BKSHMUJRE', 'Básquetbol', 55),
  (50, '50', 'BK-SH', 'Básquetbol', 56),
  (51, '51', 'BKINSHMUJRE', 'Básquetbol', 57),
  (52, '52', 'BKINSHHOMRE', 'Básquetbol', 58),
  (53, '53', 'BKSHMUJPRO', 'Básquetbol', 59),
  (54, '54', 'BK-SH PRO', 'Básquetbol', 60),
  (55, '55', 'VOMUJV03', 'Vóleibol', 61),
  (56, '56', 'VOMUJMAV03', 'Vóleibol', 62),
  (57, '57', 'VOMUJVCC03', 'Vóleibol', 63),
  (105, 'E05', 'CA-MUJ', 'Vóleibol', 64),
  (64, '64', 'HO-MUJ03', 'Hockey', 65),
  (65, '65', 'HO-MUJCC03', 'Hockey', 66),
  (106, 'E06', 'C-FALDA TUBO', 'Hockey', 67),
  (107, 'E07', 'C-FALDA CRUZADA', 'Hockey', 68),
  (108, 'E08', 'C-FALDA CON COSTADO', 'Hockey', 69),
  (109, 'E09', 'C-FALDA CON TAJALÍ', 'Hockey', 70),
  (84, '84', 'HO-MUJV02', 'Hockey', 71),
  (58, '58', 'RB-HOMU02', 'Rugby', 72),
  (59, '59', 'RB-MUJU02', 'Rugby', 73),
  (60, '60', 'RBHOMCC02', 'Rugby', 74),
  (61, '61', 'RBMUJCC02', 'Rugby', 75),
  (62, '62', 'RB-HOMCL02', 'Rugby', 76),
  (63, '63', 'RBMUJCL02', 'Rugby', 77),
  (101, 'E01', 'RB-HOMUCC02', 'Rugby', 78),
  (102, 'E02', 'RB-HOMUCC02', 'Rugby', 79),
  (103, 'E03', 'RBHOMMA02', 'Rugby', 80),
  (110, 'E10', 'RB-HOMMA02', 'Rugby', 81),
  (111, 'E11', 'RB-MUJU02', 'Rugby', 82),
  (83, '83', 'RB-MUJV02', 'Rugby', 83),
  (76, '76', 'RB-SHHOM', 'Rugby', 84),
  (78, '78', 'RB-SHMUJ', 'Rugby', 85),
  (79, '79', 'RB-SHIN', 'Rugby', 86),
  (80, '80', 'PE-MUJU03', 'Multideporte', 87),
  (81, '81', 'MUL-HOMU03', 'Multideporte', 88),
  (82, '82', 'MUL-HOMV03', 'Multideporte', 89),
  (66, '66', 'PE-HOM02', 'Salida y entrenamiento', 90),
  (67, '67', 'PE-HOM02', 'Salida y entrenamiento', 91),
  (77, '77', 'PK-HOM02', 'Salida y entrenamiento', 92),
  (70, '70', 'PA-UNI01', 'Salida y entrenamiento', 93),
  (71, '71', 'PA-INUNI01', 'Salida y entrenamiento', 94),
  (68, '68', 'PE-MUJ02', 'Salida y entrenamiento', 95)
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
       (select count(*) from cruce where estado = 'OK') || ' de 95 OK' as resumen
from cruce
order by case when estado = 'OK' then 2 when estado like 'FUERA%' then 1 else 0 end, orden_catalogo, numero;
