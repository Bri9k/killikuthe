DROP TABLE person_memberof_club;
DROP TABLE club_canuse_key;
DROP TABLE log;
DROP TABLE request_key;
DROP TABLE club;
DROP TABLE killi;
DROP TABLE place;
DROP TABLE person;


CREATE TABLE person (
	MIS CHAR(9) NOT NULL,
	first_name VARCHAR(20) NOT NULL,
	last_name VARCHAR(20) NOT NULL,
	mobileno CHAR(10) NOT NULL,
	email VARCHAR(45) NOT NULL,
	password_hash CHAR(94), -- for the werkzeug generate_password_hash function
	PRIMARY KEY (MIS),
	UNIQUE (email),
	UNIQUE (mobileno),
	CONSTRAINT CHECK (email LIKE '_%@_%._%')
);

CREATE TABLE place (
	pid INT NOT NULL AUTO_INCREMENT,
	name VARCHAR(45) NOT NULL,
	store BOOL NOT NULL,
	PRIMARY KEY (pid),
	UNIQUE (name),
	CONSTRAINT CHECK (name LIKE '_%')
);


CREATE TABLE killi (
	kid INT NOT NULL AUTO_INCREMENT,
	place_pid INT NOT NULL,
	person_MIS VARCHAR(9), 
	place_pid_store INT, -- Where is the key stored?
	PRIMARY KEY (kid, place_pid),
	FOREIGN KEY (place_pid) REFERENCES place(pid) ON DELETE CASCADE,
	-- If place is deleted key gets deleted
	FOREIGN KEY (person_MIS) REFERENCES person(MIS) ON DELETE SET NULL,
	-- If person is deleted he no longer holds key THIS HAS TO BE HANDLED DURING THE DELETION
	FOREIGN KEY (place_pid_store) REFERENCES place(pid) ON DELETE SET NULL);


CREATE TABLE club (
	cid INT NOT NULL AUTO_INCREMENT,
	clubname VARCHAR(45) NOT NULL,
	managed_by VARCHAR(9) NOT NULL,
	PRIMARY KEY (cid),
	FOREIGN KEY (managed_by) REFERENCES person(MIS), -- delete to be handled by application code
	CONSTRAINT CHECK (clubname LIKE '_%'),
	UNIQUE (clubname));


CREATE TABLE request_key (
	destination VARCHAR(9) NOT NULL, -- person requesting key
	key_id INT NOT NULL,
	place_pid INT NOT NULL, -- key being requested
	PRIMARY KEY (destination, key_id, place_pid),
	FOREIGN KEY (destination) REFERENCES person(MIS) ON DELETE CASCADE,
	-- If person removed his requests deleted
	FOREIGN KEY (key_id, place_pid) REFERENCES killi(kid, place_pid) ON DELETE CASCADE);

CREATE TABLE log (
	lid INT NOT NULL AUTO_INCREMENT,
	destination_person VARCHAR(9) NOT NULL, -- person requesting key
	destination_place INT NOT NULL,
	source_person VARCHAR(9) NOT NULL,
	source_place INT NOT NULL,
	time DATETIME NOT NULL,
	key_kid INT NOT NULL,
	key_place_pid INT NOT NULL,
	PRIMARY KEY (lid),
	FOREIGN KEY (key_kid, key_place_pid) REFERENCES killi(kid, place_pid) ON DELETE NO ACTION,
	FOREIGN KEY (destination_place) REFERENCES place(pid) ON DELETE NO ACTION,
	FOREIGN KEY (source_place) REFERENCES place(pid) ON DELETE NO ACTION,
	FOREIGN KEY (source_person) REFERENCES person(MIS) ON DELETE NO ACTION,
	FOREIGN KEY (destination_person) REFERENCES person(MIS) ON DELETE NO ACTION);

CREATE TABLE club_canuse_key (
	club_cid INT NOT NULL,
	key_kid INT NOT NULL,
	key_place_pid INT NOT NULL,
	PRIMARY KEY (club_cid, key_kid, key_place_pid),
	FOREIGN KEY (club_cid) REFERENCES club(cid) ON DELETE CASCADE,
	FOREIGN KEY (key_kid, key_place_pid) REFERENCES killi(kid, place_pid) ON DELETE CASCADE);

CREATE TABLE person_memberof_club (
	person_MIS VARCHAR(9) NOT NULL,
	club_cid INT NOT NULL,
	PRIMARY KEY (person_MIS, club_cid),
	FOREIGN KEY (person_MIS) REFERENCES person(MIS) ON DELETE CASCADE,
	FOREIGN KEY (club_cid) REFERENCES club(cid) ON DELETE CASCADE
);


