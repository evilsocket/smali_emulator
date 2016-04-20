# {'a': -1, 'ok': 1, 'ret': None}
const/16 a, -1

if-lez a,:ok

# this will trigger a fatal :D
return-object FAILFAILFAILFAILFAIL

:ok
    const/16 ok,1