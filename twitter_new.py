import tweepy
from datetime import datetime
from pyfiglet import Figlet 
import os
from prompt_toolkit import prompt

"""
将以下内容添加到 .bashrc 或 .zshrc 文件中,取决于你用的shell是哪种类型
adding following stuff to .bashrc or .zshrc file, depending on which shell you are using

export 'BEARER_TOKEN'='$YOUR_BEARER'
export 'API_KEY'='$your_api_key'
export 'API_SECRET'='$your_api_secret'
export 'ACCESS_TOKEN'='$your_access_token'
export 'ACCESS_TOKEN_SECRET'='$your_access_token_secret'

source ~/.bashrc 
加载配置文件
"""

def send_tweet_v2(text):
    
    # 创建 v2 客户端
    client = tweepy.Client(
       consumer_key=os.environ.get("API_KEY"),
        consumer_secret=os.environ.get("API_SECRET"),
        access_token=os.environ.get("ACCESS_TOKEN"),
        access_token_secret=os.environ.get("ACCESS_TOKEN_SECRET")
    )

    try:
        # 调用 v2 的创建推文接口
        response = client.create_tweet(text=text)
        print(f"PUBLISHED. ID: {response.data['id']}")
    except tweepy.TweepyException as e:
        print(f"FAILED: {e}")

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

if __name__ == "__main__":
    show_banner()  # 显示终端横幅
    
    try:
        
        tweet_text = prompt("Start typing your tweet: \n ")
        if len(tweet_text.strip()) == 0:
            print("\033[33m empty input, cancelled.\033[0m")
        else:
            final_text = f"{tweet_text}"
            send_tweet_v2(final_text)
    except KeyboardInterrupt:
        print("\n\033[33mCANCELLED. SEE YA.\033[0m")