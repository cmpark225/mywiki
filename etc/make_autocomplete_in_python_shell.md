## Create a file .pythonrc

```
# ~/.pythonrc
# enable syntax completion 

try:
    import readline
except ImportError:
    print("Module readline not avaliable.")
else:
    import rlcompleter
    readline.parse_and_bind("tab: complete")
```

## Add export code to .bashrc file

```
export PYTHONSTARTUP=~/.pythonrc
```

