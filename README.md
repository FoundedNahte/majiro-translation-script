# majiro-translation-script

Combined with the "majiro" and "mjdisasm" executables, this python script allows for automatic translation of the mjo objects within the scenario.arc file found within games made with the Majiro scripting engine.
## Installation

Make to to pip install the argostranslate library as well as download the file for the model https://www.argosopentech.com/argospm/index/

```bash
pip install argostranslate
```

## Usage
1) To begin with, use the majiro executable to unpack the "scenario.arc" file as well as produce .utf files for every .mjo file.

2) Put all the .mjo and corresponding .utf files into one folder with the exectuables, script, and "scenario.arc" file

3) Once you run the script, it will automatically go through all .mjo and .utf files, translate them, and repack them into the "scenario.arc" file in the same directory.
