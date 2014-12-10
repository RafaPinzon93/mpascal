! Creado por mpascal.py
! Rafael Pinzon, Daniel Osorio, Alejandro Lopez IS744 (2014-2)

    .section   ".text"

! program

! function: foo (start) 

foo:
        save sp, -4080, sp

! assign (start)
!  push 3.434
!  y := pop
! assign (end)
              ret
              restore

!function: foo (end)

    .section   ".rodata"

