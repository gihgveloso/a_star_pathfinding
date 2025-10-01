# NOME DO CANDIDATO: Giovanna Galvão Veloso
# CURSO DO CANDIDATO: Engenharia de Computação
# AREAS DE INTERESSE: Visão e Behaviour

import heapq
import math

# Definição das constantes de custo

# [Nível Básico] Custos base de movimento
CUSTO_RETO = 1.0
CUSTO_DIAGONAL = math.sqrt(2) # Custo ~1.414

# [Nível 1] Custos por rotação
CUSTO_ROTACAO_SUAVE = 0.25 # Rotação de 45°
CUSTO_ROTACAO_FECHADA = 0.75 # Rotação de 90°
CUSTO_ROTACAO_INVERSAO = 2.5 # Rotação de 180°

# [Nível 2] Custo por estado
MULTIPLICA_BOLA = 2.5 # Fator que aumenta os custos com a bola.

# [Nível 3] Custo por proximidade
CUSTO_ZONA_PERIGO_LADO = 3.0 # Penalidade por estar do lado de um obstáculo
CUSTO_ZONA_PERIGO_DIAGONAL = 1.5 # Penalidade por estar na diagonal de um obstáculo


def encontrar_caminho(pos_inicial, pos_objetivo, obstaculos, largura_grid, altura_grid, tem_bola=False):

    obstaculos_set = set(obstaculos) # Usa um set para buscar mais rapido

    # FUNÇÕES AUXILIARES

    def heuristica(atual, final):
        # Calcula a heurística. Foi usada distância Euclidiana (mais recomendada, porque o robô se move na diagonal também).
        return math.sqrt((atual[0] - final[0]) ** 2 + (atual[1] - final[1]) ** 2)

    # Função para obter os vizinhos válidos de uma posição
    def obter_vizinhos(pos):
        vizinhos = []
        # Movimentos em todas as 8 direções (horizontal, vertical e diagonal)
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:  # Não considerar a própria célula
                    continue

                novo_x, novo_y = pos[0] + dx, pos[1] + dy

                # Verificar limites do grid
                # Garante que o novo vizinho está dentro dos limites da largura e altura do grid.
                if 0 <= novo_x < largura_grid and 0 <= novo_y < altura_grid:
                    vizinhos.append((novo_x, novo_y))
        return vizinhos

    # Função para calcular o custo de transição entre duas células
    def calcular_custo_movimento(pos_anterior, pos_atual, pos_proxima):
        
        # Se a célula de destino é um obstáculo o custo é infinito.
        if pos_proxima in obstaculos_set:
            return float('inf')
        
        custo_total = 0.0

        # Custo total para os movimentos
        dx = abs(pos_proxima[0] - pos_atual[0]) # Deslocamento em x
        dy = abs(pos_proxima[1] - pos_atual[1]) # Deslocamento em


        if dx == 1 and dy == 1:  # Movimento diagonal
            custo_total += CUSTO_DIAGONAL
        else: # Movimento reto (horizontal ou vertical)
            custo_total += CUSTO_RETO

        custo_rotacao = 0.0
        if pos_anterior:
            vetor_entrada = (pos_atual[0] - pos_anterior[0], pos_atual[1] - pos_anterior[1])
            vetor_saída = (pos_proxima[0] - pos_atual[0], pos_proxima[1] - pos_atual[1])
            if vetor_entrada != vetor_saída: # Verifica se há rotação
                # Produto escalar para descobrir o ângulo
                produto_escalar = vetor_entrada[0] * vetor_saída[0] + vetor_entrada[1] * vetor_saída[1]

                if produto_escalar == 0:
                    custo_rotacao = CUSTO_ROTACAO_FECHADA # Rotação de 90°
                elif produto_escalar > 0:
                    custo_rotacao = CUSTO_ROTACAO_SUAVE # Rotação de 45°
                else:
                    custo_rotacao = CUSTO_ROTACAO_INVERSAO # Rotação de 180°
        if tem_bola:
            custo_rotacao *= MULTIPLICA_BOLA # Custo de estado

        custo_total += custo_rotacao

        # Custo das zonas de perigo
        for dx_obstaculo in [-1, 0, 1]:
            for dy_obstaculo in [-1, 0, 1]:
                if dx_obstaculo == 0 and dy_obstaculo == 0:
                    continue
                vizinho_do_destino = (pos_proxima[0] + dx_obstaculo, pos_proxima[1] + dy_obstaculo)
                
                if vizinho_do_destino in obstaculos_set: #Verifica se o vizinho é um obstáculo
                    eh_diagonal = (dx_obstaculo != 0 and dy_obstaculo != 0) # É diagonal só se ocorrer deslocamento em x e em y
                    if eh_diagonal:
                        custo_total += CUSTO_ZONA_PERIGO_DIAGONAL
                    else:
                        custo_total += CUSTO_ZONA_PERIGO_LADO

        return custo_total

    def reconstruir_caminho(veio_de, atual):
        # Reconstrói o caminho do final para o início e o inverte
        caminho = [] # Lista para guardar o caminho
        while atual in veio_de: # Dicionário que cria um "mapa de pistas"
            caminho.append(atual) 
            atual = veio_de[atual] # 'atual' se torna a célula que veio antes dela
        caminho.reverse()
        return caminho

    # IMPLEMENTAÇÃO DO A*

    contador = 0 # Critério de desempate na fila
    # Fila que mantém o nó mais promissor no topo, ordenada 
    # (custo_f, contador, posição inicial)
    nos_a_explorar =[(heuristica(pos_inicial, pos_objetivo), contador, pos_inicial)]
    veio_de = {}

    # Dicionario para armazenar o custo real (g(n)) 
    # Todos os custos começam como infinito
    custo_g = {(x, y): float('inf') for x in range(largura_grid) for y in range(altura_grid)}
    custo_g[pos_inicial] = 0

    # O laço continua enquanto houver nós promissores na fila de prioridade
    while nos_a_explorar:
        _, _, pos_atual = heapq.heappop(nos_a_explorar) # Pega o nó com menor custo_f da fila
        # Se o nó promissor é o objetivo, foi encontrado o caminho
        if pos_atual == pos_objetivo:
            return reconstruir_caminho(veio_de, pos_atual)
        
        # Descobre de onde veio para calcular o custo de rotação 
        pos_anterior = veio_de.get(pos_atual, None)

        for vizinho in obter_vizinhos(pos_atual): # Explora os vizinhos do nó atual
            # Calcula o custo deste movimento específico
            custo_mov = calcular_custo_movimento(pos_anterior, pos_atual, vizinho)
            if custo_mov == float('inf'):
                continue
            # Calcula o custo para chegar a este vizinho passando pelo caminho atual
            tentativa_custo_g = custo_g[pos_atual] + custo_mov
            # Se este caminho para o vizinho é melhor do que qualquer um que já encontramos atualizamos nossas informações com este novo caminho melhor
            if tentativa_custo_g < custo_g[vizinho]:
                veio_de[vizinho] = pos_atual # A "mapa de pistas" para o 'vizinho' agora aponta para 'pos_atual'.
                custo_g[vizinho] = tentativa_custo_g # Registra o novo custo, mais baixo.
                custo_f = tentativa_custo_g + heuristica(vizinho, pos_objetivo) 
                contador += 1 # Adicionamos o 'vizinho' à fila de prioridade com sua nova e melhorada pontuação.
                heapq.heappush(nos_a_explorar, (custo_f, contador, vizinho))
    return []