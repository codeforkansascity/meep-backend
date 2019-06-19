CREATE TABLE projects (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL UNIQUE,
  description VARCHAR(250),
  photo_url VARCHAR(250),
  year INTEGER,
  gge_reduced REAL,
  ghg_reduced REAL,
  project_type_id INTEGER REFERENCES project_types(id),  
);
