! Creado por mpascal.py
! Rafael Pinzon, Daniel Osorio, Alejandro Lopez IS744 (2014-2)

    .section   ".text"

! program

! function: bar (start) 

bar:
        save sp, -88, sp

! assign (start)
!  push b
!  push 5.0
!  add
!  x := pop
! assign (end)

! write (start)
!  push x
!  expr := pop
!  write(expr)
! write (end)
              ret
              restore

!function: bar (end)

! function: main (start) 

    .global main

main:
        save sp, -72, sp

! assign (start)
!  push 0
!  y := pop
! assign (end)
.Ln:
             mov 0, %o0
             call _exit
             nop
             ret
             restore

!function: main (end)

    .section   ".rodata"

