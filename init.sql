-- init.sql
CREATE DATABASE IF NOT EXISTS server_logs;
USE server_logs;

CREATE TABLE IF NOT EXISTS request_logs (
    user_id VARCHAR(20),
    request VARCHAR(1024),
    log_time TIMESTAMP(0)
);

CREATE TABLE IF NOT EXISTS response_logs (
    user_id VARCHAR(20),
    response VARCHAR(1024),
    log_time TIMESTAMP(0)
);

CREATE TABLE IF NOT EXISTS error_logs (
    user_id VARCHAR(20),
    error VARCHAR(256),
    log_time TIMESTAMP(0)
);