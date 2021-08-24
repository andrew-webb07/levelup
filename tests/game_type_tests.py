import json
from rest_framework import status
from rest_framework.test import APITestCase
from levelupapi.models import GameType, Game

class GameTypeTests(APITestCase):
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

    def test_create_game_type(self):
        """
        Ensure we can create a new game_type.
        """
        url = "/gametypes"
        data = {
            "label": "Video Games"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(json_response["label"], data["label"])
        
    def test_get_game_type(self):
        """
        Ensure we can get an existing game type.
        """
        game_type = GameType()
        game_type.label = "Sports"
        game_type.save()

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(f"/gametypes/{game_type.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(response.data["label"], game_type.label)

    def test_change_game_type(self):
        """
        Ensure we can change an existing game type.
        """
        game_type = GameType()
        game_type.label = "Mult-user"
        game_type.save()

        data = {
            "label": "Cards"
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put(f"/gametypes/{game_type.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f"/gametypes/{game_type.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["label"], data["label"])

    def test_delete_game_type(self):
        """
        Ensure we can delete an existing game.
        """
        game_type = GameType()
        game_type.label = "Sports"
        game_type.save()

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(f"/gametypes/{game_type.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f"/gametypes/{game_type.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
