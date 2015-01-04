BEGIN TRANSACTION;

DROP TABLE IF EXISTS weather;
CREATE TABLE weather (
  'date' timestamp not null,
  'room' text not null,
  'inside_temperature' REAL not null,
  'inside_humidity' REAL not null,
  'outside_temperature' REAL not null,
  'outside_humidity' REAL not null,
  'ventilation_recommended' BOOLEAN DEFAULT 0
);

COMMIT;
