import re

# INTERNO
KEYWORDS_RE = r'\b(pipeline|inicio|fim|extrair|de|carregar|em|transformar|com|se|entao|senao|fimse)\b'
FUNCAO_RE = r'\b(psql|arquivocsv|novo_csv|novo_banco|concatenar|separar|operacao|linhas)\b'
ID_RE = r'[a-zA-Z_][a-zA-Z0-9_]*'                          

# PADRÃO
STRING_RE = r'"[^"]*"'                                     
NUMERO_RE = r'\d+'                                         
OP_REL_RE = r'==|!=|>=|<=|>|<'                             
OP_ARIT_RE = r'[+\-*/]'                                    
ATRIB_RE = r'='                                            
DELIM_RE = r'[(),]'                                        
ESPACO_RE = r'[ \t\n\r]+'  # Vírgula removida para evitar criação de tupla
COMENT_RE = r'//.*'        # Adicionado para suportar comentários de linha

###
class Token:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor

    def __repr__(self):
        return f"Token({self.tipo}, '{self.valor}')"

class LexicalAnalyzer:
    def __init__(self):
        
        self.token_patterns = [
            (KEYWORDS_RE, 'KEYWORD'),
            (FUNCAO_RE,   'FUNCAO'),
            (ID_RE,       'IDENTIFICADOR'),
            (STRING_RE,   'STRING'),
            (NUMERO_RE,   'NUMERO'),
            (OP_REL_RE,   'OPERADOR_RELACIONAL'),
            (OP_ARIT_RE,  'OPERADOR_ARITMETICO'),
            (ATRIB_RE,    'ATRIBUICAO'),
            (DELIM_RE,    'DELIMITADOR'),
            (COMENT_RE,   None), # Ignora comentários
            (ESPACO_RE,   None)  # Ignora espaços
        ]
        
        self.compiled_patterns = [(re.compile(pattern), token_type) for pattern, token_type in self.token_patterns]

    def analyze(self, code):
        tokens = []
        while code:
            match = None
            for regex, token_type in self.compiled_patterns:
                match = regex.match(code)
                if match:
                    if token_type:
                        tokens.append(Token(token_type, match.group(0)))
                    code = code[match.end():]
                    break
            if not match:
                raise SyntaxError(f"Token inválido: {code[0]}")
        return tokens

def read_code_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Analizando o código
file_path = 'programa.pipe'
code = read_code_from_file(file_path)
analyzer = LexicalAnalyzer()
tokens = analyzer.analyze(code)

for token in tokens:
    print(token)