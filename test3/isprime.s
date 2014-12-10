! Creado por mpascal.py
! Rafael Pinzon, Daniel Osorio, Alejandro Lopez IS744 (2014-2)

    .section   ".text"

! program

! function: isprime (start) 

isprime:
        save sp, -72, sp

! assign (start)
!  push 2
!  i := pop
! assign (end)

! while (start)

.L1:
!  push i
!  push n
!  LT
!  relop := pop
!  if not relop: goto .L2

! if (start)
!  relop := pop
!  if not relop: goto .L3

.L3:
! if (end)

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

!function: isprime (end)

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
!  push x
!  expr := pop
!  write(expr)
! write (end)

! ifelse (start)
!  relop := pop
!  if not relop: goto else label: .L6
        sethi %hi(.Ln), %o0
        or    %o0, %lo(.Ln), %o0
        call  flprint 
        nop

! print (start)
! print (end)
!go to done .L5
.L6: !else_label
        sethi %hi(.Ln), %o0
        or    %o0, %lo(.Ln), %o0
        call  flprint 
        nop

! print (start)
! print (end)

.L5: !done_label
! ifelse (end)
.Ln:
             mov 0, %o0
             call _exit
             nop
             ret
             restore

!function: main (end)

    .section   ".rodata"

.L4:   .asciz  ""Entre un numero\n""

.L7:   .asciz  "" es primo\n""

.L8:   .asciz  "" es primo\n""

