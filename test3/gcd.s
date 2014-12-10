! Creado por mpascal.py
! Rafael Pinzon, Daniel Osorio, Alejandro Lopez IS744 (2014-2)

    .section   ".text"

! program

! function: gcd (start) 

gcd:
        save sp, -80, sp

! assign (start)
!  push y
!  g := pop
! assign (end)

! while (start)

.L1:
!  push x
!  push 0
!  GT
!  relop := pop
!  if not relop: goto .L2

! assign (start)
!  push x
!  g := pop
! assign (end)

! assign (start)
!  push y
!  push y
!  push x
!  div
!  push x
!  mult
!  sub 
!  x := pop
! assign (end)

! assign (start)
!  push g
!  y := pop
! assign (end)

!  goto .L1

.L2:

! while (end)
              ret
              restore

!function: gcd (end)

! function: main (start) 

    .global main

main:
        save sp, -80, sp
        sethi %hi(.Ln), %o0
        or    %o0, %lo(.Ln), %o0
        call  flprint 
        nop

! print (start)
! print (end)

! read (start)
! read (End)

! read (start)
! read (End)

! assign (start)
!  push x
!  push y
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

.L3:   .asciz  ""Entre dos numeros\n""

