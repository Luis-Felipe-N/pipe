# INTERNO
KEYWORDS_RE = r'\b(pipeline|inicio|fim|extrair|de|carregar|em|transformar|com|se|entao|senao|fimse)\b'
FUNCAO_RE = r'\b(psql|arquivocsv|novo_csv|novo_banco|concatenar|separar|operacao|linhas)\b'
ID_RE = r'[a-zA-Z_][a-zA-Z0-9_]*'                           # Nomes de variáveis

# PADRÃO
STRING_RE = r'"[^"]*"'                                     # Textos e caminhos
NUMERO_RE = r'\d+'                                          # Números inteiros
OP_REL_RE = r'==|!=|>=|<=|>|<'                             # Operadores relacionais
OP_ARIT_RE = r'[+\-*/]'                                    # Operadores aritméticos
ATRIB_RE = r'='                                             # Atribuição
DELIM_RE = r'[(),]'                                         # Parênteses e vírgulas
ESPACO_RE = r'[ \t\n]+',                                    # Espaços e quebras de linha (ignorados)
ERRO_RE = r'.',                                             # Erros