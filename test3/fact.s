! Creado por mpascal.py
! Rafael Pinzon, Daniel Osorio, Alejandro Lopez IS744 (2014-2)

    .section   ".text"

! program

! function: fact (start) 

fact:
        save sp, -72, sp

! ifelse (start)
!  relop := pop
!  if not relop: goto else label: .L2
!go to done .L1
.L2: !else_label

.L1: !done_label
! ifelse (end)
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

! read (start)
! read (End)

! assign (start)
!  push x
!  r := pop
! assign (end)

! write (start)
!  push r
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

.L3:   .asciz  ""Entre un numero\n""

