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
    'NUMBER': r'-?\d+(\.\d+)?',  # Supports negative numbers
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
        """ Converts the input string into tokens. """
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
        """ Retrieves the next token in the stream. """
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

    def error(self, expected=None):
        raise SyntaxError(f"Unexpected token {self.current_token}, expected {expected}")

    def eat(self, token_type):
        """ Matches and consumes the expected token. """
        print(f"Consuming token: {self.current_token}")  # Debugging line
        if self.current_token[0] == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(expected=token_type)
    
    # <prog> ::= <let-in-end> { <let-in-end> }
    def prog(self):
        """ Parses a program consisting of multiple let-in-end statements. """
        print("Starting Parsing...")  # Debugging line
        while self.current_token[0] == 'LET':
            self.let_in_end()
        print("Parsing Completed.")  # Debugging line

    # <let-in-end> ::= let <decl-list> in <type> ( <expr> ) end ;
    def let_in_end(self):
        """ Parses 'let-in-end' blocks. """
        self.eat('LET')
        self.decl_list()
        self.eat('IN')

        print("Symbol Table:", self.symbol_table)  # Debugging line

        var_type = self.type()
        self.eat('LPAREN')
        result = self.expr()
        self.eat('RPAREN')
        self.eat('END')
        self.eat('SEMICOLON')
        print("Final result:", result)  # Debugging line

    # <decl-list> ::= <decl> { <decl> }
    def decl_list(self):
        """ Parses a list of variable declarations. """
        self.decl()
        while self.current_token[0] == 'ID':
            self.decl()
            
    # <decl> ::= id : <type> = <expr> ;
    def decl(self):
        """ Parses variable declarations and stores them in the symbol table. """
        var_name = self.current_token[1]
        self.eat('ID')
        self.eat('COLON')

        if self.current_token[0] in ('INT', 'REAL'):
            var_type = self.current_token[0]
            self.eat(var_type)
        else:
            self.error()

        self.eat('ASSIGN')
        value = self.expr()
        self.eat('SEMICOLON')
        self.symbol_table[var_name] = (var_type, value)

    # <type> ::= int | real
    def type(self):
        """ Parses type declarations. """
        if self.current_token[0] in ('INT', 'REAL'):
            type_val = self.current_token[0]
            self.eat(type_val)
            return type_val
        else:
            self.error()
    
    # <expr> ::= <term> { + <term> | - <term> } | if <cond> then <expr> else <expr>
    def expr(self):
        """ Parses expressions including arithmetic and conditionals. """
        if self.current_token[0] == 'IF':
            return self.if_expr()
        result = self.term()
        while self.current_token[0] in ('PLUS', 'MINUS'):
            op = self.current_token[0]
            self.eat(op)
            right = self.term()
            result = result + right if op == 'PLUS' else result - right
        return result
    
    # <term> ::= <factor> { * <factor> | / <factor> }
    def term(self):
        """ Parses multiplication and division operations. """
        result = self.factor()
        while self.current_token[0] in ('TIMES', 'DIVIDE'):
            op = self.current_token[0]
            self.eat(op)
            right = self.factor()
            result = result * right if op == 'TIMES' else result / right
        return result
    
    # <factor> ::= ( <expr> ) | id | number | <type> ( id )
    def factor(self):
        """ Parses numbers, identifiers, type casting, or parenthesized expressions. """
        token = self.current_token

        if token[0] == 'LPAREN':  # Parentheses handling
            self.eat('LPAREN')
            result = self.expr()
            self.eat('RPAREN')
            return result

        elif token[0] == 'ID':  # Variable lookup
            var_name = token[1]
            self.eat('ID')
            if var_name in self.symbol_table:
                return self.symbol_table[var_name][1]
            self.error()

        elif token[0] == 'NUMBER':  # Number parsing
            self.eat('NUMBER')
            return float(token[1]) if '.' in token[1] else int(token[1])

        elif token[0] in ('INT', 'REAL'):  # Type casting (real ( expr ) or int ( expr ))
            var_type = token[0]
            self.eat(var_type)
            self.eat('LPAREN')
            result = self.expr()  # Now allows any expression inside type casting
            self.eat('RPAREN')
            
            # Apply type conversion
            return float(result) if var_type == 'REAL' else int(result)

        else:
            self.error()


    # <cond> ::= <oprnd> < <oprnd> | ... (all comparisons)
    def cond(self):
        """ Parses conditional expressions (comparisons). """
        left = self.factor()
        if self.current_token[0] in ('LESS', 'LESSEQ', 'GREATER', 'GREATEREQ', 'EQUAL', 'NOTEQ'):
            op = self.current_token[0]
            self.eat(op)
            right = self.factor()
            return self.evaluate_condition(left, op, right)
        self.error()

    def evaluate_condition(self, left, op, right):
        """ Evaluates conditional expressions. """
        return {
            'LESS': left < right,
            'LESSEQ': left <= right,
            'GREATER': left > right,
            'GREATEREQ': left >= right,
            'EQUAL': left == right,
            'NOTEQ': left != right
        }[op]

    def if_expr(self):
        """ Parses 'if-then-else' expressions. """
        self.eat('IF')
        condition = self.cond()
        self.eat('THEN')
        true_expr = self.expr()
        self.eat('ELSE')
        false_expr = self.expr()
        return true_expr if condition else false_expr

# Main function
if __name__ == '__main__':
    with open(sys.argv[1], 'r') as file:
        text = file.read()
    lexer = Lexer(text)
    
    print("Tokens:", lexer.tokens)  # Debugging line

    parser = Parser(lexer)
    try:
        parser.prog()
    except Exception as e:
        print(f"Error: {e}")
