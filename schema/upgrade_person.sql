
BEGIN TRANSACTION;

CREATE TEMPORARY TABLE person_backup ("id" INTEGER NOT NULL PRIMARY KEY, "uname" VARCHAR(255) NOT NULL, "role" VARCHAR(255) NOT NULL, "display_name" VARCHAR(255) NOT NULL, "updated" INTEGER NOT NULL);

INSERT INTO person_backup SELECT id, uname, role, display_name, updated FROM person;

DROP TABLE person;

CREATE TABLE person (id INTEGER NOT NULL PRIMARY KEY, uname VARCHAR(255) NOT NULL, role VARCHAR(255) NOT NULL, display_name VARCHAR(255) NOT NULL, updated INTEGER NOT NULL);

INSERT INTO person SELECT id, uname, role, display_name, updated FROM person_backup;

DROP TABLE person_backup;
COMMIT;

