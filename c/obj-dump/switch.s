
switch.o:	file format Mach-O 64-bit x86-64

Disassembly of section __TEXT,__text:
_main:
; int main() {
       0:	55 	pushq	%rbp
       1:	48 89 e5 	movq	%rsp, %rbp
       4:	48 83 ec 20 	subq	$32, %rsp
       8:	c7 45 fc 00 00 00 00 	movl	$0, -4(%rbp)
       f:	31 c0 	xorl	%eax, %eax
      11:	89 c7 	movl	%eax, %edi
; srand(time(NULL));
      13:	e8 00 00 00 00 	callq	0 <_main+0x18>
      18:	89 c1 	movl	%eax, %ecx
      1a:	89 cf 	movl	%ecx, %edi
      1c:	e8 00 00 00 00 	callq	0 <_main+0x21>
; int r = rand() % 3;
      21:	e8 00 00 00 00 	callq	0 <_main+0x26>
      26:	48 63 d0 	movslq	%eax, %rdx
      29:	48 69 d2 56 55 55 55 	imulq	$1431655766, %rdx, %rdx
      30:	48 89 d6 	movq	%rdx, %rsi
      33:	48 c1 ee 3f 	shrq	$63, %rsi
      37:	89 f1 	movl	%esi, %ecx
      39:	48 c1 ea 20 	shrq	$32, %rdx
      3d:	89 d7 	movl	%edx, %edi
      3f:	01 cf 	addl	%ecx, %edi
      41:	89 fa 	movl	%edi, %edx
      43:	8d 0c 52 	leal	(%rdx,%rdx,2), %ecx
      46:	29 c8 	subl	%ecx, %eax
      48:	89 45 f8 	movl	%eax, -8(%rbp)
; int a = 100;
      4b:	c7 45 f4 64 00 00 00 	movl	$100, -12(%rbp)
; switch(r) {
      52:	8b 45 f8 	movl	-8(%rbp), %eax
      55:	85 c0 	testl	%eax, %eax
      57:	89 45 f0 	movl	%eax, -16(%rbp)
      5a:	0f 84 2d 00 00 00 	je	45 <_main+0x8D>
      60:	e9 00 00 00 00 	jmp	0 <_main+0x65>
      65:	8b 45 f0 	movl	-16(%rbp), %eax
      68:	83 e8 01 	subl	$1, %eax
      6b:	89 45 ec 	movl	%eax, -20(%rbp)
      6e:	0f 84 25 00 00 00 	je	37 <_main+0x99>
      74:	e9 00 00 00 00 	jmp	0 <_main+0x79>
      79:	8b 45 f0 	movl	-16(%rbp), %eax
      7c:	83 e8 02 	subl	$2, %eax
      7f:	89 45 e8 	movl	%eax, -24(%rbp)
      82:	0f 84 1d 00 00 00 	je	29 <_main+0xA5>
      88:	e9 1f 00 00 00 	jmp	31 <_main+0xAC>
; a = 0;
      8d:	c7 45 f4 00 00 00 00 	movl	$0, -12(%rbp)
; break;
      94:	e9 13 00 00 00 	jmp	19 <_main+0xAC>
; a = 1;
      99:	c7 45 f4 01 00 00 00 	movl	$1, -12(%rbp)
; break;
      a0:	e9 07 00 00 00 	jmp	7 <_main+0xAC>
; a = 2;
      a5:	c7 45 f4 02 00 00 00 	movl	$2, -12(%rbp)
      ac:	31 c0 	xorl	%eax, %eax
; return 0;
      ae:	48 83 c4 20 	addq	$32, %rsp
      b2:	5d 	popq	%rbp
      b3:	c3 	retq
