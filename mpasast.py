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
_scope=[]
current=None

class Errorsemantico(Exception):

    def __init__(self, valor,lineno): # real signature unknown
        self.valor=valor
        self.lineno = lineno

    def __str__(self):
        lineno = ""
        if(self.lineno):
            lineno = self.lineno
        return repr(self.valor)+repr(lineno)



class Symbol(): #att : name scope level
    paramnum=None
    def __init__(self,name,scope,type,lineno):
        self.name=name
        self.scope=scope
        self.type=type
        self.lineno=lineno

    def changetype(self,type):
        self.type=type


def new_scope():# crea una nueva tabla de simbolos || usar cada vez que entra a una funcion
    global current
    global _scope
    current={}
    #print _scope
    _scope.append(current)
    return current

def pop_scope(): # cada que se sale de una funcion
    global current
    global _scope
    r=_scope.pop()
    current=_scope[-1]
    return r

def get_symbol(name,level=0,attr=None):
    global _scope
    for i in range(len(_scope)-(level+1),-1,-1):
        s=_scope[i]
        try:
            sym=s[name]
            # if attr:
            #     if hasattr(sym,attr):
            #         return sym
            #     else :
            return sym
        except KeyError :
            pass
    return None

def add_symbol(name,type,lineno):
    global current
    s=Symbol(name=name,scope=current,type=type,lineno=lineno)
    current[name]=s
    #print current
    return s

def set_symbol(s):
    global current
    current[s.name]=s # ingresamos a current[print]=print

def attach_symbol(t,type):
    global current
    s=current.get(t.value)
    if not s:
        s=add_symbol(t.value,type,t.lexer.lineno)
    else:
        print("Redefinicion de %s" % t.value)
    t.symtab=s



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

    def semantico(self):
        pass

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

    def semantico(self):
        global _scope
        global current
        current=new_scope()
        for func in self.funciones:
            func.semantico()

        m=get_symbol("main")
        if not m:
            print(" Error : funcion main no definida.")

    # def __repr__(self):
    #     return self.funciones[0]

@validate_fields(declaraciones=list)
class Declaraciones(AST):
    _fields = ['declaraciones']


    def append(self,e):
        self.declaraciones.append(e)

    def semantico(self):
        for declaracion in self.declaraciones:
            declaracion.semantico()

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
    _fields = ['ID', 'parametros', 'locales', 'declaraciones']

    def __str__(self):
        return self.__class__.__name__+" ("+ str(vars(self).values()[2])+")"

    def semantico(self):
        global current
        global _scope
        attach_symbol(self.ID, None)
        m = get_symbol(self.ID.value)
        new_scope()
        if self.parametros:
            self.parametros.semantico()
            m.params= self.parametros.param_decls
            set_symbol(m)
        if self.locales:
            self.locales.semantico()
        self.declaraciones.semantico()
        m = get_symbol("Freturn")
        if m:
            a = get_symbol(self.ID.value)
            self.type = m.type
            a.type = self.type
        pop_scope()

@validate_fields(param_decls=list)
class Parameters(AST):
    _fields = ['param_decls']

    def append(self,e):
        self.param_decls.append(e)

    def semantico(self):
        for parameter in self.param_decls:
            if parameter != None:
                parameter.semantico()

class Parametro(AST):
    _fields = ['ID', 'tipo']

    def __str__(self):
        #return self.__class__.__name__+" ("+ str(vars(self).values()[0])+")"
        return str(self.ID.value)

    def semantico(self):
        attach_symbol(self.ID, eval(self.tipo.token))
        self.type = eval((self.tipo.token))


@validate_fields(argumentos = list)
class Argumentos(AST):
    _fields = ['argumentos']

    def append(self,e):
        self.argumentos.append(e)

@validate_fields(locales = list)
class Locales(AST):
    _fields = ['locales']
    def append(self, e):
        self.locales.append(e)
    def semantico(self):
        for local in self.locales :
            local.semantico()

class Local(AST):
    _fields = ['local']

class Asignacion(AST):
    _fields = ['ID', 'expresion']

    def __str__(self):
        return str(self.ID.value) + " :" + str(self.expresion)

    def semantico(self):
        m=get_symbol(self.ID.value)
        if not m:
            print("Error no existe la variable %s en la linea %s"% (self.ID.value,str(self.ID.lineno)))
        else:
            self.expresion.semantico()
            if (m.type==self.expresion.type):
                pass
            else:
                if not(self.expresion.type == None):
                    print("Error en la asignacion de %s en la linea %s , %s es de tipo %s y se le esta asignando un valor del tipo %s" % (m.name,str(self.ID.lineno),m.name,m.type,self.expresion.type))


class AssignVecStatement(AST):
    _fields = ['ID','index', 'expresion']
    def __str__(self):
        return str(self.ID.value) + " [" + str(self.index) + "]" + ":"+ str(self.expresion)
    def semantico(self):
        m=get_symbol(self.ID.value)
        if not m:
            print("Error no existe la variable %s en la linea %s"% (self.ID.value,str(self.ID.lineno)))
        else:
            self.expresion.semantico()
            self.index.semantico()
            if (m.type==self.expresion.type):
                if self.index.type != int:
                    print("Error en el indice de la variable %s en la linea %s los indices deben ser enteros"% (m.name,str(self.ID.lineno)))
            else:
                if not(self.expresion.type == None):
                    print("Error en la asignacion de %s en la linea %s , %s es de tipo %s y se le esta asignando un valor del tipo %s" % (m.name,str(self.ID.lineno),m.name,m.type,self.expresion.type))

class Nint(AST):
    _fields = ['tipo','expr']
    type = int
    def __str__(self):
        return self.__class__.__name__+" ("+ str(vars(self).values()[0])+")"
    def semantico(self):
    #m=get_symbol(self.right)
        self.expr.semantico()
        self.expr.type=eval(self.tipo)
        self.type=self.expr.type

class Nfloat(AST):
    _fields = ['tipo', 'expr']
    type = float
    def semantico(self):
        #m=get_symbol(self.expr)
        self.expr.semantico()
        self.expr.type=eval(self.tipo)
        self.type=self.expr.type

    def __str__(self):
        return self.__class__.__name__+" ("+ str(vars(self).values()[0])+")"

class ArrayInt(AST):
    _fields = ['token', 'expresion']
    type = None
    def __str__(self):
        return self.__class__.__name__+" ("+ str(vars(self).values()[0])+")"

    def semantico(self):
        if self.expresion:
            self.expresion.semantico()
            if self.expresion.type != int:
                print("Error de tipo para la asignacion de tamaño en la linea %s" % (self.ID.lineno))


class ArrayFloat(AST):
    _fields = ['token', 'expresion']
    type = None
    def __str__(self):
        return self.__class__.__name__+" ("+ str(vars(self).values()[0])+")"

    def semantico(self):
        if self.expresion:
            self.expresion.semantico()
            if self.expresion.type != int:
                print("Error de tipo para la asignacion de tamaño en la linea %s" % (self.ID.lineno))


class IfStatement(AST):
    _fields = ['condition', 'then_b']

    def semantico(self):
        self.condition.semantico()
        self.then_b.semantico()

class IfStatementElse(AST):
    _fields = ['condition', 'then_b', 'else_b']

    def semantico(self):
        self.condition.semantico()
        self.then_b.semantico()
        self.else_b.semantico()

class WhileStatement(AST):
    _fields = ['condition', 'body']

    def semantico(self):
        self.condition.semantico()
        self.body.semantico()

class WriteStatements(AST):
    _fields = ['expr']

class ReadStatements(AST):
    _fields = ['expr']

    def semantico(self):
        m=get_symbol(self.expr.value)

        if not m:
            print("Error no existe la variable %s en la linea %s"% (self.expr.value,str(self.expr.lineno)))

class ExpresionIdArray(AST):
    _fields = ['id', 'expresion']
    type=None
    def __str__(self):
        #return self.__class__.__name__+" ("+ str(vars(self).values()[1])+")"
        return str(self.id.value)+ " [" + str(self.expresion)+"]"

    def Analisissemantico(self):
        n=get_symbol(self.ID.value)
        #print self.ID.value
        if not n:
            print("Error no existe la variable %s en la linea %s"% (self.ID.value,str(self.ID.lineno)))
        else:
            self.type=n.type


class ExpresionFun(AST):
    _fields = ['ID', 'arguments']
    type = None
    def __str__(self):
        #return self.__class__.__name__+" ("+ str(vars(self).values()[1])+")"
        return self.ID.value+ " ( " + str(self.arguments)+" )"

    def semantico(self):
        m=get_symbol(self.ID.value)
        if not m:
            print("Error no existe la funcion \"%s\" en la linea \"%s\""% (self.ID.value,str(self.ID.lineno)))
        if len(m.params) != len(self.arguments.argumentos):
            print("Faltan parametros en la funcion \"%s\" de la linea %s" % (m.name,m.lineno))
        else :
            i = 0
            for arg in self.arguments.argumentos:
                arg.semantico()
                if arg.type != m.params[i].type:
                    print("Error de tipos en el llamado de la funcion  \"%s\" con argumentos \"%s\" en la linea %s" % (self.ID.value, arg , self.ID.lineno))
                i +=1
            self.type = m.type


class ExpresionID(AST):
    _fields = ['ID']
    type=None
    def __str__(self):
        #return self.__class__.__name__+" ("+ str(vars(self).values()[0])+")"
        return self.ID.type + " " + self.ID.value

    def semantico(self):
        n=get_symbol(self.ID.value)
        #print self.ID.value
        if not n:
            print("Error no existe la variable %s en la linea %s"% (self.ID.value,str(self.ID.lineno)))
        else:
            self.type=n.type


class Location(AST):
    _fields = ['id']

    def __str__(self):
        return self.__class__.__name__+" ("+ str(vars(self).values()[0])+")"

class LocationArray(AST):
    _fields = ['id', 'index']

    def __str__(self):
        return self.id +" ("+ self.index +")"

class LocationExpr(AST):
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

    def Analisissemantico(self):
        self.left.Analisissemantico()
        self.right.Analisissemantico()
        if(self.left.type!=self.right.type):
            print("Error de tipos en la expresion logica %s %s %s" % (self.left,self.op,self.right))



class Return(AST):
    _fields = ['expresion', 'token']
    type = None
    def __str__(self):
        return self.token.value +" ("+ str(self.expresion) +")"

    def semantico(self):
        nombre  = "Freturn"
        self.expresion.semantico()
        self.type=self.expresion.type
        m = get_symbol(nombre)
        self.token.value = nombre
        if not m:
            attach_symbol(self.token,self.type)
        elif m.type != self.type:
            print("Conflicto de tipos con del return en la linea %s"%(repr(self.token.lineno)))

class UnaryOp(AST):
    _fields = ['op', 'left']
    type=None
    def semantico(self):
        self.left.semantico()
        self.type=self.left.type

class BinaryOp(AST):
    _fields = ['op', 'left', 'right']
    type=None
    def __str__(self):
        return self.__class__.__name__+" ("+ str(vars(self).values()[2])+")"

    def semantico(self):
        self.left.semantico()
        self.right.semantico()
        if self.left.type==self.right.type:
            self.type=self.left.type
        else:
            print("Error en la expresion : %s %s %s involucra diferentes tipos de variable en la linea."% (self.left,self.op,self.right))

class Numero(AST):
    _fields = ['numero']
    def __str__(self):
        return str(self.numero.type) + " "+ str(self.numero.value)

class NumeroInt(AST):
    _fields = ['numero']
    type = int
    def __str__(self):
        return self.__class__.__name__+" ("+ str(self.numero.value) +")"

class NumeroFloat(AST):
    _fields = ['numero']
    type = float
    def __str__(self):
        return self.__class__.__name__+" ("+ str(self.numero.value) +")"

class Literal(AST):
    _fields = ['valor']

    def __str__(self):
        return self.__class__.__name__+" ("+ str(self.valor.value) +")"


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
