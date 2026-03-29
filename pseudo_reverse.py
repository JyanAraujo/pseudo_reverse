#!/usr/bin/env python3
#Criando pseudo-reverses
#Contexto: Gostaria de utilizar sequencias que deram fowards only como output do trimmomatic
#Para isso vamos criar arquivos "pseudo-reverses"
#nada mais são que fastqs que "enganam" os softwares de merge entre fowards e reverses
#nosso objetivo aqui é inverter as sequencias fowards, onde teremos o perfeito inverso complemento
#para então os softwares de merge criarem no final uma sequencia "pareada", porém tendo o mesmo valor
#que o foward sozinho. Vamos lá

#FUNÇÕES

import pandas as pd
from pathlib import Path

def fastq_to_df(path):  #função para pegar fastq, transformar em df, cada coluna é cada linha (header, seq, qualidade)

    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}") #verifica se caminho é valido
        
    records = []  #cria lista vazia, o loop vai inserir informações aqui e depois pegar o conteudo e fazer um df

    with path.open() as f:  #loop
        while True:  #cria um loop infinito até a condição ser satisfeita, (se nao for header break)
            header = f.readline().strip()  # .readline() le a primeira linha e avança o ponteiro pra proxima
            #.strip() retira o \n do final da linha
            if not header: #aqui o indicador ta na segunda linha (que nao é o header, entao quebra)
                break

            seq = f.readline().strip() #repete pra linha de sequencia
            f.readline()              #ignora a linha com "+"
            qual = f.readline().strip() #repete pra linha de qualidade

            records.append({
                "id": header,
                "seq": seq,
                "qual": qual,
                "len": len(seq)
            }) #coloca na lista "records"

    return pd.DataFrame(records) #cria dataframe com conteudo de "records"



def invcomp_seq(lista): #pega uma lista com as sequencias vindas da coluna "seq", inverte e troca as bases
    comp = {
        "A": "T",
        "T": "A",
        "C": "G",
        "G": "C"
    } #cria dicionário, se A então é T, se T então é A etc...

    seqs_novas = [] #lista vazia, onde serão adicionadas as sequencias invertidas

    for seq in lista:
        inv = seq[::-1]  #inverte cada string (cada elemento da lista)
        inv_comp = ""  #string vazia, onde serão depositadas as bases complementares

        for base in inv:
            if base not in comp:
                raise ValueError(f"Base inválida: {base}") #teste de erro
            inv_comp += comp[base] #adiciona o inverso baseado no dicionário

        seqs_novas.append(inv_comp) #incorpora na lista nova

    return seqs_novas


def fix_header_to_R2(header): #modificação do header para 2:N:0 --> padrão pra reverse
    left, right = header.split(" ")
    right = right.replace("1:N:0:", "2:N:0:")
    return f"{left} {right}"


def pseudo_rev_list_to_df(lista, df, base_name): #pega a lista resultante, substitui pela coluna "seq" anterior,
    #transforma df em .fastq e salva como R2

    df["seq"] = lista #troca a lista de seqs reversa no dataframe

    with open(base_name, "w") as f: #cria e abre um arquivo no modo write
        for rid, seq, qual in zip(df["id"], df["seq"], df["qual"]):
            rid = fix_header_to_R2(rid)
            f.write(f"@{rid}\n{seq}\n+\n{qual}\n")


import argparse

def main():
    parser = argparse.ArgumentParser(
        description="Gera um pseudo-FASTQ reverse (R2) a partir de um FASTQ forward (R1)"
    )

    parser.add_argument(
        "-i", "--input",
        required=True,
        help="FASTQ forward (R1)"
    )

    parser.add_argument(
        "-o", "--output",
        required=True,
        help="FASTQ de saída (pseudo-R2)"
    )

    args = parser.parse_args()

    # pipeline
    df = fastq_to_df(args.input)
    seqs_rev = invcomp_seq(df["seq"])
    pseudo_rev_list_to_df(seqs_rev, df, args.output)

    print(f"✅ Pseudo-R2 gerado: {args.output}")

if __name__ == "__main__":
    main()


