from mpasast import *

def generate (file, top):
    print >>file, "! Creado por mpascal.py"
    print >>file, "! Rafael Pinzon, Daniel Osorio, Alejandro Lopez IS744 (2014-2)"
    emit_program(file,top)

def emit_program(out,top):
    print >>out,"\n! program"
    funclist = top.funciones
    for f in funclist:
        emit_function(out,f)

def emit_function(out,func):
    print >>out,"\n! function: %s (start) " % func.ID

    statements = func.declaraciones.declaraciones
    emit_statements(out, statements)

    print >>out,"! function: %s (end)" % func.ID

def emit_statements(out,statements):
    for s in statements:
        emit_statement(out,s)

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
    elif isinstance(s,Asignacion) :
        emit_assign(out,s)

def emit_print(out,s):
    print >>out, "\n! print (start)"
    print >>out, "! print (End)"

def emit_read(out,s):
    print >>out, "\n! read (start)"
    print >>out, "! read (End)"

def emit_write(out,s):
    print >>out, "\n! write (start)"
    expr = s.expr
    eval_expression(out,expr)
    print >>out, "! expr := pop"
    print >>out, "!   write(expr)"
    print >>out, "! write (End)"

def emit_while(out,s):
    print >>out, "\n! while (start)"
    print >>out, "! test:"


    statement = s.body
    emit_statement(out,statement)
    expr = s.condition
    eval_expression(out,expr)
    print >>out, "! expr := pop"
    print >>out, "! if not relop: goto done"
    expr1 = s.body.declaraciones[0].declaraciones
    emit_statements(out,expr1)

    print >>out, "! goto test"
    print >>out, "! done:"
    print >>out, "!   while(expr)"
    print >>out, "! while (End)"

def emit_if(out,s):
    print >>out, "\n! if (start)"
    print >>out, "! test:"

    expr = s.condition
    eval_expression(out,expr)

    print >>out, "! expr := pop"
    print >>out, "!   if(expr)"

    expr1 = s.then_b.declaraciones[0].declaraciones
    emit_statements(out,expr1)

    print >>out, "! goto test"
    print >>out, "! done:"
    print >>out, "! if (End)"

def emit_ifelse(out,s):
    print >>out, "\n! ifelse (start)"
    expr = s.condition
    eval_expression(out,expr)
    print >>out, "! expr := pop"
    print >>out, "!   if(expr)"

    expr1 = s.then_b.declaraciones[0].declaraciones
    emit_statements(out,expr1)

    expr2 = s.else_b.declaraciones[0].declaraciones
    emit_statements(out,expr2)


    print >>out, "! goto test"
    print >>out, "! done:"
    print >>out, "! ifelse (End)"

def emit_assign(out,s):
    print >>out, "\n! assign (start)"
    expr = s.expresion
    eval_expression(out,expr)
    print >>out, "! expr := pop"
    print >>out, "! assign(expr)"
    print >>out, "! assign (End)"



def eval_expression(out, expr):
    if isinstance(expr, NumeroFloat):
        print >>out, "!  push", expr
    if isinstance(expr, NumeroInt):
        print >>out, "!  push", expr
    if isinstance(expr, ExpresionID):
        print >>out, "!  push", expr
    if isinstance(expr, ExpresionIdArray):
        print >>out, "!  push", expr
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
            print >>out, "! add"
        elif expr.op == '-':
            eval_expression(out, left)
            eval_expression(out, right)
            print >>out, "! sub "
        elif expr.op == '*':
            eval_expression(out, left)
            eval_expression(out, right)
            print >>out, "! Mult"
        elif expr.op == '/':
            eval_expression(out, left)
            eval_expression(out, right)
            print >>out, "! Div"
    if isinstance(expr,UnaryOp):
        left = expr.left
        if expr.op == '-':
            eval_expression(out,left)
            print >>out, "! pop", expr.left
            print >>out, "! push uminus",expr.left



