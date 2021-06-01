BEGIN TRANSACTION;

CREATE TEMPORARY TABLE doi_backup(id, doi, object_url, m_id, status, bundle_name, metadata, eprint_id, repo_id, notes, updated, created);

INSERT INTO doi_backup SELECT id, doi, object_url, m_id, status, bundle_name, metadata, eprint_id, repo_id, notes, updated, created FROM doi;

DROP TABLE doi; DROP INDEX IF EXISTS doi_doi;

CREATE TABLE "doi" ("id" INTEGER NOT NULL PRIMARY KEY, "doi" VARCHAR(255) NOT NULL, "object_url" VARCHAR(255) NOT NULL, "m_id" VARCHAR(255) NOT NULL, "status" workflow NOT NULL, "bundle_name" VARCHAR(255) NOT NULL, "metadata" TEXT NOT NULL, "eprint_id" VARCHAR(255) NOT NULL, "repo_id" VARCHAR(255) NOT NULL, "notes" TEXT NOT NULL, "updated" DATETIME NOT NULL, "created" DATETIME NOT NULL);

INSERT INTO doi SELECT id, doi, object_url, m_id, status, bundle_name, metadata, eprint_id, repo_id, notes, updated, created FROM doi_backup;

CREATE UNIQUE INDEX doi_doi ON doi (doi);

DROP TABLE doi_backup;
COMMIT;

