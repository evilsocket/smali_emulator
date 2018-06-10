.method public static field5([II)Ljava/lang/String;
    .locals 12

    const/4 v4, 0x4

    const/4 v6, 0x1

    const/4 v1, 0x0

    const-string v0, ""

    move v2, v6

    move-object v9, v0

    move v5, p1

    move v0, v6

    :goto_0
    if-ge v0, v6, :cond_0

    if-nez v2, :cond_7

    :cond_0
    array-length v2, p0

    if-ge v1, v2, :cond_b

    add-int/lit8 v0, v0, -0x1

    move v2, v1

    move v3, v6

    :goto_1
    if-lez v0, :cond_a

    add-int/lit8 v5, v5, -0x1

    if-eqz v3, :cond_1

    move v0, v4

    :cond_1
    add-int/lit8 v3, v2, 0x1

    const-string v2, "z"

    invoke-virtual {v2, v1}, Ljava/lang/String;->charAt(I)C

    move-result v2

    move v8, v2

    move v2, v0

    move v0, v3

    move v3, v1

    :goto_2
    if-eqz v3, :cond_9

    add-int/lit8 v2, v2, 0x1

    move v3, v0

    move v7, v5

    move v0, v2

    move v2, v1

    :goto_3
    if-lez v3, :cond_2

    add-int/lit8 v5, v7, 0x1

    if-nez v2, :cond_8

    add-int/lit8 v3, v3, -0x1

    add-int/lit8 v3, v3, -0x1

    add-int/lit8 v3, v3, -0x1

    move v7, v5

    goto :goto_3

    :cond_2
    :goto_4
    if-nez v2, :cond_3

    add-int/lit8 v0, v0, 0x1

    move v2, v6

    goto :goto_4

    :cond_3
    move-object v5, v9

    move v9, v1

    move v11, v3

    move v3, v0

    move v0, v8

    move v8, v2

    move v2, v11

    :try_start_0
    array-length v10, p0

    if-lez v10, :cond_5

    add-int/lit8 v2, v2, 0x1

    add-int/lit8 v3, v3, -0x2

    aget v8, p0, v9

    const/4 v9, -0x7

    div-int v2, v9, v3

    xor-int/2addr v2, v8

    if-le v2, v4, :cond_4

    int-to-char v0, v2

    :cond_4
    :goto_5
    new-instance v8, Ljava/lang/StringBuilder;

    invoke-direct {v8}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v8, v5}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v8

    invoke-virtual {v8, v0}, Ljava/lang/StringBuilder;->append(C)Ljava/lang/StringBuilder;

    move-result-object v8

    invoke-virtual {v8}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    move-result-object v5

    goto :goto_5

    :cond_5
    move v0, v3

    move v2, v8

    move-object v3, v5

    :goto_6
    if-lez v0, :cond_6

    add-int/lit8 v0, v0, -0x1

    goto :goto_6

    :catch_0
    move-exception v8

    move v11, v2

    move-object v2, v5

    move v5, v3

    move v3, v11

    move v3, v5

    if-nez v3, :cond_d

    if-nez v5, :cond_d

    move-object v3, v2

    move v2, v0

    move v0, v1

    :goto_7
    array-length v2, p0

    if-ge v0, v2, :cond_c

    aget v2, p0, v0

    mul-int/lit8 v8, v7, 0x1

    sub-int v8, v0, v8

    xor-int/2addr v2, v8

    int-to-char v2, v2

    new-instance v8, Ljava/lang/StringBuilder;

    invoke-direct {v8}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v8, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v3

    invoke-virtual {v3, v2}, Ljava/lang/StringBuilder;->append(C)Ljava/lang/StringBuilder;

    move-result-object v3

    invoke-virtual {v3}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v3

    add-int/lit8 v0, v0, 0x1

    goto :goto_7

    :cond_6
    move-object v9, v3

    move v5, v7

    goto/16 :goto_0

    :cond_7
    return-object v9

    :cond_8
    move v7, v5

    goto :goto_3

    :cond_9
    move v7, v5

    move v11, v2

    move v2, v3

    move v3, v0

    move v0, v11

    goto :goto_3

    :cond_a
    move v8, v1

    move v11, v2

    move v2, v0

    move v0, v11

    goto/16 :goto_2

    :cond_b
    move v2, v6

    move v3, v1

    goto/16 :goto_1

    :cond_c
    move v0, v5

    move v2, v6

    goto :goto_6

    :cond_d
    move v0, v5

    move-object v3, v2

    move v2, v6

    goto :goto_6
.end method
