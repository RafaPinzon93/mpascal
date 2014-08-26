#!/usr/bin/env python
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
    'int' : 'INT'
    'float'
    }

tokens = ['EQUALS','PLUS','MINUS','TIMES','DIVIDE','LPAREN',
    'RPAREN','LT','LE','GT','GE','NE', 'FLOAT',
    'COMMA','SEMI','SEMICOLON', 'ASSIGN','INTEGER', 'LCORCH', 'RCORCH',
    'STRING','ID','NEWLINE', 'DECLARATION'] + list(reserved.values())

def t_ID(t):
    r'[a-zA-Z][a-zA-Z_0-9]*'
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
t_FLOAT       = r'((0|[1-9][0-9]*)\.[0-9]+)([eE][-+]?[0-9]+)?'
t_INTEGER     = r'0|[1-9][0-9]*'
t_STRING      = r'\"(.|\n|\\|")*\"'
t_ignore      = ' \t'

def t_COMMENT(t):
    r'/\*.*\*/'
    pass
    # No return value. Token discarded

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

lexer = lex.lex()

# Test it out
data = '''
fun quicksort(l:int, r:int, a:int[8192])
i:int;
j:int;
x:int;
w:int;
tmp:int;
done:int;
begin
i := l;
j := r;
x := a[(l+r)/2];
done := 0;
while done == 0 do
begin
while a[i] < x do
i := i + 1;
while x < a[j] do
j := j - 1;
if i <= j then
begin
tmp := a[i];
a[i] := a[j];
a[j] := tmp;
i:=i+1;j:=j-1
end;
if i>j then
done := 1
end;
if l<j then
tmp := quicksort(l, j, a);
if i<r then
tmp := quicksort(i, r, a)
end
fun main()
v:int[8192];
i:int;
n:int;
begin
print("Entre n: ");
read(n);
i := 0;
while i<n do
begin
read(v[i]);
i := i+1
end;
quicksort(0, n-1, v);
i := 0;
while i<n-1 do
begin
write(v[i]); print(" ");
if 0 < v[i] - v[i+1] then
begin
print("Quicksort falló "); write(i); print("\n") ; return(0)
end
else
i:=i+1
end;
write(v[i]);
print("Éxito\n")
end
'''

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok: break      # No more input
    print tok
