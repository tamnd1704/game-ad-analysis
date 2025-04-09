import json
import os
from datetime import datetime
import random

def get_dominant_colors(image_url, num_colors=3):
    """Giả lập phân tích màu sắc chủ đạo từ hình ảnh"""
    # Trong thực tế cần phân tích thật, nhưng ở đây chúng ta giả lập
    colors = [
        {"name": "red", "hex": "#FF0000"},
        {"name": "blue", "hex": "#0000FF"},
        {"name": "green", "hex": "#00FF00"},
        {"name": "yellow", "hex": "#FFFF00"},
        {"name": "purple", "hex": "#800080"},
        {"name": "orange", "hex": "#FFA500"},
        {"name": "pink", "hex": "#FFC0CB"},
        {"name": "black", "hex": "#000000"},
        {"name": "white", "hex": "#FFFFFF"},
        {"name": "gray", "hex": "#808080"}
    ]
    
    # Chọn ngẫu nhiên các màu
    selected_colors = random.sample(colors, min(num_colors, len(colors)))
    
    # Gán tỷ lệ phần trăm ngẫu nhiên
    total_percentage = 100
    result = []
    
    for i, color in enumerate(selected_colors):
        if i == len(selected_colors) - 1:
            percentage = total_percentage
        else:
            percentage = random.randint(10, total_percentage - 10)
            total_percentage -= percentage
        
        result.append({
            "hex": color["hex"],
            "name": color["name"],
            "percentage": percentage
        })
    
    return result

def analyze_ad_content(ad):
    """Phân tích nội dung quảng cáo (giả lập)"""
    analysis = {}
    
    # Phân tích màu sắc từ thumbnail
    if 'thumbnail_url' in ad and ad['thumbnail_url']:
        dominant_colors = get_dominant_colors(ad['thumbnail_url'])
        analysis['dominant_colors'] = dominant_colors
    
    # Phân tích ngẫu nhiên CTA
    cta_options = ["play", "download", "get", "install", "join", "try"]
    analysis['cta_type'] = random.choice(cta_options)
    
    # Phân tích ngẫu nhiên đối tượng mục tiêu
    audience_options = ["casual gamers", "competitive gamers", "simulation fans", "general gamers"]
    analysis['likely_audience'] = random.choice(audience_options)
    
    # Phân tích ngẫu nhiên các tính năng khác
    analysis['uses_superlatives'] = random.choice([True, False])
    analysis['mentions_free'] = random.choice([True, False])
    analysis['mentions_new'] = random.choice([True, False])
    
    return analysis

def analyze_ads():
    """Phân tích tất cả quảng cáo"""
    try:
        # Đọc tất cả quảng cáo
        with open('data/all_ads.json', 'r', encoding='utf-8') as f:
            all_ads = json.load(f)
    except Exception as e:
        print(f"Error loading ads: {e}")
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
