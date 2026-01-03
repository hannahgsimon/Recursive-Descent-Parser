import sys
import re

# Token Types
TOKEN_TYPES = {
    'LET': r'let',
    'IN': r'\bin\b',
    'END': r'end',
    'IF': r'if',
    'THEN': r'then',
    'ELSE': r'else',
    'INT': r'\bint\b',
    'REAL': r'\breal\b',
    'ID': r'[a-zA-Z][a-zA-Z0-9]*',
    'NUMBER': r'\d+(\.\d+)?',
    'ASSIGN': r'=',
    'COLON': r':',
    'SEMICOLON': r';',
    'LPAREN': r'\(', 'RPAREN': r'\)',
    'PLUS': r'\+',
    'MINUS': r'\-',
    'TIMES': r'\*',
    'DIVIDE': r'/',
    'LESS': r'<',
    'LESSEQ': r'<=',
    'GREATER': r'>',
    'GREATEREQ': r'>=',
    'EQUAL': r'==',
    'NOTEQ': r'<>'
}

# Lexer to tokenize input
class Lexer:
    def __init__(self, text):
        self.text = text
        self.tokens = self.tokenize()
        self.index = 0
    
    def tokenize(self):
        tokens = []
        while self.text:
            self.text = self.text.lstrip()
            for token_type, pattern in TOKEN_TYPES.items():
                match = re.match(pattern, self.text)
                if match:
                    token_value = match.group(0)
                    tokens.append((token_type, token_value))
                    self.text = self.text[len(token_value):]
                    break
            else:
                raise SyntaxError(f"Invalid token at: {self.text[:10]}")
        return tokens

    def get_next_token(self):
        if self.index < len(self.tokens):
            token = self.tokens[self.index]
            self.index += 1
            return token
        return ('EOF', '')

# Parser for recursive-descent parsing
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        self.symbol_table = {}

    def error(self):
        raise SyntaxError("Error")

    def eat(self, token_type):
        if self.current_token[0] == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()
    
    def prog(self):
        while self.current_token[0] == 'LET':
            self.let_in_end()

    def let_in_end(self):
        self.eat('LET')
        self.decl_list()
        self.eat('IN')
        var_type = self.type()
        result = self.expr()
        self.eat('END')
        self.eat('SEMICOLON')
        print(result)

    def decl_list(self):
        self.decl()
        while self.current_token[0] == 'ID':
            self.decl()
            
    def decl(self):
        var_name = self.current_token[1]
        self.eat('ID')
        self.eat('COLON')

        if self.current_token[0] in ('INT', 'REAL'):
            var_type = self.current_token[0]
            self.eat(var_type)
        else:
            self.error()

        if self.current_token[0] == 'ASSIGN':
            self.eat('ASSIGN')
            value = self.expr()
            self.eat('SEMICOLON')
            self.symbol_table[var_name] = (var_type, value)
        else:
            self.error()
            
    def type(self):
        if self.current_token[0] in ('INT', 'REAL'):
            type_val = self.current_token[0]
            self.eat(type_val)
            return type_val
        else:
            self.error()
    
    def expr(self):
        if self.current_token[0] == 'IF':
            return self.if_expr()
        result = self.term()
        while self.current_token[0] in ('PLUS', 'MINUS'):
            op = self.current_token[0]
            self.eat(op)
            right = self.term()
            if op == 'PLUS':
                result += right
            else:
                result -= right
        return result
    
    def term(self):
        result = self.factor()
        while self.current_token[0] in ('TIMES', 'DIVIDE'):
            op = self.current_token[0]
            self.eat(op)
            right = self.factor()
            if op == 'TIMES':
                result *= right
            else:
                result /= right
        return result
    
    def factor(self):
        token = self.current_token
        if token[0] == 'LPAREN':
            self.eat('LPAREN')
            result = self.expr()
            self.eat('RPAREN')
            return result
        elif token[0] == 'ID':
            var_name = token[1]
            self.eat('ID')
            if var_name in self.symbol_table:
                return self.symbol_table[var_name][1]
            self.error()
        elif token[0] == 'NUMBER':
            self.eat('NUMBER')
            return float(token[1]) if '.' in token[1] else int(token[1])
        elif token[0] in ('INT', 'REAL'):
            var_type = token[0]
            self.eat(var_type)
            self.eat('LPAREN')
            var_name = self.current_token[1]
            self.eat('ID')
            self.eat('RPAREN')
            if var_name in self.symbol_table:
                _, value = self.symbol_table[var_name]
                return float(value) if var_type == 'REAL' else int(value)
            self.error()
        else:
            self.error()
    
# Main function
if __name__ == '__main__':
    with open(sys.argv[1], 'r') as file:
        text = file.read()
    lexer = Lexer(text)
    parser = Parser(lexer)
    try:
        parser.prog()
    except Exception as e:
        print("Error")


