! Creado por mpascal.py
! Rafael Pinzon, Daniel Osorio, Alejandro Lopez IS744 (2014-2)

    .section   ".text"

! program

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

! assign (start)
!  push 1
!  i := pop
! assign (end)

! while (start)

.L2:
!  push i
!  push 10
!  LE
!  relop := pop
!  if not relop: goto .L3

! write (start)
!  push i
!  expr := pop
!  write(expr)
! write (end)
        sethi %hi(.Ln), %o0
        or    %o0, %lo(.Ln), %o0
        call  flprint 
        nop

! print (start)
! print (end)

! assign (start)
!  push i
!  push 1
!  add
!  i := pop
! assign (end)

!  goto .L2

.L3:

! while (end)
        sethi %hi(.Ln), %o0
        or    %o0, %lo(.Ln), %o0
        call  flprint 
        nop

! print (start)
! print (end)
.Ln:
             mov 0, %o0
             call _exit
             nop
             ret
             restore

!function: main (end)

    .section   ".rodata"

.L1:   .asciz  ""Contando a 10\n""

.L4:   .asciz  ""\n""

.L5:   .asciz  ""Adios\n""

