# macro_rules!

So why are macros useful?

Don't repeat yourself. There are many cases where you may need similar functionality in multiple places but with different types. Often, writing a macro is a useful way to avoid repeating code.

Domain-specific languages. Macros allow you to define special syntax for a specific purpose.

Variadic interfaces. Sometimes you want to define an interface that takes a variable number of arguments. An example is println! which could take any number of arguments, depending on the format string!.

