DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id    INT PRIMARY KEY,
    username   VARCHAR(50)  NOT NULL,
    email      VARCHAR(100) NOT NULL,
    created_at DATETIME     NOT NULL
);

CREATE TABLE posts (
    post_id    INT PRIMARY KEY,
    user_id    INT          NOT NULL,
    title      VARCHAR(100) NOT NULL,
    body       TEXT,
    posted_at  DATETIME     NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

INSERT INTO users VALUES (1,  'alice',  'alice@example.com',  '2026-01-05 09:00:00');
INSERT INTO users VALUES (2,  'bob',    'bob@example.com',    '2026-01-06 10:15:00');
INSERT INTO users VALUES (3,  'carol',  'carol@example.com',  '2026-01-07 11:30:00');
INSERT INTO users VALUES (4,  'dave',   'dave@example.com',   '2026-01-08 12:45:00');
INSERT INTO users VALUES (5,  'erin',   'erin@example.com',   '2026-01-09 08:20:00');
INSERT INTO users VALUES (6,  'frank',  'frank@example.com',  '2026-01-10 14:05:00');
INSERT INTO users VALUES (7,  'grace',  'grace@example.com',  '2026-01-11 15:40:00');
INSERT INTO users VALUES (8,  'heidi',  'heidi@example.com',  '2026-01-12 16:55:00');
INSERT INTO users VALUES (9,  'ivan',   'ivan@example.com',   '2026-01-13 17:10:00');
INSERT INTO users VALUES (10, 'judy',   'judy@example.com',   '2026-01-14 18:25:00');

INSERT INTO posts VALUES (1,  1,  'Hello World',      'My first post.',          '2026-02-01 09:00:00');
INSERT INTO posts VALUES (2,  1,  'SQL is fun',       'Learning joins today.',   '2026-02-02 10:00:00');
INSERT INTO posts VALUES (3,  2,  'Weekend hike',     'Went up Humpback Rock.',  '2026-02-03 11:00:00');
INSERT INTO posts VALUES (4,  3,  'Recipe: pasta',    'Boil, drain, enjoy.',     '2026-02-04 12:00:00');
INSERT INTO posts VALUES (5,  4,  'Gaming night',     'Played until 2am.',       '2026-02-05 13:00:00');
INSERT INTO posts VALUES (6,  5,  'Book review',      'Loved the ending.',       '2026-02-06 14:00:00');
INSERT INTO posts VALUES (7,  6,  'Travel tips',      'Pack light.',             '2026-02-07 15:00:00');
INSERT INTO posts VALUES (8,  7,  'Music picks',      'Top 5 albums of 2026.',   '2026-02-08 16:00:00');
INSERT INTO posts VALUES (9,  8,  'Study group',      'Meeting Thursday.',       '2026-02-09 17:00:00');
INSERT INTO posts VALUES (10, 9,  'Coffee thoughts',  'Pour-over wins.',         '2026-02-10 18:00:00');
INSERT INTO posts VALUES (11, 10, 'Final post',       'Thanks for reading.',     '2026-02-11 19:00:00');
