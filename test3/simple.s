! Creado por mpascal.py
! Rafael Pinzon, Daniel Osorio, Alejandro Lopez IS744 (2014-2)

    .section   ".text"

! program

! function: fact (start) 

fact:
        save sp, -72, sp

! assign (start)
!  push 1
!  r := pop
! assign (end)

! while (start)

.L1:
!  push n
!  push 0
!  GT
!  relop := pop
!  if not relop: goto .L2

! assign (start)
!  push r
!  push n
!  mult
!  r := pop
! assign (end)

! assign (start)
!  push n
!  push 1
!  sub 
!  n := pop
! assign (end)

!  goto .L1

.L2:

! while (end)
              ret
              restore

!function: fact (end)

! function: main (start) 

    .global main

main:
        save sp, -72, sp
        sethi %hi(.Ln), %o0
        or    %o0, %lo(.Ln), %o0
        call  flprint 
        nop

! print (start)
! print (end)
        sethi %hi(.Ln), %o0
        or    %o0, %lo(.Ln), %o0
        call  flprint 
        nop

! print (start)
! print (end)

! read (start)
! read (End)

! write (start)
!  push n
!  expr := pop
!  write(expr)
! write (end)
.Ln:
             mov 0, %o0
             call _exit
             nop
             ret
             restore

!function: main (end)

    .section   ".rodata"

.L3:   .asciz  ""Hola. Soy un factorial sencillo.\n""

.L4:   .asciz  ""Entre n :""

