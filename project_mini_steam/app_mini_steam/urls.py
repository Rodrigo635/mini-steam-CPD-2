from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('buscar_por_preco/', views.buscar_jogos_por_preco, name='buscar_jogos_por_preco'),
    path('buscar_por_faixa_preco/', views.buscar_por_faixa_preco, name='buscar_por_faixa_preco'),
    path('categorias/', views.categorias, name='categorias'),
    path('games_por_genero/<str:genre>/', views.games_por_genero, name='games_por_genero'),
    path('noticias/', views.noticias, name='noticias'),
]