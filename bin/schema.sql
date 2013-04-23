create table Ratings (
	UserID INTEGER,
	MovieID INTEGER,
	Rating INTEGER,
	Time TIMESTAMP 
);
create table Movies (
	MovieID INTEGER PRIMARY KEY,
	Title VARCHAR(64),
	Genres VARCHAR(256)
);

create table 