import pandas as pd

# Get the data
df = pd.read_csv('data.csv', dtype = {'Fund': str}) # Read funds as strings, not ints
funds = df['Fund']
categories = df['Category']
balances = df['Balance']
types = df['Type']

# Parse the data
types_and_categories = set(types + ':' + categories)
results = {f: {t: 0 for t in types_and_categories} for f in funds}
for i in range(len(df)):
    row = df.iloc[i]
    t = row['Type']
    c = row['Category']
    f = row['Fund']
    b = row['Balance']
    results[f][t + ':' + c] += b
results = pd.DataFrame.from_dict(results)
results.sort_index().to_csv('out.csv')
