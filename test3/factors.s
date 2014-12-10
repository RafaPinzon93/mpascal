! Creado por mpascal.py
! Rafael Pinzon, Daniel Osorio, Alejandro Lopez IS744 (2014-2)

    .section   ".text"

! program

! function: mod (start) 

mod:
        save sp, -72, sp
              ret
              restore

!function: mod (end)

! function: factor (start) 

factor:
        save sp, -4176, sp

! assign (start)
!  push 1
!  nfacts := pop
! assign (end)

! assign (start)
!  push 2
!  i := pop
! assign (end)

! while (start)

.L1:
!  push i
!  push n
!  LE
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

!function: factor (end)

! function: print_arr (start) 

print_arr:
        save sp, -4176, sp

! assign (start)
!  push 0
!  i := pop
! assign (end)

! while (start)

.L4:
!  push i
!  push nelem
!  LT
!  relop := pop
!  if not relop: goto .L5

! write (start)
!  push a
!  expr := pop
!  write(expr)
! write (end)
        sethi %hi(.Ln), %o0
        or    %o0, %lo(.Ln), %o0
        call  flprint 
        nop

! print (start)
! print (end)

! if (start)
!  relop := pop
!  if not relop: goto .L7
        sethi %hi(.Ln), %o0
        or    %o0, %lo(.Ln), %o0
        call  flprint 
        nop

! print (start)
! print (end)

.L7:
! if (end)

! assign (start)
!  push i
!  push 1
!  add
!  i := pop
! assign (end)

!  goto .L4

.L5:

! while (end)
              ret
              restore

!function: print_arr (end)

! function: main (start) 

    .global main

main:
        save sp, -4176, sp
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
!  push results
!  nfs := pop
! assign (end)
.Ln:
             mov 0, %o0
             call _exit
             nop
             ret
             restore

!function: main (end)

    .section   ".rodata"

.L6:   .asciz  "" ""

.L8:   .asciz  ""\n""

.L9:   .asciz  ""Enter a number\n""

