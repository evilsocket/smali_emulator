# {'a': 5, 'ok': 1, 'ret': None}
const/16 a, 5

if-gez a,:ok

# this will trigger a fatal :D
return-object FAILFAILFAILFAILFAIL

:ok
    const/16 ok,1