# {'a': [u'a', u'b', u'c'], 'i': 1, 's': u'abc', 'ret': [u'a', u'b', u'c'], 'v': u'b'}
const-string s, "abc"
const/16 a, 0
const/16 i, 1
const/16 v, 0

invoke-virtual {s}, Ljava/lang/String;->toCharArray()[C
move-result a
aget v, a, i