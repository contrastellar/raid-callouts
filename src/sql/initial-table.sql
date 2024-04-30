create table absent_players (
user_id int NOT NULL,
user_name varchar(20) NOT NULL,
date_ab date NOT NULL,
reason_ab varchar(200),
has_passed int DEFAULT 0);
/