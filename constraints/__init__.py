import os
__all__ = [i.replace(".py", "") for i in os.listdir(os.path.split(__file__)[0]) if not i.startswith("__")]
print(__all__)