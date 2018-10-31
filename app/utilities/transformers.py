def col_rename(df, args):
    return df.withColumnRenamed(args[0], args[1])

def col_drop(df, args):
    return df.drop(args[0])

def col_restructure(df, args):
    return df.withColumn(args[0], df[args[0]].cast(args[1]))