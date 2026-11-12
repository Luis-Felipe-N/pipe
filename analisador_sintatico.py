import json

class SintaxAnalyzer:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos] if self.tokens else None

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None

    def match(self, expected_tipo, expected_valor=None):
        if self.current_token and self.current_token.tipo == expected_tipo:
            if expected_valor and self.current_token.valor != expected_valor:
                raise SyntaxError(f"Erro Sintático: Esperado valor '{expected_valor}', encontrado '{self.current_token.valor}'")
            self.advance()
        else:
            encontrado = self.current_token.tipo if self.current_token else "Fim do Arquivo"
            raise SyntaxError(f"Erro Sintático: Esperado tipo '{expected_tipo}', encontrado '{encontrado}'")

    def parse(self):
        return self.programa()

    def programa(self):
        # Regra: pipeline <id> inicio <comandos> fim
        self.match("KEYWORD", "pipeline")
        
        nome_pipeline = self.current_token.valor
        self.match("IDENTIFICADOR")
        
        self.match("KEYWORD", "inicio")
        
        comandos = self.lista_comandos()
        
        self.match("KEYWORD", "fim")
        return {"tipo": "Programa", "nome": nome_pipeline, "comandos": comandos}

    def lista_comandos(self):
        comandos = []
        # Continua processando comandos até encontrar "fim" ou "fimse" (que fecham blocos)
        while self.current_token and self.current_token.valor not in ("fim", "fimse", "senao"):
            comandos.append(self.comando())
        return comandos

    def comando(self):
        # Identifica a regra pelo lookahead do Token atual
        if self.current_token.tipo == "KEYWORD" and self.current_token.valor == "se":
            return self.comando_se()
        elif self.current_token.tipo == "KEYWORD" and self.current_token.valor == "carregar":
            return self.comando_carga()
        elif self.current_token.tipo == "IDENTIFICADOR":
            id_var = self.current_token.valor
            self.match("IDENTIFICADOR")
            self.match("ATRIBUICAO", "=")
            
            if self.current_token.valor == "extrair":
                return self.comando_extracao(id_var)
            elif self.current_token.valor == "transformar":
                return self.comando_transformacao(id_var)
            else:
                raise SyntaxError(f"Comando inválido após atribuição: {self.current_token.valor}")
        else:
            raise SyntaxError(f"Token não reconhecido como início de comando: {self.current_token.valor}")

    def comando_extracao(self, id_var):
        # Regra: <id> = extrair de <funcao> ( <string> )
        self.match("KEYWORD", "extrair")
        self.match("KEYWORD", "de")
        
        fonte = self.current_token.valor
        self.match("FUNCAO")
        self.match("DELIMITADOR", "(")
        
        caminho_ou_query = self.current_token.valor
        self.match("STRING")
        self.match("DELIMITADOR", ")")
        
        return {"tipo": "Extracao", "variavel": id_var, "fonte": fonte, "alvo": caminho_ou_query}

    def comando_transformacao(self, id_var):
        # Regra: <id> = transformar <id> com <funcao> ( ... )
        self.match("KEYWORD", "transformar")
        
        origem = self.current_token.valor
        self.match("IDENTIFICADOR")
        self.match("KEYWORD", "com")
        
        funcao = self.current_token.valor
        self.match("FUNCAO")
        self.match("DELIMITADOR", "(")
        
        args = []
        # Captura todos os argumentos dentro dos parênteses da transformação
        while self.current_token and self.current_token.valor != ")":
            args.append(self.current_token.valor)
            self.advance()
            
        self.match("DELIMITADOR", ")")
        
        return {"tipo": "Transformacao", "variavel": id_var, "origem": origem, "operacao": funcao, "argumentos": " ".join(args)}

    def comando_carga(self):
        # Regra: carregar <id> em <funcao> ( <string> )
        self.match("KEYWORD", "carregar")
        
        id_var = self.current_token.valor
        self.match("IDENTIFICADOR")
        self.match("KEYWORD", "em")
        
        destino = self.current_token.valor
        self.match("FUNCAO")
        self.match("DELIMITADOR", "(")
        
        caminho = self.current_token.valor
        self.match("STRING")
        self.match("DELIMITADOR", ")")
        
        return {"tipo": "Carga", "variavel": id_var, "destino": destino, "caminho": caminho}

    def comando_se(self):
        # Regra: se linhas ( <id> ) > <numero> entao <comandos> [senao <comandos>] fimse
        self.match("KEYWORD", "se")
        
        if self.current_token.valor == "linhas":
            self.match("FUNCAO", "linhas")
            self.match("DELIMITADOR", "(")
            var_cond = self.current_token.valor
            self.match("IDENTIFICADOR")
            self.match("DELIMITADOR", ")")
            
            op = self.current_token.valor
            self.match("OPERADOR_RELACIONAL")
            
            val = self.current_token.valor
            self.match("NUMERO")
            
            condicao = f"linhas({var_cond}) {op} {val}"
        else:
            raise SyntaxError(f"Expressão condicional não suportada: {self.current_token.valor}")

        self.match("KEYWORD", "entao")
        comandos_verdadeiro = self.lista_comandos()
        
        comandos_falso = []
        if self.current_token and self.current_token.valor == "senao":
            self.match("KEYWORD", "senao")
            comandos_falso = self.lista_comandos()
            
        self.match("KEYWORD", "fimse")
        
        return {
            "tipo": "Condicional", 
            "condicao": condicao, 
            "bloco_entao": comandos_verdadeiro,
            "bloco_senao": comandos_falso
        }

# ==============================================================================
# BLOCO DE TESTE E INTEGRAÇÃO (Requer a classe LexicalAnalyzer do TP2)
# ==============================================================================
if __name__ == "__main__":
    # Certifique-se de importar o seu analisador léxico corretamente
    # from analisador_lexico import LexicalAnalyzer
    
    codigo_teste = """
    pipeline comissao_mensal inicio
        vendas = extrair de arquivocsv("/datalake/vendas.csv")
        se linhas(vendas) > 0 entao
            carregar vendas em novo_banco("financeiro.comissoes")
        senao
            carregar vendas em novo_csv("/datalake/alertas/vazio.csv")
        fimse
    fim
    """
    
    # 1. Executa o Analisador Léxico
    lexico = LexicalAnalyzer()
    tokens_gerados = lexico.analyze(codigo_teste)
    
    # 2. Executa o Analisador Sintático
    parser = Parser(tokens_gerados)
    arvore_sintatica = parser.parse()
    
    # Exibe a Árvore Sintática Abstrata (AST) em formato JSON formatado
    print(json.dumps(arvore_sintatica, indent=4, ensure_ascii=False))