-- MySQL Script generated by MySQL Workbench
-- pon, 13 lip 2015, 21:35:11
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema Dev_Cloud_db
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `Dev_Cloud_db` ;

-- -----------------------------------------------------
-- Schema Dev_Cloud_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `Dev_Cloud_db` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
USE `Dev_Cloud_db` ;

-- -----------------------------------------------------
-- Table `Dev_Cloud_db`.`Users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Dev_Cloud_db`.`Users` ;

CREATE TABLE IF NOT EXISTS `Dev_Cloud_db`.`Users` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `login` VARCHAR(45) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `name` VARCHAR(45) NULL,
  `lastname` VARCHAR(45) NULL,
  `email` VARCHAR(255) NOT NULL,
  `create_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `language` VARCHAR(45) NULL,
  `picture` BLOB NULL,
  `activation_key` VARCHAR(255) NULL,
  `is_active` INT NULL,
  `is_superuser` INT NULL,
  `last_activity` DATETIME NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `login_UNIQUE` (`login` ASC),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC))
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_polish_ci;


-- -----------------------------------------------------
-- Table `Dev_Cloud_db`.`Roles`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Dev_Cloud_db`.`Roles` ;

CREATE TABLE IF NOT EXISTS `Dev_Cloud_db`.`Roles` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `role_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;


-- -----------------------------------------------------
-- Table `Dev_Cloud_db`.`Users_in_roles`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Dev_Cloud_db`.`Users_in_roles` ;

CREATE TABLE IF NOT EXISTS `Dev_Cloud_db`.`Users_in_roles` (
  `id` INT NOT NULL,
  `user_id` INT(11) NOT NULL,
  `role_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`, `user_id`, `role_id`),
  INDEX `fk_Users_in_roles_Roles1_idx` (`role_id` ASC),
  CONSTRAINT `fk_Users_in_roles_User`
    FOREIGN KEY (`user_id`)
    REFERENCES `Dev_Cloud_db`.`Users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Users_in_roles_Roles1`
    FOREIGN KEY (`role_id`)
    REFERENCES `Dev_Cloud_db`.`Roles` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_polish_ci;


-- -----------------------------------------------------
-- Table `Dev_Cloud_db`.`Applications`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Dev_Cloud_db`.`Applications` ;

CREATE TABLE IF NOT EXISTS `Dev_Cloud_db`.`Applications` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `application_name` VARCHAR(45) NOT NULL,
  `description` VARCHAR(45) NULL,
  `memory` FLOAT NULL,
  `space` FLOAT NULL,
  `cpu` INT(11) NULL,
  `update_time` TIMESTAMP NULL,
  `instalation_procedure` TEXT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_polish_ci;


-- -----------------------------------------------------
-- Table `Dev_Cloud_db`.`Template_instances`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Dev_Cloud_db`.`Template_instances` ;

CREATE TABLE IF NOT EXISTS `Dev_Cloud_db`.`Template_instances` (
  `template_id` INT(11) NOT NULL AUTO_INCREMENT,
  `template_name` VARCHAR(45) NOT NULL,
  `cpu` INT(11) NOT NULL,
  `memory` FLOAT NOT NULL,
  PRIMARY KEY (`template_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_polish_ci;


-- -----------------------------------------------------
-- Table `Dev_Cloud_db`.`Virtual_machines`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Dev_Cloud_db`.`Virtual_machines` ;

CREATE TABLE IF NOT EXISTS `Dev_Cloud_db`.`Virtual_machines` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `vm_id` INT(11) NOT NULL,
  `ctx` VARCHAR(255) NULL,
  `disk_space` VARCHAR(45) NULL,
  `public_ip` VARCHAR(45) NULL,
  `private_ip` VARCHAR(45) NULL,
  `template_instance_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`, `template_instance_id`),
  INDEX `fk_Virtual_machines_Template_instances1_idx` (`template_instance_id` ASC),
  CONSTRAINT `fk_Virtual_machines_Template_instances1`
    FOREIGN KEY (`template_instance_id`)
    REFERENCES `Dev_Cloud_db`.`Template_instances` (`template_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_polish_ci;


-- -----------------------------------------------------
-- Table `Dev_Cloud_db`.`Installed_applications`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Dev_Cloud_db`.`Installed_applications` ;

CREATE TABLE IF NOT EXISTS `Dev_Cloud_db`.`Installed_applications` (
  `installed_app_id` INT(11) NOT NULL AUTO_INCREMENT,
  `workspace` VARCHAR(45) NULL,
  `clx_ip` VARCHAR(45) NULL,
  `public_port` INT(11) NULL,
  `private_port` INT(11) NULL,
  `user_id` INT(11) NOT NULL,
  `application_id` INT(11) NOT NULL,
  `virtual_machine_id` INT(11) NOT NULL,
  PRIMARY KEY (`installed_app_id`, `user_id`, `application_id`, `virtual_machine_id`),
  INDEX `fk_Installed_applications_User1_idx` (`user_id` ASC),
  INDEX `fk_Installed_applications_Applications1_idx` (`application_id` ASC),
  INDEX `fk_Installed_applications_Virtual_machines1_idx` (`virtual_machine_id` ASC),
  CONSTRAINT `fk_Installed_applications_User1`
    FOREIGN KEY (`user_id`)
    REFERENCES `Dev_Cloud_db`.`Users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Installed_applications_Applications1`
    FOREIGN KEY (`application_id`)
    REFERENCES `Dev_Cloud_db`.`Applications` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Installed_applications_Virtual_machines1`
    FOREIGN KEY (`virtual_machine_id`)
    REFERENCES `Dev_Cloud_db`.`Virtual_machines` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_polish_ci;


-- -----------------------------------------------------
-- Table `Dev_Cloud_db`.`Notifications`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Dev_Cloud_db`.`Notifications` ;

CREATE TABLE IF NOT EXISTS `Dev_Cloud_db`.`Notifications` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `notification_name` VARCHAR(255) NOT NULL,
  `notification_information` VARCHAR(255) NULL,
  `category` INT NULL,
  `is_read` INT NULL,
  `create_time` DATETIME NULL,
  `user_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`, `user_id`),
  INDEX `fk_Notifications_Users1_idx` (`user_id` ASC),
  CONSTRAINT `fk_Notifications_Users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `Dev_Cloud_db`.`Users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;


-- -----------------------------------------------------
-- Table `Dev_Cloud_db`.`Tasks`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `Dev_Cloud_db`.`Tasks` ;

CREATE TABLE IF NOT EXISTS `Dev_Cloud_db`.`Tasks` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `task_name` VARCHAR(255) NOT NULL,
  `is_processing` INT NULL,
  `create_time` DATETIME NULL,
  `user_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`, `user_id`),
  INDEX `fk_Notifications_Users1_idx` (`user_id` ASC),
  CONSTRAINT `fk_Notifications_Users10`
    FOREIGN KEY (`user_id`)
    REFERENCES `Dev_Cloud_db`.`Users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_general_ci;

USE `Dev_Cloud_db`;

DELIMITER $$

USE `Dev_Cloud_db`$$
DROP TRIGGER IF EXISTS `Dev_Cloud_db`.`Users_BEFORE_UPDATE` $$
USE `Dev_Cloud_db`$$
CREATE DEFINER = CURRENT_USER TRIGGER `Dev_Cloud_db`.`Users_BEFORE_UPDATE` BEFORE UPDATE ON `Users` FOR EACH ROW
     BEGIN
        -- Set the creation date
		SET new.last_activity= now();
    END;
    
    $$


DELIMITER ;
SET SQL_MODE = '';
GRANT USAGE ON *.* TO admin;
 DROP USER admin;
SET SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';
CREATE USER 'admin' IDENTIFIED BY 'adminuser';

GRANT ALL ON `Dev_Cloud_db`.* TO 'admin';

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
