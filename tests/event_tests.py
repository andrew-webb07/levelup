import json
from rest_framework import status
from rest_framework.test import APITestCase
from levelupapi.models import Event, Game, Gamer, GameType
from django.contrib.auth.models import User


class EventTests(APITestCase):
    def setUp(self):
        """
        Create a new account and create sample category
        """
        url = "/register"
        data = {
            "username": "steve",
            "password": "Admin8*",
            "email": "steve@stevebrownlee.com",
            "address": "100 Infinity Way",
            "phone_number": "555-1212",
            "first_name": "Steve",
            "last_name": "Brownlee",
            "bio": "Love those gamez!!"
        }
        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)
        self.token = json_response["token"]
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        game_type = GameType()
        game_type.label = "Board game"
        game_type.save()

        user = User.objects.get(pk=1)

        gamer = Gamer.objects.get(pk=user.id)

        game = Game()
        game.name = "Risk"
        game.description = "the game of world domination"
        game.number_of_players = 6
        game.maker = "Albert Lamorisse"
        game.game_type = game_type
        game.gamer = gamer
        game.save()


    def test_create_event(self):
        """
        Ensure we can create a new event.
        """
        url = "/events"
        data = {
            "gameId": 1,
            "date": "2021-07-31",
            "time": "7:00 PM",
            "description": "Playing Risk for 5 days",
            "title": "Risk Night",
            "attendees": []
        }

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["description"], data["description"])
        self.assertEqual(json_response["date"], data['date'])
        self.assertEqual(json_response["time"], data['time'])
        self.assertEqual(json_response["title"], data['title'])
        self.assertEqual(json_response["attendees"], data['attendees'])
        

    def test_get_event(self):
        """
        Ensure we can get an existing game.
        """
        event = Event()
        event.game_id = 1
        event.description = "This will be a party!"
        event.date = "2021-06-30"
        event.time = "02:00:00"
        event.host_id = 1
        event.save()

        # Make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        # Initiate request and store response
        response = self.client.get(f"/events/{event.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["date"], event.date)
        self.assertEqual(json_response["time"], event.time)
        self.assertEqual(json_response["description"], event.description)

    def test_change_game(self):
        """
        Ensure we can change an existing game.
        """
        event = Event()
        event.game_id = 1
        event.description = "We will play some games!"
        event.date = "2021-04-30"
        event.time = "05:00:00"
        event.host_id = 1
        event.save()

        # DEFINE NEW PROPERTIES FOR GAME
        data = {
            "gameId": 1,
            "date": "2021-05-15",
            "time": "04:00:00",
            "description": "I don't like this game",
            "attendees": []
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put(f"/events/{event.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET GAME AGAIN TO VERIFY CHANGES
        response = self.client.get(f"/events/{event.id}")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the properties are correct
        self.assertEqual(json_response["date"], data["date"])
        self.assertEqual(json_response["time"], data["time"])
        self.assertEqual(json_response["description"], data["description"])
        self.assertEqual(json_response["attendees"], [])
        

    def test_delete_event(self):
        """
        Ensure we can delete an existing event.
        """
        event = Event()
        event.game_id = 1
        event.description = "This will be a party!"
        event.date = "2021-06-30"
        event.time = "02:00:00"
        event.host_id = 1
        event.save()

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(f"/events/{event.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET GAME AGAIN TO VERIFY 404 response
        response = self.client.get(f"/events/{event.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
