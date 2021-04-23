import pandas as pd

# Get the data
df = pd.read_csv('data.csv', dtype = {'Fund': str}) # Read funds as strings, not ints
funds = df['Fund']
categories = df['Category']
balances = df['Balance']
types = df['Type']

# Parse the data
types_and_categories = set(types + ':' + categories)
simplified_types = {
        '1': 'Assets',
        '2': 'Liabilities',
        '4': 'Revenues',
        '5': 'Expenses',
        }
results = {t: {f: 0 for f in set(funds)} for t in simplified_types.values()}
for i in range(len(df)):
    row = df.iloc[i]
    t = row['Type']
    f = row['Fund']
    if t[0] in simplified_types.keys():
        results[simplified_types[t[0]]][f] += row['Balance']

# Define proprietary activities, governmental activities, and the grand total
results = pd.DataFrame.from_dict(results)
total = results.sum()
proprietary_activities = results.filter(['410', '440', '450'],
        axis = 'index').sum()
governmental_activities = total - proprietary_activities

# Determine whether fund belongs to governmental activities or proprietary.
def type_of_fund(f):
    if f in {'410', '440', '450'}:
        return 'Proprietary Activities'
    else:
        return 'Governmental Activities'

# Determine whether a fund is major or minor
def fund_major_or_minor(f):
    # Do the 10% rule
    if type_of_fund(f) == 'Proprietary Activities':
        quotient = results.loc[f] / proprietary_activities
    else:
        quotient = results.loc[f] / governmental_activities
    condition_a = (quotient >= 0.10).any()

    # Do the 5% rule.
    quotient = results.loc[f] / total
    condition_b = (quotient >= 0.05).any()

    if condition_a and condition_b:
        return 'MAJOR'
    else:
        return 'minor'

funds = list(set(funds))
funds.sort()
for f in funds:
    print('%s\t%s' % (f, fund_major_or_minor(f)))
