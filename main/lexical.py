from typing import NamedTuple
import re

class Token(NamedTuple):
    type: str
    value: str
    line: int
    column: int
    error: str

def tokenize(code):
    keywords = {"boolean", "boot","break", "continue", "digit","if", "elif", "else",
                "embark", "FALSE", "float", "for", "global", "group", "if", "index",
                "in","pair","parallel","read","remove","return", "skip","string",
                "trojan", "TRUE","void", "while"
    }

    # reserved_symbols = {'+', '-', '*', '^', '/', '//', '%', '=', '+=', '-=', '*=', '^=', '/=', '//=', '%=', '=', '!=', '>', '<', '>=', '<=','&&',
    #                     '||', '!', '++', '--', '(', ')', '#', '[', ']', ':'
    # }

    token_specification = [
        ('functions',   r'[A-Za-z0-9]+\(\)'),       # Functions
        ('digits',      r'\d+(\.\d*)?'),            # Integer or decimal number
        ('id',          r'[A-Za-z0-9]+'),           # Identifiers
        ('string',      r'\"[ -~][ -~]+\"'),        # String Literals
        ('operator',    r'[+\-*^/%&\|=\(\)]+'),     # Operators
        ('start',       r':+(\n\t+)+'),             # Start of code block 
        ('newline',     r'\n'),                     # New line
        ('whitespace',  r'[ \t]+'),                 # Skip over spaces and tabs
        ('mismatch',    r'.'),                      # Any other character
    ]
    
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    line_num = 1
    count = 0
    list_id = {}
    line_start = 0
    error = ''
    cb_count = 0
    newline_count = 0
    indent_count = []
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start
        if kind == 'functions':
            kind = value
            indent_count.append(0) #FOR NOW TO SOLVE ERROR IN USER DEFINED FUNCTIONS
        elif kind == 'digits':
            if len(value) <= 9 and len(value) >= 1 and '.' not in value:
                kind = 'int_lit'
                value = int(value)
            elif len(value) <= 13 and len(value) >= 3 and '.' in value:
                kind = 'dec_lit'
                value = float(value)
            else:
                error = f'Lexical Error at Line: {line_num}  Column: {column} : Integer/Decimal is out of bounds'
                kind = 'invalid'
        elif kind == 'id':
            if len(value) > 20:
                error = f'Lexical Error at Line: {line_num} Column: {column}: Maximum character for identifiers is 20'
                kind = 'invalid'
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
        elif kind == 'operator':
            if len(value) > 2:
                error = f'Lexical Error at Line: {line_num} Column: {column}: Invalid operator'
                kind = 'invalid'
            else:
                kind = value
        elif kind == 'start':
            cb_count += 1
            newline_count += 1
            tab_count = value.count('\t')
            indent_count.append(tab_count)
            print(indent_count)
            print(line_num)
            print(tab_count)
            if '\n' in value and '\t' in value and tab_count == indent_count[line_num-1]+1:
                kind = ':'
                value = ':'
                line_num += 1
            else:
                error = f'Lexical Error at Line: {line_num} Column: {column}: Block must be in newline and indented'
                kind = 'invalid'
                value = ':'
        elif kind == 'newline':
            line_start = mo.end()
            line_num += 1
            continue
        elif kind == 'whitespace':
            if '\t' in value:
                tab_count = value.count('\t')
                indent_count.append(tab_count)
            value = 'whitespace'
        elif kind == 'mismatch':
            error = f'Lexical Error at Line: {line_num} Column: {column}: Unexpected value'
            kind = 'invalid'
            # raise RuntimeError(f'{value} unexpected on line {line_num}')

        yield Token(kind, value, line_num, column, error)