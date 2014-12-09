! Creado por mpascal.py
! Rafael Pinzon, Daniel Osorio, Alejandro Lopez IS744 (2014-2)

    .section   ".text"

! program

! function: fact (start) 

! assign (start)
!  push 1
!  a := pop
! assign (end)

! if (start)
!  relop := pop
!  if not relop: goto .L1

! assign (start)
!  push 1
!  a := pop
! assign (end)

.L1:
! if (end)

! function: fact (end)

! function: main (start) 

    .global main

 main:

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

! function: main (end)

    .section   ".rodata"
.L2:   .asciz  ""Entre un numero\n""

