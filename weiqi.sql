drop database if exists weiqi;
create database weiqi;
use weiqi;

create table Country(
	name	varchar(100),
    flag	varchar(1000),  -- image url
	primary key (name)
);

create table Player(
  name         varchar(100) not null,
  countryName  varchar(100) null,
  ranking      varchar(5),
  DOB          date,
  AIFlag	   bit not null,
  coder	   	   decimal(10,2),
  info         text,
  algoType     varchar(100),
  foreign key(countryName) references Country(name),
  primary key (name)
);

create table Competition(
	compName varchar(100),
    primary key(compName)
);

create table Event(
	compName varchar(100),
    compIter int,
    primary key(compName, compIter),
    foreign key(compName) references Competition(compName)
);

create table Game(
	id	int,
	result	varchar(10),
	startDate date,
	compName varchar(100),
	compIter int,
	playerNameBlack varchar(100) not null,
	playerNameWhite varchar(100) not null,
	primary key(id),
	foreign key(playerNameBlack) references Player(name),
	foreign key(playerNameWhite) references Player(name),
	foreign key(compName, compIter) references Event(compName, compIter)
);

create table Hosts(
	compName varchar(100),
    countryName varchar(100),
	foreign key(compName) references Competition(compName),
	foreign key(countryName) references Country(name)
);

create table Move(
	gameID int,
    moveNo int,
    positionX int, positionY int,
    primary key(gameID, moveNo),
    foreign key(gameID) references Game(id)
);

create table Comment(
	id int,
    text_ text,
    voteCount int,
    playerNameTyped varchar(100),
    gameIDAbout int,
    moveNoAbout int,
    primary key(id),
    foreign key(playerNameTyped) references Player(name),
    foreign key(gameIDAbout, moveNoAbout) references Move(gameID, moveNo)
);

create table Votes(
	playerName varchar(100),
	commentID int,
    downUp boolean,  -- False for down, True for up
    primary key(playerNAme, commentID),
    foreign key(playerName) references Player(name),
    foreign key(commentID) references Comment(ID)
);

create table Tags(
	playerName varchar(100),
	commentID int,
    primary key(playerName, commentID),
    foreign key(playerName) references Player(name),
    foreign key(commentID) references Comment(ID)
);

