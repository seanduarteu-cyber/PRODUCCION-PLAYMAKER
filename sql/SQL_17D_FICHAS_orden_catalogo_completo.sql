-- SQL 17D · base de FICHAS (jvgifibnoigpicwklasw) · SQL Editor → New query → pegar todo → Run
-- Catálogo ordenado COMPLETO (95 moldes): ahora los moldes 01 al 10 están en el catálogo, al inicio de Fútbol.
-- Pone a cada uno de los 95 moldes su orden y su sección (deporte) según el catálogo completo.
-- No borra nada, no cambia números, códigos ni descripciones, y no toca las fichas ya ingresadas.
-- Se puede volver a correr sin problema. (Reemplaza al SQL 17A y al 17B, que ya no hace falta.)

begin;

alter table public.moldes add column if not exists orden integer;

-- los moldes nuevos 83 y 84 (si la base aún no los tiene)
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
  (1, 'FUTMUJU01', 'Fútbol', 10),
  (2, 'FUTHOMU01', 'Fútbol', 20),
  (3, 'FUTINMUJU01', 'Fútbol', 30),
  (4, 'FUTINHOMU01', 'Fútbol', 40),
  (5, 'FUTMUJV01', 'Fútbol', 50),
  (6, 'FUTHOMV01', 'Fútbol', 60),
  (7, 'FUTINMUJV01', 'Fútbol', 70),
  (8, 'FUTINHOMV01', 'Fútbol', 80),
  (9, 'FUTMUJCC01', 'Fútbol', 90),
  (10, 'FUTHOMCC01', 'Fútbol', 100),
  (11, 'FUTINMUJCC01', 'Fútbol', 110),
  (12, 'FUTINHOMCC01', 'Fútbol', 120),
  (13, 'FUTMUJU01PRO', 'Fútbol', 130),
  (14, 'FUTHOMU01PRO', 'Fútbol', 140),
  (15, 'FUTMUJV01PRO', 'Fútbol', 150),
  (16, 'FUTHOMV01PRO', 'Fútbol', 160),
  (17, 'FUTMUJU02', 'Fútbol', 170),
  (18, 'FUTHOMU02', 'Fútbol', 180),
  (19, 'FUTINMUJU02', 'Fútbol', 190),
  (20, 'FUTINHOMU02', 'Fútbol', 200),
  (21, 'FUTMUJV02', 'Fútbol', 210),
  (22, 'FUTHOMV02', 'Fútbol', 220),
  (23, 'FUTINMUJV02', 'Fútbol', 230),
  (24, 'FUTINHOMV02', 'Fútbol', 240),
  (25, 'FUTMUJU02PRO', 'Fútbol', 250),
  (26, 'FUTHOMU02PRO', 'Fútbol', 260),
  (27, 'FUTMUJV02PRO', 'Fútbol', 270),
  (28, 'FUTHOMV02PRO', 'Fútbol', 280),
  (104, 'FUTHOMMA01', 'Fútbol', 290),
  (72, 'FUTMUJCCV02', 'Fútbol', 300),
  (73, 'FUTHOMCCV02', 'Fútbol', 310),
  (74, 'FUTINMUJCCV02', 'Fútbol', 320),
  (75, 'FUTINHOMCCV02', 'Fútbol', 330),
  (69, 'FUT-SH', 'Fútbol', 340),
  (29, 'BKMUJU03', 'Básquetbol', 350),
  (30, 'BKHOMU03', 'Básquetbol', 360),
  (31, 'BKINMUJU03', 'Básquetbol', 370),
  (32, 'BKINHOMU03', 'Básquetbol', 380),
  (33, 'BKMUJV03', 'Básquetbol', 390),
  (34, 'BKHOMV03', 'Básquetbol', 400),
  (35, 'BKINMUJV03', 'Básquetbol', 410),
  (36, 'BKINHOMV03', 'Básquetbol', 420),
  (37, 'BKMUJU03RE', 'Básquetbol', 430),
  (38, 'BKHOMU03RE', 'Básquetbol', 440),
  (39, 'BKINMUJU03', 'Básquetbol', 450),
  (40, 'BKINHOMU03RE', 'Básquetbol', 460),
  (41, 'BKMUJU03PRO', 'Básquetbol', 470),
  (42, 'BKHOMU03PRO', 'Básquetbol', 480),
  (43, 'BKMUJV03PRO', 'Básquetbol', 490),
  (44, 'BKHOMV03PRO', 'Básquetbol', 500),
  (45, 'BKSHMUJ', 'Básquetbol', 510),
  (46, 'BK-SH', 'Básquetbol', 520),
  (47, 'BKINSHMUJ', 'Básquetbol', 530),
  (48, 'BKINSHHOM', 'Básquetbol', 540),
  (49, 'BKSHMUJRE', 'Básquetbol', 550),
  (50, 'BK-SH', 'Básquetbol', 560),
  (51, 'BKINSHMUJRE', 'Básquetbol', 570),
  (52, 'BKINSHHOMRE', 'Básquetbol', 580),
  (53, 'BKSHMUJPRO', 'Básquetbol', 590),
  (54, 'BK-SH PRO', 'Básquetbol', 600),
  (55, 'VOMUJV03', 'Vóleibol', 610),
  (56, 'VOMUJMAV03', 'Vóleibol', 620),
  (57, 'VOMUJVCC03', 'Vóleibol', 630),
  (105, 'CA-MUJ', 'Vóleibol', 640),
  (64, 'HO-MUJ03', 'Hockey', 650),
  (65, 'HO-MUJCC03', 'Hockey', 660),
  (106, 'C-FALDA TUBO', 'Hockey', 670),
  (107, 'C-FALDA CRUZADA', 'Hockey', 680),
  (108, 'C-FALDA CON COSTADO', 'Hockey', 690),
  (109, 'C-FALDA CON TAJALÍ', 'Hockey', 700),
  (84, 'HO-MUJV02', 'Hockey', 710),
  (58, 'RB-HOMU02', 'Rugby', 720),
  (59, 'RB-MUJU02', 'Rugby', 730),
  (60, 'RBHOMCC02', 'Rugby', 740),
  (61, 'RBMUJCC02', 'Rugby', 750),
  (62, 'RB-HOMCL02', 'Rugby', 760),
  (63, 'RBMUJCL02', 'Rugby', 770),
  (101, 'RB-HOMUCC02', 'Rugby', 780),
  (102, 'RB-HOMUCC03', 'Rugby', 790),
  (103, 'RBHOMMA02', 'Rugby', 800),
  (110, 'RB-HOMMA02', 'Rugby', 810),
  (111, 'RB-MUJU02', 'Rugby', 820),
  (83, 'RB-MUJV02', 'Rugby', 830),
  (76, 'RB-SHHOM', 'Rugby', 840),
  (78, 'RB-SHMUJ', 'Rugby', 850),
  (79, 'RB-SHIN', 'Rugby', 860),
  (80, 'PE-MUJU03', 'Multideporte', 870),
  (81, 'MUL-HOMU03', 'Multideporte', 880),
  (82, 'MUL-HOMV03', 'Multideporte', 890),
  (66, 'PE-HOM02', 'Salida y entrenamiento', 900),
  (67, 'PE-HOM02', 'Salida y entrenamiento', 910),
  (77, 'PK-HOM02', 'Salida y entrenamiento', 920),
  (70, 'PA-UNI01', 'Salida y entrenamiento', 930),
  (71, 'PA-INUNI01', 'Salida y entrenamiento', 940),
  (68, 'PE-MUJ02', 'Salida y entrenamiento', 950)
)
update public.moldes m
   set deporte = c.deporte, orden = c.orden, updated_at = now()
  from cat c
 where m.numero = c.numero;

-- un molde que no esté en el catálogo (uno nuevo, agregado después) queda al final, por su número
update public.moldes set orden = 9000 + numero where numero not in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 104, 72, 73, 74, 75, 69, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 105, 64, 65, 106, 107, 108, 109, 84, 58, 59, 60, 61, 62, 63, 101, 102, 103, 110, 111, 83, 76, 78, 79, 80, 81, 82, 66, 67, 77, 70, 71, 68);

commit;

notify pgrst, 'reload schema';

-- Revisión: debe decir «moldes del catálogo: 95» y «fuera del catálogo: 0»
select (select count(*) from public.moldes where orden < 9000) as moldes_del_catalogo,
       (select count(*) from public.moldes where orden is null) as sin_orden,
       (select count(*) from public.moldes where orden >= 9000) as fuera_del_catalogo,
       (select string_agg(numero::text, ', ' order by numero) from public.moldes where orden >= 9000) as numeros_fuera_del_catalogo;
