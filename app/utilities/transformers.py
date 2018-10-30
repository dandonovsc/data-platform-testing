def transform(self, f):
    return f(self)

def col_rename(df, source_col, target_col):
    return df.withColumnRenamed(source_col, target_col)

def col_drop(df, source_col):
    return df.drop(source_col)