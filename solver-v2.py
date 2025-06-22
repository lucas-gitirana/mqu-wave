import time
import sys
import random
from collections import defaultdict
from classes import Pedido, Corredor


# =============================
# ==== LEITURA DAS INSTÂNCIAS
# =============================
def ler_instancias(path):
    with open(path) as f:
        o, i, a = map(int, f.readline().split())

        pedidos = []
        for pid in range(o):
            parts = list(map(int, f.readline().split()))
            itens = [(parts[i], parts[i+1]) for i in range(1, len(parts), 2)]
            pedidos.append(Pedido(pid, itens))

        corredores = []
        for cid in range(a):
            parts = list(map(int, f.readline().split()))
            itens = [(parts[i], parts[i+1]) for i in range(1, len(parts), 2)]
            corredores.append(Corredor(cid, itens))

        lb, ub = map(int, f.readline().split())

        return pedidos, corredores, lb, ub


# =============================
# ==== FUNÇÕES AUXILIARES
# =============================
def avaliar(pedidos_bin, pedidos, corredores_wave):
    total = sum(
        sum(pedidos[pid].itens.values())
        for pid, included in enumerate(pedidos_bin) if included
    )
    n_corr = len(corredores_wave)
    if n_corr == 0:
        return 0
    return total / n_corr


def determinar_corredores(pedidos_bin, pedidos, corredores):
    demanda = defaultdict(int)
    for pid, included in enumerate(pedidos_bin):
        if included:
            for i, q in pedidos[pid].itens.items():
                demanda[i] += q

    corredores_ids = list(range(len(corredores)))
    random.shuffle(corredores_ids)

    fornecimento = defaultdict(int)
    usados = []

    for cid in corredores_ids:
        c = corredores[cid]
        usados.append(cid)
        for i, q in c.itens.items():
            fornecimento[i] += q

        if all(demanda[i] <= fornecimento[i] for i in demanda):
            return usados

    return None


# =============================
# ==== GERAR SOLUÇÃO INICIAL
# =============================
def gerar_solucao_inicial(pedidos, corredores, lb, ub):
    pedidos_ids = list(range(len(pedidos)))
    random.shuffle(pedidos_ids)
    pedidos_bin = [0] * len(pedidos)
    total_unidades = 0

    for pid in pedidos_ids:
        unidades = sum(pedidos[pid].itens.values())
        if total_unidades + unidades > ub:
            continue
        pedidos_bin[pid] = 1
        total_unidades += unidades
        if total_unidades >= lb:
            break

    if total_unidades < lb:
        return gerar_solucao_inicial(pedidos, corredores, lb, ub)

    corredores_wave = determinar_corredores(pedidos_bin, pedidos, corredores)
    if corredores_wave is None:
        return gerar_solucao_inicial(pedidos, corredores, lb, ub)

    return pedidos_bin, corredores_wave


# =============================
# ==== PERTURBAR
# =============================
def perturbar(pedidos_bin, pedidos, lb, ub, intensidade=0.2):
    pedidos_novo = pedidos_bin.copy()
    indices_in = [i for i, v in enumerate(pedidos_novo) if v == 1]
    indices_out = [i for i, v in enumerate(pedidos_novo) if v == 0]

    if len(indices_in) == 0:
        return pedidos_novo

    n_remover = max(1, int(len(indices_in) * intensidade))
    remover = random.sample(indices_in, min(n_remover, len(indices_in)))
    for r in remover:
        pedidos_novo[r] = 0

    total = sum(
        sum(pedidos[pid].itens.values())
        for pid, included in enumerate(pedidos_novo) if included
    )

    random.shuffle(indices_out)
    for c in indices_out:
        unidades = sum(pedidos[c].itens.values())
        if total + unidades <= ub:
            pedidos_novo[c] = 1
            total += unidades
        if total >= lb:
            break

    if total < lb:
        return perturbar(pedidos_bin, pedidos, lb, ub, intensidade)

    return pedidos_novo


# =============================
# ==== BUSCA LOCAL (First Improvement)
# =============================
def busca_local(pedidos_bin, pedidos, corredores, lb, ub):
    pedidos_atual = pedidos_bin.copy()
    melhor_corredores = determinar_corredores(pedidos_atual, pedidos, corredores)
    melhor_obj = avaliar(pedidos_atual, pedidos, melhor_corredores)

    if melhor_corredores is None:
        return pedidos_atual, melhor_corredores

    melhorou = True

    while melhorou:
        melhorou = False
        indices_in = [i for i, v in enumerate(pedidos_atual) if v == 1]
        indices_out = [i for i, v in enumerate(pedidos_atual) if v == 0]

        for p_out in indices_in:
            for p_in in indices_out:
                tentativa = pedidos_atual.copy()
                tentativa[p_out] = 0
                tentativa[p_in] = 1

                total = sum(
                    sum(pedidos[pid].itens.values())
                    for pid, included in enumerate(tentativa) if included
                )
                if total < lb or total > ub:
                    continue

                corredores_tentativa = determinar_corredores(tentativa, pedidos, corredores)
                if corredores_tentativa is None:
                    continue

                obj = avaliar(tentativa, pedidos, corredores_tentativa)

                if obj > melhor_obj:
                    pedidos_atual = tentativa
                    melhor_corredores = corredores_tentativa
                    melhor_obj = obj
                    melhorou = True
                    break
            if melhorou:
                break

    return pedidos_atual, melhor_corredores


# =============================
# ==== ILS
# =============================
def ils(pedidos, corredores, lb, ub, max_iter=100, max_tempo_segundos=None):
    start_time = time.time()

    pedidos_bin, corredores_wave = gerar_solucao_inicial(pedidos, corredores, lb, ub)
    melhor_obj = avaliar(pedidos_bin, pedidos, corredores_wave)
    melhor_solucao = (pedidos_bin, corredores_wave)

    for _ in range(max_iter):
        if max_tempo_segundos is not None:
            elapsed = time.time() - start_time
            if elapsed >= max_tempo_segundos:
                print(f"Limite de tempo atingido: {elapsed:.2f} segundos.")
                break

        pedidos_perturbados = perturbar(pedidos_bin, pedidos, lb, ub, 0.2)
        corredores_perturbados = determinar_corredores(pedidos_perturbados, pedidos, corredores)
        if corredores_perturbados is None:
            continue

        pedidos_local, corredores_local = busca_local(
            pedidos_perturbados, pedidos, corredores, lb, ub
        )

        obj = avaliar(pedidos_local, pedidos, corredores_local)

        if obj > melhor_obj:
            melhor_solucao = (pedidos_local, corredores_local)
            melhor_obj = obj
            pedidos_bin, corredores_wave = pedidos_local, corredores_local

    return melhor_solucao


# =============================
# ==== SALVAR SAÍDA
# =============================
def salvar_saida(output_path, pedidos_bin, corredores_wave):
    pedidos_wave = [i for i, v in enumerate(pedidos_bin) if v == 1]
    with open(output_path, 'w') as f:
        f.write(f"{len(pedidos_wave)}\n")
        for p in pedidos_wave:
            f.write(f"{p}\n")
        f.write(f"{len(corredores_wave)}\n")
        for c in corredores_wave:
            f.write(f"{c}\n")


# =============================
# ==== EXECUÇÃO
# =============================
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python solver.py <arquivo_entrada> <arquivo_saida>")
        sys.exit(1)

    arquivo_instancia = sys.argv[1]
    arquivo_saida = sys.argv[2]
    limite_tempo = 60

    pedidos, corredores, lb, ub = ler_instancias(arquivo_instancia)
    pedidos_wave, corredores_wave = ils(pedidos, corredores, lb, ub, max_tempo_segundos=limite_tempo)

    salvar_saida(arquivo_saida, pedidos_wave, corredores_wave)

    print('Pedidos selecionados:', [i for i, v in enumerate(pedidos_wave) if v == 1])
    print('Corredores selecionados:', corredores_wave)
    print('F.O.:', avaliar(pedidos_wave, pedidos, corredores_wave))
