from typing import NamedTuple
import lexical
import re

delimiters = {
    "whitespace": [" ", '\t', "\n"],
    "start_block": ":",
    "start_delim": [" ", '\t', "\n", ":", "("],
    "return_delim": [" ", '\t', "\n", "("],
    "arith_delim":[" ", '\t', "\n", "(", "digit_lit", "float_lit"],
    "relation_delim": [" ", '\t', "\n", "(", "digit_lit", "float_lit"],
    "equal_delim": [" ", '\t', "\n", "(", "digit_lit", "float_lit", "{"],
    "assign_delim": [" ", '\t', "\n", "(", "digit_lit", "float_lit", "\""],

    "closeb_delim": [" ", '\t', "\n", "comma", ".", "=","+","-","^","*","%","//","/", ">", "<", "["],

    "terminator_delim": [" ", '\t', "\n", "lowercase", "+", "-", "!", "#","(", ")",";"],

    "digit_delim": [" ", '\t', "\n", "=","+","-","^","*","%","//","/", ")", "}", "]"],
    "bool_delim": [" ", '\t', "\n", ",", "}", ")"],
    "str_delim": [" ", '\t', "\n", ",", "}", ")", "+", "]"]
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
    
    
    def error_trap(self):
        count = 0
        for (type, value, line_num, column, er) in zip(self.type, self.value, self.line, self.column, self.error):
            count+=1
            if (type == "digit_lit" or type == "float_lit") and str(value[count+1]) in delimiters["digit_delim"]:
                pass
            else:
                self.type = "invalid"
                self.error =  f'Lexical Error at Line: {line_num} Column: {column}: Unexpected value'
            
            if type == "id":
                if (value == "break" | value == "continue" | value == "global" | value == "group" | value == "in" | value == "group" | value == "void") \
                and value[count+1] in delimiters["whitespace"]:
                    pass
                else:
                    self.type = "invalid"
                    self.error =  f'Lexical Error at Line: {line_num} Column: {column}: Unexpected value'

                if (value == "boolean" | value == "digit" | value == "float" | value == "read" | value == "embark" | value == "string" | value == "trojan") \
                and value[count+1] == "(":
                    pass
                else:
                    self.type = "invalid"
                    self.error =  f'Lexical Error at Line: {line_num} Column: {column}: Unexpected value'

                if value[-1] is not None:
                    if (value == "elif" | value == "for" | value == "if" | value == "pair" | value == "parallel" | value == "while" | value == "route") \
                    and value[count+1] == delimiters["start_delim"]:
                        pass
                    else:
                        self.type = "invalid"
                        self.error =  f'Lexical Error at Line: {line_num} Column: {column}: Unexpected value'
                else:
                    pass

                if (value == "FALSE" | value == "TRUE") and value[count+1] == delimiters["bool_delim"]:
                    pass
                else:
                    self.type = "invalid"
                    self.error =  f'Lexical Error at Line: {line_num} Column: {column}: Unexpected value'

                if value == "else" and value[count+1] == delimiters["start_block"]:
                    pass
                else:
                    self.type = "invalid"
                    self.error =  f'Lexical Error at Line: {line_num} Column: {column}: Unexpected value'
                    
                if (value == "+" | value == "-" | value == "*" | value == "/" | value =="^" | value == "//" | value == "%") \
                and value[count+1] == delimiters["arith_delim"]:
                    pass
                else:
                    self.type = "invalid"
                    self.error =  f'Lexical Error at Line: {line_num} Column: {column}: Unexpected value'
                    
                if value == "=" and value[count+1] == delimiters["equal_delim"]:
                    pass
                else:
                    self.type = "invalid"
                    self.error =  f'Lexical Error at Line: {line_num} Column: {column}: Unexpected value'
            
            
            if type == "comment" and (value[count+1] != '\n' or value[count+1] != '#'):
                self.type = "comment"

            if value[-1] == value:
                if type == ":" and (value[count+1] == '\n' or value[count+1] != ' '):
                    pass
                else:
                        self.type = "invalid"
                        self.error =  f'Lexical Error at Line: {line_num} Column: {column}: Unexpected value'
            else:
                pass

            if type == "invalid":
                pass
            