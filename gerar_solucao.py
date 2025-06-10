import random

def gerar_solucao_inicial(pedidos, corredores, lb, ub):
    pedidos_ids = list(range(len(pedidos)))
    random.shuffle(pedidos_ids)  # ou ordenar por alguma heurística
    pedidos_wave = []
    total_unidades = 0

    for pid in pedidos_ids:
        pedido = pedidos[pid]
        unidades_pedido = sum(pedido.itens.values())

        if total_unidades + unidades_pedido > ub:
            continue

        pedidos_wave.append(pid)
        total_unidades += unidades_pedido

        if total_unidades >= lb:
            break

    # Se não chegou no LB, tentar adicionar mais pedidos
    for pid in pedidos_ids:
        if pid in pedidos_wave:
            continue
        pedido = pedidos[pid]
        unidades_pedido = sum(pedido.itens.values())
        if total_unidades + unidades_pedido <= ub:
            pedidos_wave.append(pid)
            total_unidades += unidades_pedido
        if total_unidades >= lb:
            break

    corredores_wave = determinar_corredores(pedidos_wave, pedidos, corredores)

    # Corrigir: se não foi possível abastecer, tentar outra combinação
    if corredores_wave is None:
        return gerar_solucao_inicial(pedidos, corredores, lb, ub)

    return pedidos_wave, corredores_wave


from collections import defaultdict

def determinar_corredores(pedidos_wave, pedidos, corredores):
    demanda = defaultdict(int)
    for pid in pedidos_wave:
        for i, q in pedidos[pid].itens.items():
            demanda[i] += q

    # Estratégia gulosa: incluir corredores que suprem os itens mais demandados primeiro
    corredores_ids = list(range(len(corredores)))
    random.shuffle(corredores_ids)  # ou ordenar por "capacidade útil"

    fornecimento = defaultdict(int)
    usados = []

    for cid in corredores_ids:
        c = corredores[cid]
        usados.append(cid)
        for i, q in c.itens.items():
            fornecimento[i] += q

        if all(demanda[i] <= fornecimento[i] for i in demanda):
            return usados  # solução viável encontrada

    return None  # falha em encontrar corredores suficientes

def avaliar(pedidos_wave, pedidos, corredores_wave):
    total = sum(sum(pedidos[pid].itens.values()) for pid in pedidos_wave)
    n_corr = len(corredores_wave)
    if n_corr == 0:
        return 0
    return total / n_corr
