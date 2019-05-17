#!/bin/sh

echo 'Intalling pylex'
python setup.py install

python  - << EOF
import nltk
nltk.download('averaged_perceptron_tagger')
nltk.download('tagsets')
print('Done!')

EOF
