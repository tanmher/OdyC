from typing import NamedTuple
import re

class Token(NamedTuple):
    type: str
    value: str
    line: int
    column: int
    error: list

def tokenize(code):
    keywords = {"boolean", "boot","break", "continue", "digit","if", "elif", "else",
                "embark", "FALSE", "float", "for", "global", "group", "if", "index",
                "in","pair","parallel","read","remove","return", "skip","string",
                "trojan", "TRUE","void", "while"
    }

    reserved_symbols = {'+','-', '*', '^', '/', '//', '%', '=', '+=', '-=', '*=', '^=', '/=', '//=', '%=', '=', '!=', '>', '<', '>=', '<=','&&',
                        '||', '!', '++', '--', '(', ')', '#', '[', ']', ':'
    }

    token_specification = [
        ('functions',   r'[A-Za-z0-9]+\(\)'),       # Functions
        ('digits',      r'\d+(\.\d*)?'),            # Integer or decimal number
        ('id',          r'[A-Za-z0-9]+'),           # Identifiers
        ('string',      r'\"[ -~][ -~]+\"'),        # String
        ('newline',     r'\n'),                     # Line endings
        ('whitespace',  r'[ \t]+'),                 # Skip over spaces and tabs
        ('mismatch',    r'.'),                      # Any other character
    ]
    
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    line_num = 1
    line_start = 0
    count = 0
    list_id = {}
    error = []
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        line_num = mo.start()
        column = mo.start() - line_start
        if kind == 'functions':
            kind = value
        elif kind == 'digits':
            if len(value) <= 9 and len(value) >= 1 and '.' not in value:
                kind = 'int_lit'
                value = int(value)
            elif len(value) <= 13 and len(value) >= 3 and '.' in value:
                kind = 'dec_lit'
                value = float(value)
            else:
                #error.append("Lexical Error: Integer/Decimal is out of bounds")
                pass
        elif kind == 'int_lit':
            value = int(value)
        elif kind == 'deci_lit':
            value = float(value)
        elif kind == 'id':
            if len(value) > 20:
                #error.append("Lexical Error: Maximum character for identifiers is 20")
                pass
            elif value in keywords:
                kind = value
            elif value in list_id.values():
                for key, val in list_id.items():
                    if val == value:
                        id = key
                kind = id
            else:
                count+=1
                kind = 'id' + str(count)
                list_id[kind] = value 
        elif value in reserved_symbols:
            kind = value
        elif kind == 'newline':
            line_start = mo.end()
            line_num += 1
            continue
        elif kind == 'whitespace':
            kind == 'whitespace'
        elif kind == 'mismatch':
            raise RuntimeError(f'{value!r} unexpected on line {line_num}')
        yield Token(kind, value, line_num, column, error)