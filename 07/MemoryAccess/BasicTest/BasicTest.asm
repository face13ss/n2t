@10
D=A
@R0
A=M
M=D
@R0
M=M+1
   // push constant 10
@R0
M=M-1
@R0
D=M

@R1
D=M
@0
D=D+A
A=D
M=D   // pop local 0
@21
D=A
@R0
A=M
M=D
@R0
M=M+1
   // push constant 21
@22
D=A
@R0
A=M
M=D
@R0
M=M+1
   // push constant 22
@R0
M=M-1
@R0
D=M
@R2
D=M
@2
D=D+A
A=D
M=D   // pop argument 2
@R0
M=M-1
@R0
D=M
@R2
D=M
@1
D=D+A
A=D
M=D   // pop argument 1
@36
D=A
@R0
A=M
M=D
@R0
M=M+1
   // push constant 36
@R0
M=M-1
@R0
D=M
@R3
D=M
@6
D=D+A
A=D
M=D   // pop this 6
@42
D=A
@R0
A=M
M=D
@R0
M=M+1
   // push constant 42
@45
D=A
@R0
A=M
M=D
@R0
M=M+1
   // push constant 45
@R0
M=M-1
@R0
D=M
@R4
D=M
@5
D=D+A
A=D
M=D   // pop that 5
@R0
M=M-1
@R0
D=M
@R4
D=M
@2
D=D+A
A=D
M=D   // pop that 2
@510
D=A
@R0
A=M
M=D
@R0
M=M+1
   // push constant 510
@R0
M=M-1
@R0
D=M
@R11
M=D   // pop temp 6
@R1
D=M
@0
D=D+A
A=D
D=M
@R0
M=D
@R0
M=M+1
   // push local 0
@R4
D=M
@5
D=D+A
A=D
D=M
@R0
M=D
@R0
M=M+1
   // push that 5
@R0
M=M-1
@R0
D=M
@R0
M=D+M
@R0
M=M+1

@R1
D=M
@1
D=D+A
A=D
D=M
@R0
M=D
@R0
M=M+1
   // push argument 1
@R0
M=M-1
@R0
D=M
@R0
M=D-M
@R0
M=M+1

@R3
D=M
@6
D=D+A
A=D
D=M
@R0
M=D
@R0
M=M+1
   // push this 6
@R3
D=M
@6
D=D+A
A=D
D=M
@R0
M=D
@R0
M=M+1
   // push this 6
@R0
M=M-1
@R0
D=M
@R0
M=D+M
@R0
M=M+1

@R0
M=M-1
@R0
D=M
@R0
M=D-M
@R0
M=M+1

@R3
D=M
@6
D=D+A
A=D
D=M
@R0
M=D
@R0
M=M+1
   // push temp 6
@R0
M=M-1
@R0
D=M
@R0
M=D+M
@R0
M=M+1

(END)
@END
0;JMP