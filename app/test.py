import pandas as pd

# Create a sample DataFrame
data = {
    "A": ["foo", "bar", "foo", "bar", "foo", "bar"],
    "B": [1, 2, 3, 4, 5, 6],
    "C": [7, 8, 9, 10, 11, 12],
}
df = pd.DataFrame(data)

# Group by column 'A'
grouped = df.groupby(["A", "C"])["B"].sum().reset_index()
# Convert DataFrameGroupBy to DataFrame
# df_grouped = grouped.apply(lambda x: x)
print(grouped)
