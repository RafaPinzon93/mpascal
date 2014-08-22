import ply.lex as lex

reserved = {
    'fun' : 'FUN',
    'begin' : 'BEGIN',
    'end' : 'END',
    'if' : 'IF',
    'then' : 'THEN',
    'else' : 'ELSE',
    'while' : 'WHILE',
    'print' : 'PRINT',
    'write' : 'WRITE',
    'read' : 'READ',
    'skip' : 'SKIP',
    'do' : 'DO',
    'break' : 'BREAK',
    'continue' : 'CONTINUE',
    'and' : 'AND',
    'or' : 'OR',
    'not' : 'NOT',
    'int' : 'INT',
    'float' : 'FLOAT',
    'return' : 'RETURN',
    }

tokens = ['EQUALS','PLUS','MINUS','TIMES','DIVIDE','POWER',
     'LPAREN','RPAREN','LT','LE','GT','GE','NE', 'NINT', 'NFLOAT'
     'COMMA','SEMI','SEMICOLON', 'ASSIGN','' 'INTEGER','FLOAT', 'STRING',
     'ID','NEWLINE'] + list(reserved.values())

def t_ID(t):
    r'[a-zA-Z][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_COMMENT(t):
    r'/\*.*\*/'
    pass
    # No return value. Token discarded

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
