"""
تحلیل آمار توصیفی پروژه املاک دیوار
برای اجرا:
1. مسیر فایل divar.csv را در خط 19 تنظیم کنید
2. کتابخانه‌های مورد نیاز را نصب کنید:
   pip install pandas numpy matplotlib seaborn folium plotly
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

# ============ تنظیم مسیر فایل ============

# گزینه 1: مسیر کامل فایل (توصیه می‌شود)
FILE_PATH = r'C:\Users\at690\OneDrive\Desktop\divar.csv'  # مسیر خود را اینجا قرار دهید

# =========================================

# تنظیمات نمایش
plt.style.use('default')
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 10
plt.rcParams['axes.unicode_minus'] = False

# بررسی و خواندن فایل
print("=" * 80)
print("تحلیل آمار توصیفی املاک دیوار")
print("=" * 80)

if not os.path.exists(FILE_PATH):
    print(f"\n❌ خطا: فایل یافت نشد!")
    print(f"مسیر تنظیم شده: {FILE_PATH}")
    print("\nلطفاً یکی از کارهای زیر را انجام دهید:")
    print("1. فایل divar.csv را به دسکتاپ کپی کنید")
    print("2. یا مسیر صحیح را در خط 20 این فایل تنظیم کنید")
    sys.exit(1)

print(f"✅ فایل پیدا شد: {FILE_PATH}")

# خواندن داده‌ها
try:
    df = pd.read_csv(FILE_PATH, encoding='utf-8')
except:
    try:
        df = pd.read_csv(FILE_PATH, encoding='utf-8-sig')
    except:
        df = pd.read_csv(FILE_PATH, encoding='cp1256')

print(f"✅ داده‌ها خوانده شد: {len(df):,} رکورد، {len(df.columns)} ستون")

# تبدیل تاریخ
if 'created_at_month' in df.columns:
    df['created_at_month'] = pd.to_datetime(df['created_at_month'], errors='coerce')

# تبدیل سال ساخت
if 'construction_year' in df.columns:
    df['construction_year'] = pd.to_numeric(df['construction_year'], errors='coerce')

# =====================================
# سوال 1: توزیع آگهی‌ها
# =====================================
print("\n" + "=" * 50)
print("سوال 1: توزیع آگهی‌ها در دسته‌بندی‌ها")
print("=" * 50)

if 'cat2_slug' in df.columns and 'cat3_slug' in df.columns:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

    # سطح 2
    cat2_counts = df['cat2_slug'].value_counts().head(10)
    ax1.bar(range(len(cat2_counts)), cat2_counts.values, color='steelblue')
    ax1.set_xlabel('Category Level 2')
    ax1.set_ylabel('Count')
    ax1.set_title('Top 10 Categories - Level 2')
    ax1.set_xticks(range(len(cat2_counts)))
    ax1.set_xticklabels([str(x)[:15] for x in cat2_counts.index], rotation=45, ha='right')

    # سطح 3
    cat3_counts = df['cat3_slug'].value_counts().head(10)
    ax2.bar(range(len(cat3_counts)), cat3_counts.values, color='darkgreen')
    ax2.set_xlabel('Category Level 3')
    ax2.set_ylabel('Count')
    ax2.set_title('Top 10 Categories - Level 3')
    ax2.set_xticks(range(len(cat3_counts)))
    ax2.set_xticklabels([str(x)[:15] for x in cat3_counts.index], rotation=45, ha='right')

    plt.tight_layout()
    plt.savefig('q1_categories.png', dpi=150, bbox_inches='tight')
    plt.show()

    print(f"تعداد دسته‌های سطح 2: {df['cat2_slug'].nunique()}")
    print(f"تعداد دسته‌های سطح 3: {df['cat3_slug'].nunique()}")

# =====================================
# سوال 2: هیستوگرام سال ساخت
# =====================================
print("\n" + "=" * 50)
print("سوال 2: هیستوگرام سال ساخت")
print("=" * 50)

if 'construction_year' in df.columns:
    valid_years = df[(df['construction_year'] > 1300) & (df['construction_year'] < 1405)]['construction_year']

    if len(valid_years) > 0:
        plt.figure(figsize=(10, 6))
        plt.hist(valid_years.dropna(), bins=50, color='coral', edgecolor='black', alpha=0.7)
        plt.xlabel('Construction Year')
        plt.ylabel('Count')
        plt.title('Distribution of Construction Years')
        plt.axvline(valid_years.mean(), color='red', linestyle='--',
                    label=f'Mean: {valid_years.mean():.0f}')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.savefig('q2_construction_years.png', dpi=150, bbox_inches='tight')
        plt.show()

        print(f"میانگین: {valid_years.mean():.0f}")
        print(f"میانه: {valid_years.median():.0f}")
        print(f"بازه: {valid_years.min():.0f} - {valid_years.max():.0f}")

# =====================================
# سوال 3: آگهی‌های فروش و اجاره
# =====================================
print("\n" + "=" * 50)
print("سوال 3: تعداد آگهی‌های فروش و اجاره")
print("=" * 50)

if all(col in df.columns for col in ['price_mode', 'rent_mode', 'created_at_month']):
    df_sale = df[df['price_mode'].notna() & df['created_at_month'].notna()]
    df_rent = df[df['rent_mode'].notna() & df['created_at_month'].notna()]

    if len(df_sale) > 0 and len(df_rent) > 0:
        sale_monthly = df_sale.groupby(df_sale['created_at_month'].dt.to_period('M')).size()
        rent_monthly = df_rent.groupby(df_rent['created_at_month'].dt.to_period('M')).size()

        plt.figure(figsize=(12, 6))
        x = range(min(len(sale_monthly), len(rent_monthly)))
        width = 0.35

        plt.bar([i - width / 2 for i in x], sale_monthly.values[:len(x)], width,
                label='Sale', color='dodgerblue')
        plt.bar([i + width / 2 for i in x], rent_monthly.values[:len(x)], width,
                label='Rent', color='orange')

        plt.xlabel('Month')
        plt.ylabel('Number of Ads')
        plt.title('Monthly Sale vs Rent Ads')
        plt.legend()
        plt.grid(True, alpha=0.3, axis='y')
        plt.xticks(x, [str(m)[:7] for m in sale_monthly.index[:len(x)]], rotation=45)
        plt.tight_layout()
        plt.savefig('q3_sale_rent_monthly.png', dpi=150, bbox_inches='tight')
        plt.show()

        print(f"میانگین آگهی فروش ماهانه: {sale_monthly.mean():.0f}")
        print(f"میانگین آگهی اجاره ماهانه: {rent_monthly.mean():.0f}")

# =====================================
# سوال 4: توزیع قیمت فروش
# =====================================
print("\n" + "=" * 50)
print("سوال 4: توزیع قیمت فروش")
print("=" * 50)

if 'price_value' in df.columns and 'cat3_slug' in df.columns:
    df_price = df[(df['price_value'] > 0) & df['price_value'].notna()]

    if len(df_price) > 0:
        top_cats = df_price['cat3_slug'].value_counts().head(8).index

        plt.figure(figsize=(12, 8))
        data_to_plot = []
        labels = []

        for cat in top_cats:
            cat_prices = df_price[df_price['cat3_slug'] == cat]['price_value']
            if len(cat_prices) > 0:
                data_to_plot.append(cat_prices.values)
                labels.append(str(cat)[:20])

        bp = plt.boxplot(data_to_plot, labels=labels, patch_artist=True)
        for patch in bp['boxes']:
            patch.set_facecolor('lightblue')

        plt.yscale('log')
        plt.ylabel('Price (Toman)')
        plt.title('Price Distribution by Category')
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, alpha=0.3, axis='y')
        plt.tight_layout()
        plt.savefig('q4_price_distribution.png', dpi=150, bbox_inches='tight')
        plt.show()

# =====================================
# سوال 5: توزیع جغرافیایی
# =====================================
print("\n" + "=" * 50)
print("سوال 5: توزیع جغرافیایی")
print("=" * 50)

if 'city_slug' in df.columns:
    city_counts = df['city_slug'].value_counts().head(15)

    plt.figure(figsize=(10, 8))
    plt.barh(range(len(city_counts)), city_counts.values, color='teal')
    plt.yticks(range(len(city_counts)), [str(x)[:30] for x in city_counts.index])
    plt.xlabel('Number of Ads')
    plt.title('Top 15 Cities by Number of Ads')
    plt.grid(True, alpha=0.3, axis='x')
    plt.tight_layout()
    plt.savefig('q5_cities.png', dpi=150, bbox_inches='tight')
    plt.show()

    print(f"شهر برتر: {city_counts.index[0]} با {city_counts.values[0]:,} آگهی")

# =====================================
# سوال 6: ترند قیمت اجاره
# =====================================
print("\n" + "=" * 50)
print("سوال 6: ترند قیمت اجاره")
print("=" * 50)

if 'rent_value' in df.columns and 'created_at_month' in df.columns:
    df_rent_valid = df[(df['rent_value'] > 0) &
                       df['rent_value'].notna() &
                       df['created_at_month'].notna()]

    if len(df_rent_valid) > 0:
        rent_trend = df_rent_valid.groupby(
            df_rent_valid['created_at_month'].dt.to_period('M')
        )['rent_value'].mean()

        if len(rent_trend) > 1:
            plt.figure(figsize=(12, 6))
            plt.plot(range(len(rent_trend)), rent_trend.values,
                     marker='o', linewidth=2, markersize=8, color='darkred')
            plt.xlabel('Month')
            plt.ylabel('Average Rent (Toman)')
            plt.title('Monthly Rent Trend')
            plt.grid(True, alpha=0.3)
            plt.xticks(range(len(rent_trend)),
                       [str(m)[:7] for m in rent_trend.index], rotation=45)

            # خط روند
            z = np.polyfit(range(len(rent_trend)), rent_trend.values, 1)
            p = np.poly1d(z)
            plt.plot(range(len(rent_trend)), p(range(len(rent_trend))),
                     "--", color='blue', alpha=0.5)

            plt.tight_layout()
            plt.savefig('q6_rent_trend.png', dpi=150, bbox_inches='tight')
            plt.show()

            growth = ((rent_trend.iloc[-1] / rent_trend.iloc[0]) - 1) * 100
            print(f"رشد کل: {growth:.1f}%")

# =====================================
# سوال 8: ماتریس همبستگی
# =====================================
print("\n" + "=" * 50)
print("سوال 8: ماتریس همبستگی")
print("=" * 50)

# انتخاب ستون‌های عددی
numeric_cols = ['price_value', 'rent_value', 'land_size', 'building_size',
                'rooms_count', 'construction_year', 'location_latitude',
                'location_longitude']
available_numeric = [col for col in numeric_cols if col in df.columns]

if len(available_numeric) >= 3:
    df_numeric = df[available_numeric].select_dtypes(include=[np.number])

    if len(df_numeric.columns) >= 3:
        corr_matrix = df_numeric.corr()

        plt.figure(figsize=(10, 8))
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f',
                    cmap='coolwarm', center=0, square=True)
        plt.title('Correlation Matrix')
        plt.tight_layout()
        plt.savefig('q8_correlation.png', dpi=150, bbox_inches='tight')
        plt.show()

# =====================================
# سوال 9: امکانات در مناطق
# =====================================
print("\n" + "=" * 50)
print("سوال 9: توزیع امکانات")
print("=" * 50)

amenity_cols = ['has_elevator', 'has_parking', 'has_balcony',
                'has_pool', 'has_security_guard']
available_amenities = [col for col in amenity_cols if col in df.columns]

if available_amenities and 'neighborhood_slug' in df.columns:
    top_neighborhoods = df['neighborhood_slug'].value_counts().head(10).index

    amenity_data = []
    for neighborhood in top_neighborhoods:
        n_data = df[df['neighborhood_slug'] == neighborhood]
        row = [neighborhood[:20]]

        for amenity in available_amenities:
            if amenity in n_data.columns:
                pct = (pd.to_numeric(n_data[amenity], errors='coerce') == 1).mean() * 100
                row.append(pct)
            else:
                row.append(0)

        amenity_data.append(row)

    amenity_df = pd.DataFrame(amenity_data,
                              columns=['Neighborhood'] + available_amenities)

    # Heatmap
    plt.figure(figsize=(10, 6))
    sns.heatmap(amenity_df.set_index('Neighborhood').T,
                annot=True, fmt='.1f', cmap='YlOrRd')
    plt.title('Amenities by Neighborhood (%)')
    plt.tight_layout()
    plt.savefig('q9_amenities.png', dpi=150, bbox_inches='tight')
    plt.show()

print("\n" + "=" * 80)
print("✅ تحلیل کامل شد!")
print("نمودارها در فایل‌های PNG ذخیره شدند.")
print("=" * 80)