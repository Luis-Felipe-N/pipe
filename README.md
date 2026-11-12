# Compilador 2026/02 - Pipe

Projeto desenvolvido para a disciplina de Compiladores.

**Alunos:** 
* Luis Felipe
* Afonso Dglan

**Professora:** 
* Ana Paula

**Pipe** é uma Linguagem de Domínio Específico (DSL) voltada para a área de Engenharia de Dados. Ela foi criada para abstrair a complexidade de infraestrutura e reduzir o código repetitivo (*boilerplate*) na criação de rotinas ETL/ELT. Em vez de lidar com conexões e sessões manuais, o código foca diretamente no fluxo do dado (extração, transformação e carga).

## Fases do Compilador

O projeto contempla a construção doncompilador, dividido nas seguintes etapas:

1. **Analisador Léxico:** Lê o código-fonte (arquivo `.pipe`) e utiliza Expressões Regulares (Regex) para varrer os caracteres. Ele ignora espaços, quebras de linha e comentários, agrupando o texto em uma sequência estruturada de Tokens (palavras-chave, operadores, strings, identificadores).
2. **Analisador Sintático:** Consome a lista de tokens gerada pela etapa anterior utilizando um *Parser* Descendente Recursivo. Ele valida se a ordem dos tokens respeita as regras da gramática formal (BNF) da linguagem e, caso o código esteja correto, constrói e retorna a Árvore Sintática Abstrata (AST).

## Estrutura do Repositório

* `analisador_lexico.py`: Definição das regex e lógica de varredura (geração de tokens).
* `analisador_sintatico.py`: Regras de produção e construção da AST (validação gramatical).
* `main.py`: Script orquestrador que conecta a leitura do arquivo às fases léxica e sintática.
* `programa.pipe`: Código de teste escrito com a sintaxe da linguagem PipeFlow.

## Como Executar

O projeto foi construído apenas com bibliotecas nativas do Python. Para testar o compilador, execute o arquivo principal na raiz do projeto:

```bash
python main.py

Exemplo de Saída (AST)
Se a sintaxe do arquivo .pipe estiver correta, o compilador não lançará erros e retornará a árvore lexica/sintática estruturada, como no exemplo abaixo:

-- Analisador Léxico --
Token(KEYWORD, 'pipeline')
Token(IDENTIFICADOR, 'comissao_mensal')
Token(KEYWORD, 'inicio')
Token(IDENTIFICADOR, 'vendas')
Token(ATRIBUICAO, '=')
Token(KEYWORD, 'extrair')
Token(KEYWORD, 'de')
Token(FUNCAO, 'arquivocsv')

-- Analisador Sintático --

{
    "tipo": "Programa",
    "nome": "comissao_mensal",
    "comandos": [
        {
            "tipo": "Extracao",
            "variavel": "vendas",
            "fonte": "arquivocsv",
            "alvo": "\"/datalake/vendas.csv\""
        },
        {
            "tipo": "Extracao",
            "variavel": "vendedores",
            "fonte": "psql",
            "alvo": "\"select nome, sobrenome from vendedores where ativo = 1\""
        },
        {
            "tipo": "Transformacao",
            "variavel": "comissoes",
            "origem": "vendas",
            "operacao": "operacao",
            "argumentos": "valor * 5 / 100"
        },
        {
            "tipo": "Transformacao",
            "variavel": "nomes",
            "origem": "vendedores",
            "operacao": "concatenar",
            "argumentos": "nome , sobrenome"
        },
        {
            "tipo": "Condicional",
            "condicao": "linhas(vendas) > 0",
            "bloco_entao": [
                {
                    "tipo": "Carga",
                    "variavel": "comissoes",
                    "destino": "novo_banco",
                    "caminho": "\"financeiro.comissoes_2026_09\""
                }
            ],
            "bloco_senao": [
                {
                    "tipo": "Carga",
                    "variavel": "nomes",
                    "destino": "novo_csv",
                    "caminho": "\"/datalake/alertas/sem_vendas_2026_09.csv\""
                }
            ]
        }
    ]
}
```