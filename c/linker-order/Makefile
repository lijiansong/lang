all:
	gcc -c *.cpp
	gcc a.o b.o main.o -o after
	gcc main.o a.o b.o -o before
clean:
	@rm -f a.out *.o after before
