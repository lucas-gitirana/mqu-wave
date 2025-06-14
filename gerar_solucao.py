import random

def gerar_solucao_inicial(pedidos, corredores, lb, ub):
    pedidos_ids = list(range(len(pedidos)))
    random.shuffle(pedidos_ids)
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
    random.shuffle(corredores_ids)

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


# Esta função retorna o valor da função objetivo, considerando os pedidos e corredores selecionados na wave
def avaliar(pedidos_wave, pedidos, corredores_wave):
    total = sum(sum(pedidos[pid].itens.values()) for pid in pedidos_wave)
    n_corr = len(corredores_wave)
    if n_corr == 0:
        return 0
    return total / n_corr

def perturbar(pedidos_wave, pedidos, lb, ub, intensidade=0.2):
    n_remover = max(1, int(len(pedidos_wave) * intensidade))
    pedidos_wave_novo = pedidos_wave.copy()

    # Remove aleatoriamente alguns pedidos
    remover = random.sample(pedidos_wave_novo, n_remover)
    for r in remover:
        pedidos_wave_novo.remove(r)

    # Calcula unidades atuais
    total = sum(sum(pedidos[pid].itens.values()) for pid in pedidos_wave_novo)

    # Tenta adicionar novos pedidos que não estavam na wave
    candidatos = list(set(range(len(pedidos))) - set(pedidos_wave_novo))
    random.shuffle(candidatos)
    for c in candidatos:
        unidades_c = sum(pedidos[c].itens.values())
        if total + unidades_c <= ub:
            pedidos_wave_novo.append(c)
            total += unidades_c
        if total >= lb:
            break

    # Valida se respeita LB
    if total < lb:
        return perturbar(pedidos_wave, pedidos, lb, ub, intensidade)  # recursivamente tentar outra perturbação

    return pedidos_wave_novo

def busca_local(pedidos_wave, pedidos, corredores, lb, ub, estrategia='swap'):
    pedidos_wave_atual = pedidos_wave.copy()
    melhor_corredores = determinar_corredores(pedidos_wave_atual, pedidos, corredores)
    melhor_obj = avaliar(pedidos_wave_atual, pedidos, melhor_corredores)

    if melhor_corredores is None:
        return pedidos_wave_atual, melhor_corredores  # solução não viável

    melhorou = True

    while melhorou:
        melhorou = False
        candidatos_dentro = pedidos_wave_atual.copy()
        candidatos_fora = list(set(range(len(pedidos))) - set(pedidos_wave_atual))

        # Percorre todos os swaps possíveis (pedido dentro x fora)
        for p_out in candidatos_dentro:
            for p_in in candidatos_fora:
                tentativa = pedidos_wave_atual.copy()
                tentativa.remove(p_out)
                tentativa.append(p_in)

                # Verifica limites LB e UB
                total = sum(sum(pedidos[pid].itens.values()) for pid in tentativa)
                if total < lb or total > ub:
                    continue

                # Verifica corredores viáveis
                corredores_tentativa = determinar_corredores(tentativa, pedidos, corredores)
                if corredores_tentativa is None:
                    continue

                obj = avaliar(tentativa, pedidos, corredores_tentativa)

                # Se encontrou melhoria, aceita imediatamente (FIRST IMPROVEMENT)
                if obj > melhor_obj:
                    pedidos_wave_atual = tentativa
                    melhor_corredores = corredores_tentativa
                    melhor_obj = obj
                    melhorou = True
                    break  # sai do loop interno
            if melhorou:
                break  # sai do loop externo

    return pedidos_wave_atual, melhor_corredores
