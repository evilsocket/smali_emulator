# {'a': 4, 'b': 5, 'ok': 1, 'ret': None}
const/16 a, 4
const/16 b, 5

if-lt a,b,:ok

return-object b

:ok
    const/16 ok,1