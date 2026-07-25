# Programming Language (C/Python) — Notes

---
## C Language Introduction — Notes

*(Note: the originally supplied link `c/getting-started-with-c/` now redirects to the generic "C Programming Tutorial" index page with no code on it. Substituted the actual GFG article covering this content: `c/c-language-introduction/`.)*

**1. Program skeleton**
Every C program needs a header include, a `main()` entry point, and a `return`:
```
#include <stdio.h>
int main(void)
{
    // statements
    return 0;
}
```
*Execution always starts at `main()`, regardless of where it appears in the file.*

**2. Compile/run model**
Source is written to a `.c` file (e.g. `HelloWorld.c`), a compiler (GCC, Clang, MSVC) translates it to machine code/executable, which the OS then loads into memory and runs starting at `main()`.
*C is compiled ahead of time — unlike Python's line-by-line interpretation.*

**3. Worked example (page's verbatim code)**
```c
#include <stdio.h>
int main(void)
{
    // This prints "Hello World"
    printf("Hello World");
    return 0;
}
```
Output:
```
Hello World
```

---
## Pointers in C — Notes

**1. Pointer declaration**
```
data_type *pointer_name;
```
*`*` in a declaration marks the variable as "pointer to `data_type`", not a dereference yet.*

**2. Address-of operator (`&`) — initializing a pointer**
```
pointer_name = &variable;
```
*A pointer can also be initialized to `NULL` if it doesn't yet point anywhere: `int *ptr = NULL;`.*

**3. Dereference operator (`*`)**
Applying `*` to a pointer accesses the value stored at the address it holds — same symbol as declaration, different context.

**4. Pointer size**
Size of a pointer depends on the machine architecture, not the pointed-to type: 4 bytes on 32-bit systems, 8 bytes on 64-bit systems, for *any* pointer type (`int*`, `char*`, `float*`, …).

**5. Worked examples (page's verbatim code)**

Declaring + printing an address (`%p`):
```c
#include <stdio.h>

int main() {
    // Normal Variable
    int var = 10;

    // Pointer Variable ptr that stores address of var
    int *ptr = &var;

    // Directly accessing ptr will give us an address
    printf("%p", ptr);

    return 0;
}
```
Output: `0x7fffffffe9cc`

Dereferencing to get the value back (`%d`):
```c
#include <stdio.h>

int main() {
    int var = 10;

    // Store address of var variable
    int* ptr = &var;

    // Dereferencing ptr to access the value
    printf("%d", *ptr);

    return 0;
}
```
Output: `10`

Checking pointer size with `sizeof`:
```c
#include <stdio.h>

int main() {
    int *ptr1;
    char *ptr2;

    // Finding size using sizeof()
    printf("%zu\n", sizeof(ptr1));
    printf("%zu", sizeof(ptr2));

    return 0;
}
```
Output:
```
8
8
```

---
## Python Introduction — Notes

**1. Core language traits**
Python is high-level, dynamically typed, has automatic garbage collection, and supports object-oriented, functional, and procedural styles in one language.

**2. Indentation instead of braces**
`Python uses indentation (spaces or tabs) to define code blocks instead of braces {} in C, C++ and Java.`
*A mis-indented line is a syntax error in Python — there's no `{}` fallback.*

**3. Comments**
`# is used to write comments in Python. Comments are ignored during execution.`

**4. `print()` and strings**
`print()` is a built-in function that displays text; string literals use single `'` or double `"` quotes interchangeably.

**5. Worked example (page's verbatim code)**
```python
# This is a comment. It will not be executed. 
print("Hello, World!")
```
Output:
```
Hello, World!
```

---
## Python Functions — Notes

**1. `def` syntax**
```
def function_name(arguments):
    # function body
    return value
```
- `def function_name(arguments):` defines a function with optional arguments.
- `return value` returns a result; if no `return` is used, the function returns `None` by default.

**2. Simplest example (page's verbatim code)**
```python
def fun():
    print("Welcome to GFG")

fun()
```
Output:
```
Welcome to GFG
```

**3. Worked example with a parameter and a return value (page's verbatim code)**
```python
def evenOdd(x):
    if (x % 2 == 0):
        return "Even"
    else:
        return "Odd"

print(evenOdd(16))
print(evenOdd(7))
```
Output:
```
Even
Odd
```
*This is the one to remember: parameter in the parens, `return` sends a value back to the caller instead of just printing.*

**4. Default arguments (page's verbatim code)**
```python
def myFun(x, y=50):
    print("x: ", x)
    print("y: ", y)

myFun(10)
```
Output:
```
x:  10
y:  50
```
*`y=50` is used only when the caller omits that argument.*

---
## Priority for your prep

This is the **lowest-priority subject** in your source report — score 1.25, with only **1 out of 95** questions historically drawn from Programming Language (C/Python basics). Do not over-invest here.

Minimum-viable prep, in order of likely payoff:
1. C program skeleton (`#include`, `main`, `return 0`) and that compilation happens ahead of execution.
2. Pointer syntax: `*` for declare/dereference, `&` for address-of, and that pointer size is architecture-dependent (4 vs 8 bytes), not type-dependent.
3. Python: indentation-based blocks, `def`/`return` syntax, and default arguments.

Spend at most a light pass here — one read-through of this file should be enough to not miss the single easy question this topic tends to contribute.
