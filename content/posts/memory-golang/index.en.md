---
# weight: 1
title: "Golang: How Linux distributes data"
date: 2025-09-19
lastmod: 2025-09-19
draft: false
description: "Linux memory allocation for Golang"
images: []
resources:
  - name: "featured-image"
    src: "golang-memory.jpeg"
tags: ["Golang", "Linux"]
lightgallery: true
---

<!--more-->

{{< admonition >}}
This is an empirical example showing where program data will be located.
Some things won’t be explained here, but a final conclusion will be drawn.
For better understanding, you should refer to topics like: **memory management in Go**, **ELF format**, **memory management in Linux**.
{{< /admonition >}}

When studying the basics of the language, it’s impossible to avoid the question of how memory management works.
Some specialists, while explaining, even start predicting where and what data will be located and freely use terms such as stack and heap.

But what is the situation really like? To find the answer, I turned to Linux.

---

## 1. Strings

### 1.1 Strings in different areas of a program

As a warm-up, let’s dig right in.
Consider a program with strings located in different areas:

```go
package main

import (
 "fmt"
 "time"
)

var GlobalVar string = "zzzzzzzzzzzzz"

func check() string {
 funcVar := "lllllllllllll"
 return funcVar
}

func main() {
 var mainVar string = "xxxxxxxxxxxxxx"
 mainVar = "eeeeeeeeeeeee" // rewrite
 fmt.Println(check())
 fmt.Println(mainVar, GlobalVar)
 time.Sleep(1 * time.Hour)
}
```

### 1.1 Searching in the executable file

We disable debug info and compile:

```sh
go build -ldflags="-s -w" ./main
```

After building, let’s look at the executable’s sections (just in case you forgot their names):

```sh
readelf -S main
```

\[output of sections omitted for brevity]

Searching for our values in the sections using the strings:

```sh
objdump -s main -j .rodata | grep -e eeeee -e zzzzz -e llllll -e xxxxx
```

Success — all our strings are in the **.rodata** section, close to each other.
And the string `xxxxxxxxxxxxxx` was replaced and discarded by the compiler.

### 1.2 Analyzing the process

Now let’s try to find these same strings in a running process and at the same time get familiar with process addressing.

\[process analysis with `pmap`, memory dump, and `strings` search]

### 1.3 Strings. Preliminary conclusion

The compiler placed static data in the **.rodata** segment, which is immutable and closely tied to **.text**.
Interestingly, the **funcVar** data declared inside the function also ended up in **.rodata**.
(But things will get even more interesting later—don’t switch channels.)

---

## 2. Variables

### 2.1 Pointer to a variable

Although the data itself is in **.rodata**, that doesn’t necessarily mean we operate on it directly.
Let’s check!

\[debugging with `gdb`, showing Go string representation as `{ptr *byte; len int}`]

Success — we confirmed how Go strings are stored.

### 2.2 Variable scope

Now let’s focus on variables with different scopes:

```go
package main

import (
 "fmt"
 "time"
)

func privFunc() int {
 funcVar := 200000
 return funcVar
}

var GlobalVar int = 3000 // Global

func main() {
 mainVar := 55
 fmt.Println(GlobalVar, mainVar, privFunc())
 time.Sleep(time.Duration(30) * time.Hour)
}
```

Debugging shows:

- The global variable ends up in **.data**.
- Local variables and function variables go into the `000000c000000000–000000c000400000` region, which Linux sees as anonymous `mmap()` memory.

In Go this can be either heap or stack, and our task is to figure out which is which.

Normally local variables are stored on the stack, but the compiler may put them on the heap.

\[escape analysis with `go build -gcflags="-m"`]

It turns out everything escapes to the heap, including the global variable.
This shows that Go’s runtime abstracts memory away from Linux.
Even though data physically resides in **.data**, Go exposes it via the heap, managed by the garbage collector.

### 2.3 Comparing Go’s stack and heap

By forcing the compiler not to escape a variable (using `runtime.KeepAlive`), we can keep it on the stack.
Debugging shows that stack and heap variables may live right next to each other in the same region `000000c000000000`.

---

## 3. Allocating a large memory block

We write a program that allocates 200 MB:

```go
package main

import (
 "fmt"
 "runtime"
)

func main() {
 data := make([]byte, 200*1024*1024) // 200 MB
 for i := range data {
  data[i] = byte(i % 256)
 }
 var memStats runtime.MemStats
 runtime.ReadMemStats(&memStats)
 fmt.Printf("Allocated memory: %.2f MB\n", float64(memStats.Alloc)/(1024*1024))
 fmt.Println("Press Enter to exit...")
 fmt.Scanln()
}
```

The compiler reports:
`make([]byte, 209715200) escapes to heap`

Checking with `pmap`, we see the memory in the anonymous region `000000c000000000`.

---

## 4. Memory allocation mechanism

Running under `strace` shows that memory is allocated via **mmap()**.
First, large chunks are reserved with **PROT_NONE**, then smaller regions are committed with **PROT_READ|PROT_WRITE**.

---

## 5. Conclusions

From our analysis:

1. Go has its own allocation model and entities (stack, heap) independent of Linux.
2. Global variables, statics, and strings are placed in **.rodata** and **.data**.
3. Memory from Linux is obtained via **mmap()** in an anonymous region.
4. Go’s heap and stack may lie side by side in the same address space, but only Go’s memory manager knows what is what.
5. Memory is reserved in large regions first, then split into chunks as needed during execution.

---
