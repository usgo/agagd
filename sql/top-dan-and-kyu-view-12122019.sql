CREATE VIEW top_dan_view AS
SELECT 
    m.member_id AS member_id,
    m.full_name AS full_name,
    FORMAT(p.rating, 2) AS rating
FROM
    (SELECT 
        x.pin, COUNT(*) AS game_count
    FROM
        (SELECT 
        pin_player_1 AS pin
    FROM
        games
    WHERE
        game_date > DATE_SUB(NOW(), INTERVAL 1 YEAR)
            AND exclude = 0
            AND games.online = 0 UNION ALL SELECT 
        pin_player_2 AS pin
    FROM
        games
    WHERE
        game_date > DATE_SUB(NOW(), INTERVAL 1 YEAR)
            AND exclude = 0
            AND games.online = 0) AS x
    GROUP BY x.pin) AS a
        INNER JOIN
    members m ON a.pin = m.member_id
        INNER JOIN
    players p ON p.pin_player = a.pin
WHERE
    game_count > 10 AND rating > 0
ORDER BY p.rating DESC
LIMIT 10

CREATE VIEW top_kyu_view AS
    SELECT 
        m.member_id, m.full_name, FORMAT(p.rating, 2) AS rating
    FROM
        (SELECT 
            x.pin, COUNT(*) AS game_count
        FROM
            (SELECT 
            pin_player_1 AS pin
        FROM
            games
        WHERE
            game_date > DATE_SUB(NOW(), INTERVAL 1 YEAR)
                AND exclude = 0
                AND games.online = 0 UNION ALL SELECT 
            pin_player_2 AS pin
        FROM
            games
        WHERE
            game_date > DATE_SUB(NOW(), INTERVAL 1 YEAR)
                AND exclude = 0
                AND games.online = 0) AS x
        GROUP BY x.pin) AS a
            INNER JOIN
        members m ON a.pin = m.member_id
            INNER JOIN
        players p ON p.pin_player = a.pin
    WHERE
        game_count > 10 AND rating < 0
    ORDER BY p.rating DESC
    LIMIT 10
