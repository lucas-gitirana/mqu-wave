import os
import subprocess
import multiprocessing
import itertools
import time
from datetime import datetime

# ================
# CONFIGURAÇÕES
# ================
CAMINHO_INSTANCIAS = "instancias"  # pasta onde estão os arquivos .txt
CAMINHO_SOLVER = "solver-v4.py"
RESULTADOS_DIR = "resultados"
REPETICOES = 10
INTENSIDADES = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
RESPEITA_LB_OPTIONS = [True, False]
LIMITE_TEMPO = 60  # segundos por execução
PROCESSOS_PARALELOS = multiprocessing.cpu_count()  # ou defina manualmente

# ================
# CRIAR DIRETÓRIOS
# ================
os.makedirs(RESULTADOS_DIR, exist_ok=True)

# ================
# EXECUÇÃO DE TESTE
# ================
def executar_teste(instancia_path, intensidade, respeita_lb, repeticao):
    nome_instancia = os.path.splitext(os.path.basename(instancia_path))[0]
    print(f"[EXECUTANDO] {nome_instancia} | Intensidade: {intensidade} | LB: {respeita_lb} | Run: {repeticao}")

    nome_instancia = os.path.splitext(os.path.basename(instancia_path))[0]
    saida_nome = f"{nome_instancia}__int{intensidade}__lb{respeita_lb}__run{repeticao}.out"
    caminho_saida = os.path.join(RESULTADOS_DIR, saida_nome)

    comando = [
        "python", CAMINHO_SOLVER,
        instancia_path,
        caminho_saida,
        str(intensidade),
        str(respeita_lb)
    ]

    inicio = time.time()
    try:
        resultado = subprocess.run(
            comando,
            capture_output=True,
            text=True,
            timeout=LIMITE_TEMPO + 10  # pequena margem
        )
        duracao = time.time() - inicio

        with open(os.path.join(RESULTADOS_DIR, "log_teste.csv"), "a") as log:
            log.write(f"{nome_instancia},{intensidade},{respeita_lb},{repeticao},{duracao:.2f},\"{resultado.stdout.strip()}\"\n")

    except subprocess.TimeoutExpired:
        with open(os.path.join(RESULTADOS_DIR, "log_teste.csv"), "a") as log:
            log.write(f"{nome_instancia},{intensidade},{respeita_lb},{repeticao},TIMEOUT\n")


# ================
# GERAR COMBINAÇÕES DE TESTE
# ================
tarefas = []
arquivos_instancia = [
    os.path.join(CAMINHO_INSTANCIAS, f)
    for f in os.listdir(CAMINHO_INSTANCIAS)
    if f.endswith(".txt")
]

for instancia, intensidade, respeita_lb, repeticao in itertools.product(
    arquivos_instancia,
    INTENSIDADES,
    RESPEITA_LB_OPTIONS,
    range(1, REPETICOES + 1)
):
    tarefas.append((instancia, intensidade, respeita_lb, repeticao))

print(f"Total de testes: {len(tarefas)}")
print("Todas as tarefas:")
for t in tarefas:
    print(t)

# ================
# EXECUTAR EM PARALELO
# ================
if __name__ == "__main__":
    inicio_total = datetime.now()

    with open(os.path.join(RESULTADOS_DIR, "log_teste.csv"), "w") as log:
        log.write("instancia,intensidade,respeita_lb,repeticao,duracao,stdout\n")

    with multiprocessing.Pool(PROCESSOS_PARALELOS) as pool:
        pool.starmap(executar_teste, tarefas)

    fim_total = datetime.now()
    print(f"Todos os testes finalizados. Tempo total: {fim_total - inicio_total}")
