from django.db import models

# Create your models here.

class Card(models.Model):
    suit = models.CharField(max_length=64)
    rank = models.CharField(max_length=64)
    value = models.IntegerField()

    def __str__(self):
        return self.suit, self.rank


from django.db import models

class Game(models.Model):
    player_hand = models.JSONField(default=list)
    dealer_hand = models.JSONField(default=list)
    player_score = models.IntegerField(default=0)
    dealer_score = models.IntegerField(default=0)
    is_game_over = models.BooleanField(default=False)
    winner = models.CharField(max_length=20, blank=True, null=True)

    def deal_card(self, hand):
        """Функция для раздачи карты игроку или дилеру."""

        card = Card.objects.order_by('?').first().value
        return card



    def calculate_score(self, hand):
        """Вычисляет сумму очков руки."""
        return sum(hand)





