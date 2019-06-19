CREATE TABLE addresses (
  id SERIAL PRIMARY KEY,
  city varchar(200),
  state varchar(2),
  zip int,
  address varchar(200),
  latitude real,
  longitude real,
  project_id int REFERENCES projects(id)
);

COPY addresses(id, city, state, zip, address, latitude, longitude, project_id)
FROM '/data/addresses-06-13-2019.csv'
DELIMITER ','
CSV HEADER;
