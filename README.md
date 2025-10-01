# Algoritmo A* para Navegação em Grid

Este projeto implementa o **algoritmo A\*** para busca de caminho em um grid com obstáculos, incluindo um simulador visual em **Pygame**.  
O objetivo é permitir que um robô capture a bola e leve-a até o gol de forma eficiente, equilibrando custo de movimento, rotação e proximidade de obstáculos.

---

## Estrutura do Projeto

- `candidato.py` → Implementação do algoritmo A* com heurística Euclidiana e custos personalizados.  
- `simulador.py` → Simulador visual em **Pygame**, exibindo o robô, bola, gol e obstáculos em tempo real.  
- `README.md` → Este arquivo com instruções de uso.  
- `EXPLICACAO.md` → Documentação detalhada do funcionamento interno do algoritmo (opcional).  

---

## Funcionalidades

- **Movimentos base:** suporte a deslocamentos retos e diagonais.  
- **Custos de rotação:** suaves, fechadas e inversões.  
- **Estado com bola:** penalização extra em curvas para incentivar trajetórias mais retas.  
- **Zonas de perigo:** aumenta o custo ao passar próximo de obstáculos.  
- **Heurística Euclidiana:** mais adequada para ambientes com movimento diagonal.  
- **Reconstrução de caminho:** retorna a trajetória ótima encontrada pelo A*.  

---

## Simulação

O simulador mostra:  
- Robô (azul)   
- Bola (laranja)  
- Gol (amarelo)   
- Obstáculos (vermelho) 
- Caminho calculado (ciano)  

Controles no painel inferior: **Play/Pause** e **Reset** do cenário.  

---

## Como Executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/SEU_USUARIO/a-star-pathfinding.git
   cd a-star-pathfinding
   ``
2. Crie um ambiente virtual (opcional):
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```
   
3. Instale dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Rode o simulador:
   ```bash
   python simulador.py
   ```
