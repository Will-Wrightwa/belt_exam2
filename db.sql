-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema belt_exam2
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema belt_exam2
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `belt_exam2` DEFAULT CHARACTER SET utf8 ;
USE `belt_exam2` ;

-- -----------------------------------------------------
-- Table `belt_exam2`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `belt_exam2`.`user` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NULL,
  `alias` VARCHAR(255) NULL,
  `email` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW(),
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `belt_exam2`.`friendships`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `belt_exam2`.`friendships` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `friendshipscol` VARCHAR(45) NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW(),
  `friend1_user_id` INT UNSIGNED NOT NULL,
  `friend2_user_id` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_friendships_user_idx` (`friend1_user_id` ASC),
  INDEX `fk_friendships_user1_idx` (`friend2_user_id` ASC),
  CONSTRAINT `fk_friendships_user`
    FOREIGN KEY (`friend1_user_id`)
    REFERENCES `belt_exam2`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_friendships_user1`
    FOREIGN KEY (`friend2_user_id`)
    REFERENCES `belt_exam2`.`user` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
