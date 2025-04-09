import json
import os
import requests
from io import BytesIO
from datetime import datetime
import time
import random
from bs4 import BeautifulSoup
from PIL import Image
import colorsys

def get_dominant_colors(image_url, num_colors=3):
    """Phân tích màu sắc chủ đạo từ hình ảnh"""
    try:
        # Tải hình ảnh
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))
        
        # Resize để giảm thời gian xử lý
        img = img.resize((100, 100))
        img = img.convert('RGB')
        
        # Lấy tất cả pixel
        pixels = list(img.getdata())
        
        # Nhóm các màu tương tự
        color_counts = {}
        for pixel in pixels:
            color_key = (pixel[0]//20, pixel[1]//20, pixel[2]//20)
            color_counts[color_key] = color_counts.get(color_key, 0) + 1
        
        # Sắp xếp theo số lượng
        sorted_colors = sorted(color_counts.items(), key=lambda x: x[1], reverse=True)
        
        # Lấy các màu chính
        dominant_colors = []
        for i in range(min(num_colors, len(sorted_colors))):
            color_key, count = sorted_colors[i]
            r, g, b = color_key[0]*20, color_key[1]*20, color_key[2]*20
            
            # Chuyển sang hex
            hex_color = '#{:02x}{:02x}{:02x}'.format(r, g, b)
            
            # Tính tỷ lệ
            percentage = count / len(pixels) * 100
            
            # Xác định tên màu
            color_name = get_color_name(r, g, b)
            
            dominant_colors.append({
                'hex': hex_color,
                'name': color_name,
                'percentage': round(percentage, 2)
            })
        
        return dominant_colors
    
    except Exception as e:
        print(f"Error analyzing image colors: {e}")
        return []

def get_color_name(r, g, b):
    """Xác định tên màu từ giá trị RGB"""
    # Danh sách màu cơ bản
    colors = {
        'red': (255, 0, 0),
        'green': (0, 255, 0),
        'blue': (0, 0, 255),
        'yellow': (255, 255, 0),
        'cyan': (0, 255, 255),
        'magenta': (255, 0, 255),
        'black': (0, 0, 0),
        'white': (255, 255, 255),
        'orange': (255, 165, 0),
        'purple': (128, 0, 128),
        'pink': (255, 192, 203),
        'brown': (165, 42, 42),
        'gray': (128, 128, 128)
    }
    
    # Tính khoảng cách Euclidean đến mỗi màu cơ bản
    min_distance = float('inf')
    nearest_color = 'unknown'
    
    for name, color in colors.items():
        distance = ((r - color[0])**2 + (g - color[1])**2 + (b - color[2])**2) ** 0.5
        if distance < min_distance:
            min_distance = distance
            nearest_color = name
    
    return nearest_color

def analyze_ad_content(ad):
    """Phân tích nội dung quảng cáo"""
    try:
        analysis = {}
        
        # Phân tích màu sắc từ thumbnail
        if 'thumbnail_url' in ad and ad['thumbnail_url']:
            dominant_colors = get_dominant_colors(ad['thumbnail_url'])
            analysis['dominant_colors'] = dominant_colors
        
        # Phân tích tiêu đề
        if 'title' in ad:
            title = ad['title'].lower()
            
            # Xác định call-to-action
            cta_keywords = ['download', 'play', 'install', 'get', 'join', 'try']
            cta_found = [keyword for keyword in cta_keywords if keyword in title]
            
            if cta_found:
                analysis['cta_type'] = cta_found[0]
            else:
                analysis['cta_type'] = 'unknown'
            
            # Xác định tính chất quảng cáo
            if any(word in title for word in ['free', 'gratis']):
                analysis['mentions_free'] = True
            
            if any(word in title for word in ['new', 'updated']):
                analysis['mentions_new'] = True
            
            if any(word in title for word in ['best', 'top', 'amazing', 'awesome']):
                analysis['uses_superlatives'] = True
        
        # Dự đoán đối tượng quảng cáo dựa trên tên game
        if 'game' in ad:
            game_name = ad['game'].lower()
            
            if any(word in game_name for word in ['clash', 'battle', 'war', 'fight']):
                analysis['likely_audience'] = 'competitive gamers'
            elif any(word in game_name for word in ['puzzle', 'match', 'crush']):
                analysis['likely_audience'] = 'casual gamers'
            elif any(word in game_name for word in ['farm', 'city', 'town', 'scape']):
                analysis['likely_audience'] = 'simulation fans'
            else:
                analysis['likely_audience'] = 'general gamers'
        
        return analysis
    
    except Exception as e:
        print(f"Error analyzing ad content: {e}")
        return {}

def analyze_ads():
    """Phân tích tất cả quảng cáo"""
    # Tạo thư mục để lưu kết quả phân tích
    os.makedirs('data/analysis', exist_ok=True)
    
    # Đọc tất cả quảng cáo
    try:
        with open('data/all_ads.json', 'r', encoding='utf-8') as f:
            all_ads = json.load(f)
    except:
        print("No ads found to analyze")
        return []
    
    # Phân tích từng quảng cáo
    for ad in all_ads:
        if not ad.get('analyzed', False):
            print(f"Analyzing ad: {ad.get('title', 'Unknown')}")
            
            # Phân tích nội dung
            analysis = analyze_ad_content(ad)
            
            # Cập nhật trạng thái phân tích
            ad['analyzed'] = True
            ad['analysis'] = analysis
            ad['analysis_date'] = datetime.now().strftime('%Y-%m-%d')
            
            # Đợi để tránh quá tải
            time.sleep(random.uniform(0.5, 1.5))
    
    # Lưu kết quả
    with open('data/all_ads.json', 'w', encoding='utf-8') as f:
        json.dump(all_ads, f, ensure_ascii=False, indent=2)
    
    # Tạo file phân tích tổng hợp
    generate_trend_analysis(all_ads)
    
    return all_ads

def generate_trend_analysis(all_ads):
    """Tạo phân tích xu hướng từ tất cả quảng cáo"""
    trend_analysis = {
        'color_trends': {},
        'cta_trends': {},
        'audience_trends': {},
        'update_date': datetime.now().strftime('%Y-%m-%d')
    }
    
    # Phân tích xu hướng màu sắc
    all_colors = {}
    for ad in all_ads:
        if 'analysis' in ad and 'dominant_colors' in ad['analysis']:
            for color in ad['analysis']['dominant_colors']:
                color_name = color['name']
                if color_name in all_colors:
                    all_colors[color_name] += 1
                else:
                    all_colors[color_name] = 1
    
    # Sắp xếp và lấy top màu
    sorted_colors = sorted(all_colors.items(), key=lambda x: x[1], reverse=True)
    trend_analysis['color_trends'] = [{'name': c[0], 'count': c[1]} for c in sorted_colors[:5]]
    
    # Phân tích xu hướng CTA
    cta_types = {}
    for ad in all_ads:
        if 'analysis' in ad and 'cta_type' in ad['analysis']:
            cta_type = ad['analysis']['cta_type']
            if cta_type in cta_types:
                cta_types[cta_type] += 1
            else:
                cta_types[cta_type] = 1
    
    # Sắp xếp và lấy top CTA
    sorted_ctas = sorted(cta_types.items(), key=lambda x: x[1], reverse=True)
    trend_analysis['cta_trends'] = [{'type': c[0], 'count': c[1]} for c in sorted_ctas]
    
    # Phân tích xu hướng đối tượng
    audiences = {}
    for ad in all_ads:
        if 'analysis' in ad and 'likely_audience' in ad['analysis']:
            audience = ad['analysis']['likely_audience']
            if audience in audiences:
                audiences[audience] += 1
            else:
                audiences[audience] = 1
    
    # Sắp xếp và lấy top đối tượng
    sorted_audiences = sorted(audiences.items(), key=lambda x: x[1], reverse=True)
    trend_analysis['audience_trends'] = [{'audience': a[0], 'count': a[1]} for a in sorted_audiences]
    
    # Lưu phân tích xu hướng
    with open('data/trend_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(trend_analysis, f, ensure_ascii=False, indent=2)
    
    return trend_analysis

if __name__ == "__main__":
    print("Starting ad analysis...")
    analyzed_ads = analyze_ads()
    print(f"Analyzed {len(analyzed_ads)} ads")
    print("Analysis completed!")
