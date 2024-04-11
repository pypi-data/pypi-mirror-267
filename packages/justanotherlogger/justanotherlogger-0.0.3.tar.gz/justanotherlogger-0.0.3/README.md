## Just Another Logger
A simple logger that i use in my python projects.

## Usage
You can import the logger class like this:

```py
from justanotherlogger import Logger
```
To set it up, you run:
```py
logger = Logger.Logger()
logger.setup(type=Logger.INFO, filenameDirectory = "./", filename = f"{str(datetime.date.today())}.log"):
```
| Parameter       | Usage                                                                                   |
|----------------:|-----------------------------------------------------------------------------------------|
|type             | Determines the minimum Error level of the log, Any log under this level will be ignored |
|filenameDirectory| Tells the Logger which directory to store the log in.                                   |
|filename         | Tells the logger what to call the log                                                   |

