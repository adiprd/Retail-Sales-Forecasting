import pandas as pd
import numpy as np
import random

PRODUK_PER_BULAN = 50 
TOTAL_BULAN = 24      
NAMA_FILE = 'data_retail_monthly.csv'

def generate_time_series():
    print(f"⏳ Sedang membuat data history selama {TOTAL_BULAN} bulan...")
    np.random.seed(42)
    data = []
    
    categories = ['Smartphone', 'Laptop', 'Fashion', 'Home_IoT']
    seasons = ['Winter', 'Spring', 'Summer', 'Autumn'] 

    for bulan_ke in range(1, TOTAL_BULAN + 1):

        idx_musim = (bulan_ke % 12) // 3 
        season = seasons[idx_musim]
        
        for _ in range(PRODUK_PER_BULAN):
            cat = random.choice(categories)

            tech_score = int(np.random.normal(60, 15))
            tech_score = max(10, min(100, tech_score))
            price = max(20, round(tech_score * 5 + np.random.normal(0, 50), 2))
            competitor_price = round(price * np.random.uniform(0.8, 1.25), 2)

            social_hype = random.randint(0, 100)
            ad_spend = round(np.random.uniform(0, 5000), 2)

            prev_sales = random.randint(50, 500)

            value_effect = (tech_score / price) * 2000
            hype_effect = social_hype * 3
            season_bonus = 100 if cat == 'Fashion' and season == 'Summer' else 0
            ad_effect = np.log1p(ad_spend) * 10

            demand = 50 + value_effect + hype_effect + (prev_sales * 0.5) + season_bonus + ad_effect
            demand += np.random.normal(0, 20)
            sales_qty = int(max(0, demand))
            
            data.append([bulan_ke, cat, season, price, competitor_price, tech_score, social_hype, prev_sales, ad_spend, sales_qty])

    cols = ['Month', 'Category', 'Season', 'Price', 'Competitor_Price', 'Tech_Score', 'Social_Hype', 'Prev_Sales', 'Ad_Spend', 'Sales_Qty']
    df = pd.DataFrame(data, columns=cols)
    
    df.to_csv(NAMA_FILE, index=False)
    print(f"✅ Data Time Series ({len(df)} baris) tersimpan di: {NAMA_FILE}")

if __name__ == "__main__":
    generate_time_series()
