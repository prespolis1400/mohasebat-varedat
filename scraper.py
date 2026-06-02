import requests
from bs4 import BeautifulSoup
import json
import os

def fetch_customs_rates():
    url = "https://gomrok24.com/customs-exchange-rate"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', class_='tariff-table')
        
        if not table:
            print("جدول یافت نشد!")
            return

        rates_data = []
        rows = table.find('tbody').find_all('tr')
        
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 3:
                rates_data.append({
                    "code": cols[0].text.strip(),
                    "name": cols[1].text.strip(),
                    "rate": cols[2].text.strip().replace(',', '')
                })
        
        # ذخیره در ریشه مخزن
        with open('rates.json', 'w', encoding='utf-8') as f:
            json.dump(rates_data, f, ensure_ascii=False, indent=4)
            
        print("آپدیت نرخ‌ها با موفقیت انجام شد.")

    except Exception as e:
        print(f"خطا: {e}")

if __name__ == "__main__":
    fetch_customs_rates()
