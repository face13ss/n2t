FUNCTION
@6
D=A
@R0
A=M
M=D
@R0
M=M+1
@8
D=A
@R0
A=M
M=D
@R0
M=M+1
call Class1.set 2
@R0
M=M-1
A=M
D=M
@R5
M=D
@23
D=A
@R0
A=M
M=D
@R0
M=M+1
@15
D=A
@R0
A=M
M=D
@R0
M=M+1
call Class2.set 2
@R0
M=M-1
A=M
D=M
@R5
M=D
call Class1.get 0
call Class2.get 0
(WHILE)
@WHILE
0;JMP
FUNCTION
@0
D=A
@R2
A=D+M
D=M
@R0
A=M
M=D
@R0
M=M+1
@R0
M=M-1
A=M
D=M
@Class1.vm.0
M=D
@1
D=A
@R2
A=D+M
D=M
@R0
A=M
M=D
@R0
M=M+1
@R0
M=M-1
A=M
D=M
@Class1.vm.1
M=D
@0
D=A
@R0
A=M
M=D
@R0
M=M+1
return
FUNCTION
@Class1.vm.0
D=M
@R0
A=M
M=D
@R0
M=M+1
@Class1.vm.1
D=M
@R0
A=M
M=D
@R0
M=M+1

@R0
M=M-1
@R0
A=M
D=M
@R0
M=M-1
@R0
A=M
M=M-D
@R0
M=M+1
return
FUNCTION
@0
D=A
@R2
A=D+M
D=M
@R0
A=M
M=D
@R0
M=M+1
@R0
M=M-1
A=M
D=M
@Class2.vm.0
M=D
@1
D=A
@R2
A=D+M
D=M
@R0
A=M
M=D
@R0
M=M+1
@R0
M=M-1
A=M
D=M
@Class2.vm.1
M=D
@0
D=A
@R0
A=M
M=D
@R0
M=M+1
return
FUNCTION
@Class2.vm.0
D=M
@R0
A=M
M=D
@R0
M=M+1
@Class2.vm.1
D=M
@R0
A=M
M=D
@R0
M=M+1

@R0
M=M-1
@R0
A=M
D=M
@R0
M=M-1
@R0
A=M
M=M-D
@R0
M=M+1
return
