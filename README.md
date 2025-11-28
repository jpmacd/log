# log
I've spent years trying different logging strategys for python projects, it has always been something i despised, mostly due to the amount of repetition and boiler plate code on every project.

This is my rendition of a single "log factroy" that handles everything i would expect to do with logs in python.

### Features:
- file/dir creation
- file rotation
- namespace seperation
- debugging flag
- easily modified

### Example
Using it is as simple as:

```
#python

from .log import log_factory

logger = log_factory(f"{__name__}"}

logger.info(f"This is a log message")
```
