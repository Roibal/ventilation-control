BEGIN TRANSACTION;
DROP TABLE IF EXISTS weather;
CREATE TABLE weather (
  'id' integer primary key autoincrement,
  'date' timestamp not null,
  'room' text not null,
  'inside_temperature' REAL not null,
  'inside_humidity' REAL not null,
  'outside_temperature' REAL not null,
  'outside_humidity' REAL not null,
  'ventilation_recommended' BOOLEAN DEFAULT 0
);
DELETE FROM "sqlite_sequence";
INSERT INTO "sqlite_sequence" VALUES('weather',1);

COMMIT;
