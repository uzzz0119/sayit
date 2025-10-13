"""
QQ音乐工具
处理QQ音乐链接、歌曲ID提取和歌词获取
"""
import re
import requests


def extract_qq_music_song_id(url):
    """
    从QQ音乐URL中提取歌曲ID
    
    支持的URL格式：
    - https://y.qq.com/n/ryqq/songDetail/001234567
    - https://i.y.qq.com/v8/playsong.html?songmid=001234567
    - https://c6.y.qq.com/base/fcgi-bin/u?__=xxxxx (短链接)
    
    Args:
        url (str): QQ音乐链接
    
    Returns:
        str: 歌曲ID (songmid)，如果提取失败返回 None
    """
    try:
        # 如果是短链接，先跟随重定向获取真实URL
        if 'c6.y.qq.com' in url or 'c.y.qq.com' in url:
            print(f"检测到QQ音乐短链接，正在解析真实链接...")
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                response = requests.get(url, headers=headers, allow_redirects=True, timeout=10)
                real_url = response.url
                print(f"真实链接: {real_url}")
                url = real_url
            except Exception as e:
                print(f"解析短链接时出错: {e}")
                return None
        
        # 尝试多种匹配模式
        patterns = [
            r'songDetail/(\w+)',
            r'songmid=(\w+)',
            r'/song/(\w+)',
            r'id=(\w+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                song_id = match.group(1)
                print(f"成功提取歌曲ID: {song_id}")
                return song_id
        
        print("错误: 无法从URL中提取歌曲ID")
        return None
    except Exception as e:
        print(f"提取歌曲ID时出错: {e}")
        return None


def get_qq_music_lyrics(song_id):
    """
    通过歌曲ID获取QQ音乐歌词
    
    Args:
        song_id (str): 歌曲ID
    
    Returns:
        tuple: (歌曲名, 歌手名, 歌词文本)，失败返回 (None, None, None)
    """
    try:
        headers = {
            'Referer': 'https://y.qq.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        song_name = "未知歌曲"
        artist_name = "未知歌手"
        lyrics_text = ""
        
        # 获取歌曲信息
        info_url = f"https://u.y.qq.com/cgi-bin/musicu.fcg?format=json&data=%7B%22comm%22%3A%7B%22ct%22%3A24%2C%22cv%22%3A0%7D%2C%22songinfo%22%3A%7B%22method%22%3A%22get_song_detail_yqq%22%2C%22param%22%3A%7B%22song_type%22%3A0%2C%22song_mid%22%3A%22{song_id}%22%7D%2C%22module%22%3A%22music.pf_song_detail_svr%22%7D%7D"
        
        try:
            info_response = requests.get(info_url, headers=headers, timeout=10)
            if info_response.status_code == 200:
                info_data = info_response.json()
                if 'songinfo' in info_data and 'data' in info_data['songinfo']:
                    track_info = info_data['songinfo']['data'].get('track_info', {})
                    song_name = track_info.get('name', song_name)
                    singers = track_info.get('singer', [])
                    if singers:
                        artist_name = ', '.join([s.get('name', '') for s in singers])
                    print(f"获取歌曲信息成功: {song_name} - {artist_name}")
        except Exception as e:
            print(f"获取歌曲信息时出错: {e}")
        
        # 获取歌词
        apis = [
            f"https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric_new.fcg?songmid={song_id}&format=json&nobase64=1",
            f"https://u.y.qq.com/cgi-bin/musicu.fcg?format=json&data=%7B%22comm%22%3A%7B%22ct%22%3A23%2C%22cv%22%3A0%7D%2C%22music%22%3A%7B%22module%22%3A%22music.musichallSong.PlayLyricInfo%22%2C%22method%22%3A%22GetPlayLyricInfo%22%2C%22param%22%3A%7B%22songID%22%3A0%2C%22songMID%22%3A%22{song_id}%22%7D%7D%7D"
        ]
        
        for api_url in apis:
            try:
                response = requests.get(api_url, headers=headers, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    
                    if 'lyric' in data:
                        lyrics_text = data.get('lyric', '')
                        if lyrics_text:
                            break
                    
                    if 'music' in data and 'data' in data['music']:
                        lyrics_text = data['music']['data'].get('lyric', '')
                        if lyrics_text:
                            break
            except:
                continue
        
        if not lyrics_text:
            lyrics_text = "[该歌曲暂无歌词]"
        
        # 解析LRC格式歌词
        parsed_lyrics = parse_lrc_lyrics(lyrics_text)
        
        return song_name, artist_name, parsed_lyrics
        
    except Exception as e:
        print(f"获取QQ音乐歌词时出错: {e}")
        return None, None, None


def parse_lrc_lyrics(lrc_text):
    """
    解析LRC格式的歌词，去除时间标记
    
    Args:
        lrc_text (str): LRC格式的歌词文本
    
    Returns:
        str: 纯文本歌词
    """
    try:
        if not lrc_text or lrc_text.strip() == "":
            return "[暂无歌词]"
        
        lines = lrc_text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # 去除所有时间标记
            cleaned_line = re.sub(r'\[\d{2}:\d{2}\.\d{2,3}\]', '', line)
            # 去除其他元数据标记
            cleaned_line = re.sub(r'\[(?:ar|ti|al|by|offset):[^\]]*\]', '', cleaned_line)
            
            cleaned_line = cleaned_line.strip()
            if cleaned_line:
                cleaned_lines.append(cleaned_line)
        
        result = '\n'.join(cleaned_lines)
        
        if not result.strip():
            return "[该歌曲为纯音乐，无歌词]"
        
        return result
        
    except Exception as e:
        print(f"解析歌词时出错: {e}")
        return lrc_text

