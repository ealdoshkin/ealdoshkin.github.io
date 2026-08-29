---
# weight: 1
title: "Golang: как Linux размещает данные"
date: 2025-09-19
lastmod: 2025-09-19
draft: false
description: "Как Linux размещает данные программы в памяти: эмпирический разбор для Golang"
images: []
resources:
  - name: "featured-image"
    src: "golang-memory.jpeg"
tags: ["Golang", "Linux"]
lightgallery: true
---

<!--more-->

{{< admonition >}}
Это эмпирический пример показывающий где будут лежать данные программы.
Некоторые вещи здесь не поясняются, но заключительный вывод будет сделан.
Для большего понимания следует обратиться к темам: **управление памятью в golang**, **elf-формат**,
**управление памятью в linux**.
{{< /admonition >}}

При изучении основ языка нельзя обойти вопрос о том как устроено управление памятью.
Некоторые специалисты в процессе объяснений даже начинают предсказывать где и какие данные будут находиться
и не смущаясь оперируют терминами как стэк, куча.

Но как самом деле обстоит ситуация? За ответом я решил обратиться к Linux.

## 1. Строки

### 1.1 Строки в разных областях программы

Для разогрева сначала вооружимся лопатой и резанем не щадя.
Рассмотрим программу со строками находящихся в разных областях:

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

### 1.1 Ищем в исполняемом файле

Отключаем отладочную информацию и компилируем:

```sh
go build -ldflags="-s -w" ./main
```

После сборки посмотрим секции исполняемого файла, вот вдруг успели забыть их названия?:

```sh
$ readelf -S main

Section Headers:
  [Nr] Name              Type             Address           Offset
       Size              EntSize          Flags  Link  Info  Align
  [ 0]                   NULL             0000000000000000  00000000
       0000000000000000  0000000000000000           0     0     0
  [ 1] .text             PROGBITS         0000000000401000  00001000
       00000000000905f1  0000000000000000  AX       0     0     32
  [ 2] .rodata           PROGBITS         0000000000492000  00092000
       000000000004b10c  0000000000000000   A       0     0     32
  [ 3] .typelink         PROGBITS         00000000004dd120  000dd120
       0000000000000730  0000000000000000   A       0     0     32
  [ 4] .itablink         PROGBITS         00000000004dd860  000dd860
       0000000000000070  0000000000000000   A       0     0     32
  [ 5] .gosymtab         PROGBITS         00000000004dd8d0  000dd8d0
       0000000000000000  0000000000000000   A       0     0     1
  [ 6] .gopclntab        PROGBITS         00000000004dd8e0  000dd8e0
       00000000000750b0  0000000000000000   A       0     0     32
  [ 7] .go.buildinfo     PROGBITS         0000000000553000  00153000
       0000000000000140  0000000000000000  WA       0     0     16
  [ 8] .go.fipsinfo      PROGBITS         0000000000553140  00153140
       0000000000000078  0000000000000000  WA       0     0     32
  [ 9] .noptrdata        PROGBITS         00000000005531c0  001531c0
       0000000000004d82  0000000000000000  WA       0     0     32
  [10] .data             PROGBITS         0000000000557f60  00157f60
       0000000000005072  0000000000000000  WA       0     0     32
  [11] .bss              NOBITS           000000000055cfe0  0015cfe0
       0000000000020030  0000000000000000  WA       0     0     32
  [12] .noptrbss         NOBITS           000000000057d020  0017d020
       0000000000003a80  0000000000000000  WA       0     0     32
  [13] .note.gnu.bu[...] NOTE             0000000000400fdc  00000fdc
       0000000000000024  0000000000000000   A       0     0     4
  [14] .note.go.buildid  NOTE             0000000000400f78  00000f78
       0000000000000064  0000000000000000   A       0     0     4
  [15] .shstrtab         STRTAB           0000000000000000  0015d000
       00000000000000b8  0000000000000000           0     0     1
Key to Flags:
  W (write), A (alloc), X (execute), M (merge), S (strings), I (info),
  L (link order), O (extra OS processing required), G (group), T (TLS),
  C (compressed), x (unknown), o (OS specific), E (exclude),
  D (mbind), l (large), p (processor specific)
```

Ищем наши значения в секциях ориентируясь на строки:

```sh
$ objdump -s main -j .rodata | grep -e eeeee -e zzzzz -e llllll -e xxxxx

 4b4dc0 7a7a7a7a 7a7a7a7a 7a6c6c6c 6c6c6c6c  zzzzzzzzzlllllll
 4b4dd0 6c6c6c6c 6c6c6565 65656565 65656565  lllllleeeeeeeeee
```

Успех, все наши строки лежат в секции **.rodata** близко друг к другу.
А строка `xxxxxxxxxxxxxx` была заменена и отброшена компилятором.

### 1.2 Анализируем процесс

Теперь попытаемся найти эти же строки в запущенном процессе.
И заодно познакомимся с адресацией процесса.

Запускаем программу и смотрим адресацию:

```sh
./main &
pmap -x $!
```

Приводим все к следующей таблице, следует также обратить внимание на **RSS**, **Mode** поля:

| **Address Range**  | **KB** | **RSS** | **Dirty** | **Mode** | **Mapping** | **Type**                      | **Description**                                       |
| ------------------ | ------ | ------- | --------- | -------- | ----------- | ----------------------------- | ----------------------------------------------------- |
| `0000000000400000` | 584    | 584     | 0         | `r-x--`  | `main`      | Text Segment                  | Executable code (read-only, never modified).          |
| `0000000000492000` | 772    | 772     | 0         | `r----`  | `main`      | Read-Only Data (`.rodata`)    | Constants, string literals.                           |
| `0000000000553000` | 40     | 40      | 20        | `rw---`  | `main`      | Data Segment (`.data`/`.bss`) | Initialized/uninitialized variables (20 KB modified). |
| `000000000055d000` | 144    | 64      | 64        | `rw---`  | `[anon]`    | Heap                          | Dynamic memory (e.g., `malloc`, `new`).               |
| `000000c000000000` | 4096   | 404     | 404       | `rw---`  | `[anon]`    | Large Heap/MMAP               | Big anonymous allocation (e.g., `mmap`).              |
| `000000c000400000` | 61440  | 0       | 0         | `-----`  | `[anon]`    | Reserved Virtual Space        | Reserved but unused (no physical memory).             |
| `00007feaf14ce000` | 640    | 24      | 24        | `rw---`  | `[anon]`    | Anonymous RW                  | Likely thread-local storage or fragmented heap.       |
| `00007ffc27e7e000` | 136    | 20      | 20        | `rw---`  | `[stack]`   | Stack                         | Local variables and function call frames.             |
| `ffffffffff600000` | 4      | 0       | 0         | `--x--`  | `[anon]`    | vsyscall                      | Legacy kernel page for fast syscalls (rarely used).   |

Анализируем что находится в секции **.rodata**, берем соответствующие адреса из таблицы:

```sh
sudo gdb -p $! -batch -ex "dump memory /tmp/heap_dump.bin 0x0000000000492000 0x0000000000553000"
```

Смотрим полученный дамп с помощью поиска строк:

```sh
$ sudo strings /tmp/heap_dump.bin | grep -e eeeee -e zzzzz -e llllll -e xxxxx

runtime: sp=abi mismatchwrong timersillegal seekinvalid slothost is downnot pollablegotypesaliashttpmuxgo121multipathtcprandautoseedtlsunsafeekmzzzzzzzzzzzzzllllllllllllleeeeeeeeeeeee3814697265625wakeableSleepprofMemActiveprofMemFuturetraceStackTabexecRInternaltestRInternalGC sweep waitsynctest.WaitSIGQUIT: quitSIGKILL: killout of memory is nil, not value method  span.base()=bad flushGen , not pointer != sweepgen  MB globals,  work.nproc=  work.nwait=  nStackRoots= flushedWork double unlock s.spanclass= MB) workers=min too large-byte block (runtime: val=runtime: seq= failed with timer_settimefatal error:  idlethreads= syscalltick=load64 failedxadd64 failedxchg64 failedmp.g0 stack [nil stackbase}
```

### 1.3 Строки. Предварительный вывод

Компилятор разместил статические данные в сегменте **.rodata**, который является неизменным и тесно связан с **.text**.
Интересно что данные переменной **funcVar** которая были объявлена в функции, также оказалась в **.rodata**.
(Но дальше будет еще интереснее, не переключайтесь.)

## 2. Переменные

### 2.1 Указатель на переменную

И так, хотя сами данные у нас находятся в секции **.rodata**, это еще не значит что мы оперируем ими напрямую.
Так ли это? Пойдем проверять!

Собираем код из предыдущего примера и на всякий случай отключаем оптимизации и встраивание:

```sh
go build -gcflags="all=-N -l" -o strings2 ./main.go
```

Подключаемся отладчиком:

```sh

(gdb) break main.main # Устанавливаем breakpoint
(gdb) run
(gdb) next
(gdb) p &mainVar # Смотрим указатель
$1 = (string *) 0xc000106ec0 # Указатель находится в области Large Heap
(gdb) info locals # Смотрим переменную
mainVar = 0x4d706e 'x' <repeats 14 times> # Указатель указывает на .rodata
(gdb) x/14cb 0x4d706e # Читаем строку, указываем длину
0x4d706e: 120 'x' 120 'x' 120 'x' 120 'x' 120 'x' 120 'x' 120 'x' 120 'x'
0x4d7076: 120 'x' 120 'x' 120 'x' 120 'x' 120 'x' 120 'x'
```

Вспоминаем, что строка в Go представляет структуру вида:

```go
type string struct {
    ptr *byte // 8 bytes
    len int   // 8 bytes
}
```

Мы можем обратиться к ее полям:

```sh
(gdb) x/gx 0xc000106ec0 # Считываем адрес
0xc000106ec0: 0x00000000004d706e
(gdb) x/gx 0xc000106ec8 # Отступаем указатель, считываем длину
0xc000106ec8: 0x000000000000000e # Длина строки ровна 14 байт
```

Успех! Аналогичный результат мы можем получить и для других строк.
Повторяться здесь не будем.

### 2.2 Область видимости переменных

Теперь сосредоточимся на поиске переменных в разных областях видимости:

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

Смотрим значение под отладчиком:

```sh
(gdb) p main.GlobalVar # Проверяем глобальную переменну
$1 = 3000
(gdb) p &main.GlobalVar
$2 = (int *) 0x562228 <main[GlobalVar]> # .data сегмент
(gdb) x/gx 0x562228
0x562228 <main.GlobalVar>: 0x0000000000000bb8 # 3000

(gdb) info locals
mainVar = 55
(gdb) print &mainVar
$2 = (int *) 0xc000106ef0 # это mmap huge heap область
(gdb) x/gx 0xc000106ef0
0xc000106ef0: 0x0000000000000037 # 55

(gdb) info locals
funcVar = 200000
$1 = (int *) 0xc000114ec0 # это mmap huge heap область
(gdb) x/gx 0xc000114ec0
0xc000114ec0: 0x0000000000030d40 # 200000
```

Итак, глобальная переменная оказалась в **.data**,
а все остальное оказалось в области **000000c000000000**-**000000c000400000**,
в Linux эта область представляет анонимную память созданную с помощью **mmap()**.
В Golang же это может быть heap или stack.
И теперь наша задача выяснить что это за конкретная область!

Обычно локальные переменные хранятся в стэке,
но компилятор также может поместить их в кучу.

Запускаем команду которая покажет какие оптимизации выполняются компилятором:

```sh
go build -gcflags="-m" -o check_var ./main.go

./main.go:17:14: GlobalVar escapes to heap
./main.go:17:25: mainVar escapes to heap
./main.go:17:42: ~r0 escapes to heap
```

И вот с одной стороны стало понятно, что все улетело в кучу, а с другой
возник вопрос: "Почему **GlobalVar** также оказалась в куче, хотя она находится в **.data**?
Тут, собственно, нужно окончательно понять, что Golang от Linux живет в своей реальности.
И хотя данные лежат в **.data** доступны они будут через кучу, которая в свою очередь
отслеживается сборщиком мусора.

### 2.3 Сравниваем стэк и кучу Golang

Модифицируем нашу программу, чтобы переменная из вызываемой функции осталась в стэке:

```go
func privFunc() int {
 funcVar := 200000
 runtime.KeepAlive(funcVar) // Добавим данную аннотацию
 return funcVar
}
```

Соберем и удостоверимся что переменная не попала в heap:

```sh
$ go build -gcflags="all=-N -l -m" -o check_var

./main.go:11:20: funcVar does not escape
./main.go:19:13: ... argument does not escape
./main.go:19:14: GlobalVar escapes to heap
./main.go:19:25: mainVar escapes to heap
./main.go:19:42: privFunc() escapes to heap

```

Теперь посмотрим как обстоят дела в отладчике:

```sh
(gdb) p &mainVar
$1 = (int *) 0xc000110ef0
.....
(gdb) p &funcVar
$2 = (int *) 0xc000110eb8
```

Вот так и дела! Хотя компилятор и определил их как кучу и стэк, а лежать
они продолжают рядом в одном и том же регионе **000000c000000000**.

## 3. Выделение большого участка памяти

Напишем программу аллоцирующую 200 МБ памяти:

```go
package main

import (
 "fmt"
 "runtime"
)

func main() {
 // Allocate 200MB (200 * 1024 * 1024 bytes)
 data := make([]byte, 200*1024*1024)

 // Use the memory (to prevent compiler optimizations)
 for i := range data {
  data[i] = byte(i % 256)
 }

 // Print memory stats
 var memStats runtime.MemStats
 runtime.ReadMemStats(&memStats)

 fmt.Printf("Allocated memory: %.2f MB\n", float64(memStats.Alloc)/(1024*1024))

 // Prevent immediate exit to observe memory usage
 fmt.Println("Press Enter to exit...")
 fmt.Scanln()
}
```

Компилятор при сборке сообщает, что данные были выделены в куче:

```sh
make([]byte, 209715200) escapes to heap
```

Посмотрим где хранятся наши данные, обращаемся к процессу:

```sh
$ pmap -x $PID

Address           Kbytes     RSS   Dirty Mode  Mapping
0000000000400000     804     804       8 r-x-- heap
00000000004c9000     744     744       0 r---- heap
0000000000583000      44      44      20 rw--- heap
000000000058e000     140      68      68 rw---   [ anon ]
000000c000000000  208896  205348  205348 rw---   [ anon ]
000000c00cc00000  118784       0       0 -----   [ anon ]
....
```

И так, данные вновь лежат в полюбившийся анонимной области **000000c000000000**.

## 4. Механизм выделения памяти

Теперь обратим внимание на процесс выделения памяти,
для этого запустим программу c помощью **Strace**:

```sh
$ strace ./main

mmap(0xc000000000, 67108864, PROT_NONE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0xc000000000
mmap(0xc000000000, 4194304, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_ANONYMOUS, -1, 0) = 0xc000000000
mmap(0xc004000000, 268435456, PROT_NONE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0xc004000000
mmap(0xc000400000, 209715200, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_ANONYMOUS, -1, 0) = 0xc000400000
```

Находим что память выделяется через **mmap()**, где сначала резервируются большие куски через **PROT_NONE**,
а затем выделяются части от них с помощью флагов **PROT_READ|PROT_WRITE** на чтение и запись.

## 5. Выводы

Проанализируем полученные данные:

1. У Golang своя аллокация и свои сущности (стэк, куча) никак несвязанные с Linux
2. Глобальные переменные, статика, строки будут предоставлены через **.rodata**, **.data**
3. Память от Linux будет предоставлена через mmap() в анонимной области
4. Куча и стэк Golang могут находится рядом в одном адресном пространстве, но что есть что, знает только Golang MM
5. При выделении памяти сначала резервируются большой регион, а затем он в процессе работы режется на куски
