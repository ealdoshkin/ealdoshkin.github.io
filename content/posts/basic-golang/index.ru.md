---
# weight: 1
title: "Основы Golang"
date: 2025-03-28
lastmod: 2025-03-28
draft: false
description: "Основа языка Golang"
images: []
resources:
  - name: "featured-image"
    src: "golang-basic.webp"

tags: ["Golang"]
categories: ["Documentation"]

lightgallery: true
---

Golang в кратком изложении. Шпаргалка по базовым положениям.

<!--more-->

{{< admonition >}}
Это короткий конспект по языку Golang.
Если вы новичок и хотите выучить язык с абсолютного нуля, то рекомендую обратиться
к [Golang tutorial](https://go.dev/doc/tutorial/).
{{< /admonition >}}

Go — это компилируемый, статически типизированный язык программирования, разработанный Google.
Первая стабильная версия была выпущена в 2012 году.

## 1. Объявление переменных

Явное объявление (ключевое слово var):

```go
var car string
var name string = "John"
var age int = 25
var isStudent bool = false
```

Неявное объявление (через присвоение :=):

```go
// Возможно во внутренней функции
name := "Alice"  // Тип определен как string
age := 30        // Тип определен как int
isStudent := true // bool
```

Имя переменной — это произвольный идентификатор, состоящий из букв,
цифр и символа подчеркивания (**\_**). Также нельзя использовать зарезервированные слова.

Частные переменные начинаются со строчной буквы и доступны только из пакета,
публичные переменные начинаются с заглавной буквы и доступны из других пакетов.

## 2. Базовые типы в Go

### 2.1. Примитивные типы

| Тип                       | Описание                                 | Мин./макс. значение                 | Зн. по умолч |
| ------------------------- | ---------------------------------------- | ----------------------------------- | ------------ |
| `bool`                    | Boolean (`true`, `false`)                | `false` / `true`                    | `false`      |
| `string`                  | Неизменяемая последовательность символов | `""` / N/A                          | `""`         |
| `int`                     | Целое число (платформо-зависимое)        | `-2^63` to `2^63-1` (64-bit)        | `0`          |
| `int8`                    |                                          | `-128` to `127`                     | `0`          |
| `int16`                   |                                          | `-32,768` to `32,767`               | `0`          |
| `int32`                   |                                          | `-2,147,483,648` to `2,147,483,647` | `0`          |
| `int64`                   |                                          | `-2^63` to `2^63-1`                 | `0`          |
| `uint`                    | Беззнаковое целое число (п.-з.)          | `0` to `-2^64` (64-bit)             | `0`          |
| `uint8`                   |                                          | `0` to `255`                        | `0`          |
| `uint16`                  |                                          | `0` to `65,535`                     | `0`          |
| `uint32`                  |                                          | `0` to `4,294,967,295`              | `0`          |
| `uint64`                  |                                          | `0` to `2^64 - 1`                   | `0`          |
| `float32`, `float64`      | Число с плавующей точкой                 | `~2.3E-308` to `~1.8E308`           | `0.0`        |
| `complex64`, `complex128` | Комплексное число                        | N/A                                 | `(0+0i)`     |
| `byte`                    | Байт (псевдоним `uint8`)                 | `0` to `255`                        | `0`          |
| `rune`                    | Unicode символ (псевдоним `uint32`)      | `0` to `2^31-1`                     | `0`          |

### 2.2. Составные типы

| Тип         | Описание                                            | Размер (в байтах)                          | По умолчанию |
| ----------- | --------------------------------------------------- | ------------------------------------------ | ------------ |
| `array`     | Коллекция фиксированного размера                    | Зависит от типа элементов и длины          | `[0,0,...]`  |
| `slice`     | Коллекция динамического размера (на основе массива) | 24 (на 64-битной системе)                  | `nil`        |
| `map`       | Хранилище ключ-значение                             | Варьируется (зависит от ключей и значений) | `nil`        |
| `struct`    | Пользовательский тип данных (группировка полей)     | Сумма размеров полей (с выравниванием)     | `{}`         |
| `pointer`   | Содержит адрес памяти переменной                    | 4 (на 32-битной) / 8 (на 64-битной)        | `nil`        |
| `interface` | Определяет поведение, но не хранит данные           | 16 (на 64-битной системе)                  | `nil`        |

## 3. Указатели

Указатели хранят адреса памяти:

```go
var p *int // создать указатель
a := 2
p = &a
*p++
fmt.Println(*p) // значение (3)
fmt.Println(&p) // адрес (0xc0000a2038)
```

## 4. Константа

Константа содержит неизменяемое значение, созданное при ее объявлении.

```go
const Pi float64 = 3.14159
const Greeting = "Hello, Go!"
```

Перечисление констант:

```go
const (
  Sunday = iota // 0
  Monday
  Tuesday
  Wednesday
  Thursday
  Friday
  Saturday  // 6
  _         // пропустить 7
  New       // 8
)
```

## 5. Логические операторы

| Оператор | Название | Описание                                                    |
| -------- | -------- | ----------------------------------------------------------- |
| `&&`     | И (AND)  | Возвращает `true`, если **обе** условия истинны             |
| `\|\|`   | ИЛИ (OR) | Возвращает `true`, если **хотя бы одно** из условий истинно |
| `!`      | НЕ (NOT) | Инвертирует (отрицает) булево выражение                     |

## 6. Управление потоком исполнения

| Ключевое слово | Назначение                                                              |
| -------------- | ----------------------------------------------------------------------- |
| `fallthrough`  | Принудительно выполняет следующий `case` в `switch`, игнорируя условия. |
| `continue`     | Пропускает текущую итерацию цикла и переходит к следующей.              |
| `break`        | Немедленно выходит из цикла или оператора `switch`.                     |
| `return`       | Завершает выполнение функции и может возвращать значения.               |
| `goto`         | Переходит к помеченному оператору (используйте с осторожностью).        |
| `defer`        | Откладывает выполнение функции до выхода из окружающей функции.         |
| `panic`        | Вызывает ошибку и останавливает выполнение программы.                   |
| `recover`      | Перехватывает `panic`, чтобы предотвратить завершение программы.        |

## 7. Операторы создания и манипуляции в Go

| Функция                   | Назначение                                                                         |
| ------------------------- | ---------------------------------------------------------------------------------- |
| `new(T)`                  | Выделяет память для типа `T`, возвращает указатель на `T`. `p := new(int)`         |
| `make(T, size, cap)`      | Создаёт срезы, отображения (maps) или каналы с заданным размером и ёмкостью.       |
| `append(slice, elems...)` | Добавляет элементы в срез, возвращая новый срез, если ёмкость изменилась.          |
| `copy(dst, src)`          | Копирует элементы из `src` в `dst`, возвращает количество скопированных элементов. |
| `len(container)`          | Возвращает длину среза, отображения, массива или строки.                           |
| `cap(slice)`              | Возвращает ёмкость среза.                                                          |
| `delete(map, key)`        | Удаляет ключ из отображения (map).                                                 |

## 8. Пользовательский тип

Golang позволяет определить новый тип:

```go
type Age int
var myAge Age = 25
```

## 9. Составные типы (коллекции и структуры)

Группируйте несколько значений с помощью массивов, срезов, карт, структур и указателей.

### 9.1 Массивы (фиксированный размер)

Массивы имеют фиксированную длину и хранят элементы одного типа:

```go
var numbers [3]int = [3]int{10, 20, 30}
fmt.Println(numbers[0]) // Вывод: 10

numbers := [...]int{1, 2, 3} // Объявление без указания точного размера
```

### 9.2 Срезы (динамический размер)

Срезы более гибкие, чем массивы, и содержат:

- емкость,
- длину,
- указатель на базовый массив.

```go
var slice1 = make([]int, 4, 7) // Установка длинны и емкости
nums := []int{10, 20, 30} // создаем срез с 3 элементами
slice4 := array[:] // Конвертируем массив в срез
nums = append(nums, 40) // Добавляем значение в срез
```

Усечение среза:

```go
baseArray := [8]string{"Anna", "Max", "Eva", "Leo", "Nina", "Tom", "Sophie", "Chris"} // Базовый массив

slice1 := baseArray[1:5] // с 2 по 5 элемент [Max Eva Leo Nina]
slice2 := baseArray[:3]  // с 1 по 3 элемент [Anna Max Eva]
slice3 := baseArray[4:]  // с 5 [Nina Tom Sophie Chris]
```

Удалить элемент из среза:

```go
a := []int{1, 2, 3, 4, 5, 6, 7}
a = append(a[0:2], a[3:]...)
fmt.Println(a) // [1 2 4 5 6 7]
```

### 9.3 Карта или Мапа (ключ-значение)

Карта хранит значения с использованием ключа:
карта — это ссылка на хэш-таблицу.

```go
person := map[string]int{"Alice": 25, "Bob": 30}
fmt.Println(person["Alice"]) // Вывод: 25
```

Проверить ключ в карте:

```go
if value, ok := m[1]; ok {
 fmt.Println(value) // Если ключ существует
}
```

### 9.4 Структуры

Позволяют группировать различные типы в один блок:

```go
type Person struct {
  Name string
  Age int
}
p := Person{Name: "John", Age: 30}
fmt.Println(p.Name) // Вывод: John
```

Анонимная структура:

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

## 10. Строка

Строка — это неизменяемая последовательность символов.
Но строка может быть представлена ​​как []byte или []rune и модифицирована.
**Rune** (псевдоним **int32**) определяет символ (1–4 байта) для поддержки UTF-8.

## 11. Форматирование `fmt.Printf`

| Формат | Описание                                     |
| ------ | -------------------------------------------- |
| `%v`   | Значение в стандартном формате               |
| `%+v`  | Структура с именами полей                    |
| `%#v`  | Представление значения в синтаксисе Go       |
| `%T`   | Тип значения                                 |
| `%%`   | Литерал `%`                                  |
| `%d`   | Десятичное число                             |
| `%b`   | Двоичное число                               |
| `%o`   | Восьмеричное число                           |
| `%x`   | Шестнадцатеричное число (нижний регистр)     |
| `%X`   | Шестнадцатеричное число (верхний регистр)    |
| `%c`   | Символьное представление                     |
| `%U`   | Юникод-формат                                |
| `%f`   | Десятичное число (по умолчанию 6 знаков)     |
| `%.2f` | Фиксированное число знаков после запятой (2) |
| `%e`   | Научная нотация (нижний регистр)             |
| `%E`   | Научная нотация (верхний регистр)            |
| `%g`   | Компактное представление float (`e` или `f`) |
| `%G`   | Компактное представление float (верхний `E`) |
| `%s`   | Строка                                       |
| `%q`   | Заключённая в кавычки строка                 |
| `%x`   | Шестнадцатеричный дамп (нижний регистр)      |
| `%X`   | Шестнадцатеричный дамп (верхний регистр)     |
| `%t`   | Булево значение                              |
| `%p`   | Адрес указателя                              |

## 12. Функция

В Go параметры передаются в функцию по значению, то есть передается их копия.
Изменения параметров внутри функции не влияют на исходные переменные.
Включая ссылку.

**Замыкание** — это анонимная функция, которая запоминает переменные
из окружающей ее области действия:

```go
func counter() func() int {
    count := 0
    return func() int {
        count++
        return count
    }
}

func main() {
    inc := counter() // Создать встраивание
    fmt.Println(inc()) // 1
    fmt.Println(inc()) // 2
    fmt.Println(inc()) // 3
}
```

Функция-конструктор:

```go
func newProduct(name, category string, price float64)
 *Product {
     return &Product{name, category, price}
}
```

## 13. Интерфейсы (Динамический тип)

Интерфейсы определяют поведение без указания точных типов:

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
fmt.Println(animal.Speak()) // Вывод: Woof!
```

Определяем тип переменной:

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

## 14. Ошибка

Чтобы создать ошибку, нужно реализовать интерфейс:

```go
type error interface {
 Error() string
}
```

Другие способы создание ошибки:

```go
err := errors.New("my error") // Создаем ошибку
eff := fmt.Errorf("other error")
panic("division by zero!") // Сгенерировать ошибку и выйти
```

## 15. Defer, panic и recover

Использование вместе:

```go
func safeFunction() {
    defer func() {
        if r := recover(); r != nil { // Обработка panic
            fmt.Println("Recovered:", r)
        }
    }()

    fmt.Println("Before panic")
    panic("Unexpected error!")  // Вызываем panic
    fmt.Println("After panic")
}
```

## 16. Горутины

**Горутины** — это легкие потоки в Go, которые позволяют выполнять функции одновременно.
В отличие от традиционных потоков, они управляются средой выполнения Go,
что делает их эффективными и масштабируемыми.

### 16.1. Основы горутин

Вы можете запустить новую горутину, используя ключевое слово go перед вызовом функции.

Запуск функции как горутины:

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

    time.Sleep(1 * time.Second) // Ожидаем завершение горутин

// Последовательность вывода может отличаться:
// Hello from main function!
// Hello from goroutine!
}
```

### 16.2. Запуск нескольких горутин

Создание горутин в цикле:

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
  go printNumber(i) // Создаем новую горутину на каждой итерации
  }
    time.Sleep(1 * time.Second) // Предотвращаем раннее завершение работы main
}
```

### 16.3. Синхронизация с помощью sync.WaitGroup

Использование `sync.WaitGroup` для ожидания горутин:

```go
package main

import (
  "fmt"
  "sync"
)

func worker(id int, wg *sync.WaitGroup) {
  fmt.Printf("Worker %d started\n", id)
  wg.Done() // Уменьшаем счетчик WaitGroup
}

func main() {
  var wg sync.WaitGroup

  for i := 1; i <= 3; i++ {
    wg.Add(1) // Увеличиваем счетчик
    go worker(i, &wg)
  }

  wg.Wait() // Ожидаем завершение горутин
  fmt.Println("All workers finished")
}
```

### 16.4. Связь между горутинами (каналами)

Создание и использование канала:

```go
package main

import "fmt"

func sendMessage(ch chan string) {
  ch <- "Hello from Goroutine!" // Отправляем данные в канал
}

func main() {
  ch := make(chan string) // Создаем канал

  go sendMessage(ch)

  msg := <-ch // Получение данных из канала
  fmt.Println(msg)
}
```

### 16.5. Буферизованные и небуферизованные каналы

Небуферизованные каналы (по умолчанию) блокируются до тех пор, пока данные не будут получены.
Буферизованные каналы позволяют хранить сообщения.

Пример буферизованного канала:

```go
ch := make(chan int, 3) // Размер буфера 3
ch <- 1
ch <- 2
ch <- 3
fmt.Println(<-ch) // Вывод: 1
```

### 16.6. Закрытие канала

```go
   ch := make(chan int)

go func() {
  for i := 1; i <= 5; i++ {
  ch <- i
}
  close(ch) // Закрываем канал
}()

for num := range ch {
  fmt.Println(num) // Читать пока канал не закроется
}
```

### 16.7. Оператор Select (обработка нескольких каналов)

Оператор select позволяет goroutine ожидать на нескольких каналах:

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

  select { // Слушаем каналы
  case msg1 := <-ch1:
      fmt.Println(msg1)
  case msg2 := <-ch2:
      fmt.Println(msg2)
  case <-time.After(3 * time.Second):
      fmt.Println("Timeout!")
  }

}
```

### 16.8. Пул рабочих процессов (управление горутинами)

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

### 16.9 Лучшие практики для горутин

- Всегда используйте `sync.WaitGroup` при управлении несколькими горутинами.
- Используйте каналы для безопасной связи вместо общей памяти.
- Избегайте утечек памяти, гарантируя, что все горутины завершат выполнение.
- Ограничьте горутины при обработке множества задач с использованием рабочих пулов.
- Используйте `context.Context` для отмены длительно выполняющихся горутин.

## 17. Обработка состояний гонки с помощью sync.Mutex

Когда несколько горутин обращаются к общим данным, могут возникнуть состояния гонки.
`sync.Mutex` (взаимное исключение) помогает предотвратить это.

```go
package main

import (
  "fmt"
  "sync"
  "time"
)

var counter = 0
var mu sync.Mutex // Mutex для безапасного доступа

func increment() {
  for i := 0; i < 1000; i++ {
  mu.Lock() // Блокируем доступ
  counter++ // Обновляем
  mu.Unlock() // Снимаем блокировку
  }
}

func main() {
  for i := 0; i < 5; i++ {
    go increment()
  }

  time.Sleep(time.Second)
  fmt.Println("Final Counter:", counter)
}
```

## 18. Синхронизация чтения-записи с помощью sync.RWMutex

Если у вас несколько читателей, но только один писатель, используйте `sync.RWMutex`:

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
  rw.RLock() // Блокировка на чтение
  fmt.Printf("Reader %d reads value: %d\n", id, value)
  rw.RUnlock()
}

func writeValue(newValue int) {
  rw.Lock() // Блокировка на запись
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
// Несколько читателей могут читать одновременно, но писать может только один писатель.
}
```

## 19. Отмена горутины с помощью context.Context

Горутины не останавливаются автоматически при выходе из main. Используйте контекст для управления ими.

Отмена горутины:

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
  cancel() // Отправляем сигнал завершения

  time.Sleep(time.Second)
}
```

## 20. Context.WithTimeout для таймаута

Автоматическое завершение горутины по истечении времени ожидания:

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
  ctx, cancel := context.WithTimeout(context.Background(), 2*time.Second)
  defer cancel() // Завершаем

      go worker(ctx)

      time.Sleep(3 * time.Second)

}
```

## 21. Использование sync.Once для однократной инициализации

Используйте `sync.Once`, чтобы гарантировать, что функция будет запущена
только один раз, даже если она вызывается несколько раз:

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
   once.Do(initConfig) // Запустить единожды
  }()
 }

 wg.Wait()
}

```

## 22. Использование sync.Cond для координации горутин

`sync.Cond` позволяет горутинам ожидать условия перед продолжением:

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
    cond.Wait() // Ожидание сигнала
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
  cond.Broadcast() // Уведомить ожидающее горутины
  cond.L.Unlock()

  time.Sleep(time.Second)
}
```

## 23. Лучшие практики синхронизации горутин

- `sync.WaitGroup` для ожидания завершения горутин.
- `sync.Mutex` или `sync.RWMutex` для предотвращения состояний гонки.
- каналы для безопасной связи между горутинами.
- `context.Context` для контролируемой отмены.
- рабочие пулы для эффективного управления горутинами.
- `sync.Once` для однократного выполнения.
