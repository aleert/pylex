[![asciicast](https://asciinema.org/a/yfPQ1cb9FFc21tJgroVc6K5jd.svg)](https://asciinema.org/a/yfPQ1cb9FFc21tJgroVc6K5jd?t=7)

### What it is?
A small tool for statical code analysis made for fun and study.
It can count most common words used in function defenitions, class defenitions etc.

### Example usage:
* Count all verbs used in names of django and tornado functions and output results to json file:
```
pylex django tornado --output=report.json
```
that is equivalent to:
```
pylex django tornado --pt-of-speech='VB' --node-type='FunctionDef' -O=report.json
```
which is also equivalent to shorthand options syntax:
```
pylex django tornado -P='VB' -N='function' -O=report.json
```

* Explore five most common names that are nouns for every *.py file classes under the
directory you are currently in:
```
pylex . --top=5 -P='NN' -N='ClassDef' --S
```
* Explore git repositories with shorthand syntax <user>/<package> available for github:
```
pylex django/django --top=5 -P='NN' -N='assign'
pylex https://github.com/django/django.git --top=5 -P='NN' -N='assigh'
```

### System requirements

You should have `git>1.7.0` installed. Windows and Unix systems should both work, with some
visual lag on Windows if you use pylex to explore git repositories(result output is file).

### How to install.
If you want to install it as real CLI app do the following:

* For most convinient way - run `./setup.sh` which will install pylex and download
some additional data required for nltk.

* Or you can run `python setup.py install` and then - `python -m nltk.downloader 'averaged_perceptron_tagger'`.

* You can build wheels with `pip` or `poetry`, but then i guess you know what yor are doing.


### How to use.

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
* **--top=N** : Print only N most common words. 
* **-P|--pt-of-speech=** : Part of speech as of  (NN for noun,
                VB for verb, CD for cardinal etc.)
                To list all available options run `nltk.help.upenn_tagset()` from python
                or check [this stackoveflow question](https://stackoverflow.com/questions/15388831/what-are-all-possible-pos-tags-of-nltk)
* **-N|--node-type=** : Node type to explore. FunctionDef (or just function), ClassDef(class) and Assign(assign)
             are currently accepted. 
* **-S|--split** : Generate output for every *.py file explored.
* **--json**, **--csv** : output as json or csv
* **-O|--output=** : print output to file appending, if file exists. Do not write progress info if --json or --csv selected.

### Known issues
If you try to explore git repo on Windows, git progress will be somewhat meshed. Otherwise function normally,
and writing json or csv to files does not include git progress.
