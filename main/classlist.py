from typing import NamedTuple
import lexical
import re

delimiters = {
    "whitespace": ["whitespace", "newline"],
    "start_block": ":",
    "start_delim": ["whitespace", "newline", ":", "("],
    "return_delim": ["whitespace", "newline", "("],
    "arith_delim":["whitespace", "newline", "(", "digit_lit", "float_lit"],
    "relation_delim": ["whitespace", "newline", "(", "digit_lit", "float_lit"],
    "equal_delim": ["whitespace", "newline", "(", "digit_lit", "float_lit", "{"],
    "assign_delim": ["whitespace", "newline", "(", "digit_lit", "float_lit", "\""],


    "closeb_delim": ["whitespace", "comma", ".", "=","+","-","^","*","%","//","/", ">", "<", "["],

    "terminator_delim": ["whitespace", "lowercase", "+", "-", "!", "#","(", ")",";"],

    "digit_delim": ["whitespace", "newline", "=","+","-","^","*","%","//","/", ")", "}", "]"],
    "bool_delim": ["whitespace", "newline", ",", "}", ")"],
    "str_delim": ["whitespace", "newline", ",", "}", ")", "+", "]"]
}

class list_tokens():
    def __init__(self, expression):
        self.type = []
        self.value = []
        self.line = []
        self.column = []
        self.error = []

        for token in lexical.tokenize(expression):
            self.type.append(token.type)
            self.value.append(token.value)
            self.line.append(token.line)
            self.column.append(token.column)
            self.error.append(token.error)
            count=0
    
    
    def error_trap(self):
        count=0
        for (type, value, line_num, column, er) in zip(self.type, self.value,self.line,self.column, self.error):
            count+=1
            if (type == "digit_lit" or type == "float_lit") and value[count+1] in delimiters["digit_delim"]:
                pass
            else:
                self.type = "invalid"
                self.error = f'Lexical Error at Line: {line_num} Column: {column}: Maximum character for identifiers is 20'
            
            if type == "id":
                if (value == "break" | value == "continue" | value == "global" | value == "group" | value == "in" | value == "group" | value == "void") \
                and value[count+1] in delimiters["whitespace"]:
                    pass
                else:
                    self.type = "invalid"
                    self.error = f'Lexical Error at Line: {line_num} Column: {column}: Maximum character for identifiers is 20'

                if (value == "boolean" | value == "digit" | value == "float" | value == "read" | value == "embark" | value == "string" | value == "trojan") \
                and value[count+1] == "(":
                    pass
                else:
                    self.type = "invalid"
                    self.error = f'Lexical Error at Line: {line_num} Column: {column}: Maximum character for identifiers is 20'

                if (value == "elif" | value == "for" | value == "if" | value == "pair" | value == "parallel" | value == "while" | value == "route") \
                and value[count+1] == delimiters["start_delim"]:
                    pass
                else:
                    self.type = "invalid"
                    self.error = f'Lexical Error at Line: {line_num} Column: {column}: Maximum character for identifiers is 20'

                if (value == "FALSE" | value == "TRUE") and value[count+1] == delimiters["bool_delim"]:
                    pass
                else:
                    self.type = "invalid"
                    self.error = f'Lexical Error at Line: {line_num} Column: {column}: Maximum character for identifiers is 20'

                if value == "else" and value[count+1] == delimiters["start_block"]:
                    pass
                else:
                    self.type = "invalid"
                    self.error = f'Lexical Error at Line: {line_num} Column: {column}: Maximum character for identifiers is 20'
                    
                if (value == "+" | value == "-" | value == "*" | value == "/" | value =="^" | value == "//" | value == "%") \
                and value[count+1] == delimiters["arith_delim"]:
                    pass
                else:
                    self.type = "invalid"
                    self.error = f'Lexical Error at Line: {line_num} Column: {column}: Maximum character for identifiers is 20'
                    
                if value == "=" and value[count+1] == delimiters["equal_delim"]:
                    pass
                else:
                    self.type = "invalid"
                    self.error = f'Lexical Error at Line: {line_num} Column: {column}: Maximum character for identifiers is 20'
                
