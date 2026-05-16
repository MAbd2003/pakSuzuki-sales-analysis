# Pak Suzuki Motors - Sales Analysis Dashboard
# Author: Muhammad Abdullah
# Tools: Python, Pandas, Matplotlib, Seaborn
# Purpose: Automotive sales KPI analysis for management reporting

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# ── 1. CREATE REALISTIC PAK SUZUKI SALES DATA ─────────────
np.random.seed(42)

models = ['Suzuki Alto', 'Suzuki Cultus', 'Suzuki Wagon R', 'Suzuki Jimny', 'Suzuki Bolan']
cities = ['Karachi', 'Lahore', 'Islamabad', 'Peshawar', 'Multan', 'Faisalabad']
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

prices = {
    'Suzuki Alto': 1800000,
    'Suzuki Cultus': 2200000,
    'Suzuki Wagon R': 2600000,
    'Suzuki Jimny': 4500000,
    'Suzuki Bolan': 1600000
}

targets = {
    'Suzuki Alto': 500,
    'Suzuki Cultus': 350,
    'Suzuki Wagon R': 300,
    'Suzuki Jimny': 100,
    'Suzuki Bolan': 200
}

rows = []
for month_idx, month in enumerate(months):
    for model in models:
        for city in cities:
            units = np.random.randint(20, 120)
            price = prices[model]
            revenue = units * price
            target = targets[model] // 6
            rows.append({
                'Month': month,
                'Month_Num': month_idx + 1,
                'Model': model,
                'City': city,
                'Units_Sold': units,
                'Price_PKR': price,
                'Revenue_PKR': revenue,
                'Target_Units': target,
                'Achievement_%': round((units / target) * 100, 1)
            })

df = pd.DataFrame(rows)

print("="*60)
print("PAK SUZUKI MOTORS - SALES ANALYSIS DASHBOARD")
print("="*60)
print(f"Total Records: {len(df)}")
print(f"Total Units Sold: {df['Units_Sold'].sum():,}")
print(f"Total Revenue: PKR {df['Revenue_PKR'].sum():,.0f}")
print(f"Average Monthly Achievement: {df['Achievement_%'].mean():.1f}%")

# ── 2. KPI SUMMARY ────────────────────────────────────────
print("\n" + "="*60)
print("KPI SUMMARY BY MODEL")
print("="*60)
kpi = df.groupby('Model').agg(
    Total_Units=('Units_Sold', 'sum'),
    Total_Revenue=('Revenue_PKR', 'sum'),
    Avg_Achievement=('Achievement_%', 'mean')
).sort_values('Total_Units', ascending=False)
print(kpi.to_string())

print("\n" + "="*60)
print("KPI SUMMARY BY CITY")
print("="*60)
city_kpi = df.groupby('City').agg(
    Total_Units=('Units_Sold', 'sum'),
    Total_Revenue=('Revenue_PKR', 'sum')
).sort_values('Total_Revenue', ascending=False)
print(city_kpi.to_string())

# ── 3. VISUALIZATIONS ─────────────────────────────────────
sns.set(style="whitegrid")
fig, axes = plt.subplots(2, 3, figsize=(18, 11))
fig.suptitle('Pak Suzuki Motors - Sales Analysis Dashboard\nMuhammad Abdullah',
             fontsize=18, fontweight='bold', color='#1F4E79')

# Chart 1 - Total Units by Model
model_sales = df.groupby('Model')['Units_Sold'].sum().sort_values(ascending=True)
axes[0,0].barh(model_sales.index, model_sales.values,
               color=['#2E75B6','#1F4E79','#4472C4','#5B9BD5','#9DC3E6'])
axes[0,0].set_title('Total Units Sold by Model', fontweight='bold')
axes[0,0].set_xlabel('Units Sold')
for i, v in enumerate(model_sales.values):
    axes[0,0].text(v + 10, i, f'{v:,}', va='center', fontsize=9)

# Chart 2 - Revenue by City
city_rev = df.groupby('City')['Revenue_PKR'].sum().sort_values(ascending=False) / 1e9
axes[0,1].bar(city_rev.index, city_rev.values, color='#2E75B6')
axes[0,1].set_title('Total Revenue by City (Billion PKR)', fontweight='bold')
axes[0,1].set_xlabel('City')
axes[0,1].set_ylabel('Revenue (Billion PKR)')
axes[0,1].tick_params(axis='x', rotation=45)
for i, v in enumerate(city_rev.values):
    axes[0,1].text(i, v + 0.1, f'{v:.1f}B', ha='center', fontsize=9)

# Chart 3 - Monthly Sales Trend
monthly = df.groupby('Month_Num')['Units_Sold'].sum()
axes[0,2].plot(monthly.index, monthly.values, marker='o',
               color='#1F4E79', linewidth=2.5, markersize=7)
axes[0,2].fill_between(monthly.index, monthly.values, alpha=0.2, color='#2E75B6')
axes[0,2].set_title('Monthly Sales Trend (2024)', fontweight='bold')
axes[0,2].set_xlabel('Month')
axes[0,2].set_ylabel('Units Sold')
axes[0,2].set_xticks(range(1,13))
axes[0,2].set_xticklabels(months, rotation=45, fontsize=8)

# Chart 4 - Target vs Achievement by Model
achievement = df.groupby('Model')['Achievement_%'].mean().sort_values(ascending=False)
colors = ['#2E75B6' if x >= 100 else '#C00000' for x in achievement.values]
axes[1,0].bar(achievement.index, achievement.values, color=colors)
axes[1,0].axhline(y=100, color='black', linestyle='--', linewidth=1.5, label='Target 100%')
axes[1,0].set_title('Target Achievement % by Model', fontweight='bold')
axes[1,0].set_xlabel('Model')
axes[1,0].set_ylabel('Achievement %')
axes[1,0].tick_params(axis='x', rotation=45)
axes[1,0].legend()

# Chart 5 - Heatmap City vs Model
heatmap_data = df.groupby(['City', 'Model'])['Units_Sold'].sum().unstack()
sns.heatmap(heatmap_data, ax=axes[1,1], cmap='Blues',
            annot=True, fmt='g', cbar_kws={'label': 'Units Sold'})
axes[1,1].set_title('Sales Heatmap: City vs Model', fontweight='bold')
axes[1,1].tick_params(axis='x', rotation=45)

# Chart 6 - Revenue Share by Model (Pie)
model_rev = df.groupby('Model')['Revenue_PKR'].sum()
axes[1,2].pie(model_rev.values, labels=model_rev.index,
              autopct='%1.1f%%', colors=['#1F4E79','#2E75B6','#4472C4','#5B9BD5','#9DC3E6'],
              startangle=90)
axes[1,2].set_title('Revenue Share by Model', fontweight='bold')

plt.tight_layout()
plt.savefig('suzuki_dashboard.png', dpi=150, bbox_inches='tight')
plt.show()
print("\nDashboard saved as suzuki_dashboard.png!")
print("\n✅ PAK SUZUKI SALES ANALYSIS COMPLETE!")
print("\nKey Insights:")
print(f"  Best selling model: {model_sales.idxmax()}")
print(f"  Highest revenue city: {city_rev.idxmax()}")
print(f"  Best month: Month {monthly.idxmax()}")