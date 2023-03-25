import re
from collections import namedtuple

Token = namedtuple('Token', ['type', 'value'])

class Lexer:
    def __init__(self, filename):
        with open(filename, 'r') as file:
            self.source = file.read()
        self.tokens = []
        self.current_token = None

    def tokenize(self):
        keywords = {'and': 'LOGICAL_AND', 'or': 'LOGICAL_OR'}
        token_specification = [         
            ('INTEGER_LITERAL', r'\d'),  # Integer
            ('FLOATING_POINT_LITERAL', r'\.\d+'),  # Decimal number
            ('EQUALS', r'=='),  # Equals
            ('LESS_THAN_OR_EQUAL_TO', r'<='),  # Less than or equal to operation
            ('GREATER_THAN_OR_EQUAL_TO', r'>='),  # Greater than or equal to operation
            ('LESS_THAN', r'<'),  # Less than operation
            ('GREATER_THAN', r'>'),  # Greater than operation
            ('ASSIGNMENT', r'='),  # Assignment operator
            ('END', r';'),  # Statement terminator
            ('ID', r'[A-Za-z]+'),  # Identifiers
            ('OP', r'[+\-*/%()]'),  # Arithmetic operators
            ('NEWLINE', r'\n'),  # Line endings
            ('SKIP', r'[ \t]+'),  # Skip over spaces and tabs
            ('MISMATCH', r'.'),  # Any other character
        ]
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
        for mo in re.finditer(tok_regex, self.source):
            kind = mo.lastgroup
            value = mo.group()
            if kind == 'INTEGER_LITERAL':
                value = int(value)
            elif kind == 'FLOATING_POINT_LITERAL':
                value = float(value)
            elif kind == 'ID' and value in keywords:
                kind = keywords[value]
            elif kind == 'OP':
                if value == '+':
                    kind = 'ADDITION'
                elif value == '-':
                    kind = 'SUBTRACTION'
                elif value == '*':
                    kind = 'MULTIPLICATION'
                elif value == '/':
                    kind = 'DIVISION'
                elif value == '%':
                    kind = 'MODULO'
                elif value == '(':
                    kind = 'LEFT_PARENTHESIS'
                elif value == ')':
                    kind = 'RIGHT_PARENTHESIS'
            elif kind == 'SKIP':
                continue
            elif kind == 'MISMATCH':
                raise RuntimeError(f'{value!r} unexpected')
            self.tokens.append(Token(kind, value))
        return self.tokens

lexer = Lexer('test.txt')
tokens = lexer.tokenize()
for token in tokens:
    print(token)