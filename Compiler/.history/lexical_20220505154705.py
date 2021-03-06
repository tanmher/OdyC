from ast import operator
from typing import NamedTuple
import re
import string

'''This is a multiline comment.'''

class Token(NamedTuple):
    type: str
    value: str
    line: int
    column: int
    error: str


def tokenize(code):
    L_type = []
    L_specification = []
    L_value = []
    L_line = []
    L_column = []
    L_error = []

    keywords = {"boolean", "boot","break","codex", "continue", "digit","if", "elf", "else",
                "embark", "FALSE", "fixed", "float", "for", "global", "group", "if", 
                "in", "pair", "parallel", "read","remove", "return", "route","skip", "string",
                "TROJAN", "TRUE", "while", "HALT"
    }

    reserved_symbols = ['+', '-', '*', '^', '/', '//', '%', '=','+=', '-=', '*=', '^=', '/=', '//=', '%=', '==', '!=', '>', '<', '>=', '<=','&&',
                        '||', '!', '++', '--', '(', ')', '#', '[', ']', ':', ',', '{', '}', ';', '.'
    ]
    operators = {
        'arithmetic': ['+-', '*', '^', '/', '//', '%' ],
        'assignment':[ '=','==', '+=', '-=', '*=', '^=', '/=', '//=', '%=' ],
        'relational': [ '==', '!=', '>', '<', '>=', '<=' ],
        'logical': [ '&&', '||', '!' ],
        'unarry': [ '++', '--' ]
    }
    

    token_specification = [
        ('digits',      r'\d+(\.\d*)?'),                    # Integer or decimal number
        ('id',          r'[A-Za-z0-9]+'),                   # Identifiers
        ('string_lit',  r'\"[ -~][ -~]+\"'),                # String Literals
        ('operators',    r'(==|\+=|-=|\*=|\^=|/=|%=|!=|>=|<=|&&|\|\||!|--|\+\+|>|<|=|\+|-|\*|\^|//|/|%)'),   # Operators
        ('symbols',     r'[;\.:,]'),                        # Symbols
        ('close',       r'[\(\)\[\]\{\}]'),                 # Brackets, Parenthesis
        ('newline',     r'\n'),                             # New line
        ('whitespace',  r'[ \t]+'),                         # Skip over spaces and tabs
        ('comment',      r'#[ -~]*'),                       # Comment
        ('mismatch',    r'.'),                              # Any other character
    ]
    
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    line_num = 1
    count = 0
    list_id = {}
    line_start = 0
    cb_count = 0
    indent_count = []
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        error = ''
        value = mo.group()
        column = mo.start() - line_start
        L_specification.append(kind)

        if kind == 'functions':
            kind = value
            indent_count.append(0)
        elif kind == 'digits':
            if len(value) <= 10 and len(value) >= 1 and '.' not in value:
                kind = 'digit_lit'
                value = int(value)
            elif len(value) <= 15 and len(value) >= 3 and '.' in value:
                kind = 'float_lit'
                value = float(value)
            else:
                error = f'Lexical Error at Line: {line_num}  Column: {column} : Integer/Decimal is out of bounds'
                kind = 'invalid'
        elif kind == 'id':
            if len(value) > 20:
                error = f'Lexical Error at Line: {line_num} Column: {column}: Maximum character for identifiers is 20'
                kind = 'invalid'
            elif value in keywords:
                if value == "TRUE" or value == "FALSE":
                    kind = 'bool_lit'
                else:
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
        elif kind == 'operators' and value in reserved_symbols:
            kind = value
        elif kind == "string_lit":
            value = value.replace('\\n', '\n')
            value = value.replace("\\t", "\t")
            value = value.replace("\"", '"')
            value = value.replace("\\", '\ ')
        elif kind == 'close' and value in reserved_symbols:
            kind = value
        elif kind == "symbols":
            kind = value
        elif kind == 'newline':
            line_start = mo.end()
            line_num += 1
            kind = 'newline'
            value = '\n'
        elif kind == 'whitespace':

            tab_count = 0
            if '\t' in value:
                tab_count = value.count('\t')
            indent_count.append(tab_count)
            
            value = ' '
        elif kind == 'mismatch':
            error = f'Lexical Error at Line: {line_num} Column: {column}: Unexpected value'
            kind = 'invalid'

        L_type.append(kind)
        L_value.append(value)
        L_line.append(line_num)
        L_column.append(column)
        L_error.append(error)
    

    delimiters = {
        "whitespace": [" ", '\t', "\n"],
        "start_block": ":",
        "start_delim": [" ", '\t', "\n", "("],
        "return_delim": [" ", '\t', "\n", "("],
        "arith_delim":[" ", '\t', "\n", "(", "digit_lit", "float_lit"], 
        "relation_delim": [" ", '\t', "\n", "(", "digit_lit", "float_lit"], 
        "log_delim": [" ", '\t', "\n", "(", "digit_lit", "float_lit",],
        "equal_delim": [" ", '\t', "\n", "(", "digit_lit", "float_lit", "[", "{", "\""],
        "assign_delim": [" ", '\t', "\n", "(", "digit_lit", "float_lit"],  
        "unary_delim": [" ", '\t', "\n", ";", "(", ")", "digit_lit", "float_lit", "\""], 

        "comma_delim": [" ", '\t', "\n", "+", "-" , "{", "!", "[", ],

        "openp_delim": [" ", "~", "\"", "+", "-", "++", "--", "(", ")", "!" , "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", 
                        "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "4", "8", "6"],
        "closep_delim": [" ", "\t", "\n", ";", ",", ".", "=","+","-","^","*","%","//","/", ">", "<", ")", ":", "]"],
        
        "openb_delim": [" ", "+", "-", "(", "]", "[", "\"", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", 
                        "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "4", "8", "6"], 
        "closeb_delim": [" ", "\t", "\n",";",",", ".", "=","+","-","^","*","%","//","/", ">", "<", "[", "]", ")"],

        "openc_delim": [" ", "\t", "\n", "\"", "}"],
        "closec_delim": [" ", "\t", "\n", "\"", ";","a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", 
                        "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "4", "8", "6" ],

        "id_delim": [" ", '\t', "\n", ";", ",", ".", "=","+","-","^","*","%","//","/", ">", "<", "[", "]", "(", ")", "!","++","--","==", '+=', '-=', '*=', '^=', '/=', '//=', '%=', '!=', '>=', '<=','&&','|','||', ":"],
        
        "terminator_delim": [" ", '\t', "\n", "HALT"],

        "digit_delim": [" ", '\t', "\n", ";", ",", "=","+","-","^","*","%","//","/", ")", "}", "]", ":", "==", "+=", "-=" ,"*=", "^=", "%=", "!=", ">", "<", ">=", "<=", "&", "&&", "|", "||", "!", "--", "++"],
        "float_delim": [" ", '\t', "\n", ";", "=","+","-","^","*","%","//","/", ")", "}", ":", ",",  "==", "+=", "-=" ,"*=", "^=", "%=", "!=", ">", "<", ">=", "<=", "&", "&&", "|", "||", "!", "--", "++"],
        "bool_delim": [" ", '\t', "\n",";", ",", "}", ")",  "==", "+=", "-=" ,"*=", "^=", "%=", "!=", ">", "<", ">=", "<=", "&", "&&", "|", "||", "!", "--", "++"],
        "string_delim": [" ", '\t', "\n", ";", ",", "}", ")", "+", "]", "==", "+=", "-=" ,"*=", "^=", "%=", "!=", ">", "<", ">=", "<=", "&", "&&", "|", "||", "!", "--", "++"],
        "ascii": string.printable
    }

    count = 0
    temp_type = L_type
    temp_error = L_error
    for (type, value, line_num, column) in zip(L_type, L_value, L_line, L_column):
        
        if (count+1) == len(L_value)-1:
            pass
        elif type in list_id and L_value[count+1] in delimiters["id_delim"]:
            pass
        elif type == "digit_lit"  and (L_value[count+1] in delimiters["digit_delim"] or L_value[count+1] == "\n"):
            pass
        elif type == "float_lit" and (L_value[count+1] in delimiters["float_delim"] or L_value[count+1] == "\n"):
            pass
        elif type == "bool_lit" and L_value[count+1] in delimiters["bool_delim"]:
                pass
        elif type == "comment" and (L_value[count+1] in delimiters["whitespace"]):
            pass
        elif type == "multi_comment" and (L_value[count+1] in delimiters["whitespace"] or L_value[count+1] in keywords):
            pass
        elif type in keywords:
            if (value == "break" or value == "continue" or value == "skip") \
            and (L_value[count+1] == ";"):
                pass
            elif (value == "boolean" or value == "digit" or value == "float" or value == "read" or value == "embark" or value == "string" ) \
            and L_value[count+1] == "(":
                pass
            elif (value == "elf" or value == "for" or value == "if" or value == "pair" or value == "parallel" or value == "while" or value == "route") \
            and L_value[count+1] in delimiters["start_delim"]:
                pass
            elif (value == "else" or value == "TROJAN") and L_value[count+1] in delimiters["start_block"]:
                pass
            elif (value == "codex" or value == "fixed" or value == "global" or value == "group" or value == "in" or value == "void") and L_value[count+1] == " ":
                pass
            elif value == "HALT" and L_value[count+1] in delimiters["whitespace"]:
                pass
            elif value == "return" and L_value[count+1] in delimiters["start_delim"]:
                pass
            else:
                temp_type[count] = "invalid"
                L_type = temp_type
                temp_error[count] = f'Lexical Error at Line: {line_num} Column: {column}: Found an unexpected value after this token'
                L_error = temp_error

        elif value in reserved_symbols:
            
            if (value == "+" or value == "-" or value == "*" or value == "^" or value == "/" or value == "%" or value == "//") \
            and (L_value[count+1] in delimiters["arith_delim"] or L_type[count+1] in list_id or L_type[count+1] == "digit_lit" or L_type[count+1] == "float_lit"):
                pass
            elif (value == "+=" or value == "-=" or value == "*=" or value == "^=" or value == "/=" or value == "%=") \
            and (L_value[count+1] in delimiters["assign_delim"] or L_type[count+1] in list_id or L_type[count+1] == "digit_lit" or L_type[count+1] == "float_lit"):
                pass
            elif (value == "==" or  value == "!=" or value == ">" or value == "<" or value == ">=" or value == "<=") \
                and (L_value[count+1] in delimiters["relation_delim"] or L_type[count+1] in list_id or L_type[count+1] == "digit_lit" or L_type[count+1] == "float_lit"):
                pass
            elif (value =='&&' or value =='||' or value == '!') \
            and (L_value[count+1] in delimiters["log_delim"] or L_type[count+1] in list_id or L_type[count+1] == "digit_lit" or L_type[count+1] == "float_lit" or L_type[count+1] == "bool_lit"):
                pass
            elif (value == "++" or value == "--") \
            and (L_value[count+1] in delimiters["unary_delim"] or L_type[count+1] in list_id or L_type[count+1] == "digit_lit" or L_type[count+1] == "float_lit"):
                pass
            elif (value == "=" ) and (L_value[count+1] in delimiters["equal_delim"] or L_type[count+1] in list_id or L_type[count+1] == "digit_lit" or L_type[count+1] == "float_lit"):
                pass
            elif value == "[" and (L_value[count+1] in delimiters["openb_delim"] or L_type[count+1] == "digit_lit" or L_type[count+1] == "float_lit" or L_type[count+1] == "string_lit" or  L_type[count+1] in list_id):
                pass
            elif value == "]" and L_value[count+1] in delimiters["closeb_delim"]:
                pass
            elif value == "(" and (L_value[count+1] in delimiters["openp_delim"] or L_type[count+1] == "digit_lit" or L_type[count+1] == "float_lit" or L_type[count+1] == "string_lit" or  L_type[count+1] in list_id):
                pass
            elif value == ")" and L_value[count+1] in delimiters["closep_delim"]:
                pass
            elif value == "{" and (L_value[count+1] in delimiters["openc_delim"] or L_type[count+1] == "digit_lit" or L_type[count+1] == "float_lit" or L_type[count+1] == "string_lit" or  L_type[count+1] in list_id):
                pass
            elif value == "}" and L_value[count+1] in delimiters["closec_delim"]:
                pass
            elif value == "\'" and L_value[count+1] in delimiters["closec_delim"]:
                pass
            elif value == "\"" and (L_value[count+1] in delimiters["ascii"] or L_value[count+1] in delimiters["whitespace"] or L_value[count+1] == ":"):
                pass
            elif type == ":" and (L_value[count+1] == '\n' or L_value[count+1] == ' ' or L_value[count+1] == '\t'):
                pass
            elif value == "," and L_value[count+1] in delimiters["comma_delim"]:
                pass
            elif value == "!" and (L_value[count] in delimiters["log_delim"] or L_type[count+1] in list_id):
                pass
            elif value == "." and (L_type[count+1] in list_id):
                pass
            elif value == ";" and (L_type[count+1] in list_id or L_value[count+1] in delimiters["terminator_delim"] or L_value[count+1] in keywords):
                pass
            else:
                temp_type[count] = "invalid"
                L_type = temp_type
                temp_error[count] = f'Lexical Error at Line: {line_num} Column: {column}: Found an unexpected value after this token'
                L_error = temp_error

        elif type == "string_lit" and L_value[count+1] in delimiters["string_delim"]:
            pass
        elif value == " ":
            pass

        elif type == "invalid":
            pass
        elif value == "\n" or value == "\t" or value == " ":
            pass
        else:
            temp_type[count] = "invalid"
            L_type = temp_type
            temp_error[count] = f'Lexical Error at Line: {line_num} Column: {column}: Unexpected value'
            L_error = temp_error

        
        yield Token(L_type[count], L_value[count], L_line[count], L_column[count], L_error[count])
        
        count+=1

    