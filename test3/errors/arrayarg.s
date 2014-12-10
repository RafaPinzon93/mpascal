! Creado por mpascal.py
! Rafael Pinzon, Daniel Osorio, Alejandro Lopez IS744 (2014-2)

    .section   ".text"

! program

! function: foo (start) 

foo:
        save sp, -560, sp

! assign (start)
!  push 0
!  i := pop
! assign (end)

! while (start)

.L1:
!  push i
!  push 40
!  LT
!  relop := pop
!  if not relop: goto .L2

! assign (start)
!  push i
!  push 1
!  add
!  i := pop
! assign (end)

!  goto .L1

.L2:

! while (end)
              ret
              restore

!function: foo (end)

! function: main (start) 

    .global main

main:
        save sp, -760, sp
.Ln:
             mov 0, %o0
             call _exit
             nop
             ret
             restore

!function: main (end)

    .section   ".rodata"

