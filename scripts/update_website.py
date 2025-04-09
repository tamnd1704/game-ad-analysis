import json
import os
import shutil
from datetime import datetime

def update_website_data():
    """Cập nhật dữ liệu cho website"""
    # Tạo thư mục cho website nếu chưa tồn tại
    os.makedirs('docs', exist_ok=True)
    os.makedirs('docs/data', exist_ok=True)
    os.makedirs('docs/images', exist_ok=True)
    
    # Sao chép tất cả file JSON sang thư mục docs/data
    data_files = ['all_ads.json', 'youtube_ads.json', 'facebook_ads.json', 'top_games.json', 'trend_analysis.json']
    
    for file in data_files:
        src_path = os.path.join('data', file)
        dst_path = os.path.join('docs/data', file)
        
        if os.path.exists(src_path):
            shutil.copy2(src_path, dst_path)
    
    # Tạo file cập nhật timestamp
    update_info = {
        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'status': 'success'
    }
    
    with open('docs/data/update_info.json', 'w', encoding='utf-8') as f:
        json.dump(update_info, f, ensure_ascii=False, indent=2)
    
    # Tạo các trang HTML nếu chưa tồn tại
    if not os.path.exists('docs/index.html'):
        create_index_html()
    
    if not os.path.exists('docs/ad-library.html'):
        create_ad_library_html()
    
    if not os.path.exists('docs/trends.html'):
        create_trends_html()
    
    if not os.path.exists('docs/top-games.html'):
        create_top_games_html()
    
    print("Website data updated successfully!")

def create_index_html():
    """Tạo trang chủ"""
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Game Ad Analyzer</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f8f9fa;
        }
        .navbar {
            background-color: #6610f2 !important;
        }
        .hero-section {
            background: linear-gradient(135deg, #6610f2 0%, #6f42c1 100%);
            color: white;
            padding: 60px 0;
            margin-bottom: 30px;
        }
        .card {
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s;
            margin-bottom: an:w-20px;
        }
        .card:hover {
            transform: translateY(-5px);
        }
        .card-header {
            background-color: #6f42c1;
            color: white;
            border-radius: 10px 10px 0 0 !important;
        }
        .stat-number {
            font-size: 2rem;
            font-weight: bold;
            color: #6610f2;
        }
        .update-info {
            font-size: 0.9rem;
            color: #6c757d;
        }
        .icon-large {
            font-size: 2.5rem;
            color: #6610f2;
            margin-bottom: 15px;
        }
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="index.html">
                <i class="fas fa-chart-line"></i> Game Ad Analyzer
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link active" href="index.html">Dashboard</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="ad-library.html">Ad Library</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="trends.html">Trends</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="top-games.html">Top Games</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section class="hero-section">
        <div class="container text-center">
            <h1 class="display-4">Game Ad Analyzer</h1>
            <p class="lead">AI-powered analysis of mobile game advertisements</p>
            <p class="update-info">Last Update: <span id="lastUpdate">Loading...</span></p>
        </div>
    </section>

    <!-- Dashboard Section -->
    <section class="container mb-5">
        <div class="row">
            <!-- Stats Cards -->
            <div class="
