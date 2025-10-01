# EDROM - Desafio de Busca de Caminho com A*

## NOME DO CANDIDATO: Giovanna Galvão Veloso
## CURSO DO CANDIDATO: Engenharia de Computação
## ÁREAS DE INTERESSE: Visão e Behaviour

### Visão Geral do Projeto

### 1. Definição de Custos (`candidato.py`)

A calibração dos valores de custo é crucial para influenciar o comportamento do robô. Esses valores foram definidos através de um processo de ajuste e calibração, visando equilibrar os diferentes comportamentos desejados para que o robô tome decisões inteligentes no ambiente do grid.

#### Custos Base de Movimento:

* `CUSTO_RETO = 1.0`: Aplicado a movimentos horizontais ou verticais.
* `CUSTO_DIAGONAL = math.sqrt(2)`: Equivalente à hipotenusa de um quadrado de lado 1, aplicado a movimentos diagonais (aproximadamente 1.414).

#### Custos por Rotação:

* `CUSTO_ROTACAO_SUAVE = 0.25`: Penalidade para rotações de 45° (e.g., de um movimento reto para um diagonal).
* `CUSTO_ROTACAO_FECHADA = 0.75`: Penalidade para rotações de 90°. Este custo é estrategicamente menor que o custo de um movimento reto (`CUSTO_RETO`) para incentivar o robô a fazer curvas mais fechadas se isso economizar uma distância considerável.
* `CUSTO_ROTACAO_INVERSAO = 2.5`: Penalidade alta para rotações de 180°, desencorajando esse movimento por ser ineficiente e um último recurso.

#### Custo por Estado (Posse da Bola):

* `MULTIPLICA_BOLA = 2.5`: Um fator multiplicador aplicado aos custos de rotação quando o robô está com a bola. Isso força o robô a buscar caminhos mais retos em direção ao gol, refletindo a necessidade de maior cautela ao possuir o objetivo.

#### Custo por Proximidade (Zonas de Perigo):

* `CUSTO_ZONA_PERIGO_LADO = 3.0`: Penalidade aplicada quando a próxima célula está adjacente (lado a lado) a um obstáculo.
* `CUSTO_ZONA_PERIGO_DIAGONAL = 1.5`: Penalidade aplicada quando a próxima célula está na diagonal de um obstáculo.

### 2. Funções Auxiliares (`candidato.py`)

A função principal `encontrar_caminho` utiliza diversas funções auxiliares para implementar o algoritmo A*.

#### `obstaculos_set`

Para otimizar a verificação de obstáculos, a lista de obstáculos é convertida em um `set` (`obstaculos_set`). Esta estrutura de dados, baseada em hashing, permite verificações de pertinência (se uma célula é um obstáculo) em tempo médio quase constante (O(1)). Isso é significativamente mais eficiente do que percorrer uma lista sequencialmente, especialmente em ambientes com muitos obstáculos ou muitas verificações, pois o hashing permite acesso direto à informação.

#### `heuristica(atual, final)`

Esta função calcula a estimativa de custo do nó `atual` até o nó `final`. A **distância Euclidiana** foi escolhida para este cálculo, dada pela fórmula:

$$ \sqrt{(atual_x - final_x)^2 + (atual_y - final_y)^2} $$

A distância Euclidiana é mais apropriada neste contexto do que a distância de Manhattan, pois o robô pode se mover na diagonal. A distância de Manhattan seria mais eficiente apenas se os movimentos fossem restritos a direções ortogonais (horizontal e vertical). A heurística é um componente essencial do algoritmo A*, que calcula o custo total ($$f(n)$$) como a soma do custo real percorrido ($$g(n)$$) e o custo heurístico estimado ($$h(n)$$).

#### `obter_vizinhos(pos)`

Esta função atua como os "olhos" do robô, identificando todas as 8 posições vizinhas válidas (horizontal, vertical e diagonal) a partir de uma dada `pos`. Dois laços `for` são utilizados para gerar os 8 vetores de deslocamento possíveis (de -1 a 1 em `dx` e `dy`), excluindo o deslocamento (0,0) que representa a própria célula. Antes de adicionar um vizinho à lista, a função verifica se as novas coordenadas (`novo_x`, `novo_y`) estão dentro dos limites `largura_grid` e `altura_grid`, garantindo que o robô permaneça dentro do mapa.

#### `calcular_custo_movimento(pos_anterior, pos_atual, pos_proxima)`

Esta função é o "cérebro" do robô, definindo o custo real de transição entre três células consecutivas: `pos_anterior`, `pos_atual` e `pos_proxima`. Ela atribui uma "pontuação" a cada movimento potencial, permitindo que o robô tome decisões lógicas. O custo total é a soma de vários componentes:

1.  **Custo Base:**
    * Calcula-se a diferença absoluta nas coordenadas x e y (`dx`, `dy`) entre `pos_atual` e `pos_proxima`.
    * Se `dx == 1` e `dy == 1`, o movimento é diagonal e `CUSTO_DIAGONAL` é adicionado. Caso contrário (movimento reto), `CUSTO_RETO` é adicionado.
    * Se `pos_proxima` for um obstáculo, o custo é definido como infinito (`float('inf')`), efetivamente bloqueando essa rota.

2.  **Custo de Rotação:**
    * Penaliza mudanças de direção para incentivar caminhos mais suaves.
    * São criados dois vetores: `vetor_entrada` (da `pos_anterior` para `pos_atual`) e `vetor_saída` (da `pos_atual` para `pos_proxima`).
    * O **produto escalar** entre `vetor_entrada` e `vetor_saída` é utilizado para determinar o ângulo de rotação:
        * Produto escalar `== 0`: rotação de 90° (vetores ortogonais).
        * Produto escalar `> 0`: rotação de 45° (vetores na mesma direção geral).
        * Produto escalar `< 0`: rotação de 180° (vetores em direções opostas).
    * O custo de rotação apropriado (`CUSTO_ROTACAO_FECHADA`, `CUSTO_ROTACAO_SUAVE`, `CUSTO_ROTACAO_INVERSAO`) é adicionado. Se os vetores forem iguais, não há rotação e nenhum custo é adicionado.

3.  **Custo de Estado (com Bola):**
    * Verifica a variável booleana `tem_bola`. Se for `True`, o `custo_rotacao` é multiplicado por `MULTIPLICA_BOLA`, aumentando a penalidade por curvas e incentivando trajetórias mais diretas.

4.  **Custo de Perigo (Zona de Perigo):**
    * A função itera sobre os 8 vizinhos da `pos_proxima`.
    * Se qualquer um desses vizinhos for um obstáculo (`in obstaculos_set`), uma penalidade é aplicada:
        * Se o obstáculo estiver diretamente ao lado do destino (movimento horizontal ou vertical), `CUSTO_ZONA_PERIGO_LADO` é adicionado.
        * Se o obstáculo estiver na diagonal do destino, `CUSTO_ZONA_PERIGO_DIAGONAL` é adicionado.
    * Após a aplicação da penalidade, a iteração é interrompida para essa `pos_proxima`.

#### `reconstruir_caminho(veio_de, atual)`

Esta função reconstrói o caminho encontrado pelo algoritmo A\* a partir do dicionário `veio_de`. Este dicionário armazena o predecessor de cada nó no caminho mais curto encontrado até então. A função inicia uma lista vazia `caminho` e percorre `veio_de` do nó `atual` (o objetivo) de volta até o nó inicial (que não terá um predecessor em `veio_de`), adicionando cada nó ao `caminho`. Finalmente, a lista `caminho` é invertida para apresentar a rota na ordem correta, do início ao objetivo.

### 3. Implementação do A* (`encontrar_caminho` na `candidato.py`)

A função `encontrar_caminho` implementa o algoritmo A* para encontrar o caminho mais curto entre `pos_inicial` e `pos_objetivo`, considerando os obstáculos e os custos definidos.

1.  **Inicialização:**
    * `contador`: Inicializado em 0, serve como critério de desempate na fila de prioridade (`nos_a_explorar`). Se dois caminhos têm o mesmo custo `f`, o que foi adicionado primeiro será explorado primeiro.
    * `nos_a_explorar`: Uma fila de prioridade (implementada com `heapq`) que armazena tuplas `(custo_f, contador, posição)`. O nó com o menor `custo_f` (custo total estimado) é sempre o primeiro a ser retirado. É inicializada com o nó de partida e seu custo heurístico.
    * `veio_de`: Um dicionário que mapeia cada nó para o nó que o precedeu no caminho mais barato descoberto até o momento.
    * `custo_g`: Um dicionário que armazena o custo real conhecido (`g(n)`) para chegar a cada nó a partir do início. Todos os custos são inicializados como infinito, exceto o `pos_inicial`, que é 0.

2.  **Loop Principal:**
    * O laço `while nos_a_explorar` continua enquanto houver nós promissores a serem explorados na fila de prioridade.
    * `heapq.heappop(nos_a_explorar)`: Remove e retorna o nó com o menor `custo_f` da fila. Os valores `custo_f` e `contador` são descartados (`_`), e a `pos_atual` é utilizada para o processamento.
    * **Verificação de Objetivo:** Se `pos_atual` for igual a `pos_objetivo`, o caminho ótimo foi encontrado. A função `reconstruir_caminho` é chamada e o caminho é retornado.
    * **Cálculo de Posição Anterior:** `pos_anterior = veio_de.get(pos_atual, None)`: Obtém a posição anterior para calcular o custo de rotação, passando `None` se a `pos_atual` for o nó inicial.
    * **Exploração de Vizinhos:** Para cada `vizinho` da `pos_atual` (obtido por `obter_vizinhos`):
        * `custo_mov`: O custo de transição de `pos_atual` para `vizinho` é calculado por `calcular_custo_movimento`. Se o `vizinho` for um obstáculo (custo infinito), ele é ignorado.
        * `tentativa_custo_g`: Calcula o custo total para chegar ao `vizinho` passando pela `pos_atual` (`custo_g[pos_atual] + custo_mov`).
        * **Atualização do Caminho:** Se `tentativa_custo_g` for menor que `custo_g[vizinho]` (indicando que o caminho recém-calculado é mais barato para este `vizinho`):
            * `veio_de[vizinho] = pos_atual`: Atualiza o "mapa de pistas" para apontar a `pos_atual` como o predecessor mais eficiente para o `vizinho`.
            * `custo_g[vizinho] = tentativa_custo_g`: Atualiza o custo real mais baixo para o `vizinho`.
            * `custo_f = tentativa_custo_g + heuristica(vizinho, pos_objetivo)`: Recalcula o custo `f` total estimado para o `vizinho`.
            * `contador += 1`: Incrementa o contador para desempate.
            * `heapq.heappush(nos_a_explorar, (custo_f, contador, vizinho))`: Adiciona o `vizinho` à fila de prioridade com seu novo custo `f`.

3.  **Caminho Não Encontrado:** Se o laço terminar e `nos_a_explorar` estiver vazio sem ter alcançado o objetivo, significa que não há caminho possível, e uma lista vazia `[]` é retornada.
