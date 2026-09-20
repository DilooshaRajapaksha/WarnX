CREATE DATABASE weather_db;
CREATE DATABASE action_db;
CREATE DATABASE coordination_db;
CREATE DATABASE learning_db;

\connect weather_db
CREATE EXTENSION IF NOT EXISTS postgis;

\connect action_db
CREATE EXTENSION IF NOT EXISTS postgis;

\connect coordination_db
CREATE EXTENSION IF NOT EXISTS postgis;

\connect learning_db
CREATE EXTENSION IF NOT EXISTS postgis;
