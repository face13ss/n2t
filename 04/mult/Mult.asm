// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
//
// This program only needs to handle arguments that satisfy
// R0 >= 0, R1 >= 0, and R0*R1 < 32768.

// Put your code here.

(MAIN)
    @R2
    M=0

    // check R0 == 0
    @R0
    D=M
    @END
    D;JEQ
    
    // save R0
    @var0
    M=D

    // check R1 == 0
    @R1
    D=M
    @END
    D;JEQ

    @i
    M=D-1
    @LOOP
    0;JMP

(LOOP)
    @i
    D=M
    @RESULT
    D;JEQ

    @var0
    D=M
    @R0
    M=M+D
    @i
    M=M-1
    @LOOP
    0;JMP

(RESULT)
    @R0
    D=M
    @R2
    M=D
    @END
    0;JMP

(END)
    @END
    0;JMP