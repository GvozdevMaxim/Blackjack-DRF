# blackjack/urls.py
from django.urls import path
from .views import StartGameView, HitView, StandView

urlpatterns = [
    path('start/', StartGameView.as_view(), name='start-game'),
    path('<int:pk>/hit/', HitView.as_view(), name='hit'),
    path('<int:pk>/stand/', StandView.as_view(), name='stand'),
]
