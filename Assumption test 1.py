import pandas as pd
import numpy as np
from scipy import stats



divar = pd.read_csv(rf"C:\Users\Asus\Desktop\Divar.csv")
city_size = pd.read_csv(rf"C:\Users\Asus\Desktop\iran_city_classification.csv")
divar2 = divar[["building_size","city_slug"]]
divar3 = divar2.dropna().copy()
divar_merge = pd.merge(divar3, city_size,left_on="city_slug",right_on="نام شهر", how='left')
divar_merge["city_0_1"] = divar_merge["دسته‌بندی"].apply(lambda x: 0 if x == "کلان‌شهر" else 1)
big_city_0 = divar_merge[divar_merge['city_0_1'] == 0]['building_size']
small_city_1 = divar_merge[divar_merge['city_0_1'] == 1]['building_size']
big_city_0_var = np.var(big_city_0, ddof=1)
small_city_1_var = np.var(small_city_1, ddof=1)
levene_stat, levene_p_value = stats.levene(big_city_0, small_city_1)
if levene_p_value < 0.05:
    equal_variances = False
else:
    equal_variances = True
print(big_city_0_var)
print(small_city_1_var)
print(big_city_0.mean())
print(small_city_1.mean())
t_statistic, p_value_ttest = stats.ttest_ind(big_city_0, small_city_1, equal_var=equal_variances, alternative='less')
if p_value_ttest < 0.05:
    print("hypothesis is True")
else:
    print("hypothesis is False")
