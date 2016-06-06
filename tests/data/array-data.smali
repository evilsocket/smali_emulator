# {'a': 2, 'b': 2097152, 'ret': 2097152}

const/16 a, 2
const/16 b, 4

new-array b, b, [I
fill-array-data b, :array_0

aget b, b, a

return b

:array_0
.array-data 4
    0x800000
    0x400000
    0x200000
    0x100000
.end array-data
