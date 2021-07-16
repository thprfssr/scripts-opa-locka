import pandas as pd

# Get the data
df = pd.read_csv('data.csv', dtype = {'Fund': str}) # Read funds as strings, not ints
funds = df['Fund']
categories = df['Category']
balances = df['Balance']
types = df['Type']

# Parse the data
types_and_categories = set(types + ':' + categories)
results = {t: {f: 0 for f in set(funds)} for t in set(types)}
for i in range(len(df)):
    row = df.iloc[i]
    t = row['Type']
    f = row['Fund']
    results[t][f] += row['Balance']
results = pd.DataFrame.from_dict(results)
results.sort_index().to_csv('condensed-summary.csv')
