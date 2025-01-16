-- SQLite
.tables

SELECT * from roles;
SELECT * from users;
SELECT * from documents;
SELECT * from top_images;
SELECT * from news;
SELECT * from news_types;

update users SET confirmed = 1 WHERE id = 1; 

delete from documents WHERE id = 1 or id = 2  
        or id = 3 or id = 4 or id = 5 or id = 6
        or id = 7 or id = 8 or id = 9;    


update documents set title='xx' where id = 10;
update documents set title='yy' where id = 11;

DROP TABLE alembic_version;