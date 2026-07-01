# Caminho Mais Longo (Passeio Turístico Máximo)

Trabalho da disciplina IC0004 - Algoritmos e Grafos (Prof. George Lima, UFBA).

Yves Luan do Rosário Moura e Patrick César Santos Silva.

A atividade é sobre o problema do Caminho Mais Longo: num grafo com pesos nas arestas, achar o caminho simples (sem repetir vértice) de maior soma de pesos entre uma origem S e um destino D. A história do enunciado é a de um turista que quer fazer o trajeto mais longo e bonito possível de patinete, sem passar duas vezes pela mesma rua.

O trabalho tem duas partes:

- **Parte A (teoria):** provar que o problema é NP-Difícil, usando uma redução do Caminho Hamiltoniano.
- **Parte B (experimentos):** implementar duas soluções e comparar na prática — uma exata (backtracking) e uma gulosa — olhando tempo de execução e qualidade do resultado.

## As duas soluções

- **Exata (backtracking):** um DFS que testa todos os caminhos simples de S até D e guarda o de maior peso. Acha sempre a resposta certa, mas o tempo explode rápido porque num grafo completo o número de caminhos é da ordem de (n-2)!.
- **Gulosa:** sempre vai pro vizinho ainda não visitado ligado pela maior aresta. É rápida (O(n²)), mas não garante o melhor caminho e às vezes nem chega no destino.

## Organização das pastas

- `src/` — o código (`caminho_mais_longo.py`)
- `imagens/` — os gráficos gerados pelos experimentos
- `Documentos/` — o relatório completo em PDF, com as duas partes

## Rodando o código

Precisa ter Python 3 e o matplotlib instalado:

```bash
pip install matplotlib
python3 src/caminho_mais_longo.py
```

Isso roda os testes para n = 5, 8, 10, 12 e 15, mostra os resultados no terminal e salva os dois gráficos na pasta `imagens/`.

## O que deu nos testes

| n  | Peso ótimo | Peso guloso | Guloso ficou quão pior |
|----|------------|-------------|------------------------|
| 5  | 227        | 95          | 58,1%                  |
| 8  | 574        | 521         | 9,2%                   |
| 10 | 747        | 180         | 75,9%                  |
| 12 | 960        | 726         | 24,4%                  |
| 15 | não terminou | 1192      | -                      |

Resumindo: a partir de n=12 a solução exata já demora uns 10 segundos, e em n=15 ela não termina (tive que cortar em 20 segundos). O guloso resolve tudo em microssegundos, só que a qualidade varia demais — em alguns casos ficou quase 76% pior que o ótimo. A explicação de por que isso acontece está no relatório.

Obs.: a semente do sorteio está fixa (`random.seed(42)`), então os pesos dão sempre iguais. Só os tempos que mudam de um computador pro outro.
