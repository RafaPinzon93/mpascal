! Creado por mpascal.py
! Rafael Pinzon, Daniel Osorio, Alejandro Lopez IS744 (2014-2)

    .section   ".text"

! program

! function: sum (start) 

sum:
        save sp, -4080, sp

! assign (start)
!  push 0
!  s := pop
! assign (end)

! assign (start)
!  push 0
!  i := pop
! assign (end)

! while (start)

.L1:
!  push i
!  push n
!  LT
!  relop := pop
!  if not relop: goto .L2

! assign (start)
!  push s
!  push a
!  add
!  s := pop
! assign (end)

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

!function: sum (end)

! function: main (start) 

    .global main

main:
        save sp, -4080, sp
        sethi %hi(.Ln), %o0
        or    %o0, %lo(.Ln), %o0
        call  flprint 
        nop

! print (start)
! print (end)

! read (start)
! read (End)

! ifelse (start)
!  relop := pop
!  if not relop: goto else label: .L5
!go to done .L4
.L5: !else_label

.L4: !done_label
! ifelse (end)
.Ln:
             mov 0, %o0
             call _exit
             nop
             ret
             restore

!function: main (end)

    .section   ".rodata"

.L3:   .asciz  ""Entre un numero n : ""

