+++
title = "Python's for loop explained"
date = "2019-01-04T13:50:46+02:00"
author = "Oscar Forner"
tags = ["Python", "For", "Loop"]
categories = ["Development"]
+++

**Have you ever thought about how the *for loop* is implemented in Python?** I always thought it would iterate over all elements in the sequence, like it does, but that first it would query the sequence to know its length and then request that many elements. **Turns out, it does not work like that.**

```python
>>> for item in range(5):
... 	print(item)
...
0
1
2
3
4
```

So, how does it work? Basically, **the *for loop* just keeps requesting more elements from the sequence until it raises a `StopIteration` or an `IndexError` exception**. The `Collection protocol` that behaves that way is the `Iterator protocol`. **Therefore, anything that implements the `Iterator protocol` could be used in the *for loop*.**

## Iterator protocol
The only requirements for a class to implment the `Iterator protocol` is the following:

* `__next__()` method that returns the following element in the sequence. It will raise the `StopIteration` exception when all elements in the sequence have been visited.
* `__iter__()` method that returns the iterator itself.

Alternatively, the `Iterator protocol` can fallback to be implemented by just using the `__getitem__()` method.

### Default implementation
The following example of a default implementation of the `Iterator protocol` will show how the *for loop* behaves when the `__iter__` and `__next__` methods are available.

```python
class MyIterator:
    def __init__(self, data):
        self._index = 0
        self._data = data
    
    def __iter__(self):
        print('Called __iter__ method')
        return self
    
    def __next__(self):
        print(f'Called __next__ method {self._index} times')
        if self._index >= len(self._data):
            raise StopIteration()
        
        result = self._data[self._index]
        self._index += 1
        return result
```

```python
>>> for _ in MyIterator([1, 2, 3, 4, 5]):
...     pass
...
Called __iter__ method
Called __next__ method 0 times
Called __next__ method 1 times
Called __next__ method 2 times
Called __next__ method 3 times
Called __next__ method 4 times
Called __next__ method 5 times
```

Note how the first thing the *for loop* does is to call the `__iter__` method, and then it keeps calling the `__next__` method until it raises the `StopIteration` exception.

### Alternative implementation
The following example of an alternative implementation of the `Iterator protocol` will show how the *for loop* behaves when the `__iter__` and `__next__` methods are not available, but the `__getitem__` method is.

```python
class AlternativeIterator:
    def __init__(self, data):
        self._data = data
    
    def __getitem__(self, index):
        print(f'Called __getitem__ method with index {index}')
        return self._data[index]
```

```python
>>> for _ in AlternativeIterator([1, 2, 3, 4, 5]):
...     pass
...
Called __getitem__ method with index 0
Called __getitem__ method with index 1
Called __getitem__ method with index 2
Called __getitem__ method with index 3
Called __getitem__ method with index 4
Called __getitem__ method with index 5
```
Note how the *for loop* just keeps calling the `__getitem__` method with an ever increasing index until the `IndexError` exception is raised.

## Closing notes
As you have seen, Python's approach to the *for loop* is to keep requesting elements until the iterator runs out of data and raises an exception. This is a very interesting approach and proves that Python exceptions are an integral part of the language and not a last minute addition to the language.