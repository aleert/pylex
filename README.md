[![asciicast](https://asciinema.org/a/yfPQ1cb9FFc21tJgroVc6K5jd.svg)](https://asciinema.org/a/yfPQ1cb9FFc21tJgroVc6K5jd?t=7)

### What it is?
A small tool for statical code analysis made for fun and study.
It can count most common words used in function defenitions, class defenitions etc.

### Example usage:
* Count all verbs used in names of django and tornado funcions:
```
pylex django tornado
```
that is equivalent to:
```
pylex django tornado --pt-of-speech='VB' --node-type='FunctionDef'
```
which is also equivalent to shorthand options syntax:
```
pylex django tornado -P='VB' -N='FunctionDef'
```

* Explore five most common names that are nouns for every *.py file classes under the
directory you are currently in:
```
pylex . --top=5 -P='NN' -N='ClassDef' --S
```

### How to install.
If you want to install it as real CLI app do the following:

After you clone this repository you should get poetry with 

```
pip install poetry
```
After that navigate to folder with `pyproject.toml` and run
```
poetry build
```
Now you will have a `dist/` folder with `.whl` file. Install it with
```
pip install <generated_file_name>.whl
```


### How to use.
If you never used `nltk` before you may need to download some data.
```python
import nltk
nltk.download('averaged_perceptron_tagger')
```
should be enough.

If you installed `pylex` as CLI you can run
```
pylex <modules> <options>
```
If you just copied repository - run
```
python ./pylex/cli.py <modules> <options>
```
For `<modules>` you can specify either installed packages,
or paths to *.py files or path to folders(incl. relative paths).

### Available options
* --top=N : Print only N most common words. 
* -P|--pt-of-speech= : Part of speech as of nltk.help.upenn_tagset() (NN for noun,
                VB for verb, CD for cardinal etc.)
* -N|--node-type= : Node type to explore. FunctionDef (or just function), ClassDef(class) and Assign(assign)
             are currently accepted. 
* -S|--split : Generate output for every *.py file explored.
* --json, --csv: output as json or csv
* -O|--output=: print output to file. Do not write progress info if --json or --csv selected.

### Known issues
If you try to explore git repo on Windows, git progress will be somewhat meshed. Otherwise function normally,
and writing json or csv to files does not include git progress.
