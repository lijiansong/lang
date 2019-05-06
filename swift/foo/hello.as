	.section	__TEXT,__text,regular,pure_instructions
	.macosx_version_min 10, 9
	.globl	_main
	.p2align	4, 0x90
_main:
	.cfi_startproc
	pushq	%rbp
Lcfi0:
	.cfi_def_cfa_offset 16
Lcfi1:
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
Lcfi2:
	.cfi_def_cfa_register %rbp
	subq	$96, %rsp
	movl	$1, %eax
	movl	%eax, %ecx
	movl	%edi, -4(%rbp)
	movq	%rcx, %rdi
	movq	%rsi, -16(%rbp)
	callq	__T0s27_allocateUninitializedArraySayxG_BptBwlFyp_Tgq5
	movq	%rax, %rdi
	movq	%rax, -24(%rbp)
	movq	%rdx, -32(%rbp)
	callq	_swift_bridgeObjectRetain
	movq	-24(%rbp), %rdi
	movq	%rax, -40(%rbp)
	callq	_swift_bridgeObjectRelease
	leaq	L___unnamed_1(%rip), %rdi
	movl	$13, %r8d
	movl	%r8d, %esi
	movl	$1, %edx
	movq	__T0SSN@GOTPCREL(%rip), %rax
	movq	-32(%rbp), %rcx
	movq	%rax, 24(%rcx)
	callq	__T0S2SBp21_builtinStringLiteral_Bw17utf8CodeUnitCountBi1_7isASCIItcfC
	movq	-32(%rbp), %rsi
	movq	%rax, (%rsi)
	movq	%rdx, 8(%rsi)
	movq	%rcx, 16(%rsi)
	callq	__T0s5printySayypGd_SS9separatorSS10terminatortFfA0_
	movq	%rax, -48(%rbp)
	movq	%rdx, -56(%rbp)
	movq	%rcx, -64(%rbp)
	callq	__T0s5printySayypGd_SS9separatorSS10terminatortFfA1_
	movq	-24(%rbp), %rdi
	movq	-48(%rbp), %rsi
	movq	-56(%rbp), %r9
	movq	%rdx, -72(%rbp)
	movq	%r9, %rdx
	movq	-64(%rbp), %r10
	movq	%rcx, -80(%rbp)
	movq	%r10, %rcx
	movq	%rax, %r8
	movq	-72(%rbp), %r9
	movq	-80(%rbp), %rax
	movq	%rax, (%rsp)
	callq	__T0s5printySayypGd_SS9separatorSS10terminatortF
	xorl	%eax, %eax
	addq	$96, %rsp
	popq	%rbp
	retq
	.cfi_endproc

	.section	__TEXT,__cstring,cstring_literals
L___unnamed_1:
	.asciz	"Hello, world!"

	.private_extern	___swift_reflection_version
	.section	__TEXT,__const
	.globl	___swift_reflection_version
	.weak_definition	___swift_reflection_version
	.p2align	1
___swift_reflection_version:
	.short	3

	.no_dead_strip	___swift_reflection_version
	.linker_option "-lswiftCore"
	.linker_option "-lswiftSwiftOnoneSupport"
	.linker_option "-lobjc"
	.section	__DATA,__objc_imageinfo,regular,no_dead_strip
L_OBJC_IMAGE_INFO:
	.long	0
	.long	1344


.subsections_via_symbols
