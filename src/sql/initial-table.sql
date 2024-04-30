create table absent_players (
user_id int NOT NULL,
user_name varchar NOT NULL,
date_ab date NOT NULL,
reason_ab varchar,
has_passed int DEFAULT 0);
/
