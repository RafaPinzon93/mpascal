! Creado por mpascal.py
! Rafael Pinzon, Daniel Osorio, Alejandro Lopez IS744 (2014-2)

    .section   ".text"

! program

! function: main (start) 

    .global main

 main:

! read (start)
! read (End)

! read (start)
! read (End)

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

! write (start)
!  push g
!  expr := pop
!  write(expr)
! write (end)

! function: main (end)

    .section   ".rodata"

