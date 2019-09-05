drop table if exists users;
drop table if exists roles;
drop table if exists locations;
drop table if exists projects;
drop table if exists project_types;

create extension if not exists "postgis";

create table roles (
 id serial primary key,
 role_name varchar(20)
);

create table users (
 id serial primary key,
 password_hash varchar(100),
 email varchar(20),
 role_id integer references roles(id)
);

create table project_types (
 id serial primary key,
 type_name varchar(30)
);

create table projects (
 id serial primary key,
 name varchar(100),
 description varchar(250),
 photo_url varchar(250),
 website_url varchar(250),
 year integer,
 gge_reduced real,
 ghg_reduced real,
 project_type_id integer references project_types(id)
);

create table locations (
 id serial primary key,
 address varchar(50),
 city varchar(50),
 state varchar(2),
 zip_code integer,
 location geometry,
 project_id integer references projects(id)
);
