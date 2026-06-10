import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# 데이터 저장 디렉토리
data_dir = "bmw_data"
os.makedirs(data_dir, exist_ok=True)

# 난수 시드 설정
np.random.seed(42)

# 1. BMW 모델 정보
models_data = {
    'Model_ID': ['M001', 'M002', 'M003', 'M004', 'M005', 'M006', 'M007', 'M008'],
    'Model_Name': ['BMW 320i', 'BMW 330i', 'BMW 530i', 'BMW X3', 'BMW X5', 'BMW X7', 'BMW M440i', 'BMW i7'],
    'Category': ['Sedan', 'Sedan', 'Sedan', 'SUV', 'SUV', 'SUV', 'Performance', 'EV'],
    'Engine_Type': ['Petrol', 'Petrol', 'Petrol', 'Petrol', 'Petrol', 'Petrol', 'Petrol', 'Electric'],
    'Engine_CC': [2000, 2998, 2998, 1998, 2998, 3498, 3000, 0],
    'Horsepower': [184, 255, 281, 248, 340, 375, 503, 516],
    'Price_USD': [42000, 50000, 60000, 48000, 65000, 85000, 75000, 95000],
    'Fuel_Efficiency_MPG': [29, 26, 25, 24, 22, 20, 18, np.inf],
    'Launch_Year': [2020, 2019, 2021, 2020, 2019, 2022, 2021, 2023]
}
df_models = pd.DataFrame(models_data)
df_models.to_csv(f'{data_dir}/bmw_models.csv', index=False)
print("[OK] bmw_models.csv created")

# 2. 지역별 판매 정보 (2024년)
regions = ['Seoul', 'Busan', 'Incheon', 'Daegu', 'Daejeon', 'Gwangju', 'Ulsan', 'Gyeonggi']
models = df_models['Model_Name'].tolist()

sales_region_data = []
for region in regions:
    for model in models:
        sales_region_data.append({
            'Region': region,
            'Model': model,
            'Jan': np.random.randint(10, 50),
            'Feb': np.random.randint(10, 50),
            'Mar': np.random.randint(15, 60),
            'Apr': np.random.randint(15, 60),
            'May': np.random.randint(20, 70),
            'Jun': np.random.randint(20, 70),
            'Jul': np.random.randint(15, 65),
            'Aug': np.random.randint(15, 65),
            'Sep': np.random.randint(18, 68),
            'Oct': np.random.randint(18, 68),
            'Nov': np.random.randint(12, 55),
            'Dec': np.random.randint(12, 55),
        })
df_sales_region = pd.DataFrame(sales_region_data)
df_sales_region.to_csv(f'{data_dir}/sales_by_region.csv', index=False)
print("[OK] sales_by_region.csv created")

# 3. 월별 판매 정보
months = ['2024-01', '2024-02', '2024-03', '2024-04', '2024-05', '2024-06',
          '2024-07', '2024-08', '2024-09', '2024-10', '2024-11', '2024-12']
sales_month_data = []
for month in months:
    for model in models:
        total_sales = np.random.randint(100, 400)
        sales_month_data.append({
            'Month': month,
            'Model': model,
            'Total_Sales': total_sales,
            'Target': 300,
            'Achievement_Rate': round(total_sales / 300 * 100, 2),
            'Revenue_USD': total_sales * df_models[df_models['Model_Name'] == model]['Price_USD'].values[0]
        })
df_sales_month = pd.DataFrame(sales_month_data)
df_sales_month.to_csv(f'{data_dir}/sales_by_month.csv', index=False)
print("[OK] sales_by_month.csv created")

# 4. 재고 정보
inventory_data = []
for model in models:
    for region in regions:
        inventory_data.append({
            'Model': model,
            'Region': region,
            'Stock_Qty': np.random.randint(5, 50),
            'Reserved_Qty': np.random.randint(0, 20),
            'Available_Qty': np.random.randint(5, 40),
            'Last_Updated': datetime.now().strftime('%Y-%m-%d')
        })
df_inventory = pd.DataFrame(inventory_data)
df_inventory.to_csv(f'{data_dir}/inventory.csv', index=False)
print("[OK] inventory.csv created")

# 5. 고객 정보
customer_data = []
customer_id = 10001
for i in range(1000):
    customer_data.append({
        'Customer_ID': customer_id + i,
        'Purchase_Date': (datetime(2024, 1, 1) + timedelta(days=np.random.randint(0, 365))).strftime('%Y-%m-%d'),
        'Model': np.random.choice(models),
        'Region': np.random.choice(regions),
        'Age': np.random.randint(25, 75),
        'Gender': np.random.choice(['M', 'F']),
        'Customer_Type': np.random.choice(['Individual', 'Corporate']),
        'Satisfaction_Score': np.random.randint(1, 11),
        'Repeat_Purchase': np.random.choice(['Yes', 'No'], p=[0.3, 0.7])
    })
df_customer = pd.DataFrame(customer_data)
df_customer.to_csv(f'{data_dir}/customer_info.csv', index=False)
print("[OK] customer_info.csv created")

# 6. 옵션/사양 정보
options_data = {
    'Option_ID': ['OPT001', 'OPT002', 'OPT003', 'OPT004', 'OPT005', 'OPT006', 'OPT007', 'OPT008', 'OPT009', 'OPT010'],
    'Option_Name': [
        'Panoramic Sunroof', 'Premium Sound System', 'Adaptive LED Headlights',
        '4-Zone Climate Control', 'Leather Upholstery', 'Navigation System',
        'Harman Kardon System', 'Wireless Phone Charging', 'Parking Assist Plus',
        'All-Wheel Drive'
    ],
    'Category': ['Comfort', 'Audio', 'Lighting', 'Climate', 'Interior', 'Navigation',
                 'Audio', 'Technology', 'Safety', 'Drivetrain'],
    'Price_USD': [1500, 2000, 1800, 1200, 2500, 1600, 3000, 800, 2200, 3500],
    'Availability': [True, True, True, True, True, True, True, True, True, True],
    'Popularity_Score': [8.5, 8.2, 8.8, 7.5, 8.9, 8.1, 8.7, 7.8, 8.4, 8.6]
}
df_options = pd.DataFrame(options_data)
df_options.to_csv(f'{data_dir}/options.csv', index=False)
print("[OK] options.csv created")

# 7. 딜러 정보
dealers_data = []
dealer_id = 1001
for i in range(50):
    dealers_data.append({
        'Dealer_ID': dealer_id + i,
        'Dealer_Name': f'BMW Showroom {i+1}',
        'Region': np.random.choice(regions),
        'Address': f'{np.random.choice(regions)} District {np.random.randint(1, 20)}',
        'Phone': f'02-XXXX-{np.random.randint(1000, 9999)}',
        'Employees': np.random.randint(5, 30),
        'Established_Year': np.random.randint(2000, 2023),
        'Monthly_Target': np.random.randint(50, 200),
        'Rating': round(np.random.uniform(3.5, 5.0), 1)
    })
df_dealers = pd.DataFrame(dealers_data)
df_dealers.to_csv(f'{data_dir}/dealers.csv', index=False)
print("[OK] dealers.csv created")

# 8. 딜러별 판매 정보
dealer_sales_data = []
for _, dealer in df_dealers.iterrows():
    for month in months:
        for model in models:
            dealer_sales_data.append({
                'Dealer_ID': dealer['Dealer_ID'],
                'Dealer_Name': dealer['Dealer_Name'],
                'Month': month,
                'Model': model,
                'Sales_Qty': np.random.randint(0, 15),
                'Revenue': np.random.randint(0, 500000)
            })
df_dealer_sales = pd.DataFrame(dealer_sales_data)
df_dealer_sales.to_csv(f'{data_dir}/sales_by_dealer.csv', index=False)
print("[OK] sales_by_dealer.csv created")

# 9. 일일 판매 정보 (최근 3개월)
daily_sales_data = []
start_date = datetime(2024, 10, 1)
for i in range(91):
    current_date = start_date + timedelta(days=i)
    if current_date.weekday() < 5:  # 평일만
        for model in np.random.choice(models, np.random.randint(3, 8)):
            daily_sales_data.append({
                'Date': current_date.strftime('%Y-%m-%d'),
                'Model': model,
                'Sales_Qty': np.random.randint(1, 5),
                'Region': np.random.choice(regions),
                'Dealer_ID': np.random.choice(df_dealers['Dealer_ID'].tolist()),
            })
df_daily_sales = pd.DataFrame(daily_sales_data)
df_daily_sales.to_csv(f'{data_dir}/daily_sales.csv', index=False)
print("[OK] daily_sales.csv created")

# 10. 고객 만족도 정보
satisfaction_data = []
for i in range(500):
    satisfaction_data.append({
        'Survey_ID': 5001 + i,
        'Customer_ID': np.random.randint(10001, 11001),
        'Model': np.random.choice(models),
        'Quality_Score': np.random.randint(1, 11),
        'Service_Score': np.random.randint(1, 11),
        'Price_Satisfaction': np.random.randint(1, 11),
        'Overall_Satisfaction': np.random.randint(1, 11),
        'Would_Recommend': np.random.choice(['Yes', 'No']),
        'Survey_Date': (datetime(2024, 1, 1) + timedelta(days=np.random.randint(0, 365))).strftime('%Y-%m-%d')
    })
df_satisfaction = pd.DataFrame(satisfaction_data)
df_satisfaction.to_csv(f'{data_dir}/customer_satisfaction.csv', index=False)
print("[OK] customer_satisfaction.csv created")

# 11. 옵션별 추가 판매 정보
option_sales_data = []
for i in range(1500):
    option_sales_data.append({
        'Transaction_ID': 20001 + i,
        'Customer_ID': np.random.randint(10001, 11001),
        'Option_ID': np.random.choice(df_options['Option_ID'].tolist()),
        'Option_Name': np.random.choice(df_options['Option_Name'].tolist()),
        'Purchase_Date': (datetime(2024, 1, 1) + timedelta(days=np.random.randint(0, 365))).strftime('%Y-%m-%d'),
        'Price': np.random.randint(800, 3500),
        'Dealer_ID': np.random.choice(df_dealers['Dealer_ID'].tolist())
    })
df_option_sales = pd.DataFrame(option_sales_data)
df_option_sales.to_csv(f'{data_dir}/option_sales.csv', index=False)
print("[OK] option_sales.csv created")

# 12. 경쟁사 비교 정보
competitors_data = []
competitor_models = ['Audi A4', 'Mercedes C-Class', 'Lexus IS', 'Porsche 911', 'Tesla Model 3']
for comp_model in competitor_models:
    for month in months:
        competitors_data.append({
            'Month': month,
            'Competitor_Model': comp_model,
            'Market_Share': round(np.random.uniform(5, 25), 2),
            'Avg_Price_USD': np.random.randint(40000, 100000),
            'Customer_Satisfaction': round(np.random.uniform(3.5, 5.0), 1)
        })
df_competitors = pd.DataFrame(competitors_data)
df_competitors.to_csv(f'{data_dir}/competitor_analysis.csv', index=False)
print("[OK] competitor_analysis.csv created")

print(f"\nComplete! 12 CSV files have been created in '{data_dir}' folder")
print(f"\nGenerated files:")
for file in sorted(os.listdir(data_dir)):
    file_path = os.path.join(data_dir, file)
    file_size = os.path.getsize(file_path) / 1024
    print(f"  - {file} ({file_size:.1f} KB)")
