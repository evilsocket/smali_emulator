# {'i': 1, 's': u'hello', 'ret': u'e'}
const-string s, "hello"
const/12 i, 1

invoke-virtual {s, i}, Ljava/lang/String;->charAt(I)C
