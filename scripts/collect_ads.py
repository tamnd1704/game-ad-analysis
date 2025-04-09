import requests
from bs4 import BeautifulSoup
import json
import os
import time
import random
from datetime import datetime

# Tạo thư mục để lưu dữ liệu nếu chưa tồn tại
os.makedirs('data', exist_ok=True)

# Danh sách game cần theo dõi
GAMES = [
    "Candy Crush Saga",
    "Coin Master",
    "Gardenscapes",
    "Homescapes",
    "PUBG Mobile",
    "Genshin Impact",
    "Roblox",
    "Clash of Clans",
    "Call of Duty Mobile",
    "Mobile Legends"
]

def fetch_youtube_ads():
    """Thu thập quảng cáo từ YouTube không cần API key"""
    all_ads = []
    
    for game in GAMES:
        # Tạo query an toàn cho URL
        query = "+".join(game.split()) + "+mobile+game+ad"
        
        # Tìm kiếm trên YouTube
        url = f"https://www.youtube.com/results?search_query={query}&sp=EgQQARgB"  # Filter for short videos
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        
        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Trích xuất script chứa dữ liệu video
            scripts = soup.find_all('script')
            for script in scripts:
                if 'var ytInitialData = ' in str(script):
                    data_text = str(script).split('var ytInitialData = ')[1].split(';</script>')[0]
                    data = json.loads(data_text)
                    
                    # Phân tích các kết quả video
                    video_data = data.get('contents', {}).get('twoColumnSearchResultsRenderer', {}).get('primaryContents', {}).get('sectionListRenderer', {}).get('contents', [{}])[0].get('itemSectionRenderer', {}).get('contents', [])
                    
                    for item in video_data:
                        if 'videoRenderer' in item:
                            video = item['videoRenderer']
                            video_id = video.get('videoId')
                            title = video.get('title', {}).get('runs', [{}])[0].get('text', '')
                            
                            if video_id and title:
                                thumbnail_url = f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"
                                video_url = f"https://www.youtube.com/watch?v={video_id}"
                                
                                # Thêm vào danh sách quảng cáo
                                all_ads.append({
                                    'id': video_id,
                                    'title': title,
                                    'game': game,
                                    'source': 'youtube',
                                    'thumbnail_url': thumbnail_url,
                                    'video_url': video_url,
                                    'found_date': datetime.now().strftime('%Y-%m-%d'),
                                    'analyzed': False
                                })
            
            # Đợi để tránh bị chặn
            time.sleep(random.uniform(2, 5))
            
        except Exception as e:
            print(f"Error fetching YouTube ads for {game}: {e}")
    
    # Lưu dữ liệu
    with open('data/youtube_ads.json', 'w', encoding='utf-8') as f:
        json.dump(all_ads, f, ensure_ascii=False, indent=2)
    
    return all_ads

def fetch_facebook_ads():
    """Thu thập quảng cáo từ Facebook Ad Library không cần API"""
    all_ads = []
    
    for game in GAMES:
        # Tạo query an toàn cho URL
        query = "+".join(game.split())
        
        # Truy cập Facebook Ad Library
        url = f"https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=US&q={query}&sort_data[direction]=desc&sort_data[mode]=relevancy_monthly_grouped"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        
        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find ad containers
            ad_containers = soup.find_all('div', {'class': '_7jyg _7jyi'})
            
            for container in ad_containers:
                # Extract ad ID
                ad_id = container.get('id', '')
                
                # Extract ad title/text
                ad_text_element = container.find('div', {'class': '_7jyr'})
                ad_text = ad_text_element.text if ad_text_element else ''
                
                # Extract image URL if available
                img_element = container.find('img')
                img_url = img_element.get('src') if img_element else ''
                
                if ad_id and ad_text:
                    all_ads.append({
                        'id': ad_id,
                        'title': ad_text[:100],  # Limit title length
                        'game': game,
                        'source': 'facebook',
                        'thumbnail_url': img_url,
                        'ad_url': url + f"#{ad_id}",
                        'found_date': datetime.now().strftime('%Y-%m-%d'),
                        'analyzed': False
                    })
            
            # Đợi để tránh bị chặn
            time.sleep(random.uniform(2, 5))
            
        except Exception as e:
            print(f"Error fetching Facebook ads for {game}: {e}")
    
    # Lưu dữ liệu
    with open('data/facebook_ads.json', 'w', encoding='utf-8') as f:
        json.dump(all_ads, f, ensure_ascii=False, indent=2)
    
    return all_ads

def fetch_top_games():
    """Thu thập thông tin top games từ các nguồn miễn phí"""
    top_games = []
    
    # Tạo URL để lấy top games từ Google Play (phần hiển thị công khai)
    url = "https://play.google.com/store/apps/category/GAME/collection/topselling_free"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find game containers
        game_containers = soup.find_all('div', {'class': 'ZmHEEd'})
        
        rank = 1
        for container in game_containers:
            # Extract game title
            title_element = container.find('div', {'class': 'WsMG1c'})
            title = title_element.text if title_element else ''
            
            # Extract developer
            dev_element = container.find('div', {'class': 'KoLSrc'})
            developer = dev_element.text if dev_element else ''
            
            # Extract icon URL
            icon_element = container.find('img', {'class': 'T75of'})
            icon_url = icon_element.get('src') if icon_element else ''
            
            # Extract app URL
            link_element = container.find('a', {'class': 'JC71ub'})
            app_url = "https://play.google.com" + link_element.get('href') if link_element else ''
            
            if title:
                top_games.append({
                    'rank': rank,
                    'title': title,
                    'developer': developer,
                    'icon_url': icon_url,
                    'app_url': app_url,
                    'store': 'google_play',
                    'update_date': datetime.now().strftime('%Y-%m-%d')
                })
                rank += 1
        
    except Exception as e:
        print(f"Error fetching top games: {e}")
    
    # Lưu dữ liệu
    with open('data/top_games.json', 'w', encoding='utf-8') as f:
        json.dump(top_games, f, ensure_ascii=False, indent=2)
    
    return top_games

def merge_all_ads():
    """Kết hợp tất cả quảng cáo vào một file JSON"""
    all_ads = []
    
    # Đọc YouTube ads
    try:
        with open('data/youtube_ads.json', 'r', encoding='utf-8') as f:
            youtube_ads = json.load(f)
            all_ads.extend(youtube_ads)
    except:
        pass
    
    # Đọc Facebook ads
    try:
        with open('data/facebook_ads.json', 'r', encoding='utf-8') as f:
            facebook_ads = json.load(f)
            all_ads.extend(facebook_ads)
    except:
        pass
    
    # Loại bỏ trùng lặp dựa vào ID
    unique_ads = {}
    for ad in all_ads:
        unique_ads[ad['id']] = ad
    
    all_ads = list(unique_ads.values())
    
    # Lưu tất cả quảng cáo
    with open('data/all_ads.json', 'w', encoding='utf-8') as f:
        json.dump(all_ads, f, ensure_ascii=False, indent=2)
    
    return all_ads

if __name__ == "__main__":
    print("Starting to collect YouTube ads...")
    youtube_ads = fetch_youtube_ads()
    print(f"Collected {len(youtube_ads)} YouTube ads")
    
    print("Starting to collect Facebook ads...")
    facebook_ads = fetch_facebook_ads()
    print(f"Collected {len(facebook_ads)} Facebook ads")
    
    print("Starting to collect top games...")
    top_games = fetch_top_games()
    print(f"Collected {len(top_games)} top games")
    
    print("Merging all ads...")
    all_ads = merge_all_ads()
    print(f"Total unique ads: {len(all_ads)}")
    
    print("Ad collection completed!")
