all:
	g++ -E a.cpp -o a.i
	g++ -E b.cpp -o b.i
	g++ -E b.cpp -o main.i
	g++ -c *.cpp
	gcc a.o b.o main.o -o after
	gcc main.o a.o b.o -o before
clean:
	@rm -f a.out *.o after before *.i
