# -*- coding: utf-8 -*-
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
    'return' : 'RETURN',
    'int' : 'NINT',
    'float' : 'NFLOAT'
    }

tokens = ['EQUALS','PLUS','MINUS','TIMES','DIVIDE','LPAREN',
    'RPAREN','LT','LE','GT','GE','NE', 'FLOAT',
    'COMMA','SEMI', 'ASSIGN','INTEGER', 'LCORCH', 'RCORCH',
    'STRING','INVSTRING','ID','NEWLINE', 'DECLARATION', 'INVCOMNENT'] + list(reserved.values())

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

t_EQUALS      = r'='
t_ASSIGN      = r':='
t_DECLARATION = r':'
t_PLUS        = r'\+'
t_MINUS       = r'-'
t_TIMES       = r'\*'
# t_POWER   = r'\^'
t_DIVIDE      = r'/'
t_LPAREN      = r'\('
t_RPAREN      = r'\)'
t_LCORCH      = r'\['
t_RCORCH      = r'\]'
t_LT          = r'<'
t_LE          = r'<='
t_GT          = r'>'
t_GE          = r'>='
t_NE          = r'!='
t_COMMA       = r'\,'
t_SEMI        = r';'
t_FLOAT       = r'((0|[1-9][0-9]*)\.[0-9]+)([eE][-+]?[0-9]+)?|([1-9][0-9]*)([eE][-+]?[0-9]+)'
t_INTEGER     = r'0|[1-9][0-9]*'

t_ignore      = ' \t'

def t_INVFLOAT(t):
    r'((0[0-9]+)\.[0-9]*|\.[0-9]*|0[0-9]*[eE][+-]?[0-9]*)'
    print "Flotante invalido = "+t.value+" en la linea %s" %t.lexer.lineno
    #t.lexer.skip(1)
    pass

def t_INVINT(t):
    r'((0)[0-9]+)'
    print "Entero invalido = %s" %t.value
    pass

def t_STRING(t):
    r'\"((\\["\\n])|((\\\")*[^"\\](\\\")*))*?\"'
    #r'\"([^\\\n]|[^"]|[^\\\\"])*?\"'
    return t

def t_INVSTRING(t):
    #r'\"((\\[^"\\n])|((\\\")*[^"\\](\\\")*))*?\"'
    r'\"((\\\")*[^"]|[^"](\\\")*)*\"*'
    invString = t.value[1:]
    for i in range(0, len(invString)-1):
        if invString[i] == '\\':
            if invString[i+1] != '\"' and invString[i+1] != '\\' and invString[i+1] != "n":
                print "String invalida.. caracter de escape no valido ",(invString[i]+ invString[i+1])," en la linea ",t.lexer.lineno
                t.lexer.skip(1)
                pass
            else:
                i += 1
    final = t.value[-2:]
    if not '\"' in final:
        print "String no finalizada"
    t.lexer.skip(1)

def t_COMMENT(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
    pass
    # No return value. Token discarded

def t_INVCOMMENT(t):
    r'(/\*(.|\n)*(/\*)*)|\*/'
    t.lexer.lineno += t.value.count('\n')
    if t.value.count('/*') > 1 :
        print "Comentario invalido en la linea '%s'... no se permiten comentarios anidados" % t.lexer.lineno
    elif t.value[-2:] == '*/':
        print "Comentario no abierto en la linea '%s'" %t.lexer.lineno
    else:
        print "Comentario no finalizado"
    pass

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

lexer = lex.lex()


pruebas = open("Pruebas.pas", "r")
str = pruebas.read()
# print str
# Give the lexer some input
lexer.input(str)

pruebas.close()

# Tokenize
while True:
    tok = lexer.token()
    if not tok: break      # No more input
    print tok
