import pandas as pd
import numpy as np
from scipy import stats

divar = pd.read_csv(rf"C:\Users\Asus\Desktop\Divar.csv")
divar2 = divar[["price_value","deed_type"]]
divar2 = divar2[divar2['price_value'].notna()]
divar2["deed_type"].value_counts()
divar3 = divar2.copy()
divar3["deed_type_0_1"] = divar2["deed_type"].apply(lambda x: 0 if pd.isna(x) or x == 'unselect' else 1).copy()
prices_with_deed = divar3[divar3['deed_type_0_1'] == 0]['price_value']
prices_without_deed = divar3[divar3['deed_type_0_1'] == 1]['price_value']

t_statistic, p_value = stats.ttest_ind(prices_with_deed, prices_without_deed, equal_var=False)

print(f"T-statistic: {t_statistic}")
print(f"P-value: {p_value}")
print("mean price houses with deed",prices_with_deed.mean())
print("mean price houses without deed",prices_without_deed.mean())
if p_value < 0.05:
    print("hypothesis is True")
else:   
    print("hypothesis is False")
