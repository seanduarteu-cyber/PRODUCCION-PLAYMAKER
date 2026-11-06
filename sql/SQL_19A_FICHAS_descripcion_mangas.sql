-- SQL 19A · base de FICHAS (jvgifibnoigpicwklasw) · SQL Editor → New query → pegar todo → Run
-- Descripción de la manga en cada camiseta, según el código del molde:
--   …01 → manga clásica · …02 → manga raglán (las dos se hacen en manga corta o larga) · …03 → sin mangas
-- (ej: «Fútbol, cuello redondo» → «Fútbol, manga clásica, cuello redondo»; «Básquetbol, cuello v» → «Básquetbol, sin mangas, cuello v»).
-- Cambia solo la descripción de 61 camisetas, y solo si el código coincide. No toca números, códigos ni fichas.
-- Se puede volver a correr sin problema.

with nuevo(numero, codigo, descripcion) as (values
  (1, 'FUTMUJU01', 'Fútbol, manga clásica, cuello redondo'),
  (2, 'FUTHOMU01', 'Fútbol, manga clásica, cuello redondo'),
  (3, 'FUTINMUJU01', 'Fútbol infantil, manga clásica, cuello redondo'),
  (4, 'FUTINHOMU01', 'Fútbol infantil, manga clásica, cuello redondo'),
  (5, 'FUTMUJV01', 'Fútbol, manga clásica, cuello v'),
  (6, 'FUTHOMV01', 'Fútbol, manga clásica, cuello v'),
  (7, 'FUTINMUJV01', 'Fútbol infantil, manga clásica, cuello v'),
  (8, 'FUTINHOMV01', 'Fútbol infantil, manga clásica, cuello v'),
  (9, 'FUTMUJCC01', 'Fútbol, manga clásica, cuello camisero'),
  (10, 'FUTHOMCC01', 'Fútbol, manga clásica, cuello camisero'),
  (11, 'FUTINMUJCC01', 'Fútbol infantil, manga clásica, cuello camisero'),
  (12, 'FUTINHOMCC01', 'Fútbol infantil, manga clásica, cuello camisero'),
  (13, 'FUTMUJU01PRO', 'Fútbol, pro, manga clásica, cuello redondo'),
  (14, 'FUTHOMU01PRO', 'Fútbol, pro, manga clásica, cuello redondo'),
  (15, 'FUTMUJV01PRO', 'Fútbol, pro, manga clásica, cuello v'),
  (16, 'FUTHOMV01PRO', 'Fútbol, pro, manga clásica, cuello v'),
  (17, 'FUTMUJU02', 'Fútbol, manga raglán, cuello redondo'),
  (18, 'FUTHOMU02', 'Fútbol, manga raglán, cuello redondo'),
  (19, 'FUTINMUJU02', 'Fútbol infantil, manga raglán, cuello redondo'),
  (20, 'FUTINHOMU02', 'Fútbol infantil, manga raglán, cuello redondo'),
  (21, 'FUTMUJV02', 'Fútbol, manga raglán, cuello v'),
  (22, 'FUTHOMV02', 'Fútbol, manga raglán, cuello v'),
  (23, 'FUTINMUJV02', 'Fútbol infantil, manga raglán, cuello v'),
  (24, 'FUTINHOMV02', 'Fútbol infantil, manga raglán, cuello v'),
  (25, 'FUTMUJU02PRO', 'Fútbol, pro, manga raglán, cuello redondo'),
  (26, 'FUTHOMU02PRO', 'Fútbol, pro, manga raglán, cuello redondo'),
  (27, 'FUTMUJV02PRO', 'Fútbol, pro, manga raglán, cuello v'),
  (28, 'FUTHOMV02PRO', 'Fútbol, pro, manga raglán, cuello v'),
  (29, 'BKMUJU03', 'Básquetbol, sin mangas, cuello redondo'),
  (30, 'BKHOMU03', 'Básquetbol, sin mangas, cuello redondo'),
  (31, 'BKINMUJU03', 'Básquetbol infantil, sin mangas, cuello redondo'),
  (32, 'BKINHOMU03', 'Básquetbol infantil, sin mangas, cuello redondo'),
  (33, 'BKMUJV03', 'Básquetbol, sin mangas, cuello v'),
  (34, 'BKHOMV03', 'Básquetbol, sin mangas, cuello v'),
  (35, 'BKINMUJV03', 'Básquetbol infantil, sin mangas, cuello v'),
  (36, 'BKINHOMV03', 'Básquetbol infantil, sin mangas, cuello v'),
  (37, 'BKMUJU03RE', 'Básquetbol, reversible, sin mangas, cuello redondo'),
  (38, 'BKHOMU03RE', 'Básquetbol, reversible, sin mangas, cuello redondo'),
  (39, 'BKINMUJU03', 'Básquetbol infantil, reversible, sin mangas, cuello redondo'),
  (40, 'BKINHOMU03RE', 'Básquetbol infantil, reversible, sin mangas, cuello redondo'),
  (41, 'BKMUJU03PRO', 'Básquetbol, pro, sin mangas, cuello redondo'),
  (42, 'BKHOMU03PRO', 'Básquetbol, pro, sin mangas, cuello redondo'),
  (43, 'BKMUJV03PRO', 'Básquetbol, pro, sin mangas, cuello v'),
  (44, 'BKHOMV03PRO', 'Básquetbol, pro, sin mangas, cuello v'),
  (58, 'RB-HOMU02', 'Rugby, manga raglán, cuello redondo'),
  (59, 'RB-MUJU02', 'Rugby, manga raglán, cuello redondo'),
  (60, 'RBHOMCC02', 'Rugby, manga raglán, cuello camisero'),
  (61, 'RBMUJCC02', 'Rugby, manga raglán, cuello camisero'),
  (62, 'RB-HOMCL02', 'Rugby, manga raglán, cuello clásico'),
  (63, 'RBMUJCL02', 'Rugby, manga raglán, cuello clásico'),
  (72, 'FUTMUJCCV02', 'Fútbol, manga raglán, cuello camisero en v'),
  (73, 'FUTHOMCCV02', 'Fútbol, manga raglán, cuello camisero en v'),
  (74, 'FUTINMUJCCV02', 'Fútbol infantil, manga raglán, cuello camisero en v'),
  (75, 'FUTINHOMCCV02', 'Fútbol infantil, manga raglán, cuello camisero en v'),
  (83, 'RB-MUJV02', 'Rugby, manga raglán, cuello v'),
  (84, 'HO-MUJV02', 'Hockey, manga raglán, cuello v'),
  (101, 'RB-HOMUCC02', 'Rugby, manga raglán con costados, cuello redondo'),
  (103, 'RBHOMMA02', 'Rugby, manga raglán, cuello mao'),
  (104, 'FUTHOMMA01', 'Fútbol, manga clásica, cuello mao'),
  (110, 'RB-HOMMA02', 'Rugby, manga raglán, cuello mao'),
  (111, 'RB-MUJU02', 'Rugby, manga raglán, cuello mao')
)
update public.moldes m
   set descripcion = n.descripcion, updated_at = now()
  from nuevo n
 where m.numero = n.numero and m.codigo = n.codigo and m.descripcion is distinct from n.descripcion;

notify pgrst, 'reload schema';

-- Revisión: las camisetas con su manga (las …03 y la E02 dicen «sin mangas»)
select case when numero between 101 and 199 then 'E' || lpad((numero - 100)::text, 2, '0') else lpad(numero::text, 2, '0') end as molde, codigo, descripcion
  from public.moldes where prenda = 'camiseta' order by orden, numero;
