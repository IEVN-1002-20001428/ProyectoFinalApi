-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Dec 05, 2023 at 06:54 PM
-- Server version: 8.0.31
-- PHP Version: 8.0.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `proy_libros_bd`
--

-- --------------------------------------------------------

--
-- Table structure for table `categoria`
--

DROP TABLE IF EXISTS `categoria`;
CREATE TABLE IF NOT EXISTS `categoria` (
  `id_categoria` tinyint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(200) COLLATE utf8mb3_spanish_ci NOT NULL,
  PRIMARY KEY (`id_categoria`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `clientes`
--

DROP TABLE IF EXISTS `clientes`;
CREATE TABLE IF NOT EXISTS `clientes` (
  `nom` varchar(45) COLLATE utf8mb3_spanish_ci DEFAULT NULL,
  `usuario` varchar(20) COLLATE utf8mb3_spanish_ci DEFAULT NULL,
  `contrasenia` varchar(12) COLLATE utf8mb3_spanish_ci NOT NULL,
  `correo` varchar(200) COLLATE utf8mb3_spanish_ci NOT NULL,
  `direccion` varchar(200) COLLATE utf8mb3_spanish_ci NOT NULL,
  `id_cliente` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id_cliente`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish_ci;

--
-- Dumping data for table `clientes`
--

INSERT INTO `clientes` (`nom`, `usuario`, `contrasenia`, `correo`, `direccion`, `id_cliente`) VALUES
('Carlos Martínez', 'carlos', '12345678', 'carlos@gmail.com', 'Calle Marron #123', 1);

-- --------------------------------------------------------

--
-- Table structure for table `libros`
--

DROP TABLE IF EXISTS `libros`;
CREATE TABLE IF NOT EXISTS `libros` (
  `id_libro` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(200) COLLATE utf8mb3_spanish_ci NOT NULL,
  `descripcion` varchar(500) COLLATE utf8mb3_spanish_ci NOT NULL,
  `precio` float NOT NULL,
  `autor` varchar(200) COLLATE utf8mb3_spanish_ci NOT NULL,
  `editorial` varchar(200) COLLATE utf8mb3_spanish_ci NOT NULL,
  `existencias` tinyint NOT NULL,
  `id_categoria` varchar(100) COLLATE utf8mb3_spanish_ci DEFAULT NULL,
  `imagen` varchar(200) COLLATE utf8mb3_spanish_ci DEFAULT NULL,
  PRIMARY KEY (`id_libro`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish_ci;

--
-- Dumping data for table `libros`
--

INSERT INTO `libros` (`id_libro`, `nombre`, `descripcion`, `precio`, `autor`, `editorial`, `existencias`, `id_categoria`, `imagen`) VALUES
(1, 'Gran guía visual del cosmos', 'Después del éxito de Historia visual de la filosofía, llega una nueva guía visual dedicada al cosmos. Más de 200 conceptos clave de los cosmos explicados con imágenes comprensibles e innovadoras que, de un modo accesible, ilustran el origen y la evolución del universo, las leyes físicas que lo rigen y los descubrimientos científicos más importantes. ', 469, 'Toshifumi Fumatase', 'Blackie Books', 3, 'Ciencia ficción', 'gran_guia_del_cosmos.jpg'),
(3, 'La armadura de la luz', 'Vuelve el mejor Follett con la emocionante quinta entrega de la saga Los pilares de la Tierra. El choque de progreso y tradición y una guerra que amenaza con engullir toda Europa en la más ambiciosa y épica novela del maestro de la ficción histórica.La revolución está en el aire1792. Un gobierno despótico está decidido a convertir Inglaterra en un poderoso imperio comercial.', 669, 'Ken Follett', 'Plaza Janés', 19, 'Novela', 'La armadura de la luz.jpg'),
(4, 'Dos noches en Lisboa', 'El marido de Ariel ha desaparecido sin avisar, no le ha dejado ninguna nota y ni siquiera responde al móvil. ¿Ha salido a correr y lo han asaltado? ¿Secuestrado? ¿Asesinado? ¿Podría ser un estafador, un traficante de drogas o, quizá, un espía? ¿Tal vez se ha asustado ante este repentino matrimonio y la ha abandonado? Consulta, primero, al personal del hotel, luego a la policía, después a la embajada de Estados Unidos, y cada vez se enfrenta a más preguntas que no puede responder: ¿A qué ha venid', 359, 'Chris Pavone', 'Motus', 21, 'Novela', 'Dos noches en Lisboa.jpg'),
(5, 'Cuatro veranos', 'Conocer el mar, hacer amigos, enamorarse del amor, de la poesía, del cine y de la comida; seguir creciendo y descubrir el dolor, el deseo de venganza, pero también el miedo de ver cómo todo puede acabar en un instante; aprender a encontrar la belleza en los objetos más cotidianos o a experimentar las aventuras más extraordinarias; todo eso y más, durante el verano. ', 228, 'Benito Taibo', 'Planeta', 18, 'Juvenil', 'Cuatro veranos.jpg'),
(6, 'El problema final', 'LA NUEVA NOVELA DE ARTURO PÉREZ-REVERTEUn crimen imposible. Un detective insospechado.No se trata de un desafío entre el asesino y el detective, sino de un duelo de inteligencia entre el autor y el lector.Haría falta un policíasugirió alguien. Un detective. Tenemos uno dijo Foxá.Todos siguieron la dirección de su mirada. Eso es ridículo protesté. ¿Se han vuelto locos?Usted fue Sherlock Holmes.Nadie fue Sherlock Holmes. Ese detective no existió jamás. ', 399, 'Arturo Pérez Reverte', 'Alfaguara', 44, 'Novela', 'El problema final.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
CREATE TABLE IF NOT EXISTS `usuarios` (
  `nombre` varchar(200) COLLATE utf8mb3_spanish_ci NOT NULL,
  `correo` varchar(200) COLLATE utf8mb3_spanish_ci NOT NULL,
  `contrasenia` varchar(12) COLLATE utf8mb3_spanish_ci NOT NULL,
  `rol` tinyint(1) NOT NULL,
  PRIMARY KEY (`correo`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish_ci;

--
-- Dumping data for table `usuarios`
--

INSERT INTO `usuarios` (`nombre`, `correo`, `contrasenia`, `rol`) VALUES
('admin', 'admin@a.com', '12345', 1);

-- --------------------------------------------------------

--
-- Table structure for table `ventas`
--

DROP TABLE IF EXISTS `ventas`;
CREATE TABLE IF NOT EXISTS `ventas` (
  `id_venta` tinyint NOT NULL AUTO_INCREMENT,
  `id_cliente` tinyint NOT NULL,
  `total` double NOT NULL,
  `fecha_venta` date DEFAULT NULL,
  `estatus` int NOT NULL,
  PRIMARY KEY (`id_venta`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `venta_detalle`
--

DROP TABLE IF EXISTS `venta_detalle`;
CREATE TABLE IF NOT EXISTS `venta_detalle` (
  `id_ventadetalle` int NOT NULL AUTO_INCREMENT,
  `id_venta` int NOT NULL,
  `id_libro` int NOT NULL,
  `cantidad` int NOT NULL,
  `precio_unitario` int NOT NULL,
  `total` int NOT NULL,
  PRIMARY KEY (`id_ventadetalle`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_spanish_ci;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
