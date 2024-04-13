```python3
from gllogger import gL

# First, call it in your main.py file.
gL.getLogger(__name__)
gL.setGlobalLevel(logging.DEBUG)

# You can log into the console.
gL.init("console")

# You can pass logs into a function.
def gL_function(text):
    print(text)
gL.setFunction(gL_function)
gL.init("function")

# You can write logs to files.
import os
gL.setLogDir(os.path.join(os.getcwd(), "log", ))
gL.init("logging")

# Then, use the following function anywhere to log.
gL.debugs("a", 1, True, )
gL.infos()
gL.warns()
gL.errors()

```
