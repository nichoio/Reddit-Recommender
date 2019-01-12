##Creating the Reddit Recommender Schema where the tables will be stored in 
CREATE SCHEMA IF NOT EXISTS reddit_recommender; 

#######################
#		GENERAL		  #
#######################
DROP TABLE IF EXISTS reddit_recommender.user;
CREATE TABLE reddit_recommender.user( 
    name VARCHAR(50), 
    facebook_u_id VARCHAR(50), 
    twitter_u_id VARCHAR(50), 
    reddit_u_id VARCHAR(50),
    PRIMARY KEY(facebook_u_id));
    

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
	l_id INT AUTO_INCREMENT,
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
	p_id INT AUTO_INCREMENT,
	facebook_u_id VARCHAR(50),
    message LONGTEXT, 
    place VARCHAR(50),
    PRIMARY KEY(p_id,facebook_u_id),
    FOREIGN KEY(facebook_u_id) REFERENCES user(facebook_u_id) ON DELETE CASCADE);

#Creating the Events Table       
DROP TABLE IF EXISTS reddit_recommender.facebook_events;
CREATE TABLE reddit_recommender.facebook_events(
	e_id INT AUTO_INCREMENT,
	facebook_u_id VARCHAR(50), 
    name VARCHAR(50),
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
	g_id INT AUTO_INCREMENT,
	facebook_u_id VARCHAR(50), 
    name VARCHAR(100),
    description LONGTEXT,
    PRIMARY KEY(g_id,facebook_u_id),
    FOREIGN KEY(facebook_u_id) REFERENCES user(facebook_u_id) ON DELETE CASCADE);