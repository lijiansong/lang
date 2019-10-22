## Dart

### 1、Dart Type System


The Dart language is `type safe`: it uses a combination of static type checking and runtime checks to ensure that a variable’s value always matches the variable’s static type. Although types are mandatory, type annotations are optional because of type inference.

#### 1.1 Soundness of Dart's type system?

Soundness is about ensuring your program can’t get into certain invalid states. A sound type system means you can never get into a state where an expression evaluates to a value that doesn’t match the expression’s static type. For example, if an expression’s static type is String, at runtime you are guaranteed to only get a string when you evaluate it.

Dart’s type system, like the type systems in Java and C#, is sound. It enforces that soundness using a combination of static checking (compile-time errors) and runtime checks. For example, assigning a String to int is a compile-time error. Casting an Object to a string using as String fails with a runtime error if the object isn’t a string.

#### 1.2 The benefits of soundness

A sound type system has several benefits:

- Revealing type-related bugs at compile time.
A sound type system forces code to be unambiguous about its types, so type-related bugs that might be tricky to find at runtime are revealed at compile time.

- More readable code.
Code is easier to read because you can rely on a value actually having the specified type. In sound Dart, types can’t lie.

- More maintainable code.
With a sound type system, when you change one piece of code, the type system can warn you about the other pieces of code that just broke.

- Better ahead of time (AOT) compilation.
While AOT compilation is possible without types, the generated code is much less efficient.


### Reference

- <https://dart.dev/guides/language/sound-dart>