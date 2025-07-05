import os
import subprocess
import csv
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Parâmetros fixos
INTENSIDADE = "0.4"
RESPEITA_LB = "True"
REPETICOES = 3
PASTA_INSTANCIAS = "instancias-lote"
ARQUIVO_SAIDA = "resultados-lote2.csv"
MAX_WORKERS = 4  # Número de execuções simultâneas

def executar_solver(instancia, repeticao):
    caminho_entrada = os.path.join(PASTA_INSTANCIAS, instancia)
    caminho_saida = f"outputs-lote/output_{instancia.replace('.txt', '')}_rep{repeticao}.txt"

    inicio = time.time()
    processo = subprocess.run(
        ["python", "solver-v4.py", caminho_entrada, caminho_saida, INTENSIDADE, RESPEITA_LB],
        capture_output=True,
        text=True
    )
    fim = time.time()
    duracao = round(fim - inicio, 2)

    return {
        'instancia': instancia,
        'intensidade': INTENSIDADE,
        'respeita_lb': RESPEITA_LB,
        'repeticao': repeticao,
        'duracao': duracao,
        'stdout': processo.stdout.strip().replace('\n', '\\n')
    }

def main():
    tarefas = []

    # Gera todas as tarefas (instância x repetição)
    for instancia in sorted(os.listdir(PASTA_INSTANCIAS)):
        if not instancia.endswith(".txt"):
            continue
        for repeticao in range(1, REPETICOES + 1):
            tarefas.append((instancia, repeticao))

    print(f"Executando {len(tarefas)} tarefas com até {MAX_WORKERS} em paralelo...\n")

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor, \
         open(ARQUIVO_SAIDA, 'w', newline='', encoding='utf-8') as f_out:

        writer = csv.writer(f_out)
        writer.writerow(["instancia", "intensidade", "respeita_lb", "repeticao", "duracao", "stdout"])

        # Submete as tarefas ao executor
        futuros = {executor.submit(executar_solver, inst, rep): (inst, rep) for inst, rep in tarefas}

        for future in as_completed(futuros):
            try:
                resultado = future.result()
                writer.writerow([
                    resultado['instancia'],
                    resultado['intensidade'],
                    resultado['respeita_lb'],
                    resultado['repeticao'],
                    resultado['duracao'],
                    resultado['stdout']
                ])
                print(f"✓ {resultado['instancia']} rep {resultado['repeticao']} concluído em {resultado['duracao']}s")
            except Exception as e:
                inst, rep = futuros[future]
                print(f"✗ ERRO: {inst} rep {rep} -> {e}")

if __name__ == "__main__":
    main()
