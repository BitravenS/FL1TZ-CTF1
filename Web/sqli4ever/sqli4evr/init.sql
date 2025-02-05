CREATE DATABASE IF NOT EXISTS ctf_challenge;

USE ctf_challenge;

CREATE TABLE IF NOT EXISTS Us3rs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL
);

INSERT INTO Us3rs (name, password, email) VALUES
('test', 'test', 'test@example.com'),
('admin', 'super_duper_secret_admin_password_6511', 'admin@example.com'),
('alice', 'password123_09_11_2001', 'alice@example.com'),
('bob', 'qwertyazerty_7366', 'bob@example.com'),
('charlie', 'letmein_i_said_lemmein!!', 'charlie@example.com'),
('bitraven', 'mahboul_crypto_2010', 'bitraven@example.com'),
('admin2', 'super_duper_secret_admin_password_6511', 'admin2@example.com'),
('eve', 'password_hunter2!!', 'eve@example.com'),
('mallory', 'haxxor_password_9999', 'mallory@example.com'),
('trent', 'secure_pass_tr3nt', 'trent@example.com'),
('oscar', 'randomword123!', 'oscar@example.com'),
('victor', 'cipherkey_v1ctor2025', 'victor@example.com'),
('peggy', 'passkey_4p3ggy!', 'peggy@example.com'),
('walter', 'd0nt_guess_this_w@lter', 'walter@example.com'),
('judy', 'h@ck_this_if_you_c@nn', 'judy@example.com');

CREATE TABLE IF NOT EXISTS books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL
);

INSERT INTO books (title, author) VALUES
('SQL Injection Basics', 'John Doe'),
('Advanced SQL Exploitation', 'Jane Doe'),
('CTF Challenges for Beginners', 'FL1TZ'),
('Hacking for Fun', 'Bob Brown'),
('Union based sql injection','joe mama'),
('sqlmap 0 to hero','3ami tboun');
