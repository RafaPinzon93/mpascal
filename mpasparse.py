# -*- coding: utf-8 -*-
import ply.lex as lex
import sys, ply.yacc as yacc

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

t_EQUALS      = r'=='
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
t_FLOAT       = r'((0|[1-9][0-9]*)\.[0-9]+)([eE][-+]?[0-9]+)?|([1-9][0-9]*|0)([eE][-+]?[0-9]+)'
t_INTEGER     = r'0|[1-9][0-9]*'

t_ignore      = ' \t'

def t_INVFLOAT(t):
    r'((0[0-9]+)\.[0-9]*|\.[0-9]*|0[0-9]+[eE][+-]?[0-9]*)'
    print "Flotante invalido = "+t.value+" en la linea %s" %t.lexer.lineno
    #t.lexer.skip(1)
    pass

def t_INVINT(t):
    r'((0)[0-9]+)'
    print "Entero invalido = "+t.value+" en la linea %s" %t.lexer.lineno
    pass

def t_STRING(t):
    r'\"((\\["\\n])|((\\\")*[^"\\\n](\\\")*))*?\"'
    #r'\"([^\\\n]|[^"]|[^\\\\"])*?\"'
    return t

def t_INVSTRING(t):
    #r'\"((\\[^"\\n])|((\\\")*[^"\\](\\\")*))*?\"'
    r'\"((\\\")*[^"]|[^"](\\\")*)*(\")?'
    invString = t.value[1:]
    for i in range(0, len(invString)-1):
        if invString[i] == '\n':
            print "No se permiten strings con multiples lineas %s" % t.lexer.lineno
            t.lexer.lineno += 1
            # break

        if invString[i] == '\\':
            if invString[i+1] != '\"' and invString[i+1] != '\\' and invString[i+1] != "n":
                print "String invalida.. caracter de escape no valido ",(invString[i]+ invString[i+1])," en la linea ",t.lexer.lineno
                # break

            else:
                i += 1
    final = t.value[-2:]
    if (not '\"' in final) or (len(t.value) <= 2):
        print "String no finalizada en la linea %s" % t.lexer.lineno
    pass

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

lex.lex()

# Tokenize

# Parsing Rules

'''
Objetos Arbol de Sintaxis Abstracto (AST - Abstract Syntax Tree).

Este archivo define las clases para los diferentes tipos de nodos del
árbol de sintaxis abstracto.  Durante el análisis sintático, se debe
crear estos nodos y conectarlos.  En general, usted tendrá diferentes
nodos AST para cada tipo de regla gramatical.  Algunos ejemplos de
nodos AST pueden ser encontrados al comienzo del archivo.  Usted deberá
añadir más.
'''

# NO MODIFICAR
class AST(object):
    '''
    Clase base para todos los nodos del AST.  Cada nodo se espera
    definir el atributo _fields el cual enumera los nombres de los
    atributos almacenados.  El método a continuación __init__() toma
    argumentos posicionales y los asigna a los campos apropiados.
    Cualquier argumento adicional especificado como keywords son
    también asignados.
    '''
    _fields = []
    def __init__(self,*args,**kwargs):
        assert len(args) == len(self._fields)
        for name,value in zip(self._fields,args):
            setattr(self,name,value)
        # Asigna argumentos adicionales (keywords) si se suministran
        for name,value in kwargs.items():
            setattr(self,name,value)

    def pprint(self):
        for depth, node in flatten(self):
            print("%s%s" % (" "*(4*depth),node))

def validate_fields(**fields):
    def validator(cls):
        old_init = cls.__init__
        def __init__(self, *args, **kwargs):
            old_init(self, *args, **kwargs)
            for field,expected_type in fields.items():
                assert isinstance(getattr(self, field), expected_type)
        cls.__init__ = __init__
        return cls
    return validator

# ----------------------------------------------------------------------
# Nodos AST especificos
#
# Para cada nodo es necesario definir una clase y añadir la especificación
# del apropiado _fields = [] que indique que campos deben ser almacenados.
# A modo de ejemplo, para un operador binario es posible almacenar el
# operador, la expresión izquierda y derecha, como esto:
#
#    class Binop(AST):
#        _fields = ['op','left','right']
# ----------------------------------------------------------------------

# Unos pocos nodos ejemplos

class PrintStatement(AST):
    '''
    print expression ;
    '''
    _fields = ['expr']

class Literal(AST):
    '''
    Un valor constante como 2, 2.5, o "dos"
    '''
    _fields = ['value']

class Program(AST):
    _fields = ['program']

@validate_fields(statements=list)
class Statements(AST):
    _fields = ['statements']

    def append(self,e):
        self.statements.append(e)

class Statement(AST):
    _fields = ['statement']

class Extern(AST):
    _fields = ['func_prototype']

class FuncPrototype(AST):
    _fields = ['id', 'params', 'typename']

@validate_fields(param_decls=list)
class Parameters(AST):
    _fields = ['param_decls']

    def append(self,e):
        self.param_decls.append(e)

class ParamDecl(AST):
    _fields = ['id', 'typename']

class AssignmentStatement(AST):
    _fields = ['location', 'value']

class ConstDeclaration(AST):
    _fields = ['id', 'value']

class VarDeclaration(AST):
    _fields = ['id', 'typename', 'value']

class IfStatement(AST):
    _fields = ['condition', 'then_b', 'else_b']

class WhileStatement(AST):
    _fields = ['condition', 'body']

class LoadLocation(AST):
    _fields = ['name']

class StoreVar(AST):
    _fields = ['name']

class UnaryOp(AST):
    _fields = ['op', 'left']

class BinaryOp(AST):
    _fields = ['op', 'left', 'right']

class RelationalOp(AST):
    _fields = ['op', 'left', 'right']

class Group(AST):
    _fields = ['expression']

class FunCall(AST):
    _fields = ['id', 'params']

class ExprList(AST):
    _fields = ['expressions']

    def append(self, e):
        self.expressions.append(e)

class Empty(AST):
    _fields = []


# Usted deberá añadir mas nodos aquí.  Algunos nodos sugeridos son
# BinaryOperator, UnaryOperator, ConstDeclaration, VarDeclaration,
# AssignmentStatement, etc...

# ----------------------------------------------------------------------
#                  NO MODIFIQUE NADA AQUI ABAJO
# ----------------------------------------------------------------------

# Las clase siguientes para visitar y reescribir el AST son tomadas
# desde el módulo ast de python .

# NO MODIFIQUE
class NodeVisitor(object):
    '''
    Clase para visitar nodos del árbol de sintaxis.  Se modeló a partir
    de una clase similar en la librería estándar ast.NodeVisitor.  Para
    cada nodo, el método visit(node) llama un método visit_NodeName(node)
    el cual debe ser implementado en la subclase.  El método genérico
    generic_visit() es llamado para todos los nodos donde no hay coincidencia
    con el método visit_NodeName().

    Es es un ejemplo de un visitante que examina operadores binarios:

        class VisitOps(NodeVisitor):
            visit_Binop(self,node):
                print("Operador binario", node.op)
                self.visit(node.left)
                self.visit(node.right)
            visit_Unaryop(self,node):
                print("Operador unario", node.op)
                self.visit(node.expr)

        tree = parse(txt)
        VisitOps().visit(tree)
    '''
    def visit(self,node):
        '''
        Ejecuta un método de la forma visit_NodeName(node) donde
        NodeName es el nombre de la clase de un nodo particular.
        '''
        if node:
            method = 'visit_' + node.__class__.__name__
            visitor = getattr(self, method, self.generic_visit)
            return visitor(node)
        else:
            return None

    def generic_visit(self,node):
        '''
        Método ejecutado si no se encuentra médodo aplicable visit_.
        Este examina el nodo para ver si tiene _fields, es una lista,
        o puede ser recorrido completamente.
        '''
        for field in getattr(node,"_fields"):
            value = getattr(node,field,None)
            if isinstance(value, list):
                for item in value:
                    if isinstance(item,AST):
                        self.visit(item)
            elif isinstance(value, AST):
                self.visit(value)

# NO MODIFICAR
class NodeTransformer(NodeVisitor):
    '''
    Clase que permite que los nodos del arbol de sintraxis sean
    reemplazados/reescritos.  Esto es determinado por el valor retornado
    de varias funciones visit_().  Si el valor retornado es None, un
    nodo es borrado. Si se retorna otro valor, reemplaza el nodo
    original.

    El uso principal de esta clase es en el código que deseamos aplicar
    transformaciones al arbol de sintaxis.  Por ejemplo, ciertas optimizaciones
    del compilador o ciertas reescrituras de pasos anteriores a la generación
    de código.
    '''
    def generic_visit(self,node):
        for field in getattr(node,"_fields"):
            value = getattr(node,field,None)
            if isinstance(value,list):
                newvalues = []
                for item in value:
                    if isinstance(item,AST):
                        newnode = self.visit(item)
                        if newnode is not None:
                            newvalues.append(newnode)
                    else:
                        newvalues.append(n)
                value[:] = newvalues
            elif isinstance(value,AST):
                newnode = self.visit(value)
                if newnode is None:
                    delattr(node,field)
                else:
                    setattr(node,field,newnode)
        return node

# NO MODIFICAR
def flatten(top):
    '''
    Aplana el arbol de sintaxis dentro de una lista para efectos
    de depuración y pruebas.  Este retorna una lista de tuplas de
    la forma (depth, node) donde depth es un entero representando
    la profundidad del arból de sintaxis y node es un node AST
    asociado.
    '''
    class Flattener(NodeVisitor):
        def __init__(self):
            self.depth = 0
            self.nodes = []
        def generic_visit(self,node):
            self.nodes.append((self.depth,node))
            self.depth += 1
            NodeVisitor.generic_visit(self,node)
            self.depth -= 1

    d = Flattener()
    d.visit(top)
    return d.nodes

precedence = (
    ('right', 'ELSE'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'ID'),
    ('left', 'SKIP'),
    ('right', 'SEMI'),
)

def p_programa_funciones(p):
    "programa : programa funcion"
    p[0] = (p[1], p[2])

def p_programa_funcion(p):
    "programa : funcion"
    p[0] = p[1]

def p_funcion(p):
    "funcion : FUN ID LPAREN argumentos RPAREN locales BEGIN declaraciones END"
    p[0] = ('FUN', p[2], p[4], p[5], p[7], p[9])

def p_argumentos_mpar(p):
    '''argumentos : mparametros'''
    p[0] = p[1]

def p_parametro(p):
    '''parametro : ID DECLARATION tipo'''
    if len(p) == 4: p[0] = (p[1], p[3])
    else: p[0] = p[1]

def p_mparametros(p):
    '''mparametros : mparametros SEMI parametro
                  | parametro
                  | empty'''
    if len(p) > 4: p[0] = (p[1], p[3], p[5])
    else: p[0] = p[1]

def p_locales(p):
    '''locales : locales ID DECLARATION tipo SEMI
              | ID DECLARATION tipo SEMI
              | funcion '''
    if len(p) > 5: p[0] = (p[1], p[2], p[4])
    elif len(p) == 5: p[0] = (p[1], p[3])
    else: p[0] = p[1]

def p_locales_empty(p):
    '''locales : empty '''
    p[0] = p[1]

def p_asignacion(p):
    '''asignacion : ID ASSIGN expresion
                 | ID LCORCH index RCORCH ASSIGN expresion
                 | empty '''
    if len(p) == 5: p[0] = (p[1], p[4])
    elif len(p) > 6: p[0] = (p[1], p[3], p[7])
    else: p[0] = p[1]

def p_declaracion_while(p):
    '''declaracion : WHILE relacion DO declaracion'''
    p[0] = ('WHILE', p[1], p[4])

def p_declaracion_if(p):
    '''declaracion : IF relacion THEN declaracion
                  | IF relacion THEN declaracion ELSE declaracion
    '''
    if len(p) == 5:
        p[0] = ('IF', p[2], p[4])
    else:
        p[0] = ('IF', p[2], p[4], p[6])


def p_declaracion_print(p):
    '''
        declaracion : PRINT LPAREN STRING RPAREN
    '''
    p[0] = ('PRINT', p[3])

def p_declaracion_write(p):
    '''
        declaracion : WRITE LPAREN expresion RPAREN
    '''
    p[0] = ('WRITE', p[3])

def p_declaracion_read(p):
    '''
        declaracion : READ LPAREN expresion RPAREN
    '''
    p[0] = ('READ', p[3])

def p_declaracion_return(p):
    '''
        declaracion : RETURN expresion
    '''
    p[0] = ('RETURN', p[2])


def p_declaracion_es(p):
    '''
        declaracion : BEGIN declaraciones END
    '''
    p[0] = p[2]

def p_declaracion_exp(p):
    '''
        declaracion : expresion
    '''
    p[0] = p[1]

def p_declaracion_ass(p):
    '''
        declaracion : asignacion
    '''
    p[0] = p[1]

def p_declaraciones(p):
    '''declaraciones : declaraciones SEMI declaracion'''
    p[0] = (p[1], p[3])

def p_declaraciones_b(p):
    '''declaraciones : declaraciones BREAK'''
    p[0] = ('BREAK', p[2])

def p_declaraciones_s(p):
    '''declaraciones : declaraciones SKIP'''
    p[0] = ('SKIP', p[2])

def p_declaraciones_dec(p):
    '''declaraciones : declaracion'''
    p[0] = p[1]

def p_index(p):
    "index : expresion"
    p[0] = p[1]


def p_tipo_INT(p):
    ''' tipo : NINT
            | NINT LCORCH expresion RCORCH
    '''
    if len(p) == 5:
        p[0] = ('NINT', p[3])
    else:
        p[0] = p[1]

def p_tipo_FLOAT(p):
    ''' tipo : NFLOAT
            | NFLOAT LCORCH expresion RCORCH
    '''
    if len(p) == 5:
        p[0] = ('NFLOAT', p[3])
    else:
        p[0] = p[1]

def p_expresion_operadores_bin(p):
    '''  expresion : expresion PLUS expresion
                  | expresion MINUS expresion
                  | expresion TIMES expresion
                  | expresion DIVIDE expresion
                  '''
    if p[2] == 'PLUS':
        p[0] = p[1] + p[3]
    elif p[2] == 'MINUS':
        p[0] = p[1] - p[3]
    elif p[2] == 'TIMES':
        p[0] = p[1] * p[3]
    elif p[2] == 'DIVIDE':
        p[0] = p[1] / p[3]

def p_expresion_signo(p):
    ''' expresion : MINUS expresion
                 | PLUS expresion '''
    if p[1] == 'MINUS':
        p[0] = -p[2]
    elif p[1] == 'PLUS':
        p[0] = p[2]

def p_expresion_parent(p):
    '''expresion :  LPAREN expresion RPAREN '''
    p[0] = p[2]

def p_expresion_ID(p):
    '''expresion : ID LPAREN argumentos RPAREN
                | ID
                | ID LCORCH expresion RCORCH
    '''
    if len(p) > 2:
        if p[2] == 'LPAREN': p[0] = (p[1], p[3])
        if p[2] == 'LCORCH': p[0] = (p[1], p[3])
    else:
        p[0]= p[1]

def p_expresion_numero(p):
    '''expresion : numero'''
    p[0] = p[1]

def p_expresion_INT(p):
    "expresion : NINT LPAREN expresion RPAREN "
    p[0] = ('NINT', p[3])

def p_expresion_FLOAT(p):
    '''expresion : NFLOAT LPAREN expresion RPAREN '''
    p[0] = ('NFLOAT', p[3])

def p_numero_INTEGER(p):
    '''numero : INTEGER'''
    p[0] = p[1]

def p_numero_FLOAT(p):
     '''numero : FLOAT '''
     p[0] = p[1]

def p_argumentos(p):
    '''argumentos : argumentos COMMA expresion
                 | expresion
    '''
    if len(p) == 4: p[0] = (p[1], p[3])
    else: p[0] = p[1]

def p_relacion(p) :
    '''
    relacion : expresion LT expresion
            | expresion GT expresion
            | expresion LE expresion
            | expresion GE expresion
            | expresion EQUALS expresion
            | expresion NE expresion
            | relacion AND relacion
            | relacion OR relacion
            | NOT relacion
            | LPAREN relacion RPAREN
    '''
    if len(p) == 4:
        if p[2] == 'LT':
            p[0] = p[1] < p[3]
        if p[2] == 'LE':
            p[0] = p[1] <= p[4]
        if p[2] == 'GT':
            p[0] = p[1] > p[3]
        if p[2] == 'GE':
            p[0] = p[1] >= p[3]
        if p[2] == 'EQUALS':
            p[0] = p[1] == p[3]
        if p[2] == 'NE':
            p[0] = p[1] != p[3]
        if p[2] == 'AND':
            p[0] = p[1] and p[3]
        if p[2] == 'OR':
            p[0] = p[1] or p[3]
        if p[1] == 'LPAREN':
            p[0] = p[2]

    if len(p) == 3:
            p[0] = not p[0]


def p_empty(p):
    'empty :'
    pass

def p_error(p):
    print "Syntax error in input!"

# Build the parser
parser = yacc.yacc()

pruebas = open("Pruebas.pas", "r")
str = pruebas.read()
# print str
# Give the lexer some input

parser.parse(str)
