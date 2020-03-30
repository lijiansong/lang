## Lambda Expression in C++11

One of the most exciting features of C++11 is ability to create lambda functions (sometimes referred to as `closures`).

For the C++11 lambdas, they provide a syntactically lightweight way to define functions on-the-fly. They can also capture (or close over) variables from the surrounding scope, either by value or by reference.

### How Lambdas Differ, Implementation-wise, from Plain Functions and Functor classes？

In this section, we investigate how lambdas differ, implementation-wise, from plain functions and functor classes (classes that implement `operator()`).

**No Capturing Cases:**

For those callable things that do not capture any variables, C++ offers three alternatives: `plain functions, functor classes, and lambdas`. This listing demonstrates each approach for a simple operation:

```
int function(int a) { return a + 3; }

class Functor {
public:
  int operator()(int a) { return a + 3; }
};

int main() {
  auto lambda = [](int a) { return a + 3; };

  Functor functor;

  volatile int y1 = function(5);
  volatile int y2 = functor(5);
  volatile int y3 = lambda(5);

  return 0;
}
```

objdump反汇编以后，plain function对应的汇编：

```
126 int function(int a) { return a + 3; }
127   400546:   55                      push   rbp
128   400547:   48 89 e5                mov    rbp,rsp
129   40054a:   89 7d fc                mov    DWORD PTR [rbp-0x4],edi
130   40054d:   8b 45 fc                mov    eax,DWORD PTR [rbp-0x4]
131   400550:   83 c0 03                add    eax,0x3
132   400553:   5d                      pop    rbp
133   400554:   c3                      ret
134   400555:   90                      nop 
```

Here, the parameter a is passed in the register edi, and the return value is placed in the eax register. The assembly was not optimized at all, so lines 106 and 108 place the argument on the stack, then immediately retrieve it. (In Intel x86 assembly syntax, the use of [] works like a pointer dereference; rbp contains the "base pointer", a pointer to the top of the stack frame.) The stack frame is 4 bytes (hence the rbp-0x4) since there is only one 4-byte value stored on it. Line 109 actually performs the addition; the remainder of the lines consist of setting up and cleaning up various registers for the function call.


functor对应的汇编：

```
203   int operator()(int a) { return a + 3; }
204   4005d0:   55                      push   rbp
205   4005d1:   48 89 e5                mov    rbp,rsp
206   4005d4:   48 89 7d f8             mov    QWORD PTR [rbp-0x8],rdi
207   4005d8:   89 75 f4                mov    DWORD PTR [rbp-0xc],esi
208   4005db:   8b 45 f4                mov    eax,DWORD PTR [rbp-0xc]
209   4005de:   83 c0 03                add    eax,0x3
210   4005e1:   5d                      pop    rbp
211   4005e2:   c3                      ret
212   4005e3:   66 2e 0f 1f 84 00 00    nop    WORD PTR cs:[rax+rax*1+0x0]
213   4005ea:   00 00 00
214   4005ed:   0f 1f 00                nop    DWORD PTR [rax]
215 
```

lambda expression对应的汇编：

```
142   auto lambda = [](int a) { return a + 3; };
143   400556:   55                      push   rbp
144   400557:   48 89 e5                mov    rbp,rsp
145   40055a:   48 89 7d f8             mov    QWORD PTR [rbp-0x8],rdi
146   40055e:   89 75 f4                mov    DWORD PTR [rbp-0xc],esi
147   400561:   8b 45 f4                mov    eax,DWORD PTR [rbp-0xc]
148   400564:   83 c0 03                add    eax,0x3
149   400567:   5d                      pop    rbp
150   400568:   c3                      ret
```

The code generated from the functor class and the lambda are identical, but differ from the plain function in one way: there is a hidden first parameter passed in rdi (due to x86 weirdness, this is the same register as edi, but it holds 8 bytes instead of 4). It is unused in this function; we will see its purpose later on. The second parameter a is passed in esi (instead of edi, as with the plain function). Due to this hidden parameter, the stack frame is now 12 bytes; 4 for a and 8 for the hidden parameter.

总结：

For plain functions that capture no variables, lambdas and functors behave the same. They differ from a plain C++ function only in that they take an additional hidden parameter, thus requiring an extra 8 bytes of stack space. (In addition, they require a single byte on main()'s stack that is related to the hidden parameter.)


**Capture By Value Cases:**

When capturing variables, we cannot use a standard C++ function, so we are left with two approaches: `functor classes and lambdas`.

```
class Functor {
public:
  Functor(const int x) : m_x(x) {}

  int operator()(int a) { return a + m_x; }

private:
  int m_x;
};

int main() {
  int x = 3;

  auto lambda = [=](int a) { return a + x; };
  Functor functor(x);

  volatile int y1 = functor(5);
  volatile int y2 = lambda(5);

  return 0;
}
```

functor汇编：

```
212   int operator()(int a) { return a + m_x; }
213   4005ee:   55                      push   rbp
214   4005ef:   48 89 e5                mov    rbp,rsp
215   4005f2:   48 89 7d f8             mov    QWORD PTR [rbp-0x8],rdi
216   4005f6:   89 75 f4                mov    DWORD PTR [rbp-0xc],esi
217   4005f9:   48 8b 45 f8             mov    rax,QWORD PTR [rbp-0x8]
218   4005fd:   8b 10                   mov    edx,DWORD PTR [rax]
219   4005ff:   8b 45 f4                mov    eax,DWORD PTR [rbp-0xc]
220   400602:   01 d0                   add    eax,edx
221   400604:   5d                      pop    rbp
222   400605:   c3                      ret
223   400606:   66 2e 0f 1f 84 00 00    nop    WORD PTR cs:[rax+rax*1+0x0]
224   40060d:   00 00 00
```

The constructor's assembly is a very long way of saying "put the contents of esi into the memory location stored in rdi". To find out what is passed as the two arguments to this function, let's have a look at the code in main() that calls the constructor:

```
157   int x = 3;
158   400575:   c7 45 f4 03 00 00 00    mov    DWORD PTR [rbp-0xc],0x3
...
...
170   volatile int y1 = functor(5);
171   400593:   48 8d 45 e0             lea    rax,[rbp-0x20]
172   400597:   be 05 00 00 00          mov    esi,0x5
173   40059c:   48 89 c7                mov    rdi,rax
174   40059f:   e8 4a 00 00 00          call   4005ee <Functor::operator()(int)>
175   4005a4:   89 45 ec                mov    DWORD PTR [rbp-0x14],eax
```

lambda expression汇编：

```
130 
131   auto lambda = [=](int a) { return a + x; };
132   400546:   55                      push   rbp
133   400547:   48 89 e5                mov    rbp,rsp
134   40054a:   48 89 7d f8             mov    QWORD PTR [rbp-0x8],rdi
135   40054e:   89 75 f4                mov    DWORD PTR [rbp-0xc],esi
136   400551:   48 8b 45 f8             mov    rax,QWORD PTR [rbp-0x8]
137   400555:   8b 10                   mov    edx,DWORD PTR [rax]
138   400557:   8b 45 f4                mov    eax,DWORD PTR [rbp-0xc]
139   40055a:   01 d0                   add    eax,edx
140   40055c:   5d                      pop    rbp
141   40055d:   c3                      ret
```

**总结：**

Capture-by-value lambdas work almost identically to a standard functor: they both allocate an object where the captured value is stored and take a hidden function parameter pointing to this object. The code executed by the function call for both the lambda and the functor are the same. The sole difference is that the lambda's constructor is inlined into the function where the lambda is created, rather than being a separate function like the functor's constructor.

**Capture By Reference Cases:**

When capturing by reference, the value captured can be modified in the same manner as a parameter passed by reference to a normal C++ function.


functor汇编：

```
167   Functor functor(x);
168   40058c:   48 8d 55 d4             lea    rdx,[rbp-0x2c]
169   400590:   48 8d 45 f0             lea    rax,[rbp-0x10]
170   400594:   48 89 d6                mov    rsi,rdx
171   400597:   48 89 c7                mov    rdi,rax
172   40059a:   e8 43 00 00 00          call   4005e2 <Functor::Functor(int&)>
173 
174   volatile int y1 = functor(5);
175   40059f:   48 8d 45 f0             lea    rax,[rbp-0x10]
176   4005a3:   be 05 00 00 00          mov    esi,0x5
177   4005a8:   48 89 c7                mov    rdi,rax
178   4005ab:   e8 4c 00 00 00          call   4005fc <Functor::operator()(int)>
179   4005b0:   89 45 d8                mov    DWORD PTR [rbp-0x28],eax
...
...
...


199 class Functor {
200 public:
201   Functor(int &x) : m_x(x) {}
202   4005e2:   55                      push   rbp
203   4005e3:   48 89 e5                mov    rbp,rsp
204   4005e6:   48 89 7d f8             mov    QWORD PTR [rbp-0x8],rdi
205   4005ea:   48 89 75 f0             mov    QWORD PTR [rbp-0x10],rsi
206   4005ee:   48 8b 45 f8             mov    rax,QWORD PTR [rbp-0x8]
207   4005f2:   48 8b 55 f0             mov    rdx,QWORD PTR [rbp-0x10]
208   4005f6:   48 89 10                mov    QWORD PTR [rax],rdx
209   4005f9:   90                      nop
210   4005fa:   5d                      pop    rbp
211   4005fb:   c3                      ret
212 
213 00000000004005fc <Functor::operator()(int)>:
214 
215   int operator()(int a) { return a + m_x++; }
216   4005fc:   55                      push   rbp
217   4005fd:   48 89 e5                mov    rbp,rsp
218   400600:   48 89 7d f8             mov    QWORD PTR [rbp-0x8],rdi
219   400604:   89 75 f4                mov    DWORD PTR [rbp-0xc],esi
220   400607:   48 8b 45 f8             mov    rax,QWORD PTR [rbp-0x8]
221   40060b:   48 8b 00                mov    rax,QWORD PTR [rax]
222   40060e:   8b 10                   mov    edx,DWORD PTR [rax]
223   400610:   8d 4a 01                lea    ecx,[rdx+0x1]
224   400613:   89 08                   mov    DWORD PTR [rax],ecx
225   400615:   8b 45 f4                mov    eax,DWORD PTR [rbp-0xc]
226   400618:   01 d0                   add    eax,edx
227   40061a:   5d                      pop    rbp
228   40061b:   c3                      ret
229   40061c:   0f 1f 40 00             nop    DWORD PTR [rax+0x0]
...
...
```

lambda表达式汇编：

```
180   volatile int y2 = lambda(5);
181   4005b3:   48 8d 45 e0             lea    rax,[rbp-0x20]
182   4005b7:   be 05 00 00 00          mov    esi,0x5
183   4005bc:   48 89 c7                mov    rdi,rax
184   4005bf:   e8 82 ff ff ff          call   400546 <main::{lambda(int)#1}::operator()(int) const>
185   4005c4:   89 45 dc                mov    DWORD PTR [rbp-0x24],eax
...
...
...
131   auto lambda = [&](int a) { return a + x++; };
132   400546:   55                      push   rbp
133   400547:   48 89 e5                mov    rbp,rsp
134   40054a:   48 89 7d f8             mov    QWORD PTR [rbp-0x8],rdi
135   40054e:   89 75 f4                mov    DWORD PTR [rbp-0xc],esi
136   400551:   48 8b 45 f8             mov    rax,QWORD PTR [rbp-0x8]
137   400555:   48 8b 00                mov    rax,QWORD PTR [rax]
138   400558:   8b 10                   mov    edx,DWORD PTR [rax]
139   40055a:   8d 4a 01                lea    ecx,[rdx+0x1]
140   40055d:   89 08                   mov    DWORD PTR [rax],ecx
141   40055f:   8b 45 f4                mov    eax,DWORD PTR [rbp-0xc]
142   400562:   01 d0                   add    eax,edx
143   400564:   5d                      pop    rbp
144   400565:   c3                      ret
```

总结：

When capturing by reference, the functor and lambda objects contain a pointer instead of a value, demonstrating that the behavior of references is implemented using pointers under the hood. As with capture-by-value, the functor and lambda call code is equivalent, but the lambda's constructor is inlined, whereas the functor's is not.

最终结论：

C++ lambdas and functors are more similar than they are different. This is to be expected; the main goal of lambdas is to be a syntactically simple means of creating functions and closures. They differ slightly from plain functions, even when no variables are being captured. To summarize the key differences:

- 1. Functors and lambdas are always passed a this pointer, whereas plain functions naturally are not. This consumes an extra register and 8 bytes of stack space.
- 2. Lambda "constructors" are inlined into the function in which the lambda is created. This significantly reduces the amount of copying performed (2 instructions for lambdas, 5 for functors), as well as avoiding a function call setup and teardown.

Overall, the costs for #1 are minor, and are probably eliminated by an optimization pass in the compiler. The costs for #2 are somewhat higher, but they are cheaper for lambdas! Again, I suspect that an optimization pass would eliminate the difference between the two.

### How are Lambda Closures Implemented?

So how does the magic of variable capture really work? It turns out that the way lambdas are implemented is by creating a small class; this class overloads the operator(), so that it acts just like a function. A lambda function is an instance of this class; when the class is constructed, any variables in the surrounding enviroment are passed into the constructor of the lambda function class and saved as member variables. This is, in fact, quite a bit like the idea of a functor that is already possible. The benefit of C++11 is that doing this becomes almost trivially easy--so you can use it all the time, rather than only in very rare circumstances where writing a whole new class makes sense.


### REFs

- 如何在 C++11 中使用 Lambda 表达式: <https://www.oracle.com/technetwork/cn/articles/servers-storage-dev/howto-use-lambda-exp-cpp11-2189895-zhs.html>

- Lambda Functions in C++11 - the Definitive Guide <https://www.cprogramming.com/c++11/c++11-lambda-closures.html>

- C++ Lambdas Under The Hood: <https://web.mst.edu/~nmjxv3/articles/lambdas.html>
