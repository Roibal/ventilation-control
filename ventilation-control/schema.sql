BEGIN TRANSACTION;

DROP TABLE IF EXISTS 'weather';
CREATE TABLE 'weather' (
  'date' timestamp not null,
  'room' text not null,
  'inside_temperature' REAL not null,
  'inside_humidity' REAL not null,
  'outside_temperature' REAL not null,
  'outside_humidity' REAL not null,
  'ventilation_recommended' BOOLEAN DEFAULT 0
);

CREATE INDEX 'weather_index' ON 'weather' ('date' DESC, 'room');

DROP TABLE IF EXISTS 'actor_status';
CREATE TABLE 'actor_status' (
  'room' text not null,
  'powered_on' timestamp not null,
  'powered_off' timestamp
);

COMMIT;
