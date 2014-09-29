Integrantes del grupo:
	- Alejandro López Correa
	- Daniel Osorio Morales
	- Rafael Pinzón Rivera

Expresiones regulares que vale la pena mensionar:

 Para los flotanes: ((0|[1-9][0-9]*)\.[0-9]+)([eE][-+]?[0-9]+)?|([1-9][0-9]*|0)([eE][-+]?[0-9]+)
 con esta expresión reconocerá todas los flotantes tipo:
    0.0
    0.123
    10.12
    1.0e+0
    1.0e-1
    1.0e2
    0e123
    12e021

Para las "Strings": \"((\\["\\n])|((\\\")*[^"\\\n](\\\")*))*?\"
se reconocerá la menor cantidad de expresiones ('*?' non-greedy) que comiencen con ["] seguido por 0 o más expresiones  que contengan caracteres de escape (\", \n, \\), ó cualquier caracter que no contenga [", \\, \n], antecedido ó seguido, por 0 o más (\").

Para los comentarios inválidos: (/\*(.|\n)*(/\*)*)|\*/
Le añadimos a diferencia de los comentarios válidos que reconociera más '/*' ó que reconociera un comentario cerrado sin abrir '*/'
