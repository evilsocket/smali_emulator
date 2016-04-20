# {'a': 5, 'b': 4, 'ok': 1, 'ret': None}
const/16 a, 5
const/16 b, 4

if-gt a,b,:ok

return-object b

:ok
    const/16 ok,1