## Create a file .pythonrc

ubuntu
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

mac
```
# ~/.pythonrc
# enable syntax completion 

try:
    import readline
except ImportError:
    print("Module readline not avaliable.")
else:
    import rlcompleter
    
    if 'libedit' in readline.__doc__:
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        readline.parse_and_bind("tab: complete")
~                                                       
```

## Add export code to .bashrc file

```
export PYTHONSTARTUP=~/.pythonrc
```

