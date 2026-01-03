import sys

# Global variables
input_string = ""  # User input string
current_index = 0  # Current position in the input string
next_token = None  # Current token
next_char = ""  # Current character
char_class = None  # Class of current character
lexeme = ""  # Stores lexeme

# Character classes
LETTER = 0
DIGIT = 1
UNKNOWN = 99

# Token codes
INT_LIT = 10
IDENT = 11
ADD_OP = 21
SUB_OP = 22
MULT_OP = 23
DIV_OP = 24
LEFT_PAREN = 25
RIGHT_PAREN = 26
EOF_TOKEN = -1 # END OF FILE - Really interesting to understand why this is so important

# Side note: the EOF indicates the end of an input. An example for this is when on C storing a character string has always at the end the null empty char '\0'. Really interesting to see that it comes from an actual grammar rule.

# Function Declarations:

def lookup(ch):
    """
    Lookup table of operators that returns the appropiate token based on next operator
    """
    global next_token # To access the next token
    token_dict = {
        '(': LEFT_PAREN,
        ')': RIGHT_PAREN,
        '+': ADD_OP,
        '-': SUB_OP,
        '*': MULT_OP,
        '/': DIV_OP
    }
    next_token = token_dict.get(ch, EOF_TOKEN)
    return next_token


def get_char():
    """
    Reads the next char and determines its class (letter, digit, unk, or EOF).
    """
    global next_char, char_class, current_index # Retrieves next character, its class and index

    if current_index < len(input_string):
        next_char = input_string[current_index]
        current_index += 1

        if next_char.isalpha():
            char_class = LETTER
        elif next_char.isdigit():
            char_class = DIGIT
        else:
            char_class = UNKNOWN
    else:
        char_class = EOF_TOKEN
        next_char = ''  # Empty string represents EOF


def get_non_blank():
    """
    Skips whitespaces.
    """
    while next_char.isspace():
        get_char()


def add_char():
    """
    Adds the current character to the lexeme.
    """
    global lexeme # retrieves current lexeme
    lexeme += next_char


def lex():
    """
    Lexical analyzer to tokenize the input.
    """
    global lexeme, next_token
    lexeme = ""
    get_non_blank()

    if char_class == LETTER:
        #  IDs/Variable Names
        add_char()
        get_char()
        while char_class in (LETTER, DIGIT):
            add_char()
            get_char()
        next_token = IDENT

    elif char_class == DIGIT:
        # Integer
        add_char()
        get_char()
        while char_class == DIGIT:
            add_char()
            get_char()
        next_token = INT_LIT

    elif char_class == UNKNOWN:
        # Parentheses/Operators
        lookup(next_char)
        add_char()
        get_char()

    elif char_class == EOF_TOKEN:
        next_token = EOF_TOKEN
        lexeme = "EOF"

    print(f"Next token is: {next_token} Next lexeme is {lexeme}")
    return next_token


def error(location):
    """
    Error validation function.
    """
    print(f"Syntax Error in {location}")
    sys.exit(1)

# Grammar section of the program
# This was the easiest to translate, it's literally just translating the CFG

def expr():
    """
    
    <expr> ::= <term> { ("+" | "-") <term> }
    
    """
    print("Enter <expr>")
    term()
    while next_token in (ADD_OP, SUB_OP):
        lex()
        term()
    print("Exit <expr>")


def term():
    """
    <term> ::= <factor> { ("*" | "/") <factor> }
    """
    print("Enter <term>")
    factor()
    while next_token in (MULT_OP, DIV_OP):
        lex()
        factor()
    print("Exit <term>")


def factor():
    """
    <factor> ::= <IDENT> | <INT_LIT> | "(" <expr> ")" 
    
    """
    print("Enter <factor>")

    if next_token in (IDENT, INT_LIT):
        lex()
    elif next_token == LEFT_PAREN:
        lex()
        expr()
        if next_token == RIGHT_PAREN:
            lex()
        else:
            error("factor() - Missing right parenthesis")
    else:
        error("factor() - Invalid token")

    print("Exit <factor>")


def main():
    global input_string, current_index

    # Get user input
    input_string = input("Enter the arithmetic expression: ") + " "  # Add space to handle EOF detection
    current_index = 0

    # Lexical analysis
    get_char()
    lex()

    # Parser
    expr()

    # Handling EOF errors
    if next_token != EOF_TOKEN:
        error("main() - Unexpected tokens after expression")

    print("Parsing complete!")

if __name__ == "__main__":
    main()
