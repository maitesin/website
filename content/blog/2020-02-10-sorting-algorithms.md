+++
title = "Sorting algorithms"
date = "2020-02-10T13:50:46+02:00"
author = "Oscar Forner"
tags = ["Sorting"]
categories = ["Algorithm"]
+++

## Introduction

Before we start, I want to define a couple of terms:

* **In place**: the algorithm does not require extra space to be executed. In other words, if you have to sort and array of *n* elements, the algorithm will use only that array of *n* elements.
* **Stable**: if two elements of the array are the same, they will keep the same relative order in the array after being sorted. For example, if you want to sort the array [<span style="color:green">3</span>, 1, 4, <span style="color:red">3</span>, 2], the result would be [1, 2, <span style="color:green">3</span>, <span style="color:red">3</span>, 4].

Arguably these are the four most important sorting algorithms, **Quicksort**, **Merge Sort**, **Heapsort** and **Insertion Sort**.

{{< rawhtml >}}
<center>
{{< /rawhtml >}}

| Algorithm | Best Time | Average Time | Worst Time | Space | Stable |
|:---:|:---:|:---:|:---:|:---:|:---:|
| Quicksort | <span style="color:green">O(n log n)</span> | <span style="color:green">O(n log n)</span> | <span style="color:red">O(n^2)</span> | <span style="color:green">O(1)</span> | <span style="color:red">No</span> |
| Merge Sort | <span style="color:green">O(n log n)</span> | <span style="color:green">O(n log n)</span> | <span style="color:green">O(n log n)</span> | <span style="color:red">O(n)</span> | <span style="color:green">Yes</span> |
| Heapsort | <span style="color:green">O(n log n)</span> | <span style="color:green">O(n log n)</span> | <span style="color:green">O(n log n)</span> | <span style="color:green">O(1)</span> | <span style="color:red">No</span> |
| Insertion Sort | <span style="color:green">O(n)</span> | <span style="color:red">O(n^2)</span> | <span style="color:red">O(n^2)</span> | <span style="color:green">O(1)</span> | <span style="color:green">Yes</span> |

{{< rawhtml >}}
</center>
{{< /rawhtml >}}

## Quicksort
**Quicksort is the fastest one of the lot**, as its constants are smaller than the others. The best case scenario *O(n log n)* happens when **the data to be sorted is not already sorted or all their values are the same**. Another of its strong points is that it is **in place**, however, it is **not stable**.

### How does it works?
Given an input array a pivot element needs to be selected (a simple approach is to select the first element in the array). Then, you have to swap elements in the array to leave all smaller elements than the pivot in the left side of the pivot, and the elements equal or greater than the pivot in the right hand side of it. **This will leave the pivot in its sorted place in the array**. Now repeat the same process with the two arrays (left and right) from the pivot until the length of the remaining arrays is less than 2.

{{< rawhtml >}}
<center>
<div style="width:28%">
{{< /rawhtml >}}
![](/img/blog/sorting/quicksort.svg)
{{< rawhtml >}}
</div>
</center>
{{< /rawhtml >}}

### Optimizations
The are two main problems with the **quicksort** algorithm that can make it run at the worst performance. In both cases, the array is always split at the beginning of it, having to do the same operation over the whole array over and over instead of having it split in about half:

1. **Sorted array**: one way to solve this problem is to **randomize the input array before starting to apply the algorithm**.
2. **All values in the array are the same**: one way to solve this problem is to use two pointers for the pivot. This way when comparing the elements in the array, on top of doing all the work done before, it **keeps track of all the equal values to the pointer and then places them at right place**. Only the remaining values have to be sorted.

### When to use it?
Since **quicksort is the fastest** of the sorting algorithms it's the most commonly used. Though, you need to be aware of it **not being stable**.

## Merge Sort
**Merge sort has the most predictable performance of the lot**, since its best and worst case scenario is the same *O(n log n)*. This is due to it not being affected by the input state or values. In addition, it is a **stable** algorithm, but it requires an extra *n* space to run, where *n* is the length of the array.

### How does it works?
Given an input array it gets split in half over and over until the length of the remaining arrays is less than 2. At that point, all these arrays are sorted, now we just need to merge these arrays, but keeping them sorted.

{{< rawhtml >}}
<center>
<div style="width:40%">
{{< /rawhtml >}}
![](/img/blog/sorting/mergesort.svg)
{{< rawhtml >}}
</div>
</center>
{{< /rawhtml >}}

### Optimizations
Since **merge sort** is a really consistent algorithm, the main optimizations have been focused on lowering the constants of its performance and making it work **in place**. The most notable optimizations are that an **in place merge sort** and **merge sort is highly parallelizable**, this means that it can be run in multiple cores, or even distributed among several machines.

### When to use it?
Since **merge sort has the most predictable execution time**, it is used when the worst case scenario cannot be allowed to be greater than *O(n log n)*. Moreover, the **merge sort algorithm is used when sorting tables, to take advantage of it being stable**.

Because of the consistent performance of the **merge sort**, being **stable** and having an **optimization to be in place**, some standard libraries from programming languages use it as its default sorting algorithm.

## Heapsort
**Heapsort has an equivalent predictable performance as merge sort**, but **heapsort is not a stable** algorithm. The **heapsort** algorithm leverages the usage and performance of the **priority queue implementation of a max-heap**.

### How does it works?
Given an input array, first of all an algorithm known as **heapify**, with cost *O(n)*, must be applied to it. This leaves the array ready to be used as a **max-heap**. At this point, the only thing left to do is extracting the *n* elements in the heap. This has a cost of *O(log n)* per element extracted, giving it a total cost of *O(n log n)*.

{{< rawhtml >}}
<center>
<div style="width:30%">
{{< /rawhtml >}}
![](/img/blog/sorting/heapsort.svg)
{{< rawhtml >}}
</div>
</center>
{{< /rawhtml >}}

### Optimizations
**Heapsort** does not have any optimizations that stand up or that give a clear improvement against the basic implementation.

### When to use it?
**Heapsort is mostly used when the data to be sorted is contantly changing**. For example, if you are not sorting a static array, but a list of elements that are going to change its values, get removed or added to the list. Your best bet is to use **priority queue** and it will keep the elements sorted.

## Insertion Sort
**Insertion sort has the best case performance**, but it also has the worst average and worst case performance. However, **insertion sort is a stable and in place** algorithm.

### How does it works?
**Insertion sort** leaves the already sorted elements to the left of the array and the unsorted elements to the right. Hence, it first sorts the first element of the array, then it sorts the second element of the array, and so on and so forth until every element of the arrray has been sorted.

{{< rawhtml >}}
<center>
<div style="width:30%">
{{< /rawhtml >}}
![](/img/blog/sorting/insertsort.svg)
{{< rawhtml >}}
</div>
</center>
{{< /rawhtml >}}

### Optimizations
**Insertion sort** does not have any optimizations that stand up or that give a clear improvement against the basic implementation.

### When to use it?
Since **insertion sort** is the only algorithm of the lot that is iterative in nature and not recursive, **it has a good performance for small arrays**. This means that even if the average case is worse than the one for **quicksort** or **merge sort**, **in practice it can be faster than them**.

## Conclusion
The more you know about the data and use case you have to sort, the better choice of sorting algorithm you will be able to make.

Finally, I want to mention that **there are hybrid approaches**. For example, when sorting an array, you can first check its length and if it's a small array you can call **insertion sort** straight away, if not you can call either **quicksort** or **merge sort** and work recursively until the length of the array is small enough for **insertion sort** to be faster.
