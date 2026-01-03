import re
import collections

'''
This entire section defines the lexical analyzer.

Takes the input from the user (ignoring whitespaces) and matches each ´character´ in the input to a token given by the regular expressions below.
Then stores the tokens in a named tuple of tokens to use it as iterable object later (this entirely based on the book example)
'''

# Token specification
NUM    = r'(?P<NUM>\d+)'
IDENT  = r'(?P<IDENT>[a-zA-Z][a-zA-Z0-9]*)'
PLUS   = r'(?P<PLUS>\+)'
MINUS  = r'(?P<MINUS>-)'
TIMES  = r'(?P<TIMES>\*)'
DIVIDE = r'(?P<DIVIDE>/)'
LPAREN = r'(?P<LPAREN>\()'
RPAREN = r'(?P<RPAREN>\))'
WS     = r'(?P<WS>\s+)'

master_pat = re.compile('|'.join([NUM, IDENT, PLUS, MINUS, TIMES, DIVIDE, LPAREN, RPAREN, WS]))

# Tokenizer
Token = collections.namedtuple('Token', ['type', 'value'])

def generate_tokens(text):
    scanner = master_pat.scanner(text)
    for match in iter(scanner.match, None):
        tok = Token(match.lastgroup, match.group())
        if tok.type != 'WS':  # Skip whitespace
            yield tok

'''
Class used to build the Top Down Recursive Descent Parser
Each function/method inside the class represents one of the CF grammar rules

Implemented as well the evaluator on this class, by adding the result variable.
This variable computes the arithmetic instruction given by the user.
'''
class ExpressionEvaluator(object):
    def parse(self, text):
        self.tokens = generate_tokens(text)
        self.tok = None  # Last token
        self.nexttok = None  # Next token
        self._advance()  # Load first lookahead token
        return self.expr()

    def _advance(self):
        '''Moves to the next token.'''
        self.tok, self.nexttok = self.nexttok, next(self.tokens, None)

    def _accept(self, toktype):
        '''
        Checks and consumes token if it matches the expected type.
        '''
        if self.nexttok and self.nexttok.type == toktype:
            self._advance()
            return True
        return False

    def _expect(self, toktype):
        '''
        Validates if the current token is the correct type.
        '''
        if not self._accept(toktype):
            raise SyntaxError(f'Expected {toktype}')

    def expr(self):
        '''
        <expr> ::= <term> { ('+'|'-') <term> }
        '''
        result = self.term()
        while self._accept('PLUS') or self._accept('MINUS'):
            op = self.tok.type
            right = self.term()
            result = result + right if op == 'PLUS' else result - right
        return result

    def term(self):
        '''
        <term> ::= <factor> { ('*'|'/') <factor> }
        '''
        result = self.factor()
        while self._accept('TIMES') or self._accept('DIVIDE'):
            op = self.tok.type
            right = self.factor()
            result = result * right if op == 'TIMES' else result / right
        return result

    def factor(self):
        '''
        <factor> ::= <IDENT> | <NUM> | '(' <expr> ')
        '''
        if self._accept('IDENT'):
            return self.tok.value
        elif self._accept('NUM'):
            return int(self.tok.value)
        elif self._accept('LPAREN'):
            result = self.expr()
            self._expect('RPAREN')
            return result
        else:
            raise SyntaxError('Expected IDENT, NUMBER, or LPAREN')

'''

'''
class ExpressionTreeBuilder(ExpressionEvaluator):
    def expr(self):
        tree = self.term()
        while self._accept('PLUS') or self._accept('MINUS'):
            op = self.tok.type
            right = self.term()
            tree = (op, tree, right)
        return tree

    def term(self):
        tree = self.factor()
        while self._accept('TIMES') or self._accept('DIVIDE'):
            op = self.tok.type
            right = self.factor()
            tree = (op, tree, right)
        return tree

    def factor(self):
        if self._accept('IDENT'):
            return self.tok.value
        elif self._accept('NUM'):
            return int(self.tok.value)
        elif self._accept('LPAREN'):
            tree = self.expr()
            self._expect('RPAREN')
            return tree
        else:
            raise SyntaxError('Expected IDENT, NUMBER, or LPAREN')

if __name__ == '__main__':
    expr_input = input("Enter an arithmetic expression: ")
    evaluator = ExpressionEvaluator()
    tree_builder = ExpressionTreeBuilder()
    try:
        result = evaluator.parse(expr_input)
        parse_tree = tree_builder.parse(expr_input)
        print("Result:", result)
        print("Parse Tree:", parse_tree)
    except SyntaxError as e:
        print("Syntax Error:", e)