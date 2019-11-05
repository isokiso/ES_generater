import pandas as pd
import converter

file = '../data/gs.csv'
with open(file,'r') as f:
    df = pd.read_csv(f, names=('Q','A'))
#df = df[~df['Q'].str.contains('英語')]
df = df[~df['A'].str.contains('I ')]
df = df.query('Q.str.contains("(長所)")' ,engine='python')

fun = lambda x:"<BOS>" + x[3:-4] + "<EOS>\n"
df['A'] = df['A'].apply(fun)
with open('../data/gs.txt', 'w') as f:
    f.writelines(df['A'].values.tolist())

