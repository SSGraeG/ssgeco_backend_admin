-- Table `user` in `eco` database
CREATE TABLE IF NOT EXISTS `user` (
  `email` VARCHAR(45) NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `phone` VARCHAR(45) NULL DEFAULT NULL,
  `address` VARCHAR(50) NULL DEFAULT NULL,
  `mileage` INT NULL DEFAULT '0',
  `password` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`email`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- Table `mileage_category` in `eco` database
CREATE TABLE IF NOT EXISTS `mileage_category` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  `usepoint` INT NOT NULL,
  `category` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- Table `mileage_tracking` in `eco` database
CREATE TABLE IF NOT EXISTS `mileage_tracking` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `use_date` DATETIME NULL DEFAULT NULL,
  `user_email` VARCHAR(45) NOT NULL,
  `category` VARCHAR(45) NOT NULL,
  `mileage_category_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_tracking_user_idx` (`user_email` ASC),
  INDEX `fk_mileage_tracking_mileage_category1_idx` (`mileage_category_id` ASC),
  CONSTRAINT `fk_tracking_user`
    FOREIGN KEY (`user_email`)
    REFERENCES `user` (`email`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_mileage_tracking_mileage_category1`
    FOREIGN KEY (`mileage_category_id`)
    REFERENCES `mileage_category` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- Table `coupon_list` in `eco` database
CREATE TABLE IF NOT EXISTS `coupon_list` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `expired_date` DATETIME NULL DEFAULT NULL,
  `user_email` VARCHAR(45) NOT NULL,
  `mileage_category_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_coupon_list_user1_idx` (`user_email` ASC),
  INDEX `fk_coupon_list_mileage_category1_idx` (`mileage_category_id` ASC),
  CONSTRAINT `fk_coupon_list_mileage_category1`
    FOREIGN KEY (`mileage_category_id`)
    REFERENCES `mileage_category` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_coupon_list_user1`
    FOREIGN KEY (`user_email`)
    REFERENCES `user` (`email`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- Table `mileage_tracking` in `eco_admin` database

CREATE TABLE IF NOT EXISTS `mileage_tracking` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `use_date` DATETIME NULL DEFAULT NULL,
  `user_email` VARCHAR(45) NOT NULL,
  `mileage_category_id` INT NOT NULL,
  `before_mileage` INT NULL DEFAULT NULL,
  `after_mileage` INT NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_tracking_user_idx` (`user_email` ASC),
  INDEX `fk_mileage_tracking_mileage_category1_idx` (`mileage_category_id` ASC),
  CONSTRAINT `fk_mileage_tracking_mileage_category1`
    FOREIGN KEY (`mileage_category_id`)
    REFERENCES `mileage_category` (`id`),
  CONSTRAINT `fk_tracking_user`
    FOREIGN KEY (`user_email`)
    REFERENCES `user` (`email`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;