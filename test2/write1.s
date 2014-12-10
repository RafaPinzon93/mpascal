! Creado por mpascal.py
! Rafael Pinzon, Daniel Osorio, Alejandro Lopez IS744 (2014-2)

! program

! function: LexToken(ID,'foo',3,54) (start) 

! assign (start)
! push NumeroInt (1)
! pop NumeroInt (1)
! push uminus NumeroInt (1)
! expr := pop
!   assign(expr)
! assign (End)

! write (start)
! push ID x
! expr := pop
!   write(expr)
! write (End)

! write (start)
! push y [NumeroInt (0)]
! expr := pop
!   write(expr)
! write (End)

! write (start)
! push y [BinaryOp (+)]
! push NumeroInt (45)
! add
! expr := pop
!   write(expr)
! write (End)

! write (start)
! push NumeroInt (1)
! push ID x
! push y [ID x]
! Mult
! push y [NumeroInt (0)]
! Div
! push NumeroFloat (2.4232)
! Mult
! add
! expr := pop
!   write(expr)
! write (End)
! function: LexToken(ID,'foo',3,54) (end)
