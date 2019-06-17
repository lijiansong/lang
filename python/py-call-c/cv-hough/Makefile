all: src/pcf.so

src/pcf.so: pcf.c
	gcc -Ofast -fPIC -shared -I/usr/include/python2.7/ pcf.c -lpython2.7 -o pcf.so

test:
	@python test.py

clean:
	rm -f src/pcf.so src/*.pyc
