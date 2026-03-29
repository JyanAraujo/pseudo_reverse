                             ------Pseudoreverse------

Programa cria sequências pseudo_reverses, isto é, para um arquivo fastq foward sem par, cria um reverse falso com o exato reverso complemento dos reads do arquivo de input.

Por exemplo:

entrada:

@read1 1:N:0
ATTGGCCGTGTTTTGAC
+
IIIIIIIIIIIIIIIII

saída:

@read1 2:N:0
GTCAAAACACGGCCAAT
+
IIIIIIIIIIIIIIIII

Quando as duas sequências passarem por processos de overllaping, o resultado tenderá ser igual à sequência de input do Pseudoreverse, ou seja, o próprio foward. 

O programa é recomendado caso precise realizar pipelines que requerem sequências paired end em uma situação onde só há disponível sequências single end. Porém estude o caso específico de sua análise antesde utilizar essa abordagem, pois o Pseudoreverse está gerando sequências falsas (não biológicas), portanto estude as consequências que esse método pode trazer para seus dados antes de continuar com o uso.

Uso:

./pseudo_reverse.py -i <foward_input> -o <nome_pseudo_reverse>


Requerimentos:

python > 3
pip install pandas
pip install argparse
		                 -----Funções-----

fastq_to_df(path) --> Cria um dataframe a partir dos dados de um fastq, criando uma coluna para id (header), seq (sequência do read) e qual (qualidade do read). Trabalhar com a estrutura de dataframe facilita a organização e manipulação dos dados para as funções seguintes.

invcomp_seq(lista) --> A partir de uma lista da coluna seq (sequência do read), e de uma biblioteca, inverte cada elemento da cadeia de strings e substitui as bases A -> T, T -> A, C -> G, G -> C. Ao final cria uma lista com as sequências novas.

fix_header_to_R2(header) --> A partir do dataframe inicial, a função localiza o trecho "1:N:0" de cadaheader, e substitui por "2:N:0". A troca é relevante para uso posteriores do arquivo pseudo reverse, pois diversos programas identificam os arquivos fastq reverses a partir desse trecho.

pseudo_rev_list_to_df(lista, df, base_name) --> Substitui o conteudo da coluna seq do dataframe inicial, pela lista nova criada em invcomp_seq(). Transforma em .fastq e salva como <nome_pseudo_reverse>.

 
