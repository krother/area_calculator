
# Postgres

## start docker container:

    docker compose up

## log into container:

    docker compose exec -it postgres /bin/bash

## log into psql client from docker

    psql -U postgres


## psql commands

- \c   show connection
- \l   show databases
- \dt  show tables
- \q   quit

## CRUD queries: Create, Read, Update, Delete
 
    -- 1) Create a table and write data to it
     
    CREATE TABLE shape (
        id INT,
        name VARCHAR(20),
        size NUMERIC,
        area NUMERIC
    );

    INSERT INTO shape VALUES (1, 'square', 3, 9);
    INSERT INTO shape VALUES (2, 'circle', 1, 3.141529);
    INSERT INTO shape VALUES (3, 'square', 10, 100);

    -- 2) Read data from the table
    SELECT * FROM shape;
    SELECT name, size, area FROM shape;
    SELECT size, area FROM shape WHERE name = 'square';
    SELECT name, count(*) FROM shape GROUP BY name;
  
    -- 3) Update a value in the database
 
    UPDATE shape SET name='big square' WHERE id=3;

    -- 4) Delete rows
    DELETE FROM shape WHERE id = 1;
