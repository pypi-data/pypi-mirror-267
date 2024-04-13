# aptll (Aplustools linking library)
[![Active Development](https://img.shields.io/badge/Maintenance%20Level-Actively%20Developed-brightgreen.svg)](https://gist.github.com/cheerfulstoic/d107229326a01ff0f333a1d3476e068d)
[![Build Status](https://github.com/Adalfarus/apt/actions/workflows/python-publish.yml/badge.svg)](https://github.com/Adalfarus/apt/actions)
[![License: GPL-3.0](https://img.shields.io/github/license/Adalfarus/apt)](https://github.com/Adalfarus/apt/blob/main/LICENSE)

 Makes writing code and switching versions easier than ever!


### Switching aplustools version
```python
from apt import aptll

# This will restart python with the current script after the 
aptll.change_version("0.1.3.6")  #  new version is installed.
```

### aplustools modules
Work as usual, just typing info from advanced editors won't work.
```python
from apt.package.timid import TimidTimer

timer = TimidTimer()
print(timer.end())
```
