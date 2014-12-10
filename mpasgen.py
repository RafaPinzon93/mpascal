from mpasast import *

import StringIO
data = StringIO.StringIO()

numberlabel = 1
marcoPila1 = 0
marcoPila = 0

def new_label():
    global numberlabel
    cadena = '.L' + str(numberlabel)
    numberlabel+=1
    return cadena

def generate(file, top):
    print >>file, "! Creado por mpascal.py"
    print >>file, "! Rafael Pinzon, Daniel Osorio, Alejandro Lopez IS744 (2014-2)"
    print >>file, '\n    .section   ".text"'
    print >>data, '\n    .section   ".rodata"'
    emit_program(file,top)
    print >>file, data.getvalue()

def emit_program(out,top):
    print >>out,"\n! program"
    funclist = top.funciones
    for f in funclist:
        emit_function(out,f)

def emit_function(out,func):
    print >>out,"\n! function: %s (start) " % func.ID.value

    if func.locales != None:
        para = func.parametros.param_decls
        local = func.locales.locales
        emit_localpara(out, local, para)
    else:
        para = func.parametros.param_decls
        emit_para1(out,para)



    if (func.ID.value == 'main'):
        print >>out,  "\n    .global main"
        print >>out,  "\nmain:"
        print >>out, "        save sp, -%i, sp" %marcoPila1
        statements = func.declaraciones.declaraciones
        emit_statements(out, statements)
        print >>out, ".Ln:"
        print >>out, "             mov 0, %o0"
        print >>out, "             call _exit"
        print >>out, "             nop"
        print >>out, "             ret"
        print >>out, "             restore"

    else:
        print >>out, "\n%s:"% func.ID.value
        print >>out, "        save sp, -%i, sp" %marcoPila1
        statements = func.declaraciones.declaraciones
        emit_statements(out, statements)
        print >>out, "              ret"
        print >>out, "              restore"
    print >>out,"\n!function: %s (end)" % func.ID.value

def emit_statements(out,statements):
    for s in statements:
        emit_statement(out,s)

def emit_localpara(out,local,para):
    global marcoPila
    global marcoPila1
    if local != None:
        for s in local:
            if s.tipo.valor != None:
                marcoPila += int(s.tipo.expresion.value.numero.value)*4
            marcoPila += 4
            emit_local(out,s)

    for s in para:
        if s != None:
            if  s.tipo.valor != None:
                   marcoPila += int(s.tipo.expresion.value.numero.value)*4
        if s == None and marcoPila > 0:
            marcoPila -= 4
        emit_para(out,s)
        marcoPila +=4

    marcoPila1 = marcoPila + 64
    b= marcoPila1%8

    if b != 0:
        marcoPila1 += 4
    marcoPila = 0

def emit_para1(out,para):
    global marcoPila
    global marcoPila1

    for s in para:
        if s != None:
            if  s.tipo.valor != None:
                   marcoPila += int(s.tipo.expresion.value.numero.value)*4
        if s == None and marcoPila > 0:
            marcoPila -= 4
        emit_para(out,s)

        marcoPila +=4
    marcoPila1 = marcoPila + 64
    b= marcoPila1%8

    if b != 0:
        marcoPila1 += 4
    marcoPila = 0


def emit_statement(out,s):
    if isinstance(s,PrintStatement):
        emit_print(out,s)
    elif isinstance(s,ReadStatements):
        emit_read(out,s)
    elif isinstance(s,WriteStatements):
        emit_write(out,s)
    elif isinstance(s,WhileStatement):
        emit_while(out,s)
    elif isinstance(s,IfStatement):
        emit_if(out,s)
    elif isinstance(s,IfStatementElse):
        emit_ifelse(out,s)
    elif isinstance(s,Asignacion):
        emit_assign(out,s)




def emit_print(out,s):
    value = s.expr
    label = new_label()
    print >>out, "        sethi %hi(.Ln), %o0"
    print >>out, "        or    %o0, %lo(.Ln), %o0"
    print >>out, "        call  flprint "
    print >>out, "        nop"
    print >>out, "\n! print (start)"
    print >>data, '\n%s:   .asciz  "%s"' % (label, value)
    print >>out, "! print (end)"

def emit_read(out,s):
    print >>out, "\n! read (start)"
    print >>out, "! read (End)"

def emit_write(out,s):
    print >>out, "\n! write (start)"
    expr = s.expr
    eval_expression(out,expr)
    print >>out, "!  expr := pop"
    print >>out, "!  write(expr)"
    print >>out, "! write (end)"

def emit_while(out,s):
    print >>out, "\n! while (start)"
    test_label = new_label()
    done_label = new_label()

    print >>out, "\n%s:" % test_label

    statement = s.body
    emit_statement(out,statement)
    expr = s.condition
    eval_expression(out,expr)
    print >>out, "!  relop := pop"
    print >>out, "!  if not relop: goto %s" % done_label
    expr1 = s.body.declaraciones[0].declaraciones
    emit_statements(out,expr1)


    print >>out, "\n!  goto %s" % test_label
    print >>out, "\n%s:" % done_label
    print >>out, "\n! while (end)"

def emit_if(out,s):
    print >>out, "\n! if (start)"
    done_label = new_label()


    expr = s.condition
    eval_expression(out,expr)

    print >>out, "!  relop := pop"
    print >>out, "!  if not relop: goto %s" % done_label
    if isinstance(s.then_b,Declaraciones):
        expr1 = s.then_b
        emit_statements(out,expr1)
    else :
        emit_statement(out,s.then_b)

    print >>out, "\n%s:" % done_label
    print >>out, "! if (end)"

def emit_ifelse(out,s):
    print >>out, "\n! ifelse (start)"

    done_label = new_label()
    else_label = new_label()

    expr = s.condition
    eval_expression(out,expr)
    print >>out, "!  relop := pop"
    print >>out, "!  if not relop: goto else label: %s" % else_label

    if isinstance(s.then_b,Declaraciones):
        expr1 = s.then_b
        emit_statements(out,expr1)
    else :
        emit_statement(out,s.then_b)

    print >>out, "!go to done %s" % done_label

    print >>out, "%s: !else_label" % else_label
    if isinstance(s.else_b, Declaraciones):
        expr2 = s.else_b.declaraciones[0].declaraciones
        emit_statements(out,expr2)
    else :
        emit_statement(out,s.then_b)

    print >>out, "\n%s: !done_label" % done_label
    print >>out, "! ifelse (end)"

def emit_assign(out,s):
    print >>out, "\n! assign (start)"
    expr = s.expresion
    eval_expression(out,expr)
    print >>out, "!  %s := pop"%s.ID.value
    print >>out, "! assign (end)"

def emit_local(out,func):
    #print marcoPila
    expr = func
    #print expr


def emit_para(out,func):
    expr = func
    #print expr

def eval_expression(out, expr):
    if isinstance(expr, NumeroFloat):
        print >>out, "!  push", expr.numero.value
    if isinstance(expr, NumeroInt):
        print >>out, "!  push", expr.numero.value
    if isinstance(expr, ExpresionID):
        print >>out, "!  push", expr.ID.value
    if isinstance(expr, ExpresionFun):
        for argumento in expr.arguments.argumentos:
            eval_expression(out, argumento)
    if isinstance(expr, ExpresionIdArray):
        print >>out, "!  push", expr.ID.value
    if isinstance(expr, RelOp):
        left = expr.left
        right = expr.right
        if expr.op == '<':
            eval_expression(out, left)
            eval_expression(out, right)
            print >>out, "!  LT"
        elif expr.op == '<=':
            eval_expression(out, left)
            eval_expression(out, right)
            print >>out, "!  LE"
        elif expr.op == '>':
            eval_expression(out, left)
            eval_expression(out, right)
            print >>out, "!  GT"
        elif expr.op == '!=':
            eval_expression(out, left)
            eval_expression(out, right)
            print >>out, "!  NE"
    if (isinstance(expr, BinaryOp)):
        left = expr.left
        right = expr.right
        if expr.op == '+':
            eval_expression(out, left)
            eval_expression(out, right)
            print >>out, "!  add"
        elif expr.op == '-':
            eval_expression(out, left)
            eval_expression(out, right)
            print >>out, "!  sub "
        elif expr.op == '*':
            eval_expression(out, left)
            eval_expression(out, right)
            print >>out, "!  mult"
        elif expr.op == '/':
            eval_expression(out, left)
            eval_expression(out, right)
            print >>out, "!  div"
    if isinstance(expr,UnaryOp):
        left = expr.left
        if expr.op == '-':
            eval_expression(out,left)
            print >>out, "! pop", expr.left
            print >>out, "! push uminus",expr.left