import re
import collections
import sys

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

# Compile the master regex pattern
master_pat = re.compile('|'.join([NUM, IDENT, PLUS, MINUS, TIMES, DIVIDE, LPAREN, RPAREN, WS]))

# Tokenizer
Token = collections.namedtuple('Token', ['type', 'value'])

def generate_tokens(text):
    """Scans input text and generates tokens (ignoring spaces)."""
    scanner = master_pat.scanner(text)
    for match in iter(scanner.match, None):
        tok = Token(match.lastgroup, match.group())
        if tok.type != 'WS':  # Skip whitespace
            yield tok

class ExpressionEvaluator:
    """Class to parse and evaluate math expressions."""
    def parse(self, text):
        self.tokens = generate_tokens(text)
        self.tok = None  # Current token
        self.nexttok = None  # Lookahead token
        self._advance()  # Load first token
        self.expr()
        if self.nexttok is not None:
            raise SyntaxError("Unexpected extra tokens")
        #print("Parsing complete!")

    def _advance(self):
        """Moves to the next token."""
        self.tok, self.nexttok = self.nexttok, next(self.tokens, None)

    def _accept(self, toktype):
        """Checks and consumes token if it matches the expected type."""
        if self.nexttok and self.nexttok.type == toktype:
            self._advance()
            return True
        return False

    def _expect(self, toktype):
        """Forces consumption of a specific token or raises an error."""
        if not self._accept(toktype):
            raise SyntaxError(f"Expected {toktype}")

    def expr(self):
        """<expr> ::= <term> { ('+'|'-') <term> }"""
        #print("Enter <expr>")
        self.term()
        while self._accept('PLUS') or self._accept('MINUS'):
            self.term()
        #print("Exit <expr>")

    def term(self):
        """<term> ::= <factor> { ('*'|'/') <factor> }"""
        #print("Enter <term>")
        self.factor()
        while self._accept('TIMES') or self._accept('DIVIDE'):
            self.factor()
        #print("Exit <term>")

    def factor(self):
        """<factor> ::= <IDENT> | <NUM> | '(' <expr> ')'"""
        #print("Enter <factor>")
        if self._accept('IDENT') or self._accept('NUM'):
            pass
        elif self._accept('LPAREN'):
            self.expr()
            self._expect('RPAREN')
        else:
            self.error("factor() - Invalid token")
        #print("Exit <factor>")

    def error(self, location):
        """Error validation function."""
        print(f"Syntax Error in {location}")
        sys.exit(1)

if __name__ == '__main__':
    expr_input = input("Enter the arithmetic expression: ")
    evaluator = ExpressionEvaluator()
    try:
        evaluator.parse(expr_input)
    except SyntaxError as e:
        print("Syntax Error:", e)
