-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema bike_db_schema
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema bike_db_schema
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `bike_db_schema` DEFAULT CHARACTER SET utf8 ;
USE `bike_db_schema` ;

-- -----------------------------------------------------
-- Table `bike_db_schema`.`DangerData`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `bike_db_schema`.`DangerData` (
  `idDangerData` INT NOT NULL AUTO_INCREMENT,
  `latitude` DOUBLE NOT NULL,
  `longitude` DOUBLE NOT NULL,
  `dangerRating` INT NOT NULL,
  PRIMARY KEY (`idDangerData`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
