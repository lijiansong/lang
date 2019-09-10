
Q: When is `std::weak_ptr` useful?
A: A good example would be a cache.

For recently accessed objects, you want to keep them in memory, so you hold a strong pointer to them. Periodically, you scan the cache and decide which objects have not been accessed recently. You don't need to keep those in memory, so you get rid of the strong pointer.

But what if that object is in use and some other code holds a strong pointer to it? If the cache gets rid of its only pointer to the object, it can never find it again. So the cache keeps a weak pointer to objects that it needs to find if they happen to stay in memory.

This is exactly what a weak pointer does -- it allows you to locate an object if it's still around, but doesn't keep it around if nothing else needs it.

# REF
- <https://zh.cppreference.com/w/cpp/memory/weak_ptr>
- <https://stackoverflow.com/questions/12030650/when-is-stdweak-ptr-useful>
