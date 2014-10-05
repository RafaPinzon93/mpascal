# -*- coding: utf-8 -*-
import ply.lex as lex
import ply.yacc as yacc
from mpaslex import tokens

precedence = (
    ('right', 'ASSIGN'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQUALS', 'NE'),
    ('left', 'LT', 'LE', 'GT', 'GE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'RCORCH'),
    ('left', 'RPAREN'),
)

def p_programa_funciones(p):
    "programa : programa funcion"
    p[0] = p[1]
    p[0].append(p[2])
    # p[1].append(p[2])
    # p[0] = p[1]

# errores experimentales
def p_programa_funciones_error(p):
    "programa : error"
    p[0] = None
    p.parser.error = 1

def p_programa_funcion(p):
    "programa : funcion"
    p[0] = Program([p[1]])
    # print p[0]

def p_funcion(p):
    "funcion : FUN ID LPAREN mparametros RPAREN locales BEGIN declaraciones END"
    p[0] = Funcion(p[2], p[4], p[6], p[8])

#errores experimentales
def p_funcion_error1(p):
    "funcion : FUN ID LPAREN error RPAREN locales BEGIN declaraciones END"
    print("Funcion con parametros mal formados %s" % p[3])
    p[0] = None
    p.parser.error = 1

def p_funcion_error2(p):
    "funcion : FUN ID LPAREN mparametros RPAREN error BEGIN declaraciones END"
    print("Funcion con locales mal formadas %s" % p[8].value)
    p[0] = None
    p.parser.error = 1

def p_funcion_error3(p):
    "funcion : FUN ID LPAREN mparametros RPAREN locales BEGIN error END"
    print("Funcion con declaraciones mal formadas %s" % p[8].value)
    p[0] = None
    p.parser.error = 1

def p_parametro(p):
    '''parametro : ID DECLARATION tipo'''
    p[0] = Parametro(p[1], p[3])

def p_mparametros(p):
    '''mparametros : mparametros COMMA parametro
                  | parametro
                  | empty'''
    if len(p) == 4:
        p[1].append(p[3])
        p[0] = p[1]
    else:
        p[0] = Parameters([p[1]])

# def p_declaracionvar(p):
#     '''declaracionvar : ID DECLARATION tipo
#     '''
#     p[0] = Locales(p[1], p[3])


def p_locales(p):

    '''locales : local
              | empty
    '''
    p[0] = Locales(p[1])

def p_local(p):
    '''
        local : local parametro SEMI
              | local funcion SEMI
              | parametro SEMI
              | funcion SEMI
    '''
    if len(p) == 4:
        p[1].append(p[2])
        p[0] = p[1]
    else: p[0] = Local([p[1]])
# def p_locales_empty(p):
#     '''locales : empty '''
#     p[0] = p[1]

def p_asignacion(p):
    '''asignacion : ID ASSIGN expresion
                  | ID LCORCH index RCORCH ASSIGN expresion
    '''
    # if len(p) == 4: p[0] = (p[1], p[4])
    # elif len(p) > 6: p[0] = (p[1], p[3], p[7])

def p_declaracion_while(p):
    '''declaracion : WHILE relacion DO declaracion'''
    p[0] = WhileStatement(p[2], p[1])

def p_declaracion_if(p):
    '''declaracion : IF relacion THEN declaracion
                  | IF relacion THEN declaracion ELSE declaracion
    '''
    if len(p) == 5:
        p[0] = IfStatement(p[2], p[4], None) #('IF', p[2], p[4])
    else:
        pass# p[0] = ('IF', p[2], p[4], p[6])


def p_declaracion_print(p):
    '''
        declaracion : PRINT LPAREN STRING RPAREN
    '''
    p[0] = PrintStatement(p[3])

def p_declaracion_write(p):
    '''
        declaracion : WRITE LPAREN expresion RPAREN
    '''
    p[0] = WriteStatements(p[3])


def p_declaracion_read(p):
    '''
        declaracion : READ LPAREN expresion RPAREN
    '''
    p[0] = ReadStatements(p[3])

def p_declaracion_return(p):
    '''
        declaracion : RETURN expresion
    '''
    p[0] = Return(p[2])


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

def p_declaracion_SkBr(p):
    '''
        declaracion : SKIP
                    | BREAK
    '''
    p[0] = Declaracion(p[1])

def p_declaracion_assi(p):
    '''
        declaracion : asignacion
    '''
    p[0] = p[1]#Asignacion(p[1])

def p_declaraciones(p):
    '''declaraciones : declaraciones SEMI declaracion'''
    p[1].append(p[3])
    p[0] = p[1]

# def p_declaracion_b(p):
#     '''declaraciones : declaraciones BREAK'''
#     p[1].append(p[2])
#     p[0] = p[1]


# def p_declaracion_s(p):
#     '''declaraciones : declaraciones SKIP'''
#     p[1].append(p[2])
#     p[0] = p[1]

def p_declaraciones_dec(p):
    '''declaraciones : declaracion'''
    p[0] = Declaraciones(p[1], declaraciones = [p[1]])

def p_index(p):
    "index : expresion"
    p[0] = p[1]


def p_tipo_INT(p):
    ''' tipo : NINT
             | NINT LCORCH expresion RCORCH
    '''
    if len(p) == 5:
        p[0] = Tipo_Nint(p[3])
    else:
        p[0] = Tipo_Nint(None)

def p_tipo_FLOAT(p):
    ''' tipo : NFLOAT
            | NFLOAT LCORCH expresion RCORCH
    '''
    if len(p) == 5:
        p[0] = Tipo_Nfloat(p[3])
    else:
        p[0] = Tipo_Nfloat(None)

def p_expresion_operadores_bin(p):
    '''  expresion : expresion PLUS expresion
                  | expresion MINUS expresion
                  | expresion TIMES expresion
                  | expresion DIVIDE expresion
                  '''
    if p[2] == 'PLUS':
        p[0] = BinaryOp(p[2], p[1], p[3])
    elif p[2] == 'MINUS':
        p[0] = BinaryOp(p[2], p[1], p[3])
    elif p[2] == 'TIMES':
        p[0] = BinaryOp(p[2], p[1], p[3])
    elif p[2] == 'DIVIDE':
        p[0] = BinaryOp(p[2], p[1], p[3])

def p_expresion_signo(p):
    ''' expresion : MINUS expresion
                 | PLUS expresion '''

    if p[1] == 'MINUS':
        p[0] = UnaryOp(p[1], p[2])
    elif p[1] == 'PLUS':
        p[0] = UnaryOp(p[1], p[2])

def p_expresion_parent(p):
    '''
        expresion :  LPAREN expresion RPAREN
                  |  LPAREN RPAREN
    '''
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = None


def p_expresion_ID(p):
    '''expresion : ID LPAREN argumentos RPAREN
                 | ID LPAREN RPAREN
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
    p[0] = Numero(p[1])


def p_expresion_INT(p):
    "expresion : NINT LPAREN expresion RPAREN "
    p[0] = Nint(p[3])

def p_expresion_FLOAT(p):
    '''expresion : NFLOAT LPAREN expresion RPAREN '''
    p[0] = Nfloat(p[3])

def p_numero_INTEGER(p):
    '''numero : INTEGER'''
    p[0] = Literal(p[1])

def p_numero_FLOAT(p):
     '''numero : FLOAT '''
     p[0] = Literal(p[1])

def p_argumentos(p):
    '''argumentos : argumentos COMMA expresion
                 | expresion
    '''
    if len(p) == 4:
        p[1].append(p[3])
        p[0] = p[1]
    else: p[0] = Argumentos([p[1]])

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
            p[0] = BinaryOp(p[2], p[1], p[3])
        if p[2] == 'LE':
            p[0] = BinaryOp(p[2], p[1], p[3])
        if p[2] == 'GT':
            p[0] = BinaryOp(p[2], p[1], p[3])
        if p[2] == 'GE':
            p[0] = BinaryOp(p[2], p[1], p[3])
        if p[2] == 'EQUALS':
            p[0] = BinaryOp(p[2], p[1], p[3])
        if p[2] == 'NE':
            p[0] = BinaryOp(p[2], p[1], p[3])
        if p[2] == 'AND':
            p[0] = BinaryOp(p[2], p[1], p[3])
        if p[2] == 'OR':
            p[0] = BinaryOp(p[2], p[1], p[3])
        if p[1] == 'LPAREN':
            p[0] = p[2]

    if len(p) == 3:
            p[0] = UnaryOp(p[1], p[2])


def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if not p:
        print("SYNTAX ERROR AT EOF")

#---------------------------------------------------------------------
#AST Structure
#---------------------------------------------------------------------

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
        assert len(args) == len(self._fields) #or len(kwargs) == len(self._fields) #assert test a condition, and could pop an error
        for name,value in zip(self._fields,args):
            setattr(self,name,value) #Adds attributes to the object (in this case self)
        # Asigna argumentos adicionales (keywords) si se suministran
        for name,value in kwargs.items():
            setattr(self,name,value)

    def pprint(self):
        for depth, node in flatten(self):
            print("%s%s" % (" "*(4*depth),node))

    def __repr__(self):

        # return ' '.join(self._fields)

        excluded = {"lineno"}
        return "{}".format(self.__class__.__name__)
        # {key: value
        # for key, value in vars(self).items()
        # if not key.startswith("_") and not key in excluded})
        # #return "{}".format(self.__class__.__name__)#vars(self))


#No la entiendo muy bien
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

@validate_fields(funciones = list)
class Program(AST):
    _fields = ['funciones']

    def append(self, e):
        self.funciones.append(e)

    # def __repr__(self):
    #     return self.funciones[0]

@validate_fields(declaraciones=list)
class Declaraciones(AST):
    _fields = ['declaraciones']

    def append(self,e):
        self.declaraciones.append(e)

class Declaracion(AST):
    _fields = ['declaracion']


class Funcion(AST):
    _fields = ['id', 'argumentos', 'locales', 'declaraciones']

@validate_fields(param_decls=list)
class Parameters(AST):
    _fields = ['param_decls']

    def append(self,e):
        self.param_decls.append(e)

class Parametro(AST):
    _fields = ['id', 'parametro']

@validate_fields(argumentos = list)
class Argumentos(AST):
    _fields = ['argumentos']

    def append(self,e):
        self.argumentos.append(e)

@validate_fields(local = list)
class Local(AST):
    _fields = ['local']
    def append(self, e):
        self.local.append(e)

class Locales(AST):
    _fields = ['locales']

class AssignmentStatement(AST):
    _fields = ['location', 'value']

class Nint(AST):
    _fields = ['expr']

class Nfloat(AST):
    _fields = ['expr']

class Tipo_Nint(AST):
    _fields = ['expresion']

class Tipo_Nfloat(AST):
    _fields = ['expresion']


# class ConstDeclaration(AST):
#     _fields = ['id', 'value']

class IfStatement(AST):
    _fields = ['condition', 'then_b', 'else_b']

class WhileStatement(AST):
    _fields = ['condition', 'body']

class WriteStatements(AST):
    _fields = ['expr']

class ReadStatements(AST):
    _fields = ['expr']

# class LoadLocation(AST):
#     _fields = ['name']

# class StoreVar(AST):
    # _fields = ['name']


class Return(AST):
    _fields = ['expresion']

class UnaryOp(AST):
    _fields = ['op', 'left']

class BinaryOp(AST):
    _fields = ['op', 'left', 'right']

# class RelationalOp(AST):
#     _fields = ['op', 'left', 'right']

# class Group(AST):
#     _fields = ['expression']

# class FunCall(AST):
#     _fields = ['id', 'params']

# class ExprList(AST):
#     _fields = ['expressions']

#     def append(self, e):
#         self.expressions.append(e)
class Numero(AST):
    _fields = ['numero']

class Literal(AST):
    _fields = ['valor']


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

# Build the parser


# print str
# Give the lexer some input

def make_parser():
    parser = yacc.yacc()
    return parser

if __name__ == '__main__':
    import mpaslex
    import sys
    lexer = mpaslex.make_lexer()
    parser = make_parser()
    program = parser.parse(open(sys.argv[1]).read())
    program.pprint()
    # Output the resulting parse tree structure


