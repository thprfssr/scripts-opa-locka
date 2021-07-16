import pandas as pd
from tqdm import tqdm

# This function translates divisions to their corresponding funds
def division_to_fund(div):

    # Define an attribute for the function in order not to read disk twice
    if not hasattr(division_to_fund, 'df'):
        filename = 'divisions_and_funds.csv'
        division_to_fund.df = pd.read_csv(filename, dtype = str)
        division_to_fund.divisions = set(division_to_fund.df['Division'])

    # Define a dictionary holding the data, and use it to find the correct fund
    divisions = division_to_fund.df['Division']
    funds = division_to_fund.df['Fund']
    dic = dict(zip(divisions, funds))
    return dic[div]

# This function returns all the divisions that fall under a given fund
def fund_to_division(fund):

    # Initialize the attributes in the function division_to_fund()
    if not hasattr(division_to_fund, 'divisions'):
        try:
            division_to_fund(None)
        except:
            pass

    # Get all the divisions under the fund
    divisions = set()
    for div in division_to_fund.divisions:
        if division_to_fund(div) == fund:
            divisions.add(div)



    return divisions


# Read the data
filename = 'je.tsv'
df = pd.read_csv(filename, sep = '\t', dtype = {'DIVISION': str})
je_numbers = set(df['JOURNAL ENTRY NO'])
divisions_and_funds = set(df['DIVISION'])
funds = set()
for e in divisions_and_funds:
    if len(e) == 3:
        funds.add(e)
    elif len(e) == 2:
        funds.add(division_to_fund(e))
    else:
        print('Error: Unknown division/fund:', e)

# Start iterating through the data in order to analyze it
for je in tqdm(je_numbers):
    for f in funds:

        # Filter the data by JE number and by Division
        U = fund_to_division(f)
        U.add(f)
        filtered = df.loc[(df['JOURNAL ENTRY NO'] == je) & (df['DIVISION'].isin(U))]
        debit = filtered['DEBIT']
        credit = filtered['CREDIT']
        net = debit - credit

        print('%s\t%s\t%.2f' % (je, f, sum(net)))
