import numpy as np
import random
import sys

from chrome_trex import DinoGame


# Sinta-se livre para brincar com os valores abaixo

CHANCE_MUT = .20     # Chance de mutação de um peso qualquer
CHANCE_CO = .25      # Chance de crossing over de um peso qualquer
NUM_INDIVIDUOS = 15  # Tamanho da população
NUM_MELHORES = 5     # Número de indivíduos que são mantidos de uma geração para a próxima
N_GERACOES = 100     # Número de gerações


def ordenar_lista(lista, ordenacao, decrescente=True):
    """
    Argumentos da Função:
        lista: lista de números a ser ordenada.
        ordenacao: lista auxiliar de números que define a prioridade da
        ordenação.
        decrescente: variável booleana para definir se a lista `ordenacao`
        deve ser ordenada em ordem crescente ou decrescente.
    Saída:
        Uma lista com o conteúdo de `lista` ordenada com base em `ordenacao`.
    Por exemplo,
        ordenar_lista([2, 4, 5, 6], [7, 2, 5, 4])
        # retorna [2, 5, 6, 4]
        ordenar_lista([1, 5, 4, 3], [3, 8, 2, 1])
        # retorna [5, 1, 4, 3]
    """
    return [x for _, x in sorted(zip(ordenacao, lista), key=lambda p: p[0], reverse=decrescente)]

def valor_das_acoes(individuo, estado):
    """
    Argumentos da Função:
        individuo: matriz 3x10 com os pesos do indivíduo.
        estado: lista com 10 números que representam o estado do jogo.
    Saída:
        Uma lista com os valores das ações no estado `estado`. Calcula os valores
        das jogadas como combinações lineares dos valores do estado, ou seja,
        multiplica a matriz de pesos pelo estado.
    """

    return individuo @ estado

def populacao_aleatoria(n):
    """
    Argumentos da Função:
        n: Número de indivíduos
    Saída:
        Uma população aleatória. População é uma lista de indivíduos,
        e cada indivíduo é uma matriz 3x10 de pesos (números).
        Os indivíduos podem tomar 3 ações (0, 1, 2) e cada linha da matriz
        contém os pesos associados a uma das ações.
    """

    populacao = []
    for i in range(n):
        populacao.append(np.random.uniform(-10, 10, (3, 10)))
    return populacao



def melhor_jogada(individuo, estado):
    """
    Argumentos da Função:
        individuo: matriz 3x10 com os pesos do indivíduo.
        estado: lista com 10 números que representam o estado do jogo.
    Saída:
        A ação de maior valor (0, 1 ou 2) calculada pela função valor_das_acoes.
    """
    # Referência: np.argmax()
    return np.argmax(valor_das_acoes(individuo, estado))


def mutacao(individuo):
    """
    Argumentos da Função:
        individuo: matriz 3x10 com os pesos do indivíduo.
    Saída:
        Essa função não tem saída. Ela apenas modifica os pesos do indivíduo,
        de acordo com chance CHANCE_MUT para cada peso.
    """

    for i in range(3):
        for j in range(10):
            if np.random.uniform(0, 1) < CHANCE_MUT:
                individuo[i][j] *= np.random.uniform(-1.5, 1.5)


def crossover(individuo1, individuo2):
    """
    Argumentos da Função:
        individuoX: matriz 3x10 com os pesos do individuoX.
    Saída:
        Um novo indivíduo com pesos que podem vir do `individuo1`
        (com chance 1-CHANCE_CO) ou do `individuo2` (com chance CHANCE_CO),
        ou seja, é um cruzamento entre os dois indivíduos. Você também pode pensar
        que essa função cria uma cópia do `individuo1`, mas com chance CHANCE_CO,
        copia os respectivos pesos do `individuo2`.
    """
    
    filho = individuo1.copy()
    for i in range(3):
        for j in range(10):
            if np.random.uniform(0, 1) < CHANCE_CO:
                filho[i][j] = individuo2[i][j]
    return filho


def calcular_fitness(jogo, individuo):
    """
    Argumentos da Função:
        jogo: objeto que representa o jogo.
        individuo: matriz 3x10 com os pesos do individuo.
    Saída:
        O fitness calculado de um indivíduo. Esse cálculo é feito simulando um
        jogo e calculando o fitness com base nessa simulação. O modo mais simples
        é usando fitness = score do jogo.
    """

    jogo.reset()
    while not jogo.game_over:
        estado = jogo.get_state()
        acao = melhor_jogada(individuo, estado)
        jogo.step(acao)
    return jogo.get_score()


def proxima_geracao(populacao, fitness):
    """
    Argumentos da Função:
        populacao: lista de indivíduos.
        fitness: lista de fitness, uma para cada indivíduo.
    Saída:
        A próxima geração com base na população atual.
        Para criar a próxima geração, segue-se o seguinte algoritmo:
          1. Colocar os melhores indivíduos da geração atual na próxima geração.
          2. Até que a população esteja completa:
             2.1. Escolher aleatoriamente dois indivíduos da geração atual.
             2.2. Criar um novo indivíduo a partir desses dois indivíduos usando
                  crossing over.
             2.3. Mutar esse indivíduo.
             2.4. Adicionar esse indivíduo na próxima geração
    """

    ordenados = ordenar_lista(populacao, fitness)
    proxima_ger = ordenados[:NUM_MELHORES]


    while len(proxima_ger) < NUM_INDIVIDUOS:
        # Selecionar 2 indivíduos, realizar crosover e mutação,
        # e adicionar o novo indivíduo à próxima geração
        ind1, ind2 = random.choices(populacao, k=2)
        filho = crossover(ind1, ind2)
        mutacao(filho)
        proxima_ger.append(filho)

    return proxima_ger


def mostrar_melhor_individuo(populacao, fitness):
    """
    Argumentos da Função:
        jogo: objeto que representa o jogo.
        populacao: lista de indivíduos.
        fitness: lista de fitness, uma para cada indivíduo.
    Saída:
        Não há saída. Simplesmente mostra o melhor indivíduo de uma população.
    """
    ind = populacao[max(range(len(populacao)), key=lambda i: fitness[i])]
    print('Melhor individuo:', ind)
    
    while True:
        if input('Pressione enter para rodar o melhor agente. Digite q para sair. ') == 'q':
            return
        jogoVisivel = DinoGame(fps=100)
        fit = calcular_fitness(jogoVisivel, ind)
        print('Fitness: {:4.1f}'.format(jogoVisivel.get_score()))
        jogoVisivel.close()
        

###############################
# CÓDIGO QUE RODA O ALGORITMO #
###############################



num_geracoes = N_GERACOES
jogo = DinoGame(fps=50_000)

populacao = populacao_aleatoria(NUM_INDIVIDUOS)

print('ger | fitness\n----+-' + '-'*5*NUM_INDIVIDUOS)

for ger in range(num_geracoes):
    fitness = []
    for ind in populacao:
        fitness.append(calcular_fitness(jogo, ind))

    populacao = proxima_geracao(populacao, fitness)

    print('{:3} |'.format(ger),
          ' '.join('{:4d}'.format(s) for s in sorted(fitness, reverse=True)))

    # Opcional: parar se o fitness estiver acima de algum valor (p.ex. 300)
    # if max(fitness) > 300:
    #     break

# Calcula a lista de fitness para a última geração
fitness = []
for ind in populacao:
    fitness.append(calcular_fitness(jogo, ind))

jogo.close()

mostrar_melhor_individuo(populacao, fitness)
