
from email.parser import Parser
import json
from analisador_lexico import LexicalAnalyzer, read_code_from_file
from analisador_sintatico import SintaxAnalyzer

file_path = 'programa.pipe'
codigo_fonte = read_code_from_file(file_path)

lexico = LexicalAnalyzer()
tokens_gerados = lexico.analyze(codigo_fonte)

parser = SintaxAnalyzer(tokens_gerados)
arvore_sintatica = parser.parse()

# Exibe a Árvore Sintática Abstrata (AST) no terminal
print(json.dumps(arvore_sintatica, indent=4, ensure_ascii=False))