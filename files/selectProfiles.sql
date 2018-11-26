SELECT `profile`.`profile_id`,
    `profile`.`first_name`,
    `profile`.`last_name`,
    `profile`.`mobile_number`,
    `profile`.`email`,
    `profile`.`user_name`,
    `profile`.`password`,
    `profile`.`created_date`,
    `profile`.`is_active`
FROM `social_network_db`.`profile`;
