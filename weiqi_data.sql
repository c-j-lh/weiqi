use weiqi;

delete from country;
INSERT INTO country VALUES ("China","China.jpg");
INSERT INTO country VALUES ("Japan","China.jpg");
INSERT INTO country VALUES ("Korea","China.jpg");
select * from country;


delete from player;
INSERT INTO player VALUES ("Shin Jinseo", null, "9p", "1984-08-24", false, null, null, null);
INSERT INTO player VALUES ("Ke Jie", "China", "9p", "1945-09-10", false, null, null, null);
INSERT INTO player VALUES ("Ichiriki Ryo", "Japan", "9p", "1986-12-25", false, null, null, null);
INSERT INTO player VALUES ("Yang Dingxin", "China", "9p", "1963-08-22", false, null, null, null);
INSERT INTO player VALUES ("Iyama Yuuta", "Japan", "9p", "1978-12-09", false, null, null, null);
INSERT INTO player VALUES ("Shin Minjun", null, "9p", "1994-12-20", false, null, null, null);
INSERT INTO player VALUES ("Tang Weixing", "China", "9p", "1955-07-10", false, null, null, null);
INSERT INTO player VALUES ("Lian Xiao", "China", "9p", "1996-04-06", false, null, null, null);
INSERT INTO player VALUES ("Fan Tingyu", "China", "9p", "1982-06-04", false, null, null, null);
INSERT INTO player VALUES ("Byun Sangil", null, "9p", "1945-07-04", false, null, null, null);
INSERT INTO player VALUES ("Park Yeonghun", "Korea", "9p", "1946-04-19", false, null, null, null);
INSERT INTO player VALUES ("Xie Ke", null, "8p", "1970-08-30", false, null, null, null);
INSERT INTO player VALUES ("Zhao Chenyu", null, "8p", "1953-04-27", false, null, null, null);
INSERT INTO player VALUES ("Xu Jiayang", null, "8p", "1979-11-06", false, null, null, null);
INSERT INTO player VALUES ("Tao Xinran", "China", "8p", "1947-05-01", false, null, null, null);
-- select * from player;
delete from game;
INSERT INTO game VALUES (0, "B+R", "2021-02-25", NULL, "Shin Jinseo", "Ke Jie");
INSERT INTO game VALUES (1, "B+R", "2021-02-24", NULL, "Shin Jinseo", "Ichiriki Ryo");
INSERT INTO game VALUES (2, "B+R", "2021-02-23", NULL, "Shin Jinseo", "Yang Dingxin");
INSERT INTO game VALUES (3, "W+R", "2021-02-22", NULL, "Iyama Yuuta", "Shin Jinseo");
INSERT INTO game VALUES (4, "W+R", "2021-02-03", NULL, "Ke Jie", "Shin Minjun");
INSERT INTO game VALUES (5, "W+R", "2021-02-01", NULL, "Shin Minjun", "Ke Jie");
INSERT INTO game VALUES (6, "W+R", "2021-01-20", NULL, "Ke Jie", "Tang Weixing");
INSERT INTO game VALUES (7, "W+R", "2021-01-20", NULL, "Ke Jie", "Tang Weixing");
INSERT INTO game VALUES (8, "B+R", "2021-01-20", NULL, "Shin Jinseo", "Lian Xiao");
INSERT INTO game VALUES (9, "W+R", "2021-01-18", NULL, "Fan Tingyu", "Shin Jinseo");
INSERT INTO game VALUES (10, "B+R", "2021-01-18", NULL, "Lian Xiao", "Byun Sangil");
INSERT INTO game VALUES (11, "W+R", "2021-01-18", NULL, "Fan Tingyu", "Shin Jinseo");
INSERT INTO game VALUES (12, "W+R", "2021-01-18", NULL, "Park Yeonghun", "Tang Weixing");
INSERT INTO game VALUES (13, "B+3.5", "2021-01-12", NULL, "Xie Ke", "Ichiriki Ryo");
INSERT INTO game VALUES (14, "B+3.5", "2021-01-12", NULL, "Xie Ke", "Ichiriki Ryo");
INSERT INTO game VALUES (15, "B+R", "2021-01-10", NULL, "Shin Jinseo", "Zhao Chenyu");
INSERT INTO game VALUES (16, "B+R", "2021-01-10", NULL, "Shin Jinseo", "Zhao Chenyu");
INSERT INTO game VALUES (17, "B+R", "2021-01-10", NULL, "Shin Jinseo", "Zhao Chenyu");
INSERT INTO game VALUES (18, "W+R", "2021-01-08", NULL, "Yang Dingxin", "Xu Jiayang");
INSERT INTO game VALUES (19, "W+0.5", "2021-01-06", NULL, "Tao Xinran", "Yang Dingxin");

delete from Move;
INSERT INTO move VALUES (0,0, 3,4);
INSERT INTO move VALUES (0,1, 17,4);
INSERT INTO move VALUES (0,2, NULL, NULL);

insert into comment values (0, "Good move", -2, "Le Heng2", 0, 2);

insert into Votes values ("Le Heng1", 0, False), ("Le Heng3", 0, False);
insert into Tags values ("Le Heng1", 0);