# pylex

### What it is?
A small tool for statical code analysis made for fun and study.
It can count most common words used in function defenitions, class defenitions etc.

### Example usage:
* Count all verbs used in names of django funcions
```
pylex count django
```
that is equivalent to 
```
pylex count django --pt-of-speech='VB' --node-type='FunctionDef'
```
which is also equivalent to shorthand options syntax
```
pylex count django --P='VB' --N='FunctionDef'
```

* Explore five most common names that are nouns for every *.py file classes under the
directory you are currently in:
```
pylex count . --top=5 --P='NN' --N='ClassDef' --S
```

### How to install.
If you want to install it as real CLI app do the following:

After you clone this repository you should get poetry with 

```
pip install poetry
```
After that navigate to folder with `pyproject.toml` and run
```python
poetry build
```
Now you will have a `dist/` folder with `.whl` file. Install it with
```
pip install <generated_file_name>.whl
```


### How to use.
If you installed it as CLI you can run
```
pylex count <modules> <options>
```
if you just copied repository - run
```
python ./pylex/cli.py count <modules> <options>
```
For `<modules>` you can specify either installed packages,
or paths to *.py files or path to folders(incl. relative paths).

### Available options
* --top=N : Print only N most common words. 
* --P|--pt-of-speech= : Part of speech as of nltk.help.upenn_tagset() (NN for noun,
                VB for verb, CD for cardinal etc.)
* --N|--node-type= : Node type to explore. FunctionDef, AsyncFunctionDef and ClassDef
             are currently accepted. 
* --S|--split : Generate output for every *.py file explored.

