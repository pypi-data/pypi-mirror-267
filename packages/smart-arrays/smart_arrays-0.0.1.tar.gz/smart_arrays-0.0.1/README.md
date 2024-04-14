# Smart Arrays

I created this project for two reasons. For a college project I wanted to have the flexibility of numpy arrays (which I absolutely love), especialy their ability to do element-wise operations and type safety (in Python, when doing math, I hate it that if you use simple lists, any element can be of any type. I need type safety!), but didn't want to have to use a library so big. I also wanted to try to understand how would one come to implement something like numpy arrays' api. This library is the result.

Everything stems out of the class SmartArray, which is a simple wrapper around a list, that has static size and is type safe. There is also a SmartList, which is the same but its size is mutable. I'll provide a list below with all available objects

| Object name        | Fixed size? | Implements [collections.abc](https://docs.python.org/3/library/collections.abc.html) |
| ------------------ | ----------- | --------------------------- |
| SmartArray         | Yes         | Sequence[T]                 |
| SmartList          | No          | MutableSequence[T] (almost) |
| SmartArrayNumber   | Yes         | Set[C]                      |
| SmartListNumber    | No          | MutableSet[C]               |
| SmartArrayComplex  | Yes         | Set[complex]                |
| SmartListComplex   | No          | MutableSet[complex]         |
| SmartArrayFloat    | Yes         | Set[float]                  |
| SmartListFloat     | No          | MutableSet[float]           |
| SmartArrayInt      | Yes         | Set[int]                    |
| SmartListInt       | No          | MutableSet[int]             |
| SmartArrayBool     | Yes         | Set[bool]                   |
| SmartListBool      | No          | MutableSet[bool]            |
| UncertaintiesArray | Yes         | Set[ufloat] (almost)        |
| UncertaintiesList  | No          | MutableSet[ufloat] (almost) |

Where T is any type and C is bound to complex. That means complex, float, int or bool. Also, if you have installed the [uncertainties](https://pythonhosted.org/uncertainties/) package, you can also use the UncertaintiesArray and UncertaintiesList. These work like SmartArrayNumber and SmartListNumber (except for some boolean, logic and binary operations) but their type is ufloat. That means that any arithmetical operation propagates the error, element-wise!

In utils I wrote some utility functions for these Arrays/Lists, for example way to save and load arrays to and from disk.

In stats I wrote functions to do some statistical analysis. 

I'm very busy with college, but I'll try to keep updating this to make it more friendly for users. :)
