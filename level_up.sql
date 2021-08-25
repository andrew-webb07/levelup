DROP VIEW GAMES_BY_USER

CREATE VIEW GAMES_BY_USER AS
 SELECT
    g.id,
    g.name,
    g.maker,
    g.description,
    g.game_type_id,
    g.number_of_players,
    u.id user_id,
    u.first_name || ' ' || u.last_name AS full_name
FROM
    levelupapi_game g
JOIN
    levelupapi_gamer gr ON g.gamer_id = gr.id
JOIN
    auth_user u ON gr.user_id = u.id


CREATE VIEW EVENTS_BY_USER AS
SELECT
                    e.id,
                    e.date,
                    e.time,
                    e.description,
                    e.title,
                    e.game_id,
                    gm.name,
                    u.id user_id,
                    u.first_name || ' ' || u.last_name AS full_name
                FROM
                    levelupapi_event e
                JOIN
                    levelupapi_eventgamer eg ON e.id = eg.event_id
                JOIN
                    levelupapi_gamer gr ON eg.gamer_id = gr.id
                JOIN
                    auth_user u ON gr.user_id = u.id
                JOIN 
                    levelupapi_game gm ON e.game_id = gm.id