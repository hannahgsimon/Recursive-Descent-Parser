# Programming Language Parser

## Overview
This repository contains a top-down recursive parser and lexical analyzer designed to process a defined context-free grammar (CFG). The project explores various implementations in both C and Python, including versions utilizing regular expressions for lexical analysis.

## Setup & Usage
1. Ensure the following prerequisites are installed:
    - For the C implementation: GCC or any compatible C compiler.
    - For the Python implementation: Python 3.x.
2. Clone the repository:
    ```bash
    git clone https://github.com/Krlosh85/CIS524-Parser
    cd CIS524-Parser
    ```
3. Compile and run the C version:
    ```bash
    gcc parser.c -o parser
    ./parser sample1.tiny
    ```
4. Run the Python version:
    ```bash
    python3 parser.py sample1.tiny
    ```
    
## Reference CFG
The initial implementation uses a simpler context-free grammar (CFG) as a foundational starting point. This CFG served as the basis for the parser's development before evolving to support more complex constructs like ```let-in-end``` declarations, type annotations, and conditional expressions in the main grammar. The following is the simpler CFG initially employed:

```bash
<expr>   ::= <term> { ("+" | "-") <term> }
<term>   ::= <factor> { ("*" | "/") <factor> }
<factor> ::= <IDENT> | <INT_LIT> | "(" <expr> ")"
<IDENT>  ::= <LETTER> { <LETTER> | <DIGIT> }
<INT_LIT> ::= <DIGIT> { <DIGIT> }
<LETTER> ::= "a" - "Z"
<DIGIT>  ::= "0" - "9"
```

## Defined CPG for Parsing
We developed a top down recursive parser and lexical analyzer for the following CFG:

```bash
<prog> ::= <let-in-end> { <let-in-end> }
<let-in-end> ::= let <decl-list> in <type> ( <expr> ) end ;
<decl-list> ::= <decl> { <decl> }
<decl> ::= id : <type> = <expr> ;
<type> ::= int | real
<expr> ::= <term> { + <term> | - <term> } |
if <cond> then <expr> else <expr>
<term> ::= <factor> { * <factor> | / <factor> }
<factor> ::= ( <expr> ) | id | number | <type> ( id )
<cond> ::= <oprnd> < <oprnd> |
<oprnd> <= <oprnd> |
<oprnd> > <oprnd> |
<oprnd> >= <oprnd> |
<oprnd> == <oprnd> |
<oprnd> <> <oprnd>
<oprnd> ::= id | intnum
```

## Implementations
We developed multiple versions of the parser and lexical analyzer:
1. Top-Down Parser with Lexical Analyzer in C
2. Top-Down Parser with Lexical Analyzer in C with user input (translated version)
3. Top-Down Parser with Lexical Analyzer in Python with user input (translated version)
4. Top-Down Parser with Lexical Analyzer using REGEX (based on textbook example) in Python
5. Top-Down Parser with Lexical Analyzer using REGEX (class version) in Python

## References
[1] Python Regex: https://docs.python.org/3/library/re.html  
[2] Simple Recursive Descent Parser from book: https://learning.oreilly.com/library/view/writing-a-simple/9781098171506/ch01.html#id1  
[3] Recursive Descent Parser example 1: https://cratecode.com/info/python-recursive-descent-parser  
[4] GFG Recursive Descent Parser example 2: https://www.geeksforgeeks.org/recursive-descent-parser/

## Authors
This project was collaboratively developed by Carlos Herrera and Hannah G. Simon.
