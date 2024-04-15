```python3
# NOTE: You should import gllogger before executing any other code.
from gllogger import gL

gL.getLogger(__name__)
gL.setGlobalLevel(logging.DEBUG)

...
```

```python3
# You can log into the console,
gL.init(gL.OT_console)

# or you can pass logs into a function,
def gL_function(text):
    print(text)
gL.setFunction(gL_function)
gL.init(gL.OT_function)

# or you can write logs to files.
import os
gL.setLogDir(os.path.join(os.getcwd(), "log", ))
gL.init(gL.OT_logging)


# Then, use the following function anywhere to log.
gL.debugs("a", 1, True, )
gL.infos()
gL.warns()
gL.errors()

"""
[DEBUG 00:00:00 main[15].<module>] a 1 True
"""

```

```python3
# You can use 'gL(Exception)' to enable logging of complete exception tracebacks,
# and if you have 'better_exceptions' installed, the tracebacks will be even more detailed.
# $ pip install better_exceptions

try:
    def f(a, b):
        return a / b
    f(1, 0)
except ZeroDivisionError as e:
    gL.warns(gL(e))

"""
[WARNING 00:00:00 main[10].<module>] Traceback (most recent call last):
  File "/tmp/main.py", line 8, in <module>
    f(1, 0)
    └ <function f at 0x04E264A8>
  File "/tmp/main.py", line 6, in f
    return a / b
           │   └ 0
           └ 1
"""

```
