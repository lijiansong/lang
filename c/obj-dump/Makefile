all:
	gcc -g -c if.c
	gcc -g -c switch.c
	objdump -S if.o 2>&1 | tee if.s
	objdump -S switch.o 2>&1 | tee switch.s
clean:
	rm -f *.o *.s
