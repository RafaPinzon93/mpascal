# -*- coding: utf-8 -*-
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

    def pprint(self, level = 0):
        # print ("%s%s%s" % (" "*(4*level),"+",flatten(self)[0][1].__class__.__name__))
        i = 0
        for depth, node in flatten(self):
            if depth % 2 == 0:
                 print ("%s%s%s" %(" "*(4*(depth)),"|--"*i, node))
            else:
                print ("%s%s%s" %(" "*(4*(depth)),"+--"*i, node))
            # print depth, node, level
            for var in vars(node).items():
                # print ("%s%s%s" %(" "*(4*(depth+1 + i)),"|--", var[0]))
                i = 1
                # if type(var[1]) == str or list:


                # for x in var[1:]:
                #     # print ("%s%s%s" %(" "*(4*(depth+1)),"|--", var[1].pprint(depth)))
                #     if type(var[1]) == str or list:
                #         print ("%s%s%s" %(" "*(4*(depth+1)),"|--", x))
                #     else:
                #         print ("%s%s%s" %(" "*(4*(depth+1)),"|--", x.pprint(depth)))



    def __repr__(self):
        return "{}".format(self.__class__.__name__)
        #return "{}".format(self.__class__.__name__)#vars(self))

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

class PrintStatement(AST):
    '''
    print expression ;
    '''
    _fields = ['expr']

    def __str__(self):
        return self.__class__.__name__+" ("+ str(vars(self).values()[0])+")"

class Declaracion(AST):
    _fields = ['declaracion']

    def __str__(self):
        return self.__class__.__name__+" ("+ str(vars(self).values()[0])+")"



class Funcion(AST):
    _fields = ['id', 'argumentos', 'locales', 'declaraciones']

    def __str__(self):
        return self.__class__.__name__+" ("+ str(vars(self).values()[2])+")"

@validate_fields(param_decls=list)
class Parameters(AST):
    _fields = ['param_decls']

    def append(self,e):
        self.param_decls.append(e)

class Parametro(AST):
    _fields = ['id', 'tipo']

    def __str__(self):
        return self.__class__.__name__+" ("+ str(vars(self).values()[0])+")"

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

    def __str__(self):
        return self.__class__.__name__+" ("+ str(vars(self).values()[0])+")"

class Nfloat(AST):
    _fields = ['expr']

    def __str__(self):
        return self.__class__.__name__+" ("+ str(vars(self).values()[0])+")"

class ArrayInt(AST):
    _fields = ['expresion']

    def __str__(self):
        return self.__class__.__name__+" ("+ str(vars(self).values()[0])+")"

class ArrayFloat(AST):
    _fields = ['expresion']

    def __str__(self):
        return self.__class__.__name__+" ("+ str(vars(self).values()[0])+")"


# class ConstDeclaration(AST):
#     _fields = ['id', 'value']

# class VarDeclaration(AST):
#     _fields = ['id', 'typename', 'value']

class IfStatement(AST):
    _fields = ['condition', 'then_b', 'else_b']

class WhileStatement(AST):
    _fields = ['condition', 'body']

class WriteStatements(AST):
    _fields = ['expr']

class ReadStatements(AST):
    _fields = ['expr']

class ExpresionIdArray(AST):
    _fields = ['id', 'expresion']

    def __str__(self):
        return self.__class__.__name__+" ("+ str(vars(self).values()[1])+")"

class ExpresionFun(AST):
    _fields = ['id', 'expresion']

    def __str__(self):
        return self.__class__.__name__+" ("+ str(vars(self).values()[1])+")"

class ExpresionID(AST):
    _fields = ['id']

    def __str__(self):
        return self.__class__.__name__+" ("+ str(vars(self).values()[0])+")"

class Location(AST):
    _fields = ['id']

    def __str__(self):
        return self.__class__.__name__+" ("+ str(vars(self).values()[0])+")"

class LocationArray(AST):
    _fields = ['id', 'expresion']

    def __str__(self):
        return self.__class__.__name__+" ("+ str(vars(self).values()[1])+")"
# class LoadLocation(AST):
#     _fields = ['name']

# class StoreVar(AST):
    # _fields = ['name']
class RelOp(AST):
    _fields = ['op', 'left', 'right']

    def __str__(self):
        return self.__class__.__name__+" ("+ str(vars(self).values()[2])+")"

class Return(AST):
    _fields = ['expresion']

    def __str__(self):
        return self.__class__.__name__+" ("+ str(vars(self).values())+")"

class UnaryOp(AST):
    _fields = ['op', 'left']

class BinaryOp(AST):
    _fields = ['op', 'left', 'right']

    def __str__(self):
        return self.__class__.__name__+" ("+ str(vars(self).values()[2])+")"

class Numero(AST):
    _fields = ['numero']


class Literal(AST):
    _fields = ['valor']

    def __str__(self):
        return self.__class__.__name__+" ("+ str(vars(self).values()[0])+")"


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
