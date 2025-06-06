import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.tree import DecisionTreeClassifier
from scipy import stats



divar = pd.read_csv(rf"C:\Users\Asus\Desktop\Divar.csv")
divar2 = divar[["price_value","has_barbecue","has_pool","has_jacuzzi","has_sauna"]]
divar3 = divar2.copy()
divar3["luxury"] = divar2["has_barbecue"] + divar2["has_pool"] + divar2["has_jacuzzi"] + divar2["has_sauna"] 
divar3 = divar3[divar3['price_value'].notna()]
luxury_prices_0 = divar3[divar3['luxury'] == 0]['price_value']
without_luxury_prices_1 = divar3[divar3['luxury'] != 0]['price_value']

print(luxury_prices_0.mean())
print(without_luxury_prices_1.mean())

t_statistic, p_value_ttest = stats.ttest_ind(luxury_prices_0, without_luxury_prices_1, equal_var=False, alternative='less')


if p_value_ttest < 0.05:
    print("hypothesis is False")
else:
    print("hypothesis is True")
