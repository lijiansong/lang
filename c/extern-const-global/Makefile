all:
	g++ -E a.cpp -o a.i
	g++ -E b.cpp -o b.i
	g++ -E b.cpp -o main.i
	gcc -c *.cpp
	gcc a.o b.o main.o -o a-b-m
	gcc b.o a.o main.o -o b-a-m
	gcc main.o a.o b.o -o m-a-b
	gcc main.o b.o a.o -o m-b-a
	gcc a.o main.o b.o -o a-m-b
	gcc b.o main.o a.o -o b-m-a
clean:
	@rm -f a.out *.o a-b-m b-a-m m-a-b m-b-a a-m-b b-m-a *.i
