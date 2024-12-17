from IPython import get_ipython

# in ipyhton shell equivalent to:
# In [1]: %load_ext autoreload
# In [2]: %autoreload 2

def autoreload():
    ipython = get_ipython()

    if ipython:
       # Only call magic if inside IPython
       ipython.magic("load_ext autoreload")
       ipython.magic("autoreload 2")
    else:
       print("Not in IPython, skipping autoreload.")
