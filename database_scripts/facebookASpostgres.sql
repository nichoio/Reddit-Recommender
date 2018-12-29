--#Creating the Reddit Recommender Schema where the tables will be stored in 
CREATE SCHEMA IF NOT EXISTS reddit_recommender; 

--######################
--FACEBOOK DATA RELATED#
--######################

--Creating the Personal Table   
DROP TABLE IF EXISTS reddit_recommender.personal;
CREATE TABLE reddit_recommender.personal(
    u_id BIGINT, 
    name VARCHAR(50),
    age_range VARCHAR(10),
    gender VARCHAR(10));

--Creating the Likes Table       
DROP TABLE IF EXISTS reddit_recommender.likes;
CREATE TABLE reddit_recommender.likes(
    u_id BIGINT,
    name VARCHAR(50),
    category VARCHAR(50),
    about LONGTEXT,
    genre VARCHAR(100));

--Creating the Posts Table       
DROP TABLE IF EXISTS reddit_recommender.posts;
CREATE TABLE reddit_recommender.posts(
	u_id BIGINT,
    message LONGTEXT, 
    place VARCHAR(50));

--Creating the Events Table       
DROP TABLE IF EXISTS reddit_recommender.events;
CREATE TABLE reddit_recommender.events(
	u_id BIGINT, 
    name VARCHAR(50),
    place TINYTEXT,
    city VARCHAR(50),
    zip VARCHAR(20),
    country VARCHAR(50),
    rsvp_status VARCHAR(20));

--Creating the Groups Table    
DROP TABLE IF EXISTS reddit_recommender.groups;
CREATE TABLE reddit_recommender.groups(
	u_id BIGINT, 
    name VARCHAR(50),
    description LONGTEXT);
