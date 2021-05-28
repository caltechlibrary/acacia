BEGIN TRANSACTION;

CREATE TEMPORARY TABLE message_backup (id INTEGER NOT NULL PRIMARY KEY, m_id VARCHAR(255) NOT NULL, m_reply_to VARCHAR(255) NOT NULL, m_date DATETIME NOT NULL, m_to VARCHAR(255) NOT NULL, m_from VARCHAR(255) NOT NULL, m_subject VARCHAR(255) NOT NULL, m_body TEXT NOT NULL, m_processed INTEGER NOT NULL);

INSERT INTO message_backup SELECT id, m_id, m_reply_to, m_date, m_to, m_from, m_subject, m_body, m_processed FROM message;


DROP TABLE message; DROP INDEX IF EXISTS message_m_id;

CREATE TABLE message (id INTEGER NOT NULL PRIMARY KEY, m_id VARCHAR(255) NOT NULL, m_reply_to VARCHAR(255) NOT NULL, m_date DATETIME NOT NULL, m_to VARCHAR(255) NOT NULL, m_from VARCHAR(255) NOT NULL, m_subject VARCHAR(255) NOT NULL, m_body TEXT NOT NULL, m_processed INTEGER NOT NULL, updated DATETIME NOT NULL, created DATETIME NOT NULL);

INSERT INTO message SELECT id, m_id, m_reply_to, m_date, m_to, m_from, m_subject, m_body, m_processed, DATETIME() AS created, DATETIME() AS updated FROM message_backup;

CREATE UNIQUE INDEX message_m_id ON message (m_id);

DROP TABLE message_backup;
COMMIT;
