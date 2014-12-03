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
    print >>out, "! write (End)"

def emit_while(out,s):
    print >>out, "\n! while (start)"
    statement = s.body
    emit_statement(out,statement)
    print >>out, "! while (End)"

def emit_if(out,s):
    print >>out, "\n! if (start)"
    print >>out, "! if (End)"

def emit_ifelse(out,s):
    print >>out, "\n! ifelse (start)"
    print >>out, "! if (End)"

def emit_assign(out,s):
    print >>out, "\n! assign (start)"
    print >>out, "! assign (End)"