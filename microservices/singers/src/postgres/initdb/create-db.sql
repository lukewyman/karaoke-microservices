CREATE USER singers_app WITH
  LOGIN
  PASSWORD 'pa55w0RD';

DROP DATABASE IF EXISTS singers;

CREATE DATABASE singers WITH
  OWNER = singers_app
  ENCODING = 'UTF8';

GRANT ALL PRIVILEGES ON DATABASE singers TO singers_app;

\c singers singers_app;

CREATE TABLE singers (
  id UUID NOT NULL, 
  email VARCHAR, 
  first_name VARCHAR, 
  last_name VARCHAR, 
  stage_name VARCHAR, 
  PRIMARY KEY (id)
);
