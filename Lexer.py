#!/usr/bin/python

import ply.lex as lex


class Lexer:

    newlines = [-1]

    def __init__(self):
        self.lexer = lex.lex(object=self)
        self.result = []

    def input(self, text):
        self.lexer.input(text)

    def token(self):
        return self.lexer.token()

    def run(self, s, **kwargs):
        self.lexer.input(s)
        for token in self.lexer:
            self.result.append(token)

    def print_result(self):
        print(self.show_result())

    def show_result(self):
        result = ""
        for token in self.result:
            result += self.show_token(token) + "\n"
        return result

    def show_token(self, token):
        return "(%d, %d): %s(%s)" % (
            token.lineno,
            Lexer.get_column(token),
            token.type,
            token.value
        )

    reserved = {
        'if': 'IF',
        'else': 'ELSE',
        'for': 'FOR',
        'while': 'WHILE',
        'break': 'BREAK',
        'continue': 'CONTINUE',
        'return': 'RETURN',
        'print': 'PRINT',
    }

    tokens = [
                 'PLUS',
                 'MINUS',
                 'TIMES',
                 'DIVIDE',
                 'ASSIGN',
                 'LESS',
                 'MORE',
                 'LESSEQUAL',
                 'MOREEQUAL',
                 'EQUAL',
                 'LPAREN',
                 'RPAREN',
                 'LCURLY',
                 'RCURLY',
                 'COLON',
                 'COMMA',
                 'SEMICOLON',
                 'ID',
                 'INT',
                 'FLOAT',
                 'STRING',
                 'TYPE'
             ] + list(reserved.values())

    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_ASSIGN = r'='
    t_LESS = r'<'
    t_MORE = r'>'
    t_LESSEQUAL = r'<='
    t_MOREEQUAL = r'>='
    t_EQUAL = r'=='
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LCURLY = r'\{'
    t_RCURLY = r'\}'
    t_COLON = r':'
    t_COMMA = r','
    t_SEMICOLON = r';'
    t_STRING = r'"([^\\\n]|(\\.))*?"'

    t_ignore = ' \t'
    t_ignore_COMMENT = r'\#.*'



    def t_TYPE(self, t):
        r'int|float|String'
        return t

    def t_ID(self, t):
        r"[a-zA-Z_][a-zA-Z_0-9]*"
        t.type = self.reserved.get(t.value, 'ID')
        return t

    def t_FLOAT(self, t):
        r"([0-9]+\.[0-9]*|\.[0-9]+) ([eE][-+]?[0-9]+)?"
        t.value = float(t.value)
        return t

    def t_INT(self, t):
        r"\d+"
        t.value = int(t.value)
        return t

    def t_newline(self, t):
        r"\n+"
        t.lexer.lineno += len(t.value)
        Lexer.add_newline(t)

    def t_error(self, t):
        print("illegal character '%s' at (%d, %d)" %
              (t.value[0], t.lineno, self.get_column(t)))
        t.lexer.skip(1)

    @staticmethod
    def get_column(t):
        return (t.lexpos - Lexer.newlines[t.lineno - 1])

    @staticmethod
    def get_position(t):
        return t.lineno, Lexer.get_column(t)

    @staticmethod
    def add_newline(t):
        for i in range(len(t.value)):
            Lexer.newlines.append(t.lexpos + i)