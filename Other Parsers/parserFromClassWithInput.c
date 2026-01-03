/* parser.c - A syntax analyzer system for simple arithmetic expressions */

#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>

/* Global Variables */
int charClass;
char lexeme[100];
char nextChar;
int lexLen;
int nextToken;
char inputString[256];  // Stores user input
int currentIndex = 0;   // Tracks current position in input

/* Function Declarations */
void addChar();
void getChar();
void getNonBlank();
int lex();
void expr();
void term();
void factor();
void error(const char *message);

/* Character Classes */
#define LETTER 0
#define DIGIT 1
#define UNKNOWN 99

/* Token Codes */
#define INT_LIT 10
#define IDENT 11
#define ASSIGN_OP 20
#define ADD_OP 21
#define SUB_OP 22
#define MULT_OP 23
#define DIV_OP 24
#define LEFT_PAREN 25
#define RIGHT_PAREN 26
#define EOF_TOKEN -1

/******************************************************/
/* Main Driver */
int main() {
    /* Get user input */
    printf("Enter an arithmetic expression: ");
    fgets(inputString, sizeof(inputString), stdin);

    /* Remove newline character if present */
    size_t len = strlen(inputString);
    if (len > 0 && inputString[len - 1] == '\n') {
        inputString[len - 1] = '\0';
    }

    /* Start processing the input */
    currentIndex = 0;
    getChar();
    lex();
    expr();

    /* Ensure the input is fully consumed */
    if (nextToken != EOF_TOKEN) {
        error("Unexpected tokens after expression");
    }

    printf("Parsing complete!\n");
    return 0;
}

/*****************************************************/
/* Look up operators and parentheses */
int lookup(char ch) {
    switch (ch) {
        case '(':
            addChar();
            nextToken = LEFT_PAREN;
            break;
        case ')':
            addChar();
            nextToken = RIGHT_PAREN;
            break;
        case '+':
            addChar();
            nextToken = ADD_OP;
            break;
        case '-':
            addChar();
            nextToken = SUB_OP;
            break;
        case '*':
            addChar();
            nextToken = MULT_OP;
            break;
        case '/':
            addChar();
            nextToken = DIV_OP;
            break;
        default:
            addChar();
            nextToken = EOF_TOKEN;
            break;
    }
    return nextToken;
}

/*****************************************************/
/* Add nextChar to lexeme */
void addChar() {
    if (lexLen <= 98) {
        lexeme[lexLen++] = nextChar;
        lexeme[lexLen] = '\0';
    } else {
        printf("Error - lexeme is too long\n");
    }
}

/*****************************************************/
/* Get the next character from user input */
void getChar() {
    if (currentIndex < strlen(inputString)) {
        nextChar = inputString[currentIndex++];
        if (isalpha(nextChar))
            charClass = LETTER;
        else if (isdigit(nextChar))
            charClass = DIGIT;
        else
            charClass = UNKNOWN;
    } else {
        charClass = EOF_TOKEN;
        nextChar = '\0';
    }
}

/*****************************************************/
/* Skip whitespace characters */
void getNonBlank() {
    while (isspace(nextChar))
        getChar();
}

/*****************************************************/
/* Lexical Analyzer */
int lex() {
    lexLen = 0;
    getNonBlank();

    switch (charClass) {
        case LETTER:
            addChar();
            getChar();
            while (charClass == LETTER || charClass == DIGIT) {
                addChar();
                getChar();
            }
            nextToken = IDENT;
            break;

        case DIGIT:
            addChar();
            getChar();
            while (charClass == DIGIT) {
                addChar();
                getChar();
            }
            nextToken = INT_LIT;
            break;

        case UNKNOWN:
            lookup(nextChar);
            getChar();
            break;

        case EOF_TOKEN:
            nextToken = EOF_TOKEN;
            strcpy(lexeme, "EOF");
            break;
    }

    printf("Next token is: %d Next lexeme is %s\n", nextToken, lexeme);
    return nextToken;
}

/*****************************************************/
/* expr: Parses <expr> -> <term> {(+ | -) <term>} */
void expr() {
    printf("Enter <expr>\n");
    term();
    while (nextToken == ADD_OP || nextToken == SUB_OP) {
        lex();
        term();
    }
    printf("Exit <expr>\n");
}

/*****************************************************/
/* term: Parses <term> -> <factor> {(* | /) <factor>} */
void term() {
    printf("Enter <term>\n");
    factor();
    while (nextToken == MULT_OP || nextToken == DIV_OP) {
        lex();
        factor();
    }
    printf("Exit <term>\n");
}

/*****************************************************/
/* factor: Parses <factor> -> id | int_constant | ( <expr> ) */
void factor() {
    printf("Enter <factor>\n");

    if (nextToken == IDENT || nextToken == INT_LIT) {
        lex();
    } else if (nextToken == LEFT_PAREN) {
        lex();
        expr();
        if (nextToken == RIGHT_PAREN) {
            lex();
        } else {
            error("factor() - Missing right parenthesis");
        }
    } else {
        error("factor() - Invalid token");
    }

    printf("Exit <factor>\n");
}

/*****************************************************/
/* Error handling function */
void error(const char *message) {
    printf("Syntax Error: %s\n", message);
    exit(1);
}
