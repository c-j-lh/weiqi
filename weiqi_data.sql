use weiqi;

delete from player;
INSERT INTO player VALUES ("Le Heng","1s","2003-12-02",false, null, null, null);
INSERT INTO player VALUES ("Le Heng2","1s","2003-12-02",false, null, null, null);
INSERT INTO player VALUES ("Le Heng3","1s","2003-12-02",false, null, null, null);
INSERT INTO player VALUES ("Le Heng4","1s","2003-12-02",false, null, null, null);
INSERT INTO player VALUES ("Le Heng5","1s","2003-12-02",false, null, null, null);
INSERT INTO player VALUES ("Le Heng6","1s","2003-12-02",false, null, null, null);
INSERT INTO player VALUES ("Le Heng7","1s","2003-12-02",false, null, null, null);
INSERT INTO player VALUES ("Le Heng8","1s","2003-12-02",false, null, null, null);
select * from player;

delete from country;
INSERT INTO country VALUES ("China","China.jpg");
INSERT INTO country VALUES ("Japan","China.jpg");
INSERT INTO country VALUES ("Korea","China.jpg");
select * from country;

delete from game;
INSERT INTO game VALUES (0,"B+7.5", "Le Heng2", "Le Heng3");