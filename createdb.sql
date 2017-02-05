drop database course_connect;
create database course_connect;
create user course_connect_user with password 'password';
grant all privileges on database course_connect to course_connect_user;
alter role course_connect_user set client_encoding to 'utf8';
alter role course_connect_user set default_transaction_isolation to 'read committed';
alter role course_connect_user set timezone to 'Asia/Kolkata';
