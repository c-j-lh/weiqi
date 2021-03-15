drop database if exists weiqi;
create database weiqi;
use weiqi;

create table Player(
  name         varchar(100) not null,
  ranking      varchar(5),
  DOB          datetime,
  AIFlag	   bit not null,
  coder	   	   decimal(10,2),
  info         text,
  algoType     varchar(100),
  primary key (name)
);

create table Country(
	name	varchar(100),
    flag	varchar(1000),  -- image url
	primary key (name)
);

create table Game(
		id	int,
        result	varchar(10),
        playerNameBlack varchar(100) not null,
        playerNameWhite varchar(100) not null,
        primary key(id),
        foreign key(playerNameBlack) references Player(name),
        foreign key(playerNameWhite) references Player(name)
);
