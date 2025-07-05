==============================================================
INSTRUÇÕES DE COMPILAÇÃO E EXECUÇÃO
==============================================================

Projeto: Resolução do problema de separação de pedidos via ILS
Autor: Lucas Gitirana
Linguagem: Python 3
--------------------------------------------------------------

1. PRÉ-REQUISITOS
------------------------------
- Python 3.8 ou superior instalado
- Nenhuma biblioteca externa é necessária
- Pode ser executado em Windows, Linux ou macOS

2. COMPILAÇÃO
------------------------------
Este projeto está implementado em Python e **NÃO requer compilação**.

Certifique-se de que os seguintes arquivos estejam no mesmo diretório:

- solver.py         → Algoritmo principal (ILS)
- classes.py        → Definição das classes Pedido e Corredor
- instance_XXXX.txt → Arquivo de entrada (instância)

3. EXECUÇÃO
------------------------------
Para executar o algoritmo, abra o terminal e digite:

    python solver.py <arquivo_entrada> <arquivo_saida> <intensidade> <respeita_lb>

Parâmetros:
- <arquivo_entrada>   → nome do arquivo da instância (ex: instance_0020.txt)
- <arquivo_saida>     → nome do arquivo onde será gravada a solução (ex: output.txt)
- <intensidade>       → valor entre 0 e 1 que define a fração de pedidos a remover na perturbação
- <respeita_lb>       → True ou False, indica se o LB deve ser respeitado durante a adição de pedidos

Exemplo:

    python solver.py instance_0020.txt output.txt 0.2 True

4. FORMATO DE SAÍDA
------------------------------
O arquivo de saída gerado seguirá o formato exigido pelo desafio:

    <número de pedidos selecionados>
    <id do pedido 1>
    ...
    <id do pedido n>
    <número de corredores selecionados>
    <id do corredor 1>
    ...
    <id do corredor m>

5. VALIDAÇÃO COM CHECKER DO DESAFIO
------------------------------
Para verificar se a solução está correta, utilize o script checker.py fornecido:

    python checker.py instance_0020.txt output.txt

6. TEMPO DE EXECUÇÃO
------------------------------
O algoritmo possui um tempo limite de execução configurado em 60 segundos.
Esse valor pode ser alterado diretamente no arquivo solver.py na linha:

    LIMITE_TEMPO = 60

==============================================================