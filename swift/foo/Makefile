all:
	swiftc hello.swift
	swiftc -dump-ast hello.swift 2>&1 | tee hello.ast
	swiftc -emit-ir hello.swift -o hello.ir
	swiftc -emit-assembly hello.swift -o hello.as
	swiftc -S hello.swift -o hello.s
clean:
	rm -f hello
