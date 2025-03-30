---
# weight: 1
title: "Golang in brief"
date: 2025-03-28
lastmod: 2025-03-28
draft: false
description: "This article contains basic knowledge of golang"
images: []
resources:
  - name: "featured-image"
    src: "golang-basic.webp"

tags: ["Golang"]
categories: ["Documentation"]

lightgallery: true
---

In a nutshell about everything in golang.

<!--more-->

{{< admonition >}}
This is a very brief summary.
If you want to get a basic understanding of Golang, check out the [Golang tutorial](https://go.dev/doc/tutorial/).
{{< /admonition >}}

Go is a compiled, statically typed programming language developed by Google.
The first stable version was released in 2012.

## 1. Declaring Variables

Explicit Declaration (var keyword):

```go
var car string
var name string = "John"
var age int = 25
var isStudent bool = false
```

Implicit Declaration (:= operator):

```go
// Possible in inner function
name := "Alice"  // Type inferred as string
age := 30        // Type inferred as int
isStudent := true // Type inferred as bool
```

A variable name is an arbitrary identifier consisting of letters,
numbers, and the underscore character (**\_**). And do not include reserved words.

Private variables start with a lowercase letter and are accessible only from within the package,
public variables start with an uppercase letter and are accessible from other packages.

## 2. Basic Types in Go

### 2.1. Primitive Types

| Type                      | Description                        | Min/Max Value                       | Default  |
| ------------------------- | ---------------------------------- | ----------------------------------- | -------- |
| `bool`                    | Boolean (`true`, `false`)          | `false` / `true`                    | `false`  |
| `string`                  | Immutable sequence of characters   | `""` / N/A                          | `""`     |
| `int`                     | Integer (platform-dependent)       | `-2^63` to `2^63-1` (64-bit)        | `0`      |
| `int8`                    |                                    | `-128` to `127`                     | `0`      |
| `int16`                   |                                    | `-32,768` to `32,767`               | `0`      |
| `int32`                   |                                    | `-2,147,483,648` to `2,147,483,647` | `0`      |
| `int64`                   |                                    | `-2^63` to `2^63-1`                 | `0`      |
| `uint`                    | Unsigned Integer (p.- d.)          | `0` to `-2^64` (64-bit)             | `0`      |
| `uint8`                   |                                    | `0` to `255`                        | `0`      |
| `uint16`                  |                                    | `0` to `65,535`                     | `0`      |
| `uint32`                  |                                    | `0` to `4,294,967,295`              | `0`      |
| `uint64`                  |                                    | `0` to `2^64 - 1`                   | `0`      |
| `float32`, `float64`      | Floating-point numbers             | `~2.3E-308` to `~1.8E308`           | `0.0`    |
| `complex64`, `complex128` | Complex numbers                    | N/A                                 | `(0+0i)` |
| `byte`                    | Represents a byte (alias `uint8`)  | `0` to `255`                        | `0`      |
| `rune`                    | Unicode character (alias `uint32`) | `0` to `2^31-1`                     | `0`      |

### 2.2. Composite Types

| Type        | Description                               | Size (bytes)                      | Default     |
| ----------- | ----------------------------------------- | --------------------------------- | ----------- |
| `array`     | Fixed-size collection                     | Depends on element type & length  | `[0,0,...]` |
| `slice`     | Dynamic-size collection (backed by array) | 24 (on 64-bit)                    | `nil`       |
| `map`       | Key-value storage                         | Varies (depends on keys/values)   | `nil`       |
| `struct`    | Custom data type (grouping fields)        | Sum of field sizes (with padding) | `{}`        |
| `pointer`   | Stores memory address of a variable       | 4 (32-bit) / 8 (64-bit)           | `nil`       |
| `interface` | Defines behavior, not data                | 16 (on 64-bit)                    | `nil`       |

## 3. Pointers

Pointer manipulation:

```go
var p *int // create pointer
a := 2
p = &a
*p++
fmt.Println(*p) // value (3)
fmt.Println(&p) // address (0xc0000a2038)
```

## 4. Constants (const keyword)

Constants have immutable values and must be initialized at the time of declaration:

```go
const Pi float64 = 3.14159
const Greeting = "Hello, Go!"
```

Numerations:

```go
const (
  Sunday = iota // 0
  Monday
  Tuesday
  Wednesday
  Thursday
  Friday
  Saturday  // 6
  _         // skip 7
  New       // 8
)
```

## 5. Logical operation

| Operator | Name | Description                                          |
| -------- | ---- | ---------------------------------------------------- |
| `&&`     | AND  | Returns `true` if **both** conditions are true       |
| `\|\|`   | OR   | Returns `true` if **at least one** condition is true |
| `!`      | NOT  | Negates a boolean expression                         |

## 6. Control Flow Keywords

| Keyword       | Purpose                                                                 |
| ------------- | ----------------------------------------------------------------------- |
| `fallthrough` | Forces execution of the next `case` in a `switch`, ignoring conditions. |
| `continue`    | Skips the current iteration of a loop and moves to the next one.        |
| `break`       | Exits a loop or `switch` statement immediately.                         |
| `return`      | Exits a function and optionally returns values.                         |
| `goto`        | Jumps to a labeled statement (use sparingly).                           |
| `defer`       | Defers execution of a function until the surrounding function exits.    |
| `panic`       | Triggers an error and stops execution.                                  |
| `recover`     | Catches a `panic` to prevent program termination.                       |

## 7. Go Creation & Manipulation Operators

| Function                  | Purpose                                                                     |
| ------------------------- | --------------------------------------------------------------------------- |
| `new(T)`                  | Allocates memory for type `T`, returns a pointer to `T`. `p := new(int)`    |
| `make(T, size, cap)`      | Creates slices, maps, or channels with a given size and capacity.           |
| `append(slice, elems...)` | Adds elements to a slice, returning a new slice if capacity changes.        |
| `copy(dst, src)`          | Copies elements from `src` to `dst`, returns the number of elements copied. |
| `len(container)`          | Returns the length of a slice, map, array, or string.                       |
| `cap(slice)`              | Returns the capacity of a slice.                                            |
| `delete(map, key)`        | Removes a key from a map.                                                   |

## 8. Custom Types (type keyword)

Golang allows defining new types:

```go
type Age int
var myAge Age = 25
```

## 9. Composite Types (Collections & Structures)

Group multiple values using arrays, slices, maps, structs, and pointers.

### 9.1 Arrays (Fixed Size)

Arrays have a fixed length and store elements of the same type:

```go
var numbers [3]int = [3]int{10, 20, 30}
fmt.Println(numbers[0]) // Output: 10

// Shorthand:
numbers := [...]int{1, 2, 3} // Compiler infers size
```

### 9.2 Slices (Dynamic Size)

Slices are more flexible than arrays and contain:

- capacity,
- length,
- pointer to an underlying array.

```go
var slice1 = make([]int, 4, 7) // Set len(), cap()
nums := []int{10, 20, 30} // Slice with 3 elements
slice4 := array[:] // Convert array to slice
nums = append(nums, 40) // Expands the slice
```

Truncate slice:

```go
baseArray := [8]string{"Anna", "Max", "Eva", "Leo", "Nina", "Tom", "Sophie", "Chris"} // the base array

slice1 := baseArray[1:5] // from 2 to 5 element [Max Eva Leo Nina]
slice2 := baseArray[:3]  // from 1 to 3 element [Anna Max Eva]
slice3 := baseArray[4:]  // to 5 [Nina Tom Sophie Chris]
```

Remove element from slice:

```go
a := []int{1, 2, 3, 4, 5, 6, 7}
a = append(a[0:2], a[3:]...)
fmt.Println(a) // [1 2 4 5 6 7]
```

### 9.3 Maps (Key-Value Pairs)

A map stores values using a key:
map is a reference to a hash table.

```go
person := map[string]int{"Alice": 25, "Bob": 30}
fmt.Println(person["Alice"]) // Output: 25
```

Check key in the map:

```go
if value, ok := m[1]; ok {
 fmt.Println(value) // key exist
}
```

### 9.4 Structures (Custom Data Types)

Allow grouping different types into a single unit:

```go
type Person struct {
  Name string
  Age int
}
p := Person{Name: "John", Age: 30}
fmt.Println(p.Name) // Output: John
```

Anonymous structure:

```go
student := struct {
  name string
  id   int64
  age  int32
}{
  name: "Julia",
  id:   12345,
  age:  30,
}
```

## 10. String

String it's the immutable sequence of characters.
But string maybe representation as []byte or []rune and modifying.
**Rune** (alias **int32**) determinate a symbol (1-4 bytes) for support UTF-8.

## 11. Format Specifiers for `fmt.Printf`

| Format | Description                     |
| ------ | ------------------------------- |
| `%v`   | Default format for the value    |
| `%+v`  | Struct with field names         |
| `%#v`  | Go syntax representation        |
| `%T`   | Type of the value               |
| `%%`   | Literal `%`                     |
| `%d`   | Decimal                         |
| `%b`   | Binary                          |
| `%o`   | Octal                           |
| `%x`   | Hexadecimal (lowercase)         |
| `%X`   | Hexadecimal (uppercase)         |
| `%c`   | Character representation        |
| `%U`   | Unicode format                  |
| `%f`   | Decimal (default precision 6)   |
| `%.2f` | Fixed decimal (2 places)        |
| `%e`   | Scientific notation (lower)     |
| `%E`   | Scientific notation (upper)     |
| `%g`   | Compact float (auto `e` or `f`) |
| `%G`   | Compact float (upper `E`)       |
| `%s`   | String                          |
| `%q`   | Quoted string                   |
| `%x`   | Hex dump (lowercase)            |
| `%X`   | Hex dump (uppercase)            |
| `%t`   | Boolean                         |
| `%p`   | Pointer address                 |

## 12. Function

In Go, parameters are passed to a function by value, meaning a copy of them is passed.
Changes to parameters inside the function do not affect the original variables.
Including the link.

**Closure** is an anonymous function that captures and remembers the variables from its surrounding scope:

```go
func counter() func() int {
    count := 0
    return func() int {
        count++
        return count
    }
}

func main() {
    inc := counter() // Creates a closure
    fmt.Println(inc()) // 1
    fmt.Println(inc()) // 2
    fmt.Println(inc()) // 3
}
```

Function of constructor:

```go
func newProduct(name, category string, price float64)
 *Product {
     return &Product{name, category, price}
}
```

## 13. Interface (Dynamic Type)

Interfaces define behavior without specifying exact types:

```go
type Speaker interface {
  MetaSpeakerInterface
  Speak() string
}
```

```go
type Dog struct{}
  func (d Dog) Speak() string {
  return "Woof!"
}

var animal Speaker = Dog{}
fmt.Println(animal.Speak()) // Output: Woof!
```

Find type of variable:

```go
func display(a interface{}) {
  // Using type switch
  switch a.(type) {
  case int, uint: //задаем два условия
    fmt.Printf("Type:%T -- Value:%v\n", a, a.(int))
  case string:
    fmt.Printf("Type:%T -- Value:%v\n", a, a.(string))
  case float64:
    fmt.Printf("Type:%T -- Value:%v\n", a, a.(float64))
  default:
    fmt.Println("Type not found")
  }
}
```

## 14. Error

To create an error, you need to implement the interface:

```go
type error interface {
 Error() string
}
```

The other possible ways of creation:

```go
err := errors.New("my error") // Create error
eff := fmt.Errorf("other error")
panic("division by zero!") // Generate error and exit
// defer - recover - panic (banch)

```

## 15. Defer, panic and recover

In together:

```go
func safeFunction() {
    defer func() {
        if r := recover(); r != nil { // Handle panic
            fmt.Println("Recovered:", r)
        }
    }()

    fmt.Println("Before panic")
    panic("Unexpected error!")  // Panic occurs
    fmt.Println("After panic")  // This will not run
}
```

## 16. Goroutines

**Goroutines** are lightweight threads in Go that allow concurrent execution of functions.
Unlike traditional threads, they are managed by the Go runtime,
making them efficient and scalable.

### 16.1. Basics of Goroutines

You can start a new goroutine using the go keyword before a function call.

Running a Function as a Goroutine:

```go
package main

import (
  "fmt"
  "time"
)

func sayHello() {
  fmt.Println("Hello from goroutine!")
}

func main() {
  go sayHello() // Starts a new goroutine
  fmt.Println("Hello from main function!")

    time.Sleep(1 * time.Second) // Wait for goroutine to finish

// Output (Order may vary):
// Hello from main function!
// Hello from goroutine!
}
```

### 16.2. Running Multiple Goroutines

Create a Goroutines in cycle:

```go
package main

import (
  "fmt"
  "time"
)

func printNumber(n int) {
  fmt.Println("Number:", n)
}

func main() {
  for i := 1; i <= 5; i++ {
  go printNumber(i) // Each call runs in a new goroutine
  }
    time.Sleep(1 * time.Second) // Prevent main from exiting early
}
```

### 16.3. Synchronization with sync.WaitGroup

Using `sync.WaitGroup` to Wait for Goroutines:

```go
package main

import (
  "fmt"
  "sync"
)

func worker(id int, wg *sync.WaitGroup) {
  fmt.Printf("Worker %d started\n", id)
  wg.Done() // Decrement WaitGroup counter
}

func main() {
  var wg sync.WaitGroup

  for i := 1; i <= 3; i++ {
    wg.Add(1) // Increment counter
    go worker(i, &wg)
  }

  wg.Wait() // Block until all goroutines finish
  fmt.Println("All workers finished")
}
```

### 16.4. Communication Between Goroutines (Channels)

Creating and Using a Channel:

```go
package main

import "fmt"

func sendMessage(ch chan string) {
  ch <- "Hello from Goroutine!" // Send data into channel
}

func main() {
  ch := make(chan string) // Create a channel

  go sendMessage(ch)

  msg := <-ch // Receive data from channel
  fmt.Println(msg)
}
```

### 16.5. Buffered vs. Unbuffered Channels

Unbuffered Channels (default) block until the data is received.
Buffered Channels allow storing messages.

Buffered Channel Example:

```go
ch := make(chan int, 3) // Buffer size of 3
ch <- 1
ch <- 2
ch <- 3
fmt.Println(<-ch) // Output: 1
```

### 16.6. Closing a Channel

```go
   ch := make(chan int)

go func() {
  for i := 1; i <= 5; i++ {
  ch <- i
}
  close(ch) // Close channel after sending
}()

for num := range ch {
  fmt.Println(num) // Reads until channel is closed
}
```

### 16.7. Select Statement (Handling Multiple Channels)

The select statement lets a goroutine wait on multiple channels:

```go
package main

import (
  "fmt"
  "time"
)

func main() {
  ch1 := make(chan string)
  ch2 := make(chan string)

  go func() {
      time.Sleep(1 * time.Second)
      ch1 <- "Message from channel 1"
  }()

  go func() {
      time.Sleep(2 * time.Second)
      ch2 <- "Message from channel 2"
  }()

  select {
  case msg1 := <-ch1:
      fmt.Println(msg1)
  case msg2 := <-ch2:
      fmt.Println(msg2)
  case <-time.After(3 * time.Second):
      fmt.Println("Timeout!")
  }

}
```

### 16.8. Worker Pool Pattern (Efficient Goroutine Management)

```go
import (
  "fmt"
  "sync"
  "time"
)

func worker(id int, jobs <-chan int, results chan<- int) {
  for j := range jobs {
    fmt.Printf("Worker %d processing job %d\n", id, j)
    time.Sleep(time.Second)
    results <- j * 2
  }
}

func main() {
  jobs := make(chan int, 5)
  results := make(chan int, 5)

  var wg sync.WaitGroup

  for w := 1; w <= 3; w++ {
    wg.Add(1)
    go func(id int) {
      worker(id, jobs, results)
      wg.Done()
    }(w)
  }

  for j := 1; j <= 5; j++ {
    jobs <- j
  }
  close(jobs)

  wg.Wait()
  close(results)

  for res := range results {
    fmt.Println("Result:", res)
  }
}
```

### 16.9 Best Practices for Goroutines

- Always use a `sync.WaitGroup` when managing multiple goroutines.
- Use channels for safe communication instead of shared memory.
- Avoid memory leaks by ensuring all goroutines finish execution.
- Limit goroutines when handling many tasks using worker pools.
- Use `context.Context` for cancellation of long-running goroutines.

## 17. Handling Race Conditions with sync.Mutex

When multiple goroutines access shared data, race conditions can occur.
The `sync.Mutex` (mutual exclusion) helps prevent this.

```go
package main

import (
  "fmt"
  "sync"
  "time"
)

var counter = 0
var mu sync.Mutex // Mutex for safe access

func increment() {
  for i := 0; i < 1000; i++ {
  mu.Lock() // Lock access
  counter++ // Safe update
  mu.Unlock() // Unlock
  }
}

func main() {
  for i := 0; i < 5; i++ {
    go increment()
  }

  time.Sleep(time.Second)
  fmt.Println("Final Counter:", counter) // Correct result
}
```

## 18. Read-Write Synchronization with sync.RWMutex

If you have multiple readers but only one writer, use `sync.RWMutex`:

```go
package main

import (
  "fmt"
  "sync"
  "time"
)

var value = 0
var rw sync.RWMutex // Read-Write Mutex

func readValue(id int) {
  rw.RLock() // Lock for reading
  fmt.Printf("Reader %d reads value: %d\n", id, value)
  rw.RUnlock()
}

func writeValue(newValue int) {
  rw.Lock() // Lock for writing
  value = newValue
  fmt.Printf("Writer updated value to %d\n", value)
  rw.Unlock()
}

func main() {
  go readValue(1)
  go readValue(2)
  go writeValue(42)
  go readValue(3)

  time.Sleep(time.Second)
// Multiple readers can read concurrently, but only one writer can write.
}
```

## 19. Goroutine Cancellation with context.Context

Goroutines don’t stop automatically when main exits. Use context to control them.

Cancelling a Goroutine:

```go
package main

import (
  "context"
  "fmt"
  "time"
)

func worker(ctx context.Context) {
  for {
    select {
      case <-ctx.Done():
        fmt.Println("Worker stopped")
        return
      default:
        fmt.Println("Working...")
        time.Sleep(500 * time.Millisecond)
    }
  }
}

func main() {
  ctx, cancel := context.WithCancel(context.Background())

  go worker(ctx)

  time.Sleep(2 * time.Second)
  cancel() // Send cancellation signal

  time.Sleep(time.Second) // Wait to see output
}
```

## 20. Using context.WithTimeout for Timeouts

Automatically cancel goroutines after a timeout:

```go
package main

import (
  "context"
  "fmt"
  "time"
)

func worker(ctx context.Context) {
  for {
    select {
      case <-ctx.Done():
        fmt.Println("Timeout reached, worker stopping")
        return
      default:
        fmt.Println("Worker is running...")
        time.Sleep(500 * time.Millisecond)
    }
  }
}

func main() {
ctx, cancel := context.WithTimeout(context.Background(), 2 * time.Second)
defer cancel() // Clean up

    go worker(ctx)

    time.Sleep(3 * time.Second) // Ensure timeout occurs

}
```

## 21. Using sync.Once for One-Time Initialization

Use `sync.Once` to ensure a function runs only once, even if called multiple times:

```go
package main

import (
 "fmt"
 "sync"
)

var once sync.Once

func initConfig() {
 fmt.Println("Initializing config...")
}

func main() {
 wg := sync.WaitGroup{}

 for i := 0; i < 3; i++ {
  wg.Add(1)
  go func() {
   defer wg.Done()
   once.Do(initConfig) // Run once
  }()
 }

 wg.Wait()
}
```

## 22. Using sync.Cond for Goroutine Coordination

`sync.Cond` lets goroutines wait for a condition before proceeding:

```go
package main

import (
  "fmt"
  "sync"
  "time"
)

var cond = sync.NewCond(&sync.Mutex{})
var ready = false

func worker(id int) {
  cond.L.Lock()
  for !ready {
    cond.Wait() // Wait for signal
  }
  fmt.Printf("Worker %d is running\n", id)
  cond.L.Unlock()
}

func main() {
  for i := 1; i <= 3; i++ {
    go worker(i)
  }

  time.Sleep(time.Second)
  cond.L.Lock()
  ready = true
  cond.Broadcast() // Notify all waiting goroutines
  cond.L.Unlock()

  time.Sleep(time.Second)
}
```

## 23. Best Practices for Goroutines synchronization

- Use `sync.WaitGroup` to wait for goroutines to complete.
- Use `sync.Mutex` or `sync.RWMutex` to prevent race conditions.
- Use channels for safe communication between goroutines.
- Use `context.Context` for controlled cancellation.
- Use worker pools to manage goroutines efficiently.
- Use `sync.Once` for single-time execution.
