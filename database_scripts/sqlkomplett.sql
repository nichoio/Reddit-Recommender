CREATE SCHEMA IF NOT EXISTS reddit_recommender; 

#######################
#	       GENERAL#
#######################
DROP TABLE IF EXISTS reddit_recommender.user;
CREATE TABLE reddit_recommender.user( 
    name VARCHAR(50), 
    facebook_gender VARCHAR(10),
    twitter_name VARCHAR(50),
    twitter_followers_count INT,
    twitter_friends_count INT,
    twitter_description VARCHAR(500),
    facebook_u_id VARCHAR(50) UNIQUE, 
    twitter_screen_name VARCHAR(50) UNIQUE, 
    reddit_u_id VARCHAR(50) UNIQUE,
    PRIMARY KEY(name));
    
#######################
#REDDIT DATA RELATED#
#######################
DROP TABLE IF EXISTS reddit_recommender.subreddits;
CREATE TABLE reddit_recommender.subreddits( 
    title VARCHAR(400), 
    display_name VARCHAR(400), 
    subscribers int,
    language VARCHAR(100),
    advertiser_category VARCHAR(200),
    public_description longtext,
    description longtext,
    PRIMARY KEY(display_name))
;

CREATE TABLE reddit_recommender.reddit_personal(
    user_name VARCHAR(100), 
    display_name VARCHAR(400),
    subscribed TINYINT(1),
    comments TINYINT(1),
    PRIMARY KEY (user_name, display_name),
    FOREIGN KEY(display_name) REFERENCES reddit_recommender.subreddits(display_name) ON DELETE CASCADE,
    FOREIGN KEY(user_name) REFERENCES reddit_recommender.user(reddit_u_id) ON DELETE CASCADE)
;

#######################
#FACEBOOK DATA RELATED#
#######################
#Creating the Personal Table  
#!NOT NEEDED ANYMORE AS WE DECIDED TO MERGE THE USER TABLES!
#DROP TABLE IF EXISTS reddit_recommender.facebook_personal;
#CREATE TABLE reddit_recommender.personal(
#    u_id BIGINT, 
#    name VARCHAR(50),
#    birthday VARCHAR(10),
#    gender VARCHAR(10));

#Creating the Likes Table       
DROP TABLE IF EXISTS reddit_recommender.facebook_likes;
CREATE TABLE reddit_recommender.facebook_likes(
	l_id VARCHAR(50),
    facebook_u_id VARCHAR(50),
    name VARCHAR(50),
    category VARCHAR(50),
    about LONGTEXT,
    genre VARCHAR(100), 
    PRIMARY KEY(l_id, facebook_u_id),
    FOREIGN KEY(facebook_u_id) REFERENCES user(facebook_u_id) ON DELETE CASCADE);

#Creating the Posts Table       
DROP TABLE IF EXISTS reddit_recommender.facebook_posts;
CREATE TABLE reddit_recommender.facebook_posts(
	p_id VARCHAR(50),
	facebook_u_id VARCHAR(50),
    message LONGTEXT, 
    place VARCHAR(50),
    PRIMARY KEY(p_id,facebook_u_id),
    FOREIGN KEY(facebook_u_id) REFERENCES user(facebook_u_id) ON DELETE CASCADE);

#Creating the Events Table       
DROP TABLE IF EXISTS reddit_recommender.facebook_events;
CREATE TABLE reddit_recommender.facebook_events(
	e_id VARCHAR(50),
	facebook_u_id VARCHAR(50), 
    name VARCHAR(200),
    place TINYTEXT,
    city VARCHAR(50),
    zip VARCHAR(20),
    country VARCHAR(50),
    rsvp_status VARCHAR(20),
    PRIMARY KEY(e_id,facebook_u_id),
    FOREIGN KEY(facebook_u_id) REFERENCES user(facebook_u_id) ON DELETE CASCADE);

#Creating the Groups Table    
DROP TABLE IF EXISTS reddit_recommender.facebook_groups;
CREATE TABLE reddit_recommender.facebook_groups(
	g_id VARCHAR(50),
	facebook_u_id VARCHAR(50), 
    name VARCHAR(100),
    description LONGTEXT,
    PRIMARY KEY(g_id,facebook_u_id),
    FOREIGN KEY(facebook_u_id) REFERENCES user(facebook_u_id) ON DELETE CASCADE);

#######################
#TWITTER DATA RELATED #
#######################
DROP TABLE IF EXISTS reddit_recommender.twitter_tweets;
CREATE TABLE reddit_recommender.twitter_tweets(
	screen_name varchar(255) NOT NULL,
	text varchar(300),
	id bigint NOT NULL,
	retweet_count int,
	favorite_count int,
	created_at varchar(255),
	PRIMARY KEY (id),
    FOREIGN KEY (screen_name) REFERENCES reddit_recommender.user(twitter_screen_name) ON DELETE CASCADE
);

DROP TABLE IF EXISTS reddit_recommender.twitter_hashtags;
CREATE TABLE reddit_recommender.twitter_hashtags(
    hashtag varchar(255) NOT NULL,
    tweetId bigint NOT NULL,
    PRIMARY KEY(hashtag, tweetId),
    FOREIGN KEY (tweetId) REFERENCES reddit_recommender.twitter_tweets(id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS reddit_recommender.twitter_friends_user;
CREATE TABLE reddit_recommender.twitter_friends_user(
    screen_name varchar(255),
    followers_count int,
    display_name varchar(255),
    description varchar(255),
    friends_count int,
    name varchar(255),
    PRIMARY KEY(screen_name)
);

DROP TABLE IF EXISTS reddit_recommender.twitter_friends;
CREATE TABLE reddit_recommender.twitter_friends(
    screen_name varchar(255),
    followed_user varchar(255),
    PRIMARY KEY(screen_name, followed_user),
    FOREIGN KEY (followed_user) REFERENCES reddit_recommender.twitter_friends_user(screen_name) ON DELETE CASCADE,
    FOREIGN KEY(screen_name) REFERENCES reddit_recommender.user(twitter_screen_name) ON DELETE CASCADE
);
