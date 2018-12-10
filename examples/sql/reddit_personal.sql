CREATE TABLE reddit_personal (
user_name VARCHAR(60),
sub_name VARCHAR(60),
subscribed TINYINT(1),
comments MEDIUMINT UNSIGNED,
PRIMARY KEY (user_name, sub_name)
) 