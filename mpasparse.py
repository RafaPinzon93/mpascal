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
        funcion : FUN ID LPAREN mparametros RPAREN local BEGIN declaraciones END
    '''
    p[0] = Funcion(p.slice[2], p[4], p[6], p[8])

def p_funcion_error1(p):
    "funcion : FUN ID LPAREN error RPAREN local BEGIN declaraciones END"
    print("Funcion con parametros invalidos ")
    p[0] = None
    p.parser.error = 1

def p_funcion_error2(p):
    "funcion : FUN ID LPAREN mparametros RPAREN error BEGIN declaraciones END"
    print("Se esperaba una expresion valida")
    p[0] = None
    p.parser.error = 1


def p_funcion_error3(p):
    "funcion : FUN ID LPAREN mparametros RPAREN local BEGIN error END"
    print("Se esperaba un END al final de la funcion")
    p[0] = None


def p_parametro(p):
    '''parametro : ID DECLARATION tipo'''
    p[0] = Parametro(p.slice[1], p[3])

def p_parametro_error(p):
    '''parametro : ID DECLARATION error'''
    print("se esperaba un tipo de declaracion conocido" )
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
    print("parametros mal escritos" )
    p[0] = None
    p.parser.error = 1

def p_mparametros_error3(p):
    '''mparametros : mparametros COMMA error'''
    print("Parametros con error en el parametro simbolo = '%s' linea = %s" %(p[3].value, p[3].lineno))
    p[0] = None
    p.parser.error = 1


def p_local(p):

    '''local : locales
              | empty
    '''
    p[0] = p[1]


def p_locales(p):
    '''
        locales : locales parametro SEMI
              | locales funcion SEMI
              | parametro SEMI
              | funcion SEMI
    '''
    if len(p) == 4:
        p[1].append(p[2])
        p[0] = p[1]
    else: p[0] = Locales([p[1]])
# def p_locales_empty(p):
#     '''locales : empty '''
#     p[0] = p[1]


def p_locales_error(p):
    '''locales : locales error SEMI
             | locales parametro error
             | locales funcion error
             | error SEMI
             | funcion error
             | parametro error'''
    p[0] = None
    p.parser.error = 1

def p_asignacion(p):
    "asignacion : ID ASSIGN expresion"
    p[0] = Asignacion(p.slice[1], p[3])

def p_asignacion_error(p):
    '''asignacion : ID error index error ASSIGN expresion
                  '''
    print ("Error en asignacion")
    p[0] = None
    p.parser.error = 1

def p_asignacion_error1(p):
    '''asignacion : ID LCORCH index RCORCH ASSIGN error
                  '''
    print ("se esperaba un SEMI")
    p[0] = None
    p.parser.error = 1

def p_asignacion_error2(p):
    '''asignacion : ID LCORCH error RCORCH ASSIGN expresion
                  '''
    print ("se esperaba un index entre los corchetes")
    p[0] = None
    p.parser.error = 1

def p_asignacion_error3(p):
    '''asignacion : ID error index RCORCH ASSIGN expresion'''
    print ("se esperaba el corchete izquierdo")
    p[0] = None
    p.parser.error = 1

def p_asignacion_error4(p):
    '''asignacion : ID LCORCH index error ASSIGN expresion
                  '''
    print ("se esperaba el corchete derecho")
    p[0] = None
    p.parser.error = 1

def p_asignacion_error5(p):
    '''asignacion : ID ASSIGN error
                  '''
    print ("se esperaba un SEMI")
    p[0] = None
    p.parser.error = 1


def p_asignacion_index(p):
    "asignacion : ID LCORCH index RCORCH ASSIGN expresion"
    p[0] = AssignVecStatement(p.slice[1], p[3], p[6])


def p_declaracion_while(p):
    '''declaracion : WHILE relacion DO declaracion'''
    p[0] = WhileStatement(p[2], p[4])

def p_declaracion_while_error(p):
    '''declaracion : WHILE error DO declaracion
                   | WHILE relacion DO error'''
    print ("se esperaba relacion valida para declaracion WHILE")
    p[0] = None
    p.parser.error = 1

def p_declaracion_if(p):
    '''declaracion : IF relacion THEN declaracion
                  | IF relacion THEN declaracion ELSE declaracion
    '''
    if len(p) == 5:
        p[0] = IfStatement(p[2], p[4], linea= p.lineno(3)) #('IF', p[2], p[4])
    else:
        p[0] = IfStatementElse(p[2], p[4], p[6], lineaT= p.lineno(3), lineaE= p.lineno(5))

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
    print ("Se esperaba una expresion valida")
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
    print ("Se esperaba una expresion valida en declaracion WRITE")
    p[0] = None
    p.parser.error = 1

def p_declaracion_read(p):
    '''
        declaracion : READ LPAREN ID LCORCH expresion RCORCH RPAREN
                    | READ LPAREN ID RPAREN
    '''
    if len(p) == 5:
        p[0] = ReadStatements(p.slice[3], None)
    else:
        p[0] = ReadStatements(p.slice[3], p[5])

def p_declaracion_read_error(p):
    '''declaracion : READ LPAREN error RPAREN
                   | READ LPAREN ID error
                   | READ error ID RPAREN
    '''
    print ("Se esperaba una expresion valida en declaracion READ")
    p[0] = None
    p.parser.error = 1

def p_declaracion_return(p):
    '''
        declaracion : RETURN expresion
    '''
    p[0] = Return(p[2], p.slice[1])

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
    #p[0] = p[2]



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
    p[0] = p[1]



def p_declaraciones(p):
    '''declaraciones : declaraciones SEMI declaracion'''
    p[0] = p[1]
    p[0].append(p[3])



def p_declaraciones_dec(p):
    '''declaraciones : declaracion'''
    p[0] = Declaraciones([p[1]])



# def p_location(p):
#     '''
#         location : ID
#                  | ID LCORCH expresion RCORCH
#     '''
#     if len(p) == 2:
#         p[0] = Location(p[1])
#     else:
#         p[0] = LocationArray(p[1], p[3])

def p_index(p):
    "index : expresion"
    p[0] = p[1]


def p_tipo_INT(p):
    ''' tipo : NINT
             | NINT LCORCH expresion RCORCH
    '''
    if len(p) == 5:
        p[0] = ArrayInt(p[1], p[3], linea= p.lineno(1))
    else:
        p[0] = ArrayInt(p[1], None, linea= p.lineno(1))

def p_tipo_FLOAT(p):
    ''' tipo : NFLOAT
             | NFLOAT LCORCH expresion RCORCH
    '''
    if len(p) == 5:
        p[0] = ArrayFloat(p[1],p.slice[3], linea= p.lineno(1))
    else:
        p[0] = ArrayFloat(p[1], None, linea= p.lineno(1))

def p_expresion_operadores_bin(p):
    '''  expresion : expresion PLUS expresion
                  | expresion MINUS expresion
                  | expresion TIMES expresion
                  | expresion DIVIDE expresion
                  '''
    p[0] = BinaryOp(p[2], p[1], p[3], linea = p.lineno(2))


def p_expresion_signo(p):
    ''' expresion : MINUS expresion %prec UNARY
                 | PLUS expresion %prec UNARY '''

    p[0] = UnaryOp(p[1], p[2])


def p_expresion_parent(p):
    '''
        expresion :  LPAREN expresion RPAREN
                  |  LPAREN RPAREN
    '''
    if len(p) == 4:
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
        if p[2] == '(':
            p[0] = ExpresionFun(p.slice[1], p[3], linea= p.lineno(1))
        else:
            p[0] = ExpresionIdArray(p.slice[1], p[3])
    elif len(p) == 4:
        p[0] = ExpresionFun(p.slice[1], None, linea= p.lineno(1))
    else:
        p[0] = ExpresionID(p.slice[1])



def p_expresion_numero(p):
    '''expresion : numero'''
    p[0] = p[1]


def p_expresion_INT(p):
    "expresion : NINT LPAREN expresion RPAREN "
    p[0] = Nint(p[1], p[3])

def p_expresion_FLOAT(p):
    '''expresion : NFLOAT LPAREN expresion RPAREN '''
    p[0] = Nfloat(p[1],p[3])


def p_numero_INTEGER(p):
    '''numero : INTEGER'''
    p[0] = NumeroInt(p.slice[1])

def p_numero_FLOAT(p):
     '''numero : FLOAT '''
     p[0] = NumeroFloat(p.slice[1])

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
        if p[1] == '(':
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
        print ("Error en simbolo '%s' linea = %s" %(p.value, p.lineno)),
    else:
        print("EOF Syntax error. No more input.")




# Build the parser


# print str
# Give the lexer some input

def make_parser():
    parser = yacc.yacc()
    return parser

def sintactico():
    import mpaslex
    import sys
    lexer = mpaslex.make_lexer()
    parser = make_parser()
    program = parser.parse(open(sys.argv[1]).read())
    program.pprint()
    program.semantico()
    print "Succeded"
    return program
    # Output the resulting parse tree structure
sintactico()
