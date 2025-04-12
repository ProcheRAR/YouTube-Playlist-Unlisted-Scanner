# YouTube Unlisted Video Detector

A lightweight Python utility for content creators and moderators to audit YouTube playlist privacy settings.

## Features
- 🎯 Batch detection of unlisted/restricted videos
- 🔗 Automatic URL generation for hidden content
- 📄 Pagination support for large playlists
- 🛠️ Simple configuration with YouTube Data API

## Usage
1. Enable [YouTube Data API](https://console.cloud.google.com/apis/library/youtube.googleapis.com)  
2. Install dependencies: `pip install google-api-python-client`  
3. Replace `YOUR_API_KEY` in script  
4. Run: `python playlist_scanner.py`  

## Use Cases
- Audit collaborative playlists for accidental leaks  
- Clean up legacy content with mixed privacy settings  
- Monitor channel content strategy compliance  
