# caminho_mais_longo.py
# Passeio Turistico Maximo - Problema do Caminho Mais Longo (Longest Simple Path)
# Compara a solucao exata (backtracking) com a heuristica gulosa em grafos
# completos com pesos aleatorios entre 1 e 100.
#
# Parte B da atividade: mede tempo de execucao e qualidade da solucao
# (peso total do caminho) para n = 5, 8, 10, 12, 15.

import time
import random
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

random.seed(42)  # semente fixa para os experimentos serem reproduziveis


def gerar_grafo(n):
    """Gera um grafo completo com n vertices como matriz de adjacencia.
    Cada aresta recebe um peso inteiro aleatorio entre 1 e 100."""
    g = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            peso = random.randint(1, 100)
            g[i][j] = peso
            g[j][i] = peso  # grafo nao direcionado -> matriz simetrica
    return g


def resolver_exato(g, n, origem, destino, limite=20.0):
    """Solucao exata por backtracking (DFS).
    Testa todos os caminhos simples de origem a destino e retorna o de maior peso.
    O parametro 'limite' interrompe a busca se ela passar de X segundos, ja que
    para grafos grandes o numero de caminhos cresce como (n-2)! e torna-se inviavel."""
    melhor = {"peso": -1, "caminho": None}
    visitado = [False] * n
    inicio = time.perf_counter()

    def buscar(atual, peso, caminho):
        if time.perf_counter() - inicio > limite:
            raise TimeoutError
        if atual == destino:
            if peso > melhor["peso"]:
                melhor["peso"] = peso
                melhor["caminho"] = list(caminho)
            return
        for prox in range(n):
            if prox != atual and not visitado[prox] and g[atual][prox] > 0:
                visitado[prox] = True
                caminho.append(prox)
                buscar(prox, peso + g[atual][prox], caminho)
                caminho.pop()
                visitado[prox] = False  # desmarca no retorno para liberar a rota

    visitado[origem] = True
    buscar(origem, 0, [origem])
    return melhor["peso"], melhor["caminho"]


def resolver_guloso(g, n, origem, destino):
    """Solucao heuristica gulosa.
    A partir da origem, sempre viaja para o vizinho nao visitado ligado pela
    aresta de maior peso. Encerra ao chegar no destino ou ao ficar preso num
    beco sem saida (sem vizinhos disponiveis)."""
    visitado = [False] * n
    visitado[origem] = True
    atual = origem
    peso = 0
    caminho = [origem]
    while atual != destino:
        escolhido = -1
        maior = -1
        for prox in range(n):
            if prox != atual and not visitado[prox] and g[atual][prox] > maior:
                maior = g[atual][prox]
                escolhido = prox
        if escolhido == -1:
            return None, caminho  # beco sem saida: nao alcancou o destino
        visitado[escolhido] = True
        peso += maior
        caminho.append(escolhido)
        atual = escolhido
    return peso, caminho


def rodar_experimentos(tamanhos, pasta_img="imagens", limite_exato=20.0):
    """Roda as duas abordagens para cada tamanho de grafo, imprime os
    resultados e gera os graficos de tempo e de qualidade."""
    if not os.path.exists(pasta_img):
        os.makedirs(pasta_img)

    resultados = []
    print("--- EXPERIMENTOS: CAMINHO MAIS LONGO ---")
    for n in tamanhos:
        g = gerar_grafo(n)
        origem, destino = 0, n - 1

        # solucao exata (com limite de tempo)
        t = time.perf_counter()
        try:
            peso_ex, cam_ex = resolver_exato(g, n, origem, destino, limite_exato)
            tempo_ex = time.perf_counter() - t
            timeout = False
        except TimeoutError:
            tempo_ex = time.perf_counter() - t
            peso_ex, cam_ex = None, None
            timeout = True

        # solucao gulosa
        t = time.perf_counter()
        peso_gu, cam_gu = resolver_guloso(g, n, origem, destino)
        tempo_gu = time.perf_counter() - t

        # quanto a gulosa ficou pior que a otima (em %)
        if peso_gu is None or peso_ex is None:
            gap = None
        else:
            gap = 100 * (peso_ex - peso_gu) / peso_ex

        resultados.append({
            "n": n, "peso_ex": peso_ex, "tempo_ex": tempo_ex, "timeout": timeout,
            "peso_gu": peso_gu, "tempo_gu": tempo_gu, "gap": gap
        })
        print(f"n={n:2d} | exato={peso_ex} ({tempo_ex:.4f}s) "
              f"timeout={timeout} | guloso={peso_gu} ({tempo_gu:.6f}s) | gap={gap}")

    gerar_grafico_tempo(resultados, pasta_img)
    gerar_grafico_qualidade(resultados, pasta_img)
    print(f"\nGraficos salvos na pasta '{pasta_img}/'.")
    return resultados


def gerar_grafico_tempo(resultados, pasta_img):
    """Grafico do tempo de execucao (escala log) das duas abordagens."""
    ns = [r["n"] for r in resultados]
    plt.figure(figsize=(7, 4.2))
    plt.plot(ns, [r["tempo_ex"] for r in resultados], "o-",
             color="black", label="Exato (Backtracking)")
    plt.plot(ns, [r["tempo_gu"] for r in resultados], "s--",
             color="gray", label="Guloso")
    for r in resultados:
        if r["timeout"]:
            plt.scatter([r["n"]], [r["tempo_ex"]], color="red", marker="x",
                        s=60, zorder=5, label="Inviavel (>20s)")
    plt.yscale("log")
    plt.xlabel("Numero de vertices (n)")
    plt.ylabel("Tempo (s) - escala log")
    plt.title("Tempo de execucao vs. n")
    plt.grid(True, which="both", ls=":", alpha=0.5)
    h, l = plt.gca().get_legend_handles_labels()
    plt.legend(dict(zip(l, h)).values(), dict(zip(l, h)).keys())
    plt.tight_layout()
    plt.savefig(os.path.join(pasta_img, "grafico_tempo.png"), dpi=150)
    plt.close()


def gerar_grafico_qualidade(resultados, pasta_img):
    """Grafico de barras comparando o peso do caminho (otimo x guloso)."""
    ns = [r["n"] for r in resultados]
    x = range(len(ns))
    plt.figure(figsize=(7, 4.2))
    plt.bar([i - 0.2 for i in x], [r["peso_ex"] or 0 for r in resultados],
            width=0.4, color="black", label="Otimo (Exato)")
    plt.bar([i + 0.2 for i in x], [r["peso_gu"] or 0 for r in resultados],
            width=0.4, color="gray", label="Guloso")
    plt.xticks(list(x), ns)
    plt.xlabel("Numero de vertices (n)")
    plt.ylabel("Peso total do caminho")
    plt.title("Qualidade da solucao")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(pasta_img, "grafico_qualidade.png"), dpi=150)
    plt.close()


if __name__ == "__main__":
    # tamanhos pedidos no enunciado
    TAMANHOS = [5, 8, 10, 12, 15]
    rodar_experimentos(TAMANHOS)
