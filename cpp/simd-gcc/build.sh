#!/bin/bash
clang -S -O0 -emit-llvm -mllvm -print-after-all foo.cpp 2>&1 | tee foo-O0.log
clang -S -O1 -emit-llvm -mllvm -print-after-all foo.cpp 2>&1 | tee foo-O1.log
clang -S -O2 -emit-llvm -mllvm -print-after-all foo.cpp 2>&1 | tee foo-O2.log
clang -S -O3 -emit-llvm -mllvm -print-after-all foo.cpp 2>&1 | tee foo-O3.log
