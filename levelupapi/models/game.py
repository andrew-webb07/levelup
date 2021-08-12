from django.db import models
from django.db.models.deletion import CASCADE

class Game(models.Model):
    name = models.CharField(max_length=100)
    game_type = models.ForeignKey("GameType", on_delete=models.CASCADE)
    description = models.CharField(max_length=150)
    number_of_players = models.IntegerField()
    gamer = models.ForeignKey("Gamer", on_delete=CASCADE)
    maker = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    @property
    def event_count(self):
        return self.__event_count

    @event_count.setter
    def event_count(self, value):
        self.__event_count = value

    @property
    def user_event_count(self):
        return self.__user_event_count

    @user_event_count.setter
    def user_event_count(self, value):
        self.__user_event_count = value