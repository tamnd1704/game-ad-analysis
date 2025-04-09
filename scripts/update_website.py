import json
import os
from datetime import datetime

def update_website_data():
    """Cập nhật thông tin cho website"""
    # Tạo thư mục data nếu chưa tồn tại
    os.makedirs('data', exist_ok=True)
    
    # Tạo file cập nhật timestamp
    update_info = {
        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'status': 'success'
    }
    
    with open('data/update_info.json', 'w', encoding='utf-8') as f:
        json.dump(update_info, f, ensure_ascii=False, indent=2)
    
    print("Website data updated successfully!")

if __name__ == "__main__":
    update_website_data()
