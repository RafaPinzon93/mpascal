! Creado por mpascal.py
! Rafael Pinzon, Daniel Osorio, Alejandro Lopez IS744 (2014-2)
    .section   ".text"

! program

! function: LexToken(ID,'fib',2,26) (start) 

! ifelse (start)
! expr := pop
!   if(expr)
! goto test
! done:
! ifelse (End)
! function: LexToken(ID,'fib',2,26) (end)

! function: LexToken(ID,'main',9,133) (start) 

! print (start)
! print (End)

! read (start)
! read (End)

! assign (start)
!  push ID x
! expr := pop
! assign(expr)
! assign (End)

! write (start)
!  push ID r
! expr := pop
!   write(expr)
! write (End)
! function: LexToken(ID,'main',9,133) (end)
    .section   ".rodata"
.L0:   .asciz  ""Entre un nuemro\n""

