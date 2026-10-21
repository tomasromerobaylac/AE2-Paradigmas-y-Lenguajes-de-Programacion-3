-- Mercado Fresco — esquema de autenticación (BCRYPT + sesiones)
-- Ejecutar en phpMyAdmin o con: mysql -u root -p < sql/mercado_fresco.sql

CREATE DATABASE IF NOT EXISTS mercado_fresco
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE mercado_fresco;

CREATE TABLE IF NOT EXISTS usuarios (
  id            INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  nombre        VARCHAR(120)      NOT NULL,
  email         VARCHAR(190)      NOT NULL,
  -- VARCHAR(255): el hash BCRYPT que genera password_hash() ocupa 60
  -- caracteres, pero se deja margen para futuros algoritmos más largos.
  password      VARCHAR(255)      NOT NULL,
  rol           ENUM('cliente', 'empleado') NOT NULL DEFAULT 'cliente',
  creado_en     TIMESTAMP         NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uq_usuarios_email (email)
) ENGINE=InnoDB;
