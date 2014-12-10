! Creado por mpascal.py
! Rafael Pinzon, Daniel Osorio, Alejandro Lopez IS744 (2014-2)

    .section   ".text"

! program

! function: foo (start) 

foo:
        save sp, -8072, sp
              ret
              restore

!function: foo (end)

    .section   ".rodata"

