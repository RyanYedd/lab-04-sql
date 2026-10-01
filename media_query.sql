SELECT u.username, u.email, p.title, p.posted_at
FROM users AS u
JOIN posts AS p ON u.user_id = p.user_id
WHERE p.posted_at >= '2026-02-03'
ORDER BY p.posted_at;
