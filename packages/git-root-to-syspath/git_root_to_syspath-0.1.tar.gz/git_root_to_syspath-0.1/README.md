# Git root to sys.path

A small package that will allow running python scripts (which refer to each other) from any level of the git directory hierarchy.

This can be useful for debugging.

Comment: The root of a submodule is the git root also.

## Why
Suppose our project contains many modules and packages in a hierarchical structure like this.

```   
── src
    ├── pk1
    │   └── mod1  
    ├── pk2
    │   ├── mod2
    │   └── mod3
    └── submodule_pk
        ├── mod4
        └── mod5
```

In each module, we want to **refer to other parts of the program via the full path** in the git repository.

So something like this in the main repository (refers to main repository):
```python:
from src.pk1.mod1 import xyz
```

or in the main repository (refers to submodule):
```python:
from src.submodule_pk.mod4 import qwe
```

And also in submodule we want to refer to other parts of the submodule like this:
```python:
from mod4 import qwe
```
Because the submodule is in another context (from its point of view) the main repository also.

---

We also want to have **test code close to what is being tested**. 

For example in mod3.py file (mod3 module):
```python:
from src.submodule_pk.mod4 import qwe
from src.pk1.mod1 import xyz

class M:
    def __init()__:
        ...
   
   def a() -> str:
        ...    
...

if __name__ == "__main__":
   
    # for simple test ....
   
    print(M().a())
```
 ---
And he also wants modules to be able to **run** as standalone scripts **from anywhere**.

```bash
cd src/pk2
python3 mod3.py
```

Or so that we can simply run them from a development environment (such as PyCharm, VC, etc.) by pressing the "Run" button.


## Instalation

Pick one

```shell
pip install git+https://gitlab.com/ivo-marvan/git_root_to_syspath
pip install git_root_to_syspath
```

## Usage
Put this line in the header of each file:

```python:
from git_root_to_syspath import agr; agr()
```

Or optionally:

```python:
from git_root_to_syspath import agr; PROJECT_ROOT = agr()
```
