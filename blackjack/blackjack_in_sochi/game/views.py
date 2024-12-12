# blackjack/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Game
from .serializer import GameSerializer

class StartGameView(APIView):
    def post(self, request):
        game = Game()

        game.deal_card(game.player_hand)
        game.deal_card(game.dealer_hand)
        game.player_score = game.calculate_score(game.player_hand)
        game.dealer_score = game.calculate_score(game.dealer_hand)
        game.save()
        serializer = GameSerializer(game)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class HitView(APIView):
    def post(self, request, pk):
        try:
            game = Game.objects.get(pk=pk)
        except Game.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if game.is_game_over:
            return Response({"message": "Game is already over."}, status=status.HTTP_400_BAD_REQUEST)

        # Игрок берёт карту
        game.deal_card(game.player_hand)
        game.player_score = game.calculate_score(game.player_hand)

        # Проверка на перебор
        if game.player_score > 21:
            game.is_game_over = True
            game.winner = 'Dealer'

        game.save()
        serializer = GameSerializer(game)
        return Response(serializer.data)

class StandView(APIView):
    def post(self, request, pk):
        try:
            game = Game.objects.get(pk=pk)
        except Game.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if game.is_game_over:
            return Response({"message": "Game is already over."}, status=status.HTTP_400_BAD_REQUEST)

        # Дилер берёт карты до тех пор, пока сумма меньше 17
        while game.dealer_score < 17:
            game.deal_card(game.dealer_hand)
            game.dealer_score = game.calculate_score(game.dealer_hand)

        # Определение победителя
        if game.dealer_score > 21 or game.player_score > game.dealer_score:
            game.winner = 'Player'
        elif game.dealer_score > game.player_score:
            game.winner = 'Dealer'
        else:
            game.winner = 'Draw'

        game.is_game_over = True
        game.save()
        serializer = GameSerializer(game)
        return Response(serializer.data)
