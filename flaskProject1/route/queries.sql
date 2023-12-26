CREATE TABLE IF NOT EXISTS `user` (
  `email` VARCHAR(45) NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `phone` VARCHAR(45) NULL DEFAULT NULL,
  `address` VARCHAR(50) NULL DEFAULT NULL,
  `mileage` INT NULL DEFAULT '0',
  `password` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`email`)
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `mileage_category` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  `usepoint` INT NOT NULL,
  `category` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

CREATE TABLE IF NOT EXISTS `mileage_tracking` (
  `id` INT ZEROFILL NOT NULL AUTO_INCREMENT,
  `use_date` DATETIME NULL DEFAULT NULL,
  `user_email` VARCHAR(45) NOT NULL,
  `category` VARCHAR(45) NOT NULL,
  `mileage_category_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_tracking_user_idx` (`user_email` ASC) VISIBLE,
  INDEX `fk_milege_tracking_mileage_category1_idx` (`mileage_category_id` ASC) VISIBLE,
  CONSTRAINT `fk_tracking_user`
    FOREIGN KEY (`user_email`)
    REFERENCES `user` (`email`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_milege_tracking_mileage_category1`
    FOREIGN KEY (`mileage_category_id`)
    REFERENCES `mileage_category` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB DEFAULT CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;
