use weiqi;

delete from player;
INSERT INTO player VALUES ("Le Heng","Korea", "1s","2003-12-02",false, null, null, null);
INSERT INTO player VALUES ("Le Heng2","Korea", "1s","2003-12-02",false, null, null, null);
INSERT INTO player VALUES ("Le Heng3","Korea", "1s","2003-12-02",false, null, null, null);
INSERT INTO player VALUES ("Le Heng4","Korea", "1s","2003-12-02",false, null, null, null);
INSERT INTO player VALUES ("Le Heng5","Korea", "1s","2003-12-02",false, null, null, null);
INSERT INTO player VALUES ("Le Heng6","Korea", "1s","2003-12-02",false, null, null, null);
INSERT INTO player VALUES ("Le Heng7","Korea", "1s","2003-12-02",false, null, null, null);
INSERT INTO player VALUES ("Le Heng8","Korea", "1s","2003-12-02",false, null, null, null);
select * from player;

delete from country;
INSERT INTO country VALUES ("China","China.jpg");
INSERT INTO country VALUES ("Japan","China.jpg");
INSERT INTO country VALUES ("Korea","China.jpg");
select * from country;

delete from game;
INSERT INTO game VALUES (0,"B+7.5", "2020-10-05", NULL, "Le Heng2", "Le Heng3");

delete from Move;
INSERT INTO move VALUES (0,0, 3,4);
INSERT INTO move VALUES (0,1, 17,4);
INSERT INTO move VALUES (0,2, NULL, NULL);

insert into comment values (0, "Good move", -2, "Le Heng2", 0, 2);

insert into Votes values ("Le Heng1", 0, False), ("Le Heng3", 0, False);
insert into Tags values ("Le Heng1", 0);