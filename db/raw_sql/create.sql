CREATE TABLE IF NOT EXISTS Users (
    user_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Medications(
    med_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TINYTEXT NOT NULL,
    cost FLOAT NOT NULL,
    quantity INT UNSIGNED NOT NULL,
    in_stock BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS Orders(
    order_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNSIGNED NOT NULL,
    med_id INT UNSIGNED NOT NULL,
    amount INT UNSIGNED NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    CONSTRAINT `fk_user_order` foreign key (`user_id`) references `Users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `fk_med_order` foreign key  (`med_id`) references `Medications` (`med_id`) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS Demand(
    demand_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNSIGNED NOT NULL,
    med_id INT UNSIGNED NOT NULL,
    amount INT UNSIGNED NOT NULL,
    CONSTRAINT `fk_user_demand` foreign key (`user_id`) references `Users` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT `fk_med_demand` foreign key  (`med_id`) references `Medications` (`med_id`) ON DELETE CASCADE ON UPDATE CASCADE
);
# create database pp character set utf8 collate utf8_general_ci;

INSERT INTO Users(`email`, `username`, `password_hash`)
VALUES ('nicik@gmail.com', 'Anatoliy Zakharchenko', 'EF797C8118F02DFB649607DD5D3F8C7623048C9C063D532CC95C5ED7A898A64F'),
       ('supercolor@gmail.com', 'Anatoliy Zakharchenko', '9377935330AC2D6DF60B8040C482E839286B91AF0C3CF44CC14621EC13DF26EF'),
       ('ohimnewuser@ukr.net', 'Romeo Gospodiowych', '9B8769A4A742959A2D0298C36FB70623F2DFACDA8436237DF08D8DFD5B37374C'),
       ('pdurov@mail.ru', 'Rick Romeos', '05F03A7011D2E3F0738F6E0E1C9491A1C0FAD74AA16528B4414A7F4A5978A641'),
       ('linakilchenko@mail.ru', 'Lina Romarko', '131E27B7715C43825F14696B907812D34FB86A529DD8C98FEDBF87016F5D9149');

INSERT INTO Medications(`name`, `description`, `cost`, `quantity`, `in_stock`)
VALUES ('Smekta', 'Super-puper preparat likue wid raku, straxu wysoty, daje wminnia keruwaty helicopterom, widprawliae na Weneru', 2, 12, TRUE),
       ('Wedmeszujky', 'Shcob strybaty wyshche neba bihaty dopomahaty treba smachni Wedmeszuyki koszen den usim szuwaty! Wedmeszujki - weseli vitaminy dla rozwytku dytyny!', 0.25, 1000, TRUE),
       ('Amizon', 'Pryvit a de vsi? - Zahworily _ A ty? - Amizon _Ukrainskoju bud laska - Amizon', 22, 0, FALSE),
       ('Ozvirin', 'Lets live friendly', 12, 123, TRUE),
       ('Waleriana', 'For nerwy (AntyOzviryn)', 13, 121, TRUE);

INSERT INTO Orders(`user_id`, `med_id`, `amount`, `completed`)
VALUES (2, 4, 5, TRUE),
       (2, 5, 10, FALSE),
       (1, 2, 1, FALSE),
       (4, 3, 1, FALSE),
       (3, 1, 3, FALSE);

INSERT INTO Demand(`user_id`, `med_id`, `amount`)
VALUES (2, 5, 100000),
       (1, 3, 10),
       (2, 5, 1000000),
       (4, 4, 1),
       (3, 1, 1);
