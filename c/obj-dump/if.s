
if.o:	file format Mach-O 64-bit x86-64

Disassembly of section __TEXT,__text:
_main:
; int main() {
       0:	55 	pushq	%rbp
       1:	48 89 e5 	movq	%rsp, %rbp
       4:	48 83 ec 10 	subq	$16, %rsp
       8:	31 c0 	xorl	%eax, %eax
       a:	89 c7 	movl	%eax, %edi
       c:	c7 45 fc 00 00 00 00 	movl	$0, -4(%rbp)
; srand(time(NULL));
      13:	e8 00 00 00 00 	callq	0 <_main+0x18>
      18:	89 c1 	movl	%eax, %ecx
      1a:	89 cf 	movl	%ecx, %edi
      1c:	e8 00 00 00 00 	callq	0 <_main+0x21>
; int r = rand() % 2;
      21:	e8 00 00 00 00 	callq	0 <_main+0x26>
      26:	b9 02 00 00 00 	movl	$2, %ecx
      2b:	99 	cltd
      2c:	f7 f9 	idivl	%ecx
      2e:	89 55 f8 	movl	%edx, -8(%rbp)
; int a = 100;
      31:	c7 45 f4 64 00 00 00 	movl	$100, -12(%rbp)
; if (r == 0) {
      38:	83 7d f8 00 	cmpl	$0, -8(%rbp)
      3c:	0f 85 0c 00 00 00 	jne	12 <_main+0x4E>
; a = 0;
      42:	c7 45 f4 00 00 00 00 	movl	$0, -12(%rbp)
; } else {
      49:	e9 07 00 00 00 	jmp	7 <_main+0x55>
; a = 1;
      4e:	c7 45 f4 01 00 00 00 	movl	$1, -12(%rbp)
      55:	31 c0 	xorl	%eax, %eax
; return 0;
      57:	48 83 c4 10 	addq	$16, %rsp
      5b:	5d 	popq	%rbp
      5c:	c3 	retq
