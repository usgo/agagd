CREATE VIEW most_rated_games_view AS
    SELECT 
        pin,
        CONCAT(players.name, ' ', players.last_name) AS Name,
        Game_Count
    FROM
        (SELECT 
            x.pin, count1 + count2 AS Game_Count
        FROM
            (SELECT 
            pin_player_1 AS pin, COUNT(game_id) AS count1
        FROM
            games
        WHERE
            game_date > NOW() - INTERVAL 1 YEAR
                AND exclude = 0
                AND games.online = 0
        GROUP BY pin_player_1) AS x
        INNER JOIN (SELECT 
            pin_player_2 AS pin, COUNT(game_id) AS count2
        FROM
            games
        WHERE
            game_date > NOW() - INTERVAL 1 YEAR
                AND exclude = 0
                AND games.online = 0
        GROUP BY pin_player_2) AS y ON y.pin = x.pin
        ORDER BY Game_Count DESC , pin
        LIMIT 10) AS p
            INNER JOIN
        players ON p.pin = players.pin_player

CREATE VIEW most_tournaments_view AS
    SELECT 
        pin,
        CONCAT(players.name, ' ', players.last_name) AS Name,
        Tournament_Count
    FROM
        (SELECT 
            y.pin, COUNT(tournament_code) AS Tournament_Count
        FROM
            (SELECT 
            pin_player_1 AS pin, tournament_code
        FROM
            games
        WHERE
            game_date > NOW() - INTERVAL 1 YEAR
                AND games.online = 0
                AND exclude = 0 UNION SELECT 
            pin_player_2 AS pin, tournament_code
        FROM
            games
        WHERE
            game_date > NOW() - INTERVAL 1 YEAR
                AND games.online = 0
                AND exclude = 0) AS y
        GROUP BY pin
        ORDER BY Tournament_Count DESC , pin
        LIMIT 10) AS p
            INNER JOIN
        players ON p.pin = players.pin_player
