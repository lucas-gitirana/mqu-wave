from classes import Pedido, Corredor
from collections import defaultdict
from gerar_solucao import gerar_solucao_inicial, determinar_corredores, avaliar

# Realiza a leitura das instâncias
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

# Calcula o total de unidades de pedidos (TALVEZ DÊ PARA TIRAR)
def total_unidades(pedidos):
    return sum(sum(p.itens.values()) for p in pedidos)

# Verifica se tem corredores suficientes (TALVEZ DÊ PARA TIRAR)
def corredores_suficientes(pedidos, corredores):
    demanda = defaultdict(int)
    for p in pedidos:
        for i, q in p.itens.items():
            demanda[i] += q

    fornecimento = defaultdict(int)
    for c in corredores:
        for i, q in c.itens.items():
            fornecimento[i] += q

    return all(demanda[i] <= fornecimento[i] for i in demanda)

# Método para fazer a busca local iterada
def ils(pedidos, corredores, lb, ub, max_iter=100):

    # Gera uma solução VIÁVEL aleatória
    melhor_solucao, corredores_wave = gerar_solucao_inicial(pedidos, corredores, lb, ub)
    # Calcula a função objetivo da solução gerada
    melhor_obj = avaliar(melhor_solucao, pedidos, corredores_wave)

    # Prints de teste
    print('Melhor solução: ', melhor_solucao)
    print('Melhor objetivo: ', melhor_obj)

    # A partir daqui, implementar as buscas locais iteradas para obter a melhor solução de fato
    """ for _ in range(max_iter):
        solucao = perturbar(melhor_solucao)
        solucao = busca_local(solucao, corredores, lb, ub)
        obj = avaliar(solucao)
        if obj > melhor_obj:
            melhor_solucao = solucao
            melhor_obj = obj """

    return melhor_solucao

# Formata a saída no padrão do desafio
def salvar_saida(output_path, pedidos_wave, corredores_wave):
    with open(output_path, 'w') as f:
        f.write(f"{len(pedidos_wave)}\n")
        for p in pedidos_wave:
            f.write(f"{p.id}\n")
        f.write(f"{len(corredores_wave)}\n")
        for c in corredores_wave:
            f.write(f"{c.id}\n")


# TESTE
pedidos, corredores, lb, ub = ler_instancias('instance_0020.txt')
print('Total unidades: ', total_unidades(pedidos))
print('Corredores suficientes? ', corredores_suficientes(pedidos, corredores))
print('ILS teste: ', ils(pedidos, corredores, lb, ub))