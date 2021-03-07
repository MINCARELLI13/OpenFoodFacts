-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema BDD_OFF
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema BDD_OFF
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS BDD_OFF DEFAULT CHARACTER SET utf8 ;
USE BDD_OFF ;

-- -----------------------------------------------------
-- Table BDD_OFF.Category
-- -----------------------------------------------------
DROP TABLE IF EXISTS BDD_OFF.Category ;

CREATE TABLE IF NOT EXISTS Category (
  id INT NOT NULL,
  name VARCHAR(100) NOT NULL,
  PRIMARY KEY (id))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table BDD_OFF.Product
-- -----------------------------------------------------
DROP TABLE IF EXISTS BDD_OFF.Product ;

CREATE TABLE IF NOT EXISTS BDD_OFF.Product (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL,
  brand VARCHAR(100) NOT NULL,
  url VARCHAR(100) NOT NULL,
  nutriscore CHAR(1) NOT NULL,
  ingredients VARCHAR(200) NOT NULL,
  stores VARCHAR(150) NULL DEFAULT NULL,
  category_id INT NOT NULL,
  PRIMARY KEY (id),
  INDEX fk_Product_category_id (category_id ASC) VISIBLE,
  CONSTRAINT fk_Product_category_id
    FOREIGN KEY (category_id)
    REFERENCES BDD_OFF.Category (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table BDD_OFF.Substitutes
-- -----------------------------------------------------
DROP TABLE IF EXISTS BDD_OFF.Substitutes ;

CREATE TABLE IF NOT EXISTS BDD_OFF.Substitutes (
  original_id INT NOT NULL,
  substitut_id INT NOT NULL,
  PRIMARY KEY (original_id, substitut_id),
  CONSTRAINT fk_Substitutes_original_id
    FOREIGN KEY (original_id)
    REFERENCES BDD_OFF.Product (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT fk_Substitutes_substitut_id
    FOREIGN KEY (substitut_id)
    REFERENCES BDD_OFF.Product (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
