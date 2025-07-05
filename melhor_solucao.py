import csv

def extrair_fo(stdout_texto):
    """Extrai a função objetivo (F.O.) de um campo de texto do stdout."""
    if not stdout_texto:
        return None
    for linha in stdout_texto.splitlines():
        if "F.O.:" in linha:
            try:
                return float(linha.strip().split("F.O.:")[1])
            except ValueError:
                return None
    return None

def encontrar_melhor_configuracao(caminho_csv):
    melhor = None

    with open(caminho_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            fo = extrair_fo(row['stdout'])
            if fo is None:
                continue

            if melhor is None or fo > melhor['fo']:
                melhor = {
                    'instancia': row['instancia'],
                    'intensidade': row['intensidade'],
                    'respeita_lb': row['respeita_lb'],
                    'repeticao': row['repeticao'],
                    'fo': fo,
                    'duracao': row['duracao']
                }

    return melhor

if __name__ == "__main__":
    caminho = "log_teste.csv"  # ajuste aqui se seu arquivo tiver outro nome
    resultado = encontrar_melhor_configuracao(caminho)

    if resultado:
        print("Melhor configuração encontrada:")
        print(f"Instância:     {resultado['instancia']}")
        print(f"Intensidade:   {resultado['intensidade']}")
        print(f"Respeita LB:   {resultado['respeita_lb']}")
        print(f"Repetição:     {resultado['repeticao']}")
        print(f"Duração (s):   {resultado['duracao']}")
        print(f"Função Obj.:   {resultado['fo']}")
    else:
        print("Nenhuma função objetivo válida encontrada.")
