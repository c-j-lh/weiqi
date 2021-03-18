CREATE DATABASE t;
USE t;

CREATE TABLE parent (id INT NOT NULL,
                     PRIMARY KEY (id)
) ENGINE=INNODB;

CREATE TABLE child (id INT NULL, 
                    parent_id INT NULL,
                    FOREIGN KEY (parent_id) REFERENCES parent(id)
) ENGINE=INNODB;


INSERT INTO child (id, parent_id) VALUES (1, NULL);
-- Query OK, 1 row affected (0.01 sec)


INSERT INTO child (id, parent_id) VALUES (2, 1);

-- ERROR 1452 (23000): Cannot add or update a child row: a foreign key 
-- constraint fails (`t/child`, CONSTRAINT `child_ibfk_1` FOREIGN KEY
-- (`parent_id`) REFERENCES `parent` (`id`))