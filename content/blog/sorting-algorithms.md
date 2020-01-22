+++
title = "Sorting algorithms"
date = "2020-02-07T13:50:46+02:00"
author = "Oscar Forner"
tags = ["Sorting"]
categories = ["Algorithm"]
+++

Before we start I want to define a couple of terms:

* **In place**: means that the algorithms does not require extra space to be executed. In other words, if you have to sort and array of *n* elements, the algorithms will use only that array of *n* elements.
* **Stable**: means that if two elements of the array are the same, they will keep the same relative order in the array after being sorted. For example, if you want to sort the array [<span style="color:green">3</span>, 1, 4, <span style="color:red">3</span>, 2], the result would be [1, 2, <span style="color:green">3</span>, <span style="color:red">3</span>, 4].

Arguably these are the for most important sorting algorithms, **Quicksort**, **Merge Sort**, **Heapsort** and **Insertion Sort**. 

<center>

| Algorithm | Best Time | Average Time | Worst Time | Space | Stable |
|:---:|:---:|:---:|:---:|:---:|:---:|
| Quicksort | <span style="color:green">O(n log n)</span> | <span style="color:green">O(n log n)</span> | <span style="color:red">O(n^2)</span> | <span style="color:green">O(1)</span> | <span style="color:red">No</span> |
| Merge Sort | <span style="color:green">O(n log n)</span> | <span style="color:green">O(n log n)</span> | <span style="color:green">O(n log n)</span> | <span style="color:red">O(n)</span> | <span style="color:green">Yes</span> |
| Heapsort | <span style="color:green">O(n log n)</span> | <span style="color:green">O(n log n)</span> | <span style="color:green">O(n log n)</span> | <span style="color:green">O(n)</span> | <span style="color:red">No</span> |
| Insertion Sort | <span style="color:green">O(n)</span> | <span style="color:red">O(n^2)</span> | <span style="color:red">O(n^2)</span> | <span style="color:green">O(1)</span> | <span style="color:green">Yes</span> |

</center>

# Quicksort
**Quicksort is the fastest one of the lot**, since its constants in the best case scenario *O(n log n)* smaller than the others, **if the data to be sorted is not already sorted or all their values are the same.** Another of it's strong points is that it is **in place**, however, it is **not stable**.

## How it works?
Given an input array a pivot element needs to be selected (a simple approach is to select the first element in the array). Then, you have to swap elements in the array to leave all smaller elements than the pivot in the left side of the pivot, and the elements equal or greater than the pivot in the right hand side of it. **This will leave the pivot in its sorted place in the array**, now repeat the same process with the two arrays (left and right) from the pivot until the remaining arrays length is less than 2.

<center>
<div style="width:28%">
![](/img/blog/sorting/quicksort.svg)
</div>
</center>

## Optimizations
The are two main problems with the **quicksort** algorithm that can make it run at the worst performance. In both cases the array is always split at the beginning of it, and the having to do the same operation over the whole array over and over instead of having it split in about half:

1. **Sorted array**: one way to solve this problem is to **randomize the input array before starting to apply the algorithm**.
2. **All values in the array are the same**: one way to solve this problem is to use two pointers for the pivot. This way when comparing the elements in the array, on top of doing all the work done before, it **keeps track of all the equal values to the pointer and then placing them in their right place**. Only the remaining values have to be sorted.

## When to use it?
Since **quicksort is the fastest** of the sorting algorithm it's the most commonly used. Only have to be aware of it **not being stable**.

# Merge Sort
**Merge sort has the most predictable performance of the lot**, since it's best and worst case scenario is the same *O(n log n)*. This is because it is not affected by the input state or values. In addition, is it a **stable** algorithm, but requires an extra *n* space to run, where *n* is the length of the array.

## How it works?
Given an input array it gets split in half over and over until the remaining arrays length is less than 2. At that point all these arrays are sorted, now we just need to merge these arrays, but keeping them ordered.

<center>
<div style="width:40%">
![](/img/blog/sorting/mergesort.svg)
</div>
</center>

## Optimizations
Since **merge sort** is a really consistent algorithm the main optimizations that it has have been focused on lowering the constants of its performance. The most notable optimization is that **merge sort is highly parallelizable**, this means that it can be run in multiple cores, even distributed among several machines.

## When to use it?
Since **merge sort has the most predictable execution time** it is used when the worst case scenario cannot be allowed to be longer than *O(n log n)*. Moreover, the **merge sort algorithm is used when sorting tables, to take advantage of it being stable**.

# Heapsort
**Heapsort has an equivalent predictable performance as merge sort**, but **heapsort is not a stable** algorithm. The **heapsort** algorithm leverages the usage and performance of the **priority queue implementation of a min-heap**.

## How it works?
Given an input array, first of all an algorithm known as **heapify**, with cost *O(n)*, must be applied to it. This leaves the array ready to be used as a **min-heap**. At this point only extracting the *n* elements in the heap is left. This has a cost of *O(log n)* per element extracted, giving it a total cost of *O(n log n)*.

<center>
<div style="width:30%">
![](/img/blog/sorting/heapsort.svg)
</div>
</center>

## Optimizations
**Heapsort** does not have any optimizations that stand up or that gives a clear improvement against the basic implementation.

## When to use it?
**Heapsort is mostly used when the data to be sorted is contantly changing**. For example, if you are not sorting a static array, but a list of elements that are going to change its values, get remove, or get added to the list. Your best bet is to use **priority queue** and it will keep the elements sorted.

# Insertion Sort
**Insertion sort has the best case performance**, but has the worst average and worst case performance. However, **insertion sort is a stable and in place** algorithm.

## How it works?
**Insertion sort** leaves the already sorted elements in the left and the unsorted elements in the right. So, it first sorts the first element of the array, then it sorts the second element of the array, and so on and so forth until every element of the arrray has been sorted.

<center>
<div style="width:30%">
![](/img/blog/sorting/insertsort.svg)
</div>
</center>

### Optimizations
**Insertion sort** does not have any optimizations that stand up or that gives a clear improvement against the basic implementation.

### When to use it?
Since **insertion sort** is the only algorithm of the lot that is iterative in nature and not recursive, **it has a good performance for small arrays**. This means that even if the average case is worse than the one for **quicksort** or **merge sort**, **in practice it can be faster than them**.

## Conclusion
The more you know about the data and use case you have to sort, the better choice of sorting algorithm you will be able to do. 

Finally, I want to mention that **there are hybrid approaches**. For example when sorting an array, you can first check it's length and if it's a small array you can call **insertion sort** straight away, if not you can call either **quicksort** or **merge sort** and work recursively until the length of the array is small enough for **insertion sort** to be faster.
