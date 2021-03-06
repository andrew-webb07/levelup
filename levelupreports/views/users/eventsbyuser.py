"""Module for generating games by user report"""
import sqlite3
from django.shortcuts import render
from levelupapi.models import Game, Event
from levelupreports.views import Connection


def userevent_list(request):
    """Function to build an HTML report of events by user"""
    if request.method == 'GET':
        # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Query for all games, with related user info.
            db_cursor.execute("""
                SELECT
                    id,
                    date,
                    time,
                    description,
                    title,
                    game_id,
                    name,
                    user_id,
                    full_name
                FROM
                    EVENTS_BY_USER

            """)

                # JOIN
                #     levelupapi_eventgamer eg ON e.id = eg.event_id
                # JOIN
                #     levelupapi_gamer gr ON eg.gamer_id = gr.id
                # JOIN
                #     auth_user u ON gr.user_id = u.id
                # JOIN 
                #     levelupapi_game gm ON e.game_id = gm.id

            dataset = db_cursor.fetchall()

            events_by_user = {}

            for row in dataset:
                event = Event()
                event.date = row["date"]
                event.time = row["time"]
                event.description = row["description"]
                event.title = row["title"]
                event.game_id = row["game_id"]

                uid = row["user_id"]

                if uid in events_by_user:
                    events_by_user[uid]['events'].append(event)

                else:
                    events_by_user[uid] = {}
                    events_by_user[uid]["id"] = uid
                    events_by_user[uid]["full_name"] = row["full_name"]
                    events_by_user[uid]["events"] = [event]

        list_of_users_with_events = events_by_user.values()

        template = 'users/list_with_events.html'
        context = {
            'userevent_list': list_of_users_with_events
        }

        return render(request, template, context)