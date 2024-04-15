# What

Convert a python script into a obfuscated shell script. \
If this shell script is run it will create the original python script. \
This can be used for obfuscation purposes or to hide the code when sharing it with others.

# Installation

```bash
pip install pytwosh
```

# Usage
```py
import pytwosh as s2p

# Create a Sh2Py object with the path of your python script as parameter
sh2py = s2p.Sh2Py("path/to/python/script.py")

# Calling this function will create a obfuscated shell script in the same
# directory as the python script that will create the original python script
sh2py.base64_encode()
```

# License
Released under the [GPL-3.0](./LICENSE)
