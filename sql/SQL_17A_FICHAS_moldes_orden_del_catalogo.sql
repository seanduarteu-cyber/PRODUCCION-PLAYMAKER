-- SQL 17A · base de FICHAS (jvgifibnoigpicwklasw) · SQL Editor → New query → pegar todo → Run
-- Catálogo ordenado (noviembre 2026):
--   1. Agrega la columna «orden» a la tabla moldes (el orden del catálogo).
--   2. Agrega los moldes nuevos del catálogo: 83 RB-MUJV02 (Rugby, raglán, cuello v) y 84 HO-MUJV02 (Hockey, raglán, cuello v).
--   3. A cada molde del catálogo le pone su orden y su deporte (la sección del catálogo: Fútbol, Básquetbol, Vóleibol,
--      Hockey, Rugby, Multideporte, Salida y entrenamiento). Los especiales (E01…E11) quedan en la sección de su deporte.
--   4. Los moldes que no están en el catálogo (01 al 10) quedan al final. No se desactivan: eso es aparte (SQL 17B).
-- No borra nada, no cambia números, códigos ni descripciones, y no toca las fichas ya ingresadas.
-- Se puede volver a correr sin problema.

begin;

alter table public.moldes add column if not exists orden integer;

do $$
begin
  if not exists (select 1 from public.moldes where numero = 84) then
    insert into public.moldes (numero, codigo, descripcion, deporte, calce, infantil, prenda, piezas, activo, updated_at)
    values (84, 'HO-MUJV02', 'Hockey, raglán, cuello v', 'Hockey', 'Femenino', false, 'camiseta', '[]', true, now());
  end if;
  if not exists (select 1 from public.moldes where numero = 83) then
    insert into public.moldes (numero, codigo, descripcion, deporte, calce, infantil, prenda, piezas, activo, updated_at)
    values (83, 'RB-MUJV02', 'Rugby, raglán, cuello v', 'Rugby', 'Femenino', false, 'camiseta', '[]', true, now());
  end if;
end $$;

with cat(numero, codigo, deporte, orden) as (values
  (11, 'FUTINMUJCC01', 'Fútbol', 10),
  (12, 'FUTINHOMCC01', 'Fútbol', 20),
  (13, 'FUTMUJU01PRO', 'Fútbol', 30),
  (14, 'FUTHOMU01PRO', 'Fútbol', 40),
  (15, 'FUTMUJV01PRO', 'Fútbol', 50),
  (16, 'FUTHOMV01PRO', 'Fútbol', 60),
  (17, 'FUTMUJU02', 'Fútbol', 70),
  (18, 'FUTHOMU02', 'Fútbol', 80),
  (19, 'FUTINMUJU02', 'Fútbol', 90),
  (20, 'FUTINHOMU02', 'Fútbol', 100),
  (21, 'FUTMUJV02', 'Fútbol', 110),
  (22, 'FUTHOMV02', 'Fútbol', 120),
  (23, 'FUTINMUJV02', 'Fútbol', 130),
  (24, 'FUTINHOMV02', 'Fútbol', 140),
  (25, 'FUTMUJU02PRO', 'Fútbol', 150),
  (26, 'FUTHOMU02PRO', 'Fútbol', 160),
  (27, 'FUTMUJV02PRO', 'Fútbol', 170),
  (28, 'FUTHOMV02PRO', 'Fútbol', 180),
  (104, 'FUTHOMMA01', 'Fútbol', 190),
  (72, 'FUTMUJCCV02', 'Fútbol', 200),
  (73, 'FUTHOMCCV02', 'Fútbol', 210),
  (74, 'FUTINMUJCCV02', 'Fútbol', 220),
  (75, 'FUTINHOMCCV02', 'Fútbol', 230),
  (69, 'FUT-SH', 'Fútbol', 240),
  (29, 'BKMUJU03', 'Básquetbol', 250),
  (30, 'BKHOMU03', 'Básquetbol', 260),
  (31, 'BKINMUJU03', 'Básquetbol', 270),
  (32, 'BKINHOMU03', 'Básquetbol', 280),
  (33, 'BKMUJV03', 'Básquetbol', 290),
  (34, 'BKHOMV03', 'Básquetbol', 300),
  (35, 'BKINMUJV03', 'Básquetbol', 310),
  (36, 'BKINHOMV03', 'Básquetbol', 320),
  (37, 'BKMUJU03RE', 'Básquetbol', 330),
  (38, 'BKHOMU03RE', 'Básquetbol', 340),
  (39, 'BKINMUJU03', 'Básquetbol', 350),
  (40, 'BKINHOMU03RE', 'Básquetbol', 360),
  (41, 'BKMUJU03PRO', 'Básquetbol', 370),
  (42, 'BKHOMU03PRO', 'Básquetbol', 380),
  (43, 'BKMUJV03PRO', 'Básquetbol', 390),
  (44, 'BKHOMV03PRO', 'Básquetbol', 400),
  (45, 'BKSHMUJ', 'Básquetbol', 410),
  (46, 'BK-SH', 'Básquetbol', 420),
  (47, 'BKINSHMUJ', 'Básquetbol', 430),
  (48, 'BKINSHHOM', 'Básquetbol', 440),
  (49, 'BKSHMUJRE', 'Básquetbol', 450),
  (50, 'BK-SH', 'Básquetbol', 460),
  (51, 'BKINSHMUJRE', 'Básquetbol', 470),
  (52, 'BKINSHHOMRE', 'Básquetbol', 480),
  (53, 'BKSHMUJPRO', 'Básquetbol', 490),
  (54, 'BK-SH PRO', 'Básquetbol', 500),
  (55, 'VOMUJV03', 'Vóleibol', 510),
  (56, 'VOMUJMAV03', 'Vóleibol', 520),
  (57, 'VOMUJVCC03', 'Vóleibol', 530),
  (105, 'CA-MUJ', 'Vóleibol', 540),
  (64, 'HO-MUJ03', 'Hockey', 550),
  (65, 'HO-MUJCC03', 'Hockey', 560),
  (106, 'C-FALDA TUBO', 'Hockey', 570),
  (107, 'C-FALDA CRUZADA', 'Hockey', 580),
  (108, 'C-FALDA CON COSTADO', 'Hockey', 590),
  (109, 'C-FALDA CON TAJALÍ', 'Hockey', 600),
  (84, 'HO-MUJV02', 'Hockey', 610),
  (58, 'RB-HOMU02', 'Rugby', 620),
  (59, 'RB-MUJU02', 'Rugby', 630),
  (60, 'RBHOMCC02', 'Rugby', 640),
  (61, 'RBMUJCC02', 'Rugby', 650),
  (62, 'RB-HOMCL02', 'Rugby', 660),
  (63, 'RBMUJCL02', 'Rugby', 670),
  (101, 'RB-HOMUCC02', 'Rugby', 680),
  (102, 'RB-HOMUCC02', 'Rugby', 690),
  (103, 'RBHOMMA02', 'Rugby', 700),
  (110, 'RB-HOMMA02', 'Rugby', 710),
  (111, 'RB-MUJU02', 'Rugby', 720),
  (83, 'RB-MUJV02', 'Rugby', 730),
  (76, 'RB-SHHOM', 'Rugby', 740),
  (78, 'RB-SHMUJ', 'Rugby', 750),
  (79, 'RB-SHIN', 'Rugby', 760),
  (80, 'PE-MUJU03', 'Multideporte', 770),
  (81, 'MUL-HOMU03', 'Multideporte', 780),
  (82, 'MUL-HOMV03', 'Multideporte', 790),
  (66, 'PE-HOM02', 'Salida y entrenamiento', 800),
  (67, 'PE-HOM02', 'Salida y entrenamiento', 810),
  (77, 'PK-HOM02', 'Salida y entrenamiento', 820),
  (70, 'PA-UNI01', 'Salida y entrenamiento', 830),
  (71, 'PA-INUNI01', 'Salida y entrenamiento', 840),
  (68, 'PE-MUJ02', 'Salida y entrenamiento', 850)
)
update public.moldes m
   set deporte = c.deporte, orden = c.orden, updated_at = now()
  from cat c
 where m.numero = c.numero;

-- fuera del catálogo (01 al 10 y cualquier otro): al final, en el orden de su número
update public.moldes set orden = 9000 + numero
 where numero not in (11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 104, 72, 73, 74, 75, 69, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 105, 64, 65, 106, 107, 108, 109, 84, 58, 59, 60, 61, 62, 63, 101, 102, 103, 110, 111, 83, 76, 78, 79, 80, 81, 82, 66, 67, 77, 70, 71, 68);

commit;

notify pgrst, 'reload schema';

-- Revisión: debe decir «moldes del catálogo: 85» y «sin orden: 0»
select (select count(*) from public.moldes where orden < 9000) as moldes_del_catalogo,
       (select count(*) from public.moldes where orden is null) as sin_orden,
       (select count(*) from public.moldes where orden >= 9000) as fuera_del_catalogo,
       (select string_agg(numero::text, ', ' order by numero) from public.moldes where orden >= 9000) as numeros_fuera_del_catalogo;
