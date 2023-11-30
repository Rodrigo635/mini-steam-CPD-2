from django.shortcuts import render
from .game_utils import generate_random_games
from .models import Game
from decimal import Decimal


def comentarios_inuteis_e_pesquisas():
    # Bônus algoritmo de levenshtein <-- similaridade de levenshtein talvez um dia eu implemente :/
    # Trie (árvore de prefixos) para buscar jogos por nome

    # Tutoriais que levei como base:
    # https://youtu.be/lxHF-mVdwK8?si=Mt109q00GWMueKhv
    # https://www.freecodecamp.org/portuguese/news/insercao-rotacao-e-fator-de-balanceamento-da-arvore-avl-explicados/
    
    # Preço que está em 2 jogos: 142,38 / 142.38
    pass


class NoJogo:
    def __init__(self, jogo):
        self.jogo = jogo
        self.esquerda = None
        self.direita = None
        # Altura pra ser usada no balanceamento da arvore
        self.altura = 1


class ArvoreJogos:
    def __init__(self):
        self.raiz = None

    def inserir(self, jogo):
        if self.raiz is None:
            self.raiz = NoJogo(jogo)
        else:
            self.raiz = self._inserir(self.raiz, jogo)

    def altura(self, no):
        if no is None:
            return 0
        return no.altura

    def atualizar_altura(self, no):
        if no is not None:
            # A função max calcula o maior entre dois valores
            no.altura = 1 + max(self.altura(no.esquerda), self.altura(no.direita))

    """
    z é o no que vai ser rodado pra direita
    y é o filho esquerdo do z
    T2 é a subárvore da direita de y
    a rotação acontece ajustando os ponteiros
    As alturas de z e y são atualizadas
    """
    def _rotacao_direita(self, z):
        y = z.esquerda
        if y is not None:
            T2 = y.direita
            y.direita = z
            z.esquerda = T2
            self.atualizar_altura(z)
            self.atualizar_altura(y)
            return y
        else:
            # Rrtorna a raiz atual se o filho esquerdo 'y' for None e a rotação não acontece
            return z

    """
    y é o no que vai ser rodado pra esquerda
    x é o filho direito do y
    T2 é o subárvore da esquerda de x
    a rotação acontece ajustando os ponteiros
    as alturas de y e x são atualizadas
    """
    def _rotacao_esquerda(self, y):
        x = y.direita
        if x is not None:
            T2 = x.esquerda
            x.esquerda = y
            y.direita = T2
            self.atualizar_altura(y)
            self.atualizar_altura(x)
            return x
        else:
            # Retorna a raiz atual se o filho direito 'x' for None e a rotação tbm não acontece
            return y

    # Calcula o fator de balanceamento do no como diferença entre as alturas das subárvores da esquerda e direita
    def _fator_de_balanceamento(self, no):
        if no is None:
            return 0
        return self.altura(no.esquerda) - self.altura(no.direita)

    def _inserir(self, no, jogo):
        if no is None:
            return NoJogo(jogo)

        if jogo.price < no.jogo.price:
            no.esquerda = self._inserir(no.esquerda, jogo)
        elif jogo.price > no.jogo.price:
            no.direita = self._inserir(no.direita, jogo)
        else:
            no.direita = self._inserir(no.direita, jogo)

        self.atualizar_altura(no)
        fator = self._fator_de_balanceamento(no)

        # A rotação acontece se o fator de balanceamento for maior que 5 ou menor que -5
        if fator > 5:
            if jogo.price < no.esquerda.jogo.price:
                return self._rotacao_direita(no)
            else:
                no.esquerda = self._rotacao_esquerda(no.esquerda)
                return self._rotacao_direita(no)

        if fator < -5:
            if jogo.price > no.direita.jogo.price:
                return self._rotacao_esquerda(no)
            else:
                no.direita = self._rotacao_direita(no.direita)
                return self._rotacao_esquerda(no)

        return no

    def _rebalancear(self, no, jogo):
        if no is None:
            return None

        no.esquerda = self._rebalancear(no.esquerda, jogo)
        no.direita = self._rebalancear(no.direita, jogo)
        self.atualizar_altura(no)
        fator = self._fator_de_balanceamento(no)

        if fator > 5:
            if jogo.price < no.esquerda.jogo.price:
                return self._rotacao_direita(no)
            else:
                no.esquerda = self._rotacao_esquerda(no.esquerda)
                return self._rotacao_direita(no)

        if fator < -5:
            if jogo.price > no.direita.jogo.price:
                return self._rotacao_esquerda(no)
            else:
                no.direita = self._rotacao_direita(no.direita)
                return self._rotacao_esquerda(no)

        return no
    
    # Com o em_ordem aqui eu percorro a arvore e armazeno todos os jogos em uma lista ordenada pela ordem que a AVL arrumou
    def em_ordem(self, no, lista_jogos):
        if no is not None:
            self.em_ordem(no.esquerda, lista_jogos)
            lista_jogos.append(no.jogo)
            self.em_ordem(no.direita, lista_jogos)

    def jogos_em_ordem(self):
        lista_jogos = []
        self.em_ordem(self.raiz, lista_jogos)
        return lista_jogos
    
    def print_da_arvore(self, no, nivel=0, prefixo="root: "):
        if no is not None:
            print(" " * (nivel * 4) + prefixo + "[ R$", no.jogo.price, "]", no.jogo.id, "-", no.jogo.name, "-", no.jogo.developer, "-", no.jogo.genre)
            if no.esquerda or no.direita:
                self.print_da_arvore(no.esquerda, nivel + 1, "esquerda - ")
                self.print_da_arvore(no.direita, nivel + 1, "direita - ")

    def mostrar_arvore(self):
        self.print_da_arvore(self.raiz)

    # GPT me deu uma ajuda nessa busca por preço pq tava dando muito erro então consultei com ele, foi mal :(
    # Ele me sugeriu usar essa nova condição de tolerância de preço, e deu certo. Então não tenho muito do que reclamar :/
    def buscar_por_preco(self, preco, tolerancia=0.001):
        return self._buscar_por_preco(self.raiz, Decimal(preco), tolerancia)

    def _buscar_por_preco(self, no, preco, tolerancia):
        if no is None:
            return []
        # Tive que atribuir o preço a um Decimal pra poder fazer a comparação por conta de erros tbm... É deu mt erro tentando fazer isso dar certo
        jogo_preco = Decimal(str(no.jogo.price))
        if abs(preco - jogo_preco) < Decimal(str(tolerancia)):
            return (
                [no.jogo] +
                self._buscar_por_preco(no.esquerda, preco, tolerancia) +
                self._buscar_por_preco(no.direita, preco, tolerancia)
            )
        elif preco < jogo_preco:
            return self._buscar_por_preco(no.esquerda, preco, tolerancia)
        else:
            return self._buscar_por_preco(no.direita, preco, tolerancia)

    # Como pedi ajuda pro GPT pra fazer a busca por preço essa saiu meio inspirada nas outras funções
    # Mas eu fiz sem pedir ajuda pra essas pq achei mais simples e não deu muito erro
    def busca_por_faixa_preco(self, preco_minimo, preco_maximo):
        lista_jogos_na_faixa = []
        self._busca_por_faixa_preco(self.raiz, preco_minimo, preco_maximo, lista_jogos_na_faixa)
        return lista_jogos_na_faixa

    # Simplesmente busco jogos entre uma faixa de preço e percorro a arvore em busca dos jogos
    def _busca_por_faixa_preco(self, no, preco_minimo, preco_maximo, lista_jogos):
        if no is not None:
            if preco_minimo <= no.jogo.price <= preco_maximo:
                lista_jogos.append(no.jogo)

            if no.jogo.price > preco_minimo:
                self._busca_por_faixa_preco(no.esquerda, preco_minimo, preco_maximo, lista_jogos)

            if no.jogo.price < preco_maximo:
                self._busca_por_faixa_preco(no.direita, preco_minimo, preco_maximo, lista_jogos)


# Minha hash de generos tá meio triste mas eu tentei :(
class HashGeneros:
    def __init__(self):
        self.genero_para_jogos = {}

    def adicionar_jogo(self, jogo):
        # Pega o genero do jogo
        genero = jogo.genre
        # Checa se já existe esse genero já tá na lista
        if genero in self.genero_para_jogos:
            # Se o genero existe eu passo esse jogo do genero que já existe para a lista
            self.genero_para_jogos[genero].append(jogo)
        else:
            # Se não existe crio uma nova lista e adiciono o jogo nela
            self.genero_para_jogos[genero] = [jogo]

    def obter_jogos(self, genero):
        return self.genero_para_jogos.get(genero, [])


# Aqui é o meu motor de busca que tá sendo usado pra chamar algumas funções da AVL e da Hash
# Tbm pra inicializar meu catálogo de jogos
class MotorBuscaJogos:
    def __init__(self):
        self.catalogo_jogos = ArvoreJogos()
        self.generos = HashGeneros()

    def montar_avl_dos_jogos(self, games):
        arvore_jogos = ArvoreJogos()
        for game in games:
            arvore_jogos.inserir(game)
        return arvore_jogos

    # Aqui eu inicializo o catálogo obviamente e tbm tenho a minha função pra chamar o gerador de jogos 
    def inicializar_catalogo(self):
        # games = generate_random_games(100)
        games = Game.objects.all()

        for game in games:
            self.catalogo_jogos.inserir(game)
            self.generos.adicionar_jogo(game)

    def buscar_por_faixa_preco(self, preco_minimo, preco_maximo):
        if self.catalogo_jogos is not None:
            return self.catalogo_jogos.busca_por_faixa_preco(preco_minimo, preco_maximo)
        else:
            return []
        
    def buscar_por_genero(self, genero):
        return self.generos.obter_jogos(genero)


def home(request):
    # Sempre vou inicializar criando a variavel 'motor_busca' e inicializando o catálogo de jogos 
    # Pq preciso pra carregar os jogos
    motor_busca = MotorBuscaJogos()
    motor_busca.inicializar_catalogo()
    arvore_jogos = motor_busca.catalogo_jogos
    if arvore_jogos.raiz:
        arvore_jogos.mostrar_arvore()
        games_na_arvore = arvore_jogos.jogos_em_ordem()
        for game in games_na_arvore:
            print("[", game.price, "]", game.id, "-", game.name, "-", game.developer, "-", game.genre, "-", game.release_date)
        print(f"Game Price Type: {type(games_na_arvore[0].price)}, Game Price: {games_na_arvore[0].price}")
        return render(request, 'home.html', {'games': games_na_arvore})
    else:
        return render(request, 'home.html', {'games': []})


def buscar_jogos_por_preco(request):
    motor_busca = MotorBuscaJogos()
    motor_busca.inicializar_catalogo()

    # Pego a informação do input do formulário 'form' de lá do html
    if request.method == 'POST':
        preco_busca = request.POST.get('busca_preco')
        if preco_busca:
            try:
                # Tive que fazer um tratamento pra colocar o . no lugar da ,
                preco_busca = float(preco_busca.replace(',', '.'))
                jogos_encontrados = motor_busca.catalogo_jogos.buscar_por_preco(preco_busca, tolerancia=0.001)
                if jogos_encontrados:
                    return render(request, 'home.html', {'games': jogos_encontrados})
                else:
                    return render(request, 'home.html')
            except ValueError:
                return render(request, 'home.html', {'erro': 'Por favor, insira um preço válido.'})
    return render(request, 'home.html', {'games': []})


def buscar_por_faixa_preco(request):
    motor_busca = MotorBuscaJogos()
    motor_busca.inicializar_catalogo()

    # Faço a leitura do input do formulário 'form' igual da outra vez mas com as 2 faixas de preço
    if request.method == 'POST':
        preco_minimo = request.POST.get('faixa1')
        preco_maximo = request.POST.get('faixa2')
        if preco_minimo and preco_maximo:
            try:
                preco_minimo = float(preco_minimo.replace(',', '.'))
                preco_maximo = float(preco_maximo.replace(',', '.'))
                jogos_na_faixa = motor_busca.buscar_por_faixa_preco(preco_minimo, preco_maximo)
                if jogos_na_faixa:
                    return render(request, 'home.html', {'games': jogos_na_faixa})
                else:
                    return render(request, 'home.html')
            except ValueError:
                return render(request, 'home.html', {'erro': 'Por favor, insira preços válidos.'})
    return render(request, 'home.html', {'games': []})


def categorias(request):
    return render(request, 'categorias.html')


def games_por_genero(request, genre):
    motor_busca = MotorBuscaJogos()
    motor_busca.inicializar_catalogo()
    jogos_por_genero = motor_busca.buscar_por_genero(genre)
    return render(request, 'games_por_genero.html', {'games': jogos_por_genero, 'genre': genre})


def noticias(request):
    return render(request, 'noticias.html')


def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('password')

        user = User.objects.filter(username=username).first()

        if user:
            return render(request, 'cadastro.html', {'error': 'Usuário já cadastrado'})
        
        user = User.objects.create_user(username=username, email=email, password=senha)
        user.save()

        return redirect('login')

def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        senha = request.POST.get('password')

        user = authenticate(username=username, password=senha)

        if user:
            login_django(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Usuário ou senha inválidos'})

def sair(request):
    logout(request)
    return redirect('home')        

