CC=g++
CFLAGS=-g -std=c++11

HTML=vim -c :TOhtml -c :wqa

DISASSEMBLER=objdump -disassemble -x86-asm-syntax=intel
SOURCES=$(wildcard *.cpp)
OBJECTS=$(SOURCES:%.cpp=%-${CC})
ASSEMBLIES=$(SOURCES:%.cpp=%-asm)
HTMLS=$(SOURCES:%=%.html)
HTMLS+=$(ASSEMBLIES:%=%.html)

.PHONY: all html clean

all: ${ASSEMBLIES}

html: ${HTMLS}

%-asm: %-${CC}
	${DISASSEMBLER} $< > $@

%-${CC}: %.cpp
	${CC} ${CFLAGS} $< -o $@

%.html: %
	${HTML} $<

clean:
	@rm -f a.out
	@rm -rf *.dSYM
