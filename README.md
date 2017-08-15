# Katakana

English to Katakana using Sequence-to-Sequence learning in Keras.

To learn more about how to train the model, checkout these resources:

* [English to Katakana using Sequence to Sequence in Keras](https://wanasit.github.io/english-to-katakana-using-sequence-to-sequence-in-keras.html)
* [Python Notebook](https://github.com/wanasit/katakana/blob/master/notebooks/Writing%20Katakana%20using%20Sequence-to-Sequence%20in%20Keras.ipynb)

The English-Katakana dataset used for training the model is also available [here](https://raw.githubusercontent.com/wanasit/katakana/master/data/joined_titles.csv)

## Use pre-trained model as a library

**Warning:** The pre-trained is a small network and not properly trained. It's not production ready 
and should be used just for demonstration propose. 

```
 pip install --upgrade git+https://github.com/wanasit/katakana.git
```

There is `to_katakana` function that takes English string as an input and return Katakana (unicode) as an output.
```python
from katakana import to_katakana 

to_katakana('katakana')
# u'\u30ab\u30bf\u30ab\u30ca' or カタカナ
```