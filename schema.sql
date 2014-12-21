BEGIN TRANSACTION;
DROP TABLE IF EXISTS mails;
CREATE TABLE mails (
  'id' integer primary key autoincrement,
  'date' text not null,
  'maildata' text not null,
  'forwarded' BOOLEAN DEFAULT 0
);
DELETE FROM "sqlite_sequence";
INSERT INTO "sqlite_sequence" VALUES('mails',1);

DROP TABLE IF EXISTS forwarding_rules;
CREATE TABLE forwarding_rules (
  'id' integer primary key autoincrement,
  'regex' text not null,
  'email_address' text not null
);

DROP TABLE IF EXISTS styling_rules;
CREATE TABLE styling_rules (
  'id' integer primary key autoincrement,
  'regex' text not null,
  'header_color' text not null
);

COMMIT;
