--Create Schema
CREATE SCHEMA play_pen; 

-- Create table: Book 
CREATE TABLE play_pen.book (
    id UUID PRIMARY KEY,
    title varchar(100) not null,
    author varchar(100) not null,
    category varchar(50) not null,
    CONSTRAINT constraint_name UNIQUE (id, title)
);

-- enable pg_trgm to allow fuzzy search
CREATE EXTENSION IF NOT EXISTS pg_trgm;
SELECT * FROM pg_extension WHERE extname = 'pg_trgm' LIMIT 100