'''
Authors: Carlos Herrera & Hannah Simon
CIS 524 - Comparative Programming Languages
Instructor: Aditi Singh, PhD

Coding assignment - Top-down Recursive-descent Parser using Python

Any questions? Need explanation in the code?
Contact us:
Carlos - c.herreramartinez@vikes.csuohio.edu
Hannah - hgsimon2@gmail.com
'''

''' CFG
The Context Free grammar provided for this python script is the following:

<prog> ::= <let-in-end> { <let-in-end> }
<let-in-end> ::= let <decl-list> in <type> ( <expr> ) end ;
<decl-list> ::= <decl> { <decl> }
<decl> ::= id : <type> = <expr> ;
<type> ::= int | real
<expr> ::= <term> { + <term> | - <term> }
            | if <cond> then <expr> else <expr>
<term> ::= <factor> { * <factor> | / <factor> }
<factor> ::= ( <expr> ) 
            | id 
            | number
            | <type> ( id )
<cond> ::= <oprnd> < <oprnd> 
            | <oprnd> <= <oprnd> 
            | <oprnd> > <oprnd> 
            | <oprnd> >= <oprnd> 
            | <oprnd> == <oprnd> 
            | <oprnd> <> <oprnd>
<oprnd> ::= id | intnum

'''

import sys
import re

'''
This entire section defines the lexical analyzer.
Takes the input from the user (ignoring whitespaces) and matches each character in the input to a token given by the regular expressions below.
'''

# Dictionary that works as the lookup table in the C example.

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

class Lexer:
    """
        Lexical Analyzer Class that breaks the given input (read from the .tiny file) into a sequence of tokens (tokenizes the input)
        It uses multiple functions to tokenize the text.
    """
    def __init__(self, text):
        self.text = text
        self.tokens = self.tokenize()
        self.index = 0
    
    def tokenize(self):
        """ 
        Converts the input into tokens using the items in the token types dictionary. 
        """
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
        
        # print("Final token list:", tokens) # Checking if everything was done successfuly.
        
        return tokens

    def get_next_token(self):
        """
        Gets the next token in the text.
        """
        if self.index < len(self.tokens):
            token = self.tokens[self.index]
            
            self.index += 1
            return token
        return ('EOF', '') # end of sentence/file

class Parser:
    """
        Top Down Recursive Descent Parser Class
        
    """
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        self.symbol_table = {}

    def error(self, expected=None):
        """
        Function to raise an error
        """
        # print(f"Expected token: {expected}")
        # print(f"Current token: {self.current_token}")
        raise SyntaxError(f"Unexpected token {self.current_token}, expected {expected}")

    def consume_token(self, token_type):
        """ Consumes the expected token. """
        #print(f"Consuming: {self.current_token}, expected: {token_type}")
        if self.current_token[0] == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(expected=token_type)
    
    def prog(self):
        """
        Grammar rule:
        <prog> ::= <let-in-end> { <let-in-end> }
        
        Parses a program consisting of multiple let-in-end statements.
        """
        
        #print("Starting to parse the tiny document")
        while self.current_token[0] == 'LET':
            self.let_in_end()
        #print("Parsing worked!")

    def let_in_end(self):
        """
        Grammar rule:
        <let-in-end> ::= let <decl-list> in <type> ( <expr> ) end ;        
        """
        self.consume_token('LET')
        self.decl_list()
        self.consume_token('IN')
        var_type = self.type()
        self.consume_token('LPAREN')
        result = self.expr()
        self.consume_token('RPAREN')
        self.consume_token('END')
        self.consume_token('SEMICOLON')
        
        print(result)

    def decl_list(self):
        """
        Grammar rule:
        <decl-list> ::= <decl> { <decl> }
        """
        self.decl()
        while self.current_token[0] == 'ID':
            self.decl()
            
    def decl(self):
        """
        Grammar rule:
        <decl> ::= id : <type> = <expr> ;
        """
        var_name = self.current_token[1]
        self.consume_token('ID')
        self.consume_token('COLON')

        if self.current_token[0] in ('INT', 'REAL'):
            var_type = self.current_token[0]
            self.consume_token(var_type)
        else:
            self.error()

        self.consume_token('ASSIGN')
        value = self.expr()
        self.consume_token('SEMICOLON')
        self.symbol_table[var_name] = (var_type, value)
    
    def type(self):
        """
        Grammar rule:
        <type> ::= int | real
        """
        if self.current_token[0] in ('INT', 'REAL'):
            type_val = self.current_token[0]
            self.consume_token(type_val)
            return type_val
        else:
            self.error()
    
    def expr(self):
        
        """
        Grammar rule:
        <expr> ::= <term> { + <term> | - <term> } | if <cond> then <expr> else <expr>
        """
        if self.current_token[0] == 'IF':
            return self.if_expr()
        result = self.term()
        while self.current_token[0] in ('PLUS', 'MINUS'):
            op = self.current_token[0]
            self.consume_token(op)
            right = self.term()
            
            if op == 'PLUS':
                result = result + right
            else:
                result = result - right
        return result
    
    def term(self):
        """
        Grammar rule:
        <term> ::= <factor> { * <factor> | / <factor> }
        """
        result = self.factor()
        while self.current_token[0] in ('TIMES', 'DIVIDE'):
            op = self.current_token[0]
            self.consume_token(op)
            right = self.factor()
            result = result * right if op == 'TIMES' else result / right
        return result
    
    def factor(self):
        
        """
        Grammar rule:
        <factor> ::= ( <expr> ) | id | number | <type> ( id )
        """
        token = self.current_token

        # print(f"Current token: {token}")
        
        if token[0] == 'LPAREN':
            self.consume_token('LPAREN')
            result = self.expr()
            self.consume_token('RPAREN')
            return result

        elif token[0] == 'ID':
            var_name = token[1]
            self.consume_token('ID')
            if var_name in self.symbol_table:
                return self.symbol_table[var_name][1]
            self.error()

        elif token[0] == 'NUMBER':
            self.consume_token('NUMBER')
            return float(token[1]) if '.' in token[1] else int(token[1])

        elif token[0] in ('INT', 'REAL'):
            var_type = token[0]
            self.consume_token(var_type)
            self.consume_token('LPAREN')
            result = self.expr()
            self.consume_token('RPAREN')
            
            return float(result) if var_type == 'REAL' else int(result) # Applying type conversion

        else:
            self.error()
            
    def cond(self):
        """
        Grammar rule:
        <cond> ::= <oprnd> < <oprnd> | <oprnd> <= <oprnd> | <oprnd> > <oprnd> | <oprnd> >= <oprnd> | <oprnd> == <oprnd> | <oprnd> <> <oprnd>
        
        Parses conditional expressions (comparisons).
        """
        
        left = self.factor()
        if self.current_token[0] in ('LESS', 'LESSEQ', 'GREATER', 'GREATEREQ', 'EQUAL', 'NOTEQ'):
            op = self.current_token[0]
            self.consume_token(op)
            right = self.factor()
            return self.evaluate_condition(left, op, right)
        self.error()

    def evaluate_condition(self, left, op, right):
        """ Evaluates conditional expressions. """
        match op:
            case 'LESS':
                return left < right
            case 'LESSEQ':
                return left <= right
            case 'GREATER':
                return left > right
            case 'GREATEREQ':
                return left >= right
            case 'EQUAL':
                return left == right
            case 'NOTEQ':
                return left != right
            case _:
                raise ValueError(f"Invalid comparison operator: {op}")

    def if_expr(self):
        """ Parses 'if-then-else' expressions. """
        self.consume_token('IF')
        condition = self.cond()
        self.consume_token('THEN')
        true_expr = self.expr()
        self.consume_token('ELSE')
        false_expr = self.expr()
        return true_expr if condition else false_expr



if __name__ == "__main__":
    # Checking for correct usage
    if len(sys.argv) < 2:
        print("To use this parser, use the following form: parser_2814075.py input_file (e.g., sample.tiny)")
        sys.exit(1)
        
    with open(sys.argv[1], 'r') as file:
        text = file.read()
    
    # Lexical analysis
    lexer = Lexer(text)
    
    #print(f"Lexical analysis done correctly")
    
    # Top down parser
    parser = Parser(lexer)
    try:
        parser.prog()
        #print(f"Parsing done correctly")
    except Exception as e:
        print(f"Error") # Here we could print the error but its not required in the project...

'''Resources:
Python Regex: https://docs.python.org/3/library/re.html 
Simple Recursive Descent Parser from book: https://learning.oreilly.com/library/view/writing-a-simple/9781098171506/ch01.html#id1
Recursive Descent Parser example 1: https://cratecode.com/info/python-recursive-descent-parser
GFG Recursive Descent Parser example 2: https://www.geeksforgeeks.org/recursive-descent-parser/
'''
