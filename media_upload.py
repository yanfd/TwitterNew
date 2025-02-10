import tweepy
from datetime import datetime
from pyfiglet import Figlet 
import os
from prompt_toolkit import prompt
from prompt_toolkit import PromptSession

# 新增v1客户端认证（用于媒体上传）
def get_v1_client():
    auth = tweepy.OAuth1UserHandler(
        consumer_key=os.environ.get("API_KEY"),
        consumer_secret=os.environ.get("API_SECRET"),
        access_token=os.environ.get("ACCESS_TOKEN"),
        access_token_secret=os.environ.get("ACCESS_TOKEN_SECRET")
    )
    return tweepy.API(auth)

def send_tweet_v2(text, media_paths=None):
    # 初始化两个客户端
    client_v2 = tweepy.Client(
        consumer_key=os.environ.get("API_KEY"),
        consumer_secret=os.environ.get("API_SECRET"),
        access_token=os.environ.get("ACCESS_TOKEN"),
        access_token_secret=os.environ.get("ACCESS_TOKEN_SECRET")
    )
    
    api_v1 = get_v1_client()
    media_ids = []

    # 上传媒体文件
    if media_paths:
        for path in media_paths:
            if not os.path.exists(path):
                print(f"⚠️ File not found: {path}")
                continue
            try:
                media = api_v1.media_upload(filename=path)
                media_ids.append(media.media_id)
                print(f"🖼️ Media uploaded: {path}")
            except Exception as e:
                print(f"❌ Failed to upload {path}: {e}")

    try:
        response = client_v2.create_tweet(
            text=text,
            media_ids=media_ids if media_paths else None
        )
        print(f"✅ PUBLISHED. ID: {response.data['id']}")
    except tweepy.TweepyException as e:
        print(f"❌ FAILED: {e}")

def show_banner():
    # 动态问候语
    hour = datetime.now().hour
    if 5 <= hour < 12:
        greeting = "🌧️ Mornin. Anything wanna share? :)"
    elif 12 <= hour < 18:
        greeting = "🌆 Good afternoon, anything wanna share? :)"
    else:
        greeting = "🌌 late at night. anything wanna share? :)"

    # 生成 ASCII 艺术字
    f = Figlet(font='slant')
    print("\033[36m" + f.renderText('NEW TWEETS') + "\033[0m")
    print(f"{greeting} \n timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)

# 修改后的主程序
if __name__ == "__main__":
    show_banner()
    
    try:
        session = PromptSession()
        # 输入文本
        tweet_text = session.prompt("Tweet text (Esc+Enter to finish): \n", multiline=True)
        
        # 输入图片路径
        media_input = session.prompt(
            "📷 Attach images (space-separated paths, empty to skip):\n "
        ).strip()

        media_paths = media_input.split() if media_input else None
        
        if not tweet_text.strip() and not media_paths:
            print("\033[33mEmpty input, cancelled.\033[0m")
        else:
            send_tweet_v2(tweet_text, media_paths)
            
    except KeyboardInterrupt:
        print("\n\033[33mCANCELLED. SEE YA.\033[0m")