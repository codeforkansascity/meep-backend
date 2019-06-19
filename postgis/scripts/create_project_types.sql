CREATE TABLE project_types (
  id SERIAL PRIMARY KEY,
  type_name VARCHAR(50)
);

INSERT INTO project_types(type_name)
VALUES ('Building'), ('Vehicle Transportation'), ('Infrastructure Transportation'), (NULL);
