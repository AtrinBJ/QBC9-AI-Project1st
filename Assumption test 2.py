import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.tree import DecisionTreeClassifier
from scipy import stats

divar = pd.read_csv(rf"C:\Users\Asus\Desktop\Divar.csv")
divar2 = divar[["building_size","construction_year"]]
divar3 = divar2.dropna().copy()
table = str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')
divar3.loc[:, "construction_year"] = divar3["construction_year"].astype(str).apply(lambda x: x.translate(table))
divar3.loc[:, "construction_year"] = divar3["construction_year"].apply(lambda x: "1369" if x == "قبل از 1370" else x)
divar3.loc[:, "construction_year"] = divar3["construction_year"].astype(int)
divar3.loc[:, "building_size"] = divar3["building_size"].astype(int)
divar3.loc[:, "construction_year_0_1"] = divar3["construction_year"].apply(lambda x: 0 if x < 1396 else 1)

old_house = divar3[divar3['construction_year_0_1'] == 0]['building_size']
modern_house = divar3[divar3['construction_year_0_1'] == 1]['building_size']

t_statistic, p_value = stats.ttest_ind(old_house, modern_house)

print(f"T-statistic: {t_statistic}")
print(f"P-value: {p_value}")

if p_value < 0.5: 
    print("hypothesis is False")
else:
    print("hypothesis is True")