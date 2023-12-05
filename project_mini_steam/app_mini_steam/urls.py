from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('buscar_por_preco/', views.buscar_jogos_por_preco, name='buscar_jogos_por_preco'),
    path('buscar_por_faixa_preco/', views.buscar_por_faixa_preco, name='buscar_por_faixa_preco'),
    path('categorias/', views.categorias, name='categorias'),
    path('games_por_genero/<str:genre>/', views.games_por_genero, name='games_por_genero'),
    path('noticias/', views.noticias, name='noticias'),
    path('login/', views.login, name='login'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('logout/', views.sair, name='sair'),
    path('sua_loja/', views.sua_loja, name='sua_loja'),
    path('comunidade/', views.comunidade, name='comunidade'),
    path('postar/', views.postar, name='postar'),
]