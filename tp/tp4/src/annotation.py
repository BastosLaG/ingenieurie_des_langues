import csv
import pandas as pd

debug = False
i = 0
def del_useless_info(filename: str) -> None:
    """_summary_
    Args:
        filename (str): database originel
    """

    df = pd.read_csv(filename)
    
    if 'Test' not in df.columns:
        df['Test'] = ''
    
    df = df[['Note', 'Test', 'Avis' ]]

    df['Avis'] = df['Avis'].str.lower()
    df['Note'] = df['Note'].str.replace('/', ' ')
    df['Note'] = df['Note'].str[:2]

    if debug: print(f"print : 1")
    df = df[~df['Note'].isin(['[]', ''])]

    if debug: print(f"print : 2")
    df['Note'] = df['Note'].astype(int)
    
    if debug: print(f"print : 3")
    df = df[(df['Note'] <= 5) | (df['Note'] >= 15)]
    if debug: print(f"print : 4")

    df['Test'] = df['Note'].apply(lambda x: '-' if x <= 5 else '+')
    df = df[['Test', 'Avis' ]]
    df.to_csv('database/new_test.csv', index=False)
    return


def main():
    filename_noise = "database/jeux_avis_populaire.csv"
    del_useless_info(filename_noise)
    pass

if __name__ == "__main__":
    # debug = True
    main()
