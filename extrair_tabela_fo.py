import csv

def extrair_fo(stdout_texto):
    """Extrai o valor da F.O. de um texto bruto de stdout."""
    if not stdout_texto:
        return None
    for linha in stdout_texto.split("\\n"):  # O stdout vem com '\n' convertido para '\\n'
        if "F.O.:" in linha:
            try:
                return float(linha.strip().split("F.O.:")[1])
            except ValueError:
                return None
    return None

def gerar_tabela_fo(entrada_csv, saida_csv):
    with open(entrada_csv, newline='', encoding='utf-8') as f_in, \
         open(saida_csv, 'w', newline='', encoding='utf-8') as f_out:

        reader = csv.DictReader(f_in)
        writer = csv.writer(f_out)

        writer.writerow(["instancia", "intensidade", "respeita_lb", "repeticao", "duracao", "fo"])

        for row in reader:
            fo = extrair_fo(row['stdout'])
            if fo is not None:
                writer.writerow([
                    row['instancia'],
                    row['intensidade'],
                    row['respeita_lb'],
                    row['repeticao'],
                    row['duracao'],
                    fo
                ])

if __name__ == "__main__":
    gerar_tabela_fo("log_teste.csv", "tabela_fo.csv")
    print("Arquivo 'tabela_fo.csv' gerado com sucesso!")
