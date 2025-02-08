-- SQLite
.tables

SELECT name FROM sqlite_master WHERE type='table';

SELECT * from roles;
SELECT * from users;
SELECT * from documents;
SELECT * from top_images;
SELECT * from news;
SELECT * from news_types;
SELECT * from products;
SELECT * from classifys;

update products SET fk_product_classify = 2 WHERE id = 2; 

delete from documents WHERE id = 1 or id = 2  
        or id = 3 or id = 4 or id = 5 or id = 6
        or id = 7 or id = 8 or id = 9;    


update documents set title='xx' where id = 10;
update documents set title='yy' where id = 11;

update users set created_at='2024-12-21 16:32:11' WHERE id=1;

DROP TABLE alembic_version;
 

DELETE FROM news;
DELETE FROM users;