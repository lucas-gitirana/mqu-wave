import sys
from classes import Pedido, Corredor
from gerar_solucao import gerar_solucao_inicial, determinar_corredores, avaliar, perturbar, busca_local

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

# Método para fazer a busca local iterada
def ils(pedidos, corredores, lb, ub, max_iter=100):
    pedidos_wave, corredores_wave = gerar_solucao_inicial(pedidos, corredores, lb, ub)
    melhor_obj = avaliar(pedidos_wave, pedidos, corredores_wave)
    melhor_solucao = (pedidos_wave, corredores_wave)

    # A partir daqui, implementar as buscas locais iteradas para obter a melhor solução de fato
    for _ in range(max_iter):
        # Perturba os pedidos
        pedidos_perturbados = perturbar(pedidos_wave, pedidos, lb, ub, 0.2)

        # A partir dos pedidos perturbados, gera os corredores viáveis
        corredores_perturbados = determinar_corredores(pedidos_perturbados, pedidos, corredores)
        if corredores_perturbados is None:
            continue  # ignora se não conseguiu gerar solução viável

        # Aplica busca local na solução perturbada
        pedidos_local, corredores_local = busca_local(
            pedidos_perturbados, pedidos, corredores, lb, ub, estrategia='swap'
        )

        # Avalia a nova solução
        obj = avaliar(pedidos_local, pedidos, corredores_local)

        # Se for melhor, atualiza o melhor
        if obj > melhor_obj:
            melhor_solucao = (pedidos_local, corredores_local)
            melhor_obj = obj
            pedidos_wave, corredores_wave = pedidos_local, corredores_local

    return melhor_solucao

# Formata a saída no padrão do desafio
def salvar_saida(output_path, pedidos_wave, corredores_wave):
    with open(output_path, 'w') as f:
        f.write(f"{len(pedidos_wave)}\n")
        for p in pedidos_wave:
            f.write(f"{p}\n")
        f.write(f"{len(corredores_wave)}\n")
        for c in corredores_wave:
            f.write(f"{c}\n")


if len(sys.argv) < 3:
    print("Uso: python leitura.py <arquivo_entrada> <arquivo_saida>")
    sys.exit(1)

arquivo_instancia = sys.argv[1]
arquivo_saida = sys.argv[2]

pedidos, corredores, lb, ub = ler_instancias(arquivo_instancia)
pedidos_wave, corredores_wave = ils(pedidos, corredores, lb, ub)
salvar_saida('output.txt', pedidos_wave, corredores_wave)

# TESTE
print('Pedidos selecionados:', pedidos_wave)
print('Corredores selecionados:', corredores_wave)
print('F.O.:', avaliar(pedidos_wave, pedidos, corredores_wave))