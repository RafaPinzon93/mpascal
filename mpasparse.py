# -*- coding: utf-8 -*-
import ply.yacc as yacc
from mpaslex import tokens
from mpasast import *

precedence = (
    ('right', 'ASSIGN'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQUALS', 'NE'),
    ('left', 'LT', 'LE', 'GT', 'GE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'ID'),
    ('left', 'SKIP'),
    ('right', 'SEMI'),
    ('right', 'UNARY'),
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
    '''
        funcion : FUN ID LPAREN mparametros RPAREN locales BEGIN declaraciones END
    '''
    p[0] = Funcion(p[2], p[4], p[6], p[8])

#errores experimentales
def p_funcion_error1(p):
    "funcion : FUN ID LPAREN error RPAREN locales BEGIN declaraciones END"
    print("Funcion con parametros mal formados ")
    p[0] = None
    p.parser.error = 1

#def p_funcion_error2(p):
    #"funcion : FUN ID LPAREN mparametros RPAREN error BEGIN declaraciones END"
    #print("Funcion con locales mal formadas")
    #p[0] = None
    #p.parser.error = 1

def p_funcion_error3(p):
    "funcion : FUN ID LPAREN mparametros RPAREN locales BEGIN error END"
    print("Funcion con declaraciones mal formadas")
    p[0] = None

def p_parametro(p):
    '''parametro : ID DECLARATION tipo'''
    p[0] = Parametro(p[1], p[3])

def p_parametro_error(p):
    '''parametro : ID DECLARATION error'''
    print("Parametro con tipo mal formado" )
    p[0] = None
    p.parser.error = 1



def p_mparametros(p):
    '''mparametros : mparametros COMMA parametro
                  | parametro
                  | empty'''
    if len(p) == 4:
        p[1].append(p[3])
        p[0] = p[1]
    else:
        p[0] = Parameters([p[1]])


def p_mparametros_error1(p):
    '''mparametros : error COMMA parametro'''
    print("parametros con error en los parametros" )
    p[0] = None
    p.parser.error = 1

def p_funcion_error2(p):
    "funcion : FUN ID LPAREN mparametros RPAREN error BEGIN declaraciones END"
    print("Funcion con locales mal formadas")
    p[0] = None
    p.parser.error = 1

def p_mparametros_error3(p):
    '''mparametros : mparametros COMMA error'''
    print("Parametros con error en el parametro simbolo = '%s' linea = %s" %(p[3].value, p[3].lineno))
    p[0] = None
    p.parser.error = 1



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

def p_local_error(p):
    '''local : local error SEMI
             | local parametro error
             | local funcion error
             | error SEMI
             | funcion error
             | parametro error'''
    if len(p) == 4:
        if p[3] == 'SEMI':
            print ("Error en local simbolo = '%s' linea = %s" %(p[2].value, p[2].lineno))
        else:
            print ("Error en local simbolo = '%s' linea = %s" %(p[3].value, p[3].lineno))
    elif len(p) == 3:
        if p[2] == 'SEMI':
            print ("Error en local simbolo = '%s' linea = %s" %(p[1].value, p[1].lineno))
        else:
            print ("Error en local simbolo = '%s' linea = %s" %(p[1].value, p[1].lineno))
    p[0] = None
    p.parser.error = 1

def p_asignacion(p):
    '''asignacion : ID ASSIGN expresion
                  | ID LCORCH index RCORCH ASSIGN expresion
    '''
    # if len(p) == 4: p[0] = (p[1], p[4])
    # elif len(p) > 6: p[0] = (p[1], p[3], p[7])

def p_asignacion_error(p):
    '''asignacion : ID ASSIGN error
                  | ID LCORCH error RCORCH ASSIGN expresion
                  | ID LCORCH index RCORCH ASSIGN error
                  | ID error index RCORCH ASSIGN expresion
                  | ID error index error ASSIGN expresion
                  | ID LCORCH index error ASSIGN expresion
                  '''
    print ("Error en asignacion")
    p[0] = None
    p.parser.error = 1

def p_declaracion_while(p):
    '''declaracion : WHILE relacion DO declaracion'''
    p[0] = WhileStatement(p[2], p[1])

def p_declaracion_location(p):
    "declaracion : location ASSIGN expresion"

def p_declaracion_while_error(p):
    '''declaracion : WHILE error DO declaracion
                   | WHILE relacion DO error'''
    print ("Error en formacion de declaracion WHILE")
    p[0] = None
    p.parser.error = 1



def p_declaracion_if(p):
    '''declaracion : IF relacion THEN declaracion
                  | IF relacion THEN declaracion ELSE declaracion
    '''
    if len(p) == 5:
        p[0] = IfStatement(p[2], p[4], None) #('IF', p[2], p[4])
    else:
        p[0] = IfStatement(p[2], p[4], p[6])

def p_declaracion_if_error(p):
    '''declaracion : IF error THEN declaracion
                   | IF relacion THEN error
                   | IF relacion THEN declaracion ELSE error'''
    print ("Error en formacion de declaracion IF")
    p[0] = None
    p.parser.error = 1


def p_declaracion_print(p):
    '''
        declaracion : PRINT LPAREN STRING RPAREN
    '''
    p[0] = PrintStatement(p[3])

def p_declaracion_print_error(p):
    '''declaracion : PRINT LPAREN error RPAREN
                   | PRINT LPAREN STRING error
                   | PRINT error STRING RPAREN
                   | PRINT error STRING error'''
    print ("Error en formacion de declaracion PRINT")
    p[0] = None
    p.parser.error = 1

def p_declaracion_write(p):
    '''
        declaracion : WRITE LPAREN expresion RPAREN
    '''
    p[0] = WriteStatements(p[3])

def p_declaracion_write_error(p):
    '''declaracion : WRITE LPAREN error RPAREN
                   | WRITE error expresion RPAREN
                   | WRITE LPAREN expresion error
                   | WRITE error expresion error'''
    print ("Error en formacion de declaracion WRITE")
    p[0] = None
    p.parser.error = 1

def p_declaracion_read(p):
    '''
        declaracion : READ LPAREN location RPAREN
    '''
    p[0] = ReadStatements(p[3])

def p_declaracion_read_error(p):
    '''declaracion : READ LPAREN error RPAREN
                   | READ error location RPAREN
                   | READ LPAREN location error
                   | READ error location error'''
    print ("Error en formacion de declaracion READ")
    p[0] = None
    p.parser.error = 1

def p_declaracion_return(p):
    '''
        declaracion : RETURN expresion
    '''
    p[0] = Return(p[2])


def p_declaracion_return_error(p):
    '''
        declaracion : RETURN error
    '''
    print ("error en formacion de declaracion RETURN")
    p[0] = None
    p.parser.error = 1

def p_declaracion_es(p):
    '''
        declaracion : BEGIN declaraciones END
    '''
    p[0] = Declaraciones([p[2]])



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


def p_declaraciones_dec(p):
    '''declaraciones : declaracion'''
    p[0] = Declaraciones([p[1]])


def p_location(p):
    '''
        location : ID
                 | ID LCORCH expresion RCORCH
    '''
    if len(p) == 2:
        p[0] = Location(p[1])
    else:
        p[0] = LocationArray(p[1], p[3])

def p_index(p):
    "index : expresion"
    p[0] = p[1]


def p_tipo_INT(p):
    ''' tipo : NINT
             | NINT LCORCH expresion RCORCH
    '''
    if len(p) == 5:
        p[0] = ArrayInt(p[3])
    else:
        p[0] = p[1]

def p_tipo_FLOAT(p):
    ''' tipo : NFLOAT
            | NFLOAT LCORCH expresion RCORCH
    '''
    if len(p) == 5:
        p[0] = ArrayFloat(p[3])
    else:
        p[0] = p[1]

def p_expresion_operadores_bin(p):
    '''  expresion : expresion PLUS expresion
                  | expresion MINUS expresion
                  | expresion TIMES expresion
                  | expresion DIVIDE expresion
                  '''
    p[0] = BinaryOp(p[2], p[1], p[3])


def p_expresion_signo(p):
    ''' expresion : MINUS expresion %prec UNARY
                 | PLUS expresion %prec UNARY '''

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
    if len(p) > 4:
        if p[2] == 'LPAREN':
            p[0] = ExpresionFun(p[1], p[3])
        else:
            p[0] = ExpresionIdArray(p[1], p[3])
    else:
        p[0] = ExpresionID(p[1])

def p_expresion_ID_error(p):
    '''expresion : ID LPAREN error RPAREN
                 | ID LPAREN argumentos error
                 | ID error argumentos RPAREN
                 | ID LPAREN error
                 | ID error expresion RCORCH'''
    print ("Error en formacion de expresion ID")
    p[0] = None
    p.parser.error = 1


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
        if p[1] == 'LPAREN':
            p[0] = p[2]
        else:
            p[0] = RelOp(p[2], p[1], p[3])
    if len(p) == 3:
            p[0] = UnaryOp(p[1], p[2])


def p_empty(p):
    'empty :'
    pass

def p_error(p):
    # x= yacc.token()
    # print ("Error simbolo '%s' linea = %s" %(x.value, x.lineno))
    if p:
        print ("Error simbolo '%s' linea = %s" %(p.value, p.lineno)),
    else:
        print("EOF Syntax error. No more input.")




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
    #print "Succeded"
    # Output the resulting parse tree structure


