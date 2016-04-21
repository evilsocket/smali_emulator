# {'a': 9, 'b': 10, 'ret': 10}

const/16 a, 9
const/16 b, 0

packed-switch a, :pswitch_data_0

const/16 b, 0xB

:goto_0
return b 

:pswitch_2
const/16 b, 0x8
goto :goto_0

:pswitch_1
const/16 b, 0x9

:pswitch_4
const/16 b, 0xA
goto :goto_0

:pswitch_data_0
.packed-switch 0x8
    :pswitch_2
    :pswitch_1
    :pswitch_4
.end packed-switch
