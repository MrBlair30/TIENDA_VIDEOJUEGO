#Crear la bd
CREATE DATABASE tienda_videojuegos;
#Usar la bd
USE tienda_videojuegos;

#Creación de las tablas
#usuario
CREATE TABLE usuario(
id_usuario INTEGER AUTO_INCREMENT PRIMARY KEY,
nombre_usuario TEXT(50) NOT NULL,
apellido_usuario TEXT(80) NOT NULL,
color VARCHAR(10) NOT NULL,
usuario VARCHAR(80) NOT NULL,
contrasena VARCHAR(8) NOT NULL,
rol ENUM('admin','cliente'),
UNIQUE(usuario)
);

#videojuegos
CREATE TABLE videojuegos(
id_videojuego INTEGER AUTO_INCREMENT PRIMARY KEY,
nombre_videojuego TEXT(50) NOT NULL,
categoria VARCHAR(80) NOT NULL,
precio DECIMAL(5,2) NOT NULL,
imagen VARCHAR(100) NOT NULL,
plataforma VARCHAR(80) NOT NULL 
);
ALTER TABLE videojuegos MODIFY imagen VARCHAR(100);

#detalles de videojuegos
CREATE TABLE detalle_videojuego(
id_videojuego INTEGER PRIMARY KEY,
sinopsis TEXT NOT NULL,
desarrollador VARCHAR(20) NOT NULL,
otras_plataformas VARCHAR(80) NOT NULL,
fecha_lanzamiento DATE NOT NULL,
FOREIGN KEY (id_videojuego) REFERENCES videojuegos(id_videojuego)
);
drop table detalle_videojuego;
#características de tabla videojuegos
DESCRIBE videojuegos;

#insertar datos en tabla videojuegos
INSERT INTO videojuegos(nombre_videojuego,categoria,precio,imagen,plataforma) 
VALUES
('Call of Duty 2','Shooter',24.50,'cod2.jpg','PS4'),
('Fifa 24','Deportes',20.00,'fifa24.jpg','Wii'),
('GTA San Andreas V','Mundo abierto',30.00,'gta5.jpg','PS5');

INSERT INTO detalle_videojuego (id_videojuego, sinopsis, desarrollador, otras_plataformas, fecha_lanzamiento)
VALUES
(1, 'Call of Duty 2 es un juego de disparos en primera persona ambientado en la Segunda Guerra Mundial. El jugador asume los roles de soldados en diferentes campañas del conflicto, con intensas batallas, efectos visuales realistas y una narrativa que destaca el sacrificio y la estrategia táctica en el campo de batalla.',
 'Infinity Ward', 
 'PC, Xbox 360', 
 '2005-10-25'),

(2, 'FIFA 24 es una simulación deportiva de fútbol que ofrece realismo mejorado con nuevas físicas del balón, animaciones más fluidas y modos de juego como Carrera, Ultimate Team y Volta. Los jugadores pueden vivir la emoción de los partidos con licencias oficiales de clubes, ligas y selecciones nacionales.',
 'EA Sports', 
 'PC, PS5, Xbox Series X', 
 '2023-09-29'),

(3, 'GTA San Andreas V es una versión expandida del clásico juego de mundo abierto donde los jugadores encarnan a CJ en su lucha por restaurar el poder de su familia en Los Santos. Con misiones cargadas de acción, exploración libre y una historia profunda llena de crimen, traición y redención.',
 'Rockstar Games', 
 'PC, Xbox One, Xbox Series S/X', 
 '2020-04-15');


#id_usuario INTEGER NOT NULL  --> Clave foránea
#FOREIGN KEY(id_usuario) REFERENCES usuario(id_usuario)

SELECT * FROM videojuegos;
SELECT * FROM usuario;
SELECT * FROM detalle_videojuego;
SELECT * FROM detalle_videojuego WHERE id_videojuego = 1;
DELETE FROM detalle_videojuego WHERE id_videojuego = 5;
DELETE FROM videojuegos WHERE id_videojuego = 5;
