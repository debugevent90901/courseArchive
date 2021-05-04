	.file	"kthsmallest.c"
 # GNU C17 (x86_64-win32-seh-rev0, Built by MinGW-W64 project) version 8.1.0 (x86_64-w64-mingw32)
 #	compiled by GNU C version 8.1.0, GMP version 6.1.2, MPFR version 4.0.1, MPC version 1.1.0, isl version isl-0.18-GMP

 # GGC heuristics: --param ggc-min-expand=100 --param ggc-min-heapsize=131072
 # options passed: 
 # -iprefix C:/Program Files/mingw-w64/x86_64-8.1.0-win32-seh-rt_v6-rev0/mingw64/bin/../lib/gcc/x86_64-w64-mingw32/8.1.0/
 # -U_REENTRANT kthsmallest.c -mtune=core2 -march=nocona -fverbose-asm
 # options enabled:  -faggressive-loop-optimizations
 # -fasynchronous-unwind-tables -fauto-inc-dec -fchkp-check-incomplete-type
 # -fchkp-check-read -fchkp-check-write -fchkp-instrument-calls
 # -fchkp-narrow-bounds -fchkp-optimize -fchkp-store-bounds
 # -fchkp-use-static-bounds -fchkp-use-static-const-bounds
 # -fchkp-use-wrappers -fcommon -fdelete-null-pointer-checks
 # -fdwarf2-cfi-asm -fearly-inlining -feliminate-unused-debug-types
 # -ffp-int-builtin-inexact -ffunction-cse -fgcse-lm -fgnu-runtime
 # -fgnu-unique -fident -finline-atomics -fira-hoist-pressure
 # -fira-share-save-slots -fira-share-spill-slots -fivopts
 # -fkeep-inline-dllexport -fkeep-static-consts -fleading-underscore
 # -flifetime-dse -flto-odr-type-merging -fmath-errno -fmerge-debug-strings
 # -fpeephole -fpic -fplt -fprefetch-loop-arrays -freg-struct-return
 # -fsched-critical-path-heuristic -fsched-dep-count-heuristic
 # -fsched-group-heuristic -fsched-interblock -fsched-last-insn-heuristic
 # -fsched-rank-heuristic -fsched-spec -fsched-spec-insn-heuristic
 # -fsched-stalled-insns-dep -fschedule-fusion -fsemantic-interposition
 # -fset-stack-executable -fshow-column -fshrink-wrap-separate
 # -fsigned-zeros -fsplit-ivs-in-unroller -fssa-backprop -fstdarg-opt
 # -fstrict-volatile-bitfields -fsync-libcalls -ftrapping-math
 # -ftree-cselim -ftree-forwprop -ftree-loop-if-convert -ftree-loop-im
 # -ftree-loop-ivcanon -ftree-loop-optimize -ftree-parallelize-loops=
 # -ftree-phiprop -ftree-reassoc -ftree-scev-cprop -funit-at-a-time
 # -funwind-tables -fverbose-asm -fzero-initialized-in-bss
 # -m128bit-long-double -m64 -m80387 -maccumulate-outgoing-args
 # -malign-double -malign-stringops -mcx16 -mfancy-math-387 -mfentry
 # -mfp-ret-in-387 -mfxsr -mieee-fp -mlong-double-80 -mmmx -mms-bitfields
 # -mno-sse4 -mpush-args -mred-zone -msse -msse2 -msse3 -mstack-arg-probe
 # -mstackrealign -mvzeroupper

	.text
	.globl	swap
	.def	swap;	.scl	2;	.type	32;	.endef
	.seh_proc	swap
swap:
	pushq	%rbp	 #
	.seh_pushreg	%rbp
	movq	%rsp, %rbp	 #,
	.seh_setframe	%rbp, 0
	subq	$16, %rsp	 #,
	.seh_stackalloc	16
	.seh_endprologue
	movq	%rcx, 16(%rbp)	 # a, a
	movq	%rdx, 24(%rbp)	 # b, b
 # kthsmallest.c:36:     int temp = *a;
	movq	16(%rbp), %rax	 # a, tmp88
	movl	(%rax), %eax	 # *a_3(D), tmp89
	movl	%eax, -4(%rbp)	 # tmp89, temp
 # kthsmallest.c:37:     *a = *b;
	movq	24(%rbp), %rax	 # b, tmp90
	movl	(%rax), %edx	 # *b_5(D), _1
 # kthsmallest.c:37:     *a = *b;
	movq	16(%rbp), %rax	 # a, tmp91
	movl	%edx, (%rax)	 # _1, *a_3(D)
 # kthsmallest.c:38:     *b = temp;
	movq	24(%rbp), %rax	 # b, tmp92
	movl	-4(%rbp), %edx	 # temp, tmp93
	movl	%edx, (%rax)	 # tmp93, *b_5(D)
 # kthsmallest.c:39: }
	nop	
	addq	$16, %rsp	 #,
	popq	%rbp	 #
	ret	
	.seh_endproc
	.globl	kthSmallest_c
	.def	kthSmallest_c;	.scl	2;	.type	32;	.endef
	.seh_proc	kthSmallest_c
kthSmallest_c:
	pushq	%rbp	 #
	.seh_pushreg	%rbp
	movq	%rsp, %rbp	 #,
	.seh_setframe	%rbp, 0
	subq	$48, %rsp	 #,
	.seh_stackalloc	48
	.seh_endprologue
	movq	%rcx, 16(%rbp)	 # arr, arr
	movl	%edx, 24(%rbp)	 # left, left
	movl	%r8d, 32(%rbp)	 # right, right
	movl	%r9d, 40(%rbp)	 # k, k
 # kthsmallest.c:44:     int pivot = arr[right];
	movl	32(%rbp), %eax	 # right, tmp113
	cltq
	leaq	0(,%rax,4), %rdx	 #, _2
	movq	16(%rbp), %rax	 # arr, tmp114
	addq	%rdx, %rax	 # _2, _3
 # kthsmallest.c:44:     int pivot = arr[right];
	movl	(%rax), %eax	 # *_3, tmp115
	movl	%eax, -12(%rbp)	 # tmp115, pivot
 # kthsmallest.c:45:     int i = left;
	movl	24(%rbp), %eax	 # left, tmp116
	movl	%eax, -4(%rbp)	 # tmp116, i
 # kthsmallest.c:46:     for (int j=left; j<right; j++) {
	movl	24(%rbp), %eax	 # left, tmp117
	movl	%eax, -8(%rbp)	 # tmp117, j
 # kthsmallest.c:46:     for (int j=left; j<right; j++) {
	jmp	.L3	 #
.L5:
 # kthsmallest.c:47:         if (arr[j] <= pivot) {
	movl	-8(%rbp), %eax	 # j, tmp118
	cltq
	leaq	0(,%rax,4), %rdx	 #, _5
	movq	16(%rbp), %rax	 # arr, tmp119
	addq	%rdx, %rax	 # _5, _6
	movl	(%rax), %eax	 # *_6, _7
 # kthsmallest.c:47:         if (arr[j] <= pivot) {
	cmpl	%eax, -12(%rbp)	 # _7, pivot
	jl	.L4	 #,
 # kthsmallest.c:48:             swap(&arr[i], &arr[j]);
	movl	-8(%rbp), %eax	 # j, tmp120
	cltq
	leaq	0(,%rax,4), %rdx	 #, _9
 # kthsmallest.c:48:             swap(&arr[i], &arr[j]);
	movq	16(%rbp), %rax	 # arr, tmp121
	addq	%rax, %rdx	 # tmp121, _10
 # kthsmallest.c:48:             swap(&arr[i], &arr[j]);
	movl	-4(%rbp), %eax	 # i, tmp122
	cltq
	leaq	0(,%rax,4), %rcx	 #, _12
 # kthsmallest.c:48:             swap(&arr[i], &arr[j]);
	movq	16(%rbp), %rax	 # arr, tmp123
	addq	%rcx, %rax	 # _12, _13
	movq	%rax, %rcx	 # _13,
	call	swap	 #
 # kthsmallest.c:49:             i++;
	addl	$1, -4(%rbp)	 #, i
.L4:
 # kthsmallest.c:46:     for (int j=left; j<right; j++) {
	addl	$1, -8(%rbp)	 #, j
.L3:
 # kthsmallest.c:46:     for (int j=left; j<right; j++) {
	movl	-8(%rbp), %eax	 # j, tmp124
	cmpl	32(%rbp), %eax	 # right, tmp124
	jl	.L5	 #,
 # kthsmallest.c:52:     swap(&arr[i], &arr[right]);
	movl	32(%rbp), %eax	 # right, tmp125
	cltq
	leaq	0(,%rax,4), %rdx	 #, _15
 # kthsmallest.c:52:     swap(&arr[i], &arr[right]);
	movq	16(%rbp), %rax	 # arr, tmp126
	addq	%rax, %rdx	 # tmp126, _16
 # kthsmallest.c:52:     swap(&arr[i], &arr[right]);
	movl	-4(%rbp), %eax	 # i, tmp127
	cltq
	leaq	0(,%rax,4), %rcx	 #, _18
 # kthsmallest.c:52:     swap(&arr[i], &arr[right]);
	movq	16(%rbp), %rax	 # arr, tmp128
	addq	%rcx, %rax	 # _18, _19
	movq	%rax, %rcx	 # _19,
	call	swap	 #
 # kthsmallest.c:54:     if (k==i) {
	movl	40(%rbp), %eax	 # k, tmp129
	cmpl	-4(%rbp), %eax	 # i, tmp129
	jne	.L6	 #,
 # kthsmallest.c:55:         return arr[k];
	movl	40(%rbp), %eax	 # k, tmp130
	cltq
	leaq	0(,%rax,4), %rdx	 #, _21
	movq	16(%rbp), %rax	 # arr, tmp131
	addq	%rdx, %rax	 # _21, _22
	movl	(%rax), %eax	 # *_22, _28
	jmp	.L7	 #
.L6:
 # kthsmallest.c:56:     } else if (k < i) {
	movl	40(%rbp), %eax	 # k, tmp132
	cmpl	-4(%rbp), %eax	 # i, tmp132
	jge	.L8	 #,
 # kthsmallest.c:57:         return kthSmallest_c(arr, left, i-1, k);
	movl	-4(%rbp), %eax	 # i, tmp133
	leal	-1(%rax), %edx	 #, _23
	movl	40(%rbp), %ecx	 # k, tmp134
	movl	24(%rbp), %eax	 # left, tmp135
	movl	%ecx, %r9d	 # tmp134,
	movl	%edx, %r8d	 # _23,
	movl	%eax, %edx	 # tmp135,
	movq	16(%rbp), %rcx	 # arr,
	call	kthSmallest_c	 #
	jmp	.L7	 #
.L8:
 # kthsmallest.c:59:         return kthSmallest_c(arr, i+1, right, k);
	movl	-4(%rbp), %eax	 # i, tmp136
	addl	$1, %eax	 #, _24
	movl	40(%rbp), %ecx	 # k, tmp137
	movl	32(%rbp), %edx	 # right, tmp138
	movl	%ecx, %r9d	 # tmp137,
	movl	%edx, %r8d	 # tmp138,
	movl	%eax, %edx	 # _24,
	movq	16(%rbp), %rcx	 # arr,
	call	kthSmallest_c	 #
.L7:
 # kthsmallest.c:61: }
	addq	$48, %rsp	 #,
	popq	%rbp	 #
	ret	
	.seh_endproc
	.ident	"GCC: (x86_64-win32-seh-rev0, Built by MinGW-W64 project) 8.1.0"
