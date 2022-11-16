import pandas as pd

class Transactions_Dataframe():

    def __init__(self, file):
        self.df = pd.read_csv(file)

    def group_by_category(self):
        self.df['Category_count'] = self.df.groupby('Category')['Category'].transform('count')
        columns = ["Category", "Debit", "Category_count"]
        summary = self.df.groupby([columns[0], columns[2]], as_index=False).sum().sort_values(columns[1])
        return summary.loc[:, summary.columns.isin(columns)]

