import pandas as pd

def conv(file):
    with open(file, 'r') as f:
        df = pd.read_csv(f, names=('Q','A'))
    fun = lambda x:"<BOS>" + x[3:-4] + "<EOS>\n"
    df['A'] = df['A'].apply(fun)

    with open('../data/morgan.txt', 'w') as f:
        f.writelines(df['A'].values.tolist())

if __name__ == '__main__':
    file = '../data/morgan.csv'
    conv(file)
