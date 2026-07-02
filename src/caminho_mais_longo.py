# Trabalho de Algoritmos e Grafos - Problema do Caminho Mais Longo

import time
import random
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

random.seed(42)  # pra repetir os mesmos resultados

melhor_peso = -1
melhor_caminho = None
estourou = False


def gerar_grafo(n):
    g = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            peso = random.randint(1, 100)
            g[i][j] = peso
            g[j][i] = peso
    return g


def buscar(g, n, atual, destino, visitado, peso, caminho, inicio, limite):
    global melhor_peso, melhor_caminho, estourou
    if estourou:
        return
    if time.time() - inicio > limite:
        estourou = True
        return
    if atual == destino:
        if peso > melhor_peso:
            melhor_peso = peso
            melhor_caminho = caminho[:]
        return
    for prox in range(n):
        if not visitado[prox] and g[atual][prox] > 0:
            visitado[prox] = True
            caminho.append(prox)
            buscar(g, n, prox, destino, visitado, peso + g[atual][prox],
                   caminho, inicio, limite)
            caminho.pop()
            visitado[prox] = False  # desmarca na volta


def resolver_exato(g, n, origem, destino, limite=20.0):
    global melhor_peso, melhor_caminho, estourou
    melhor_peso = -1
    melhor_caminho = None
    estourou = False
    visitado = [False] * n
    visitado[origem] = True
    buscar(g, n, origem, destino, visitado, 0, [origem], time.time(), limite)
    if estourou:
        return None, None
    return melhor_peso, melhor_caminho


def resolver_guloso(g, n, origem, destino):
    visitado = [False] * n
    visitado[origem] = True
    atual = origem
    peso = 0
    caminho = [origem]
    while atual != destino:
        escolhido = -1
        maior = -1
        for prox in range(n):
            if not visitado[prox] and g[atual][prox] > maior:
                maior = g[atual][prox]
                escolhido = prox
        if escolhido == -1:
            return None, caminho  # beco sem saida
        visitado[escolhido] = True
        peso = peso + maior
        caminho.append(escolhido)
        atual = escolhido
    return peso, caminho


tamanhos = [5, 8, 10, 12, 15]
lista_n = []
pesos_exato = []
tempos_exato = []
deu_timeout = []
pesos_guloso = []
tempos_guloso = []

if not os.path.exists("imagens"):
    os.mkdir("imagens")

for n in tamanhos:
    g = gerar_grafo(n)
    origem = 0
    destino = n - 1

    t = time.time()
    peso_ex, cam_ex = resolver_exato(g, n, origem, destino)
    tempo_ex = time.time() - t

    t = time.time()
    peso_gu, cam_gu = resolver_guloso(g, n, origem, destino)
    tempo_gu = time.time() - t

    lista_n.append(n)
    pesos_exato.append(peso_ex)
    tempos_exato.append(tempo_ex)
    deu_timeout.append(peso_ex is None)
    pesos_guloso.append(peso_gu)
    tempos_guloso.append(tempo_gu)

    if peso_ex is None:
        print("n =", n, "| exato: estourou o limite de 20s | guloso:", peso_gu)
    else:
        gap = 100 * (peso_ex - peso_gu) / peso_ex
        print("n =", n, "| exato:", peso_ex, "| guloso:", peso_gu,
              "| guloso ficou %.1f%% pior" % gap)
    print("    caminho exato:", cam_ex)
    print("    caminho guloso:", cam_gu)
    print("    tempo exato: %.6fs | tempo guloso: %.6fs" % (tempo_ex, tempo_gu))

# grafico de tempo
plt.figure(figsize=(8, 5))
plt.plot(lista_n, tempos_exato, "o-", label="Exato (backtracking)")
plt.plot(lista_n, tempos_guloso, "s--", label="Guloso")
for i in range(len(lista_n)):
    if deu_timeout[i]:
        plt.plot(lista_n[i], tempos_exato[i], "rx", markersize=12,
                 label="Estourou o limite (20s)")
plt.yscale("log")
plt.xlabel("Numero de vertices (n)")
plt.ylabel("Tempo (s) - escala log")
plt.title("Tempo de execucao vs. n")
plt.grid(True)
plt.legend()
plt.savefig("imagens/grafico_tempo.png")
plt.close()

# grafico de qualidade
pesos_exato_plot = []
for x in pesos_exato:
    if x is None:
        pesos_exato_plot.append(0)
    else:
        pesos_exato_plot.append(x)

posicoes = range(len(lista_n))
plt.figure(figsize=(8, 5))
plt.bar([i - 0.2 for i in posicoes], pesos_exato_plot, width=0.4,
        color="tab:blue", label="Otimo (exato)")
plt.bar([i + 0.2 for i in posicoes], pesos_guloso, width=0.4,
        color="tab:orange", label="Guloso")
plt.xticks(list(posicoes), lista_n)
plt.xlabel("Numero de vertices (n)")
plt.ylabel("Peso total do caminho")
plt.title("Qualidade da solucao")
plt.legend()
plt.savefig("imagens/grafico_qualidade.png")
plt.close()

print("Graficos salvos na pasta imagens/")
