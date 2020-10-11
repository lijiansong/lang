
# Placement new operator in C++

`Placement new` is a variation new operator in C++.

Normal `new operator` does two things : 

- (1) Allocates memory;
- (2) Constructs an object in allocated memory.

Placement new allows us to separate above two things. In placement new, we can pass a preallocated memory and construct an object in the passed memory.


- `Normal new` allocates memory in heap and constructs objects there whereas using `placement new`, object construction can be done at known address;
- With `normal new`, it is `not known` that, at what address or memory location it’s pointing to, whereas the address or memory location that it’s pointing is `known` while using `placement new`;
- The deallocation is done using `delete` operation when allocation is done by `new` but there is no placement delete, but if it is needed one can write it with the help of `destructor`.

**Syntax**:

```
new (address) (type) initializer
```

### When to use placement new?

As it allows to construct an object on memory that is `already allocated`, it is required for optimizations `as it is faster not to re-allocate all the time`. There may be cases when it is required to re-construct an object multiple times so, placement new operator might be more efficient in these cases.

Advantages of placement new operator over new operator:

- The address of memory allocation is known before hand;
- Useful when building a memory pool, a garbage collector or simply when performance and exception safety are paramount;
- There’s no danger of allocation failure since the memory has already been allocated, and constructing an object on a pre-allocated buffer takes less time;
- This feature becomes useful while working in an environment with limited resources.


How to delete the memory allocated by placement new ?

The operator delete can only delete the storage created in heap, so when placement new is used delete operator cannot be used to delete the storage. In the case of memory allocation using placement new operator, since `it is created in stack` the compiler knows when to delete it and it will handle deallocation of the memory automatically. If required, one can write it with the help of destructor.

## REFs
- <https://en.cppreference.com/w/cpp/language/new>
- <https://www.geeksforgeeks.org/placement-new-operator-cpp/>
- <https://www.jianshu.com/p/4af119c44086>
- <https://stackoverflow.com/questions/222557/what-uses-are-there-for-placement-new>
- C++ Optimization: Making use of Memory Pools: <https://jsdw.me/posts/cpp-memory-pools/>
