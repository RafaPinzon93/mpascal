! Creado por mpascal.py
! Rafael Pinzon, Daniel Osorio, Alejandro Lopez IS744 (2014-2)

    .section   ".text"

! program

! function: mrgsort (start) 

mrgsort:
        save sp, -120, sp

! if (start)
!  push p
!  push r
!  LT
!  relop := pop
!  if not relop: goto .L1

.L1:
! if (end)
              ret
              restore

!function: mrgsort (end)

! function: print_arr (start) 

print_arr:
        save sp, -120, sp

! assign (start)
!  push 0
!  i := pop
! assign (end)

! while (start)

.L2:
!  push i
!  push nnums
!  LT
!  relop := pop
!  if not relop: goto .L3

! write (start)
!  push nums
!  expr := pop
!  write(expr)
! write (end)
        sethi %hi(.Ln), %o0
        or    %o0, %lo(.Ln), %o0
        call  flprint 
        nop

! print (start)
! print (end)

!  goto .L2

.L3:

! while (end)
        sethi %hi(.Ln), %o0
        or    %o0, %lo(.Ln), %o0
        call  flprint 
        nop

! print (start)
! print (end)
              ret
              restore

!function: print_arr (end)

! function: main (start) 

    .global main

main:
        save sp, -160, sp

! assign (start)
!  push 0
!  i := pop
! assign (end)
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

.L4:   .asciz  "" ""

.L5:   .asciz  ""\n""

.L6:   .asciz  ""lista desordenada es:\n""

