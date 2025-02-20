import tweepy
from datetime import datetime
from pyfiglet import Figlet 
import os
from prompt_toolkit import prompt
from prompt_toolkit import PromptSession
import customtkinter as ctk
from tkinter import filedialog
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

    current_time = datetime.now().strftime("%H:%M")
    hour = datetime.now().hour
    if 5 <= hour < 12:
        greeting = f"{current_time} 🌧️ ›Morning ideas?"
    elif 12 <= hour < 18:
        greeting = f"{current_time} 🌆 ›Share?"
    else:
        greeting = f"{current_time} 🌌 ›Midnight thoughts?"
    return greeting
    # # 生成 ASCII 艺术字
    # f = Figlet(font='slant')
    # print("\033[36m" + f.renderText('NEW TWEETS') + "\033[0m")
    # print(f"{greeting} \n timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    # print("-" * 50)


#---------------------------------------
#GUI code
#---------------------------------------

class twitter_create(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.media_paths = []
        #window
        self.title("TwitterNew")
        self._set_window_geometry()
        self._set_appearance_mode("dark")
        #transparent all
        # self.overrideredirect(True)
        self.attributes('-alpha', 0.8)

        
        #main frame
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        

        #greetings
        greetings = show_banner()
        self.label1 = ctk.CTkLabel(
            self.main_frame, 
            text=f'{greetings}',
            font=("Monospace", 18, "bold"),
            text_color="white"
            ).pack(expand=False, fill="both", padx=20, pady=20)
        

        #text entry
        self.text_box = ctk.CTkTextbox(
            self.main_frame,
            # placeholder_text="Anything wanna share? :)",
            border_color="white",
            font=("Microsoft YaHei", 18, "bold"),
            border_width=2,
            fg_color="transparent",
            corner_radius=8
        )
        self.text_box.pack(expand=False, fill="both", padx=0, pady=5)  

        #image insert frame
        self.image_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.image_frame.pack(expand=False, fill="both", padx=0, pady=5)


        #image insert
        def file_uploading():
            
            file_paths = filedialog.askopenfilenames(
                title="select the pic you wanna share:",
                filetypes=[("Images", "*.jpg *.png *.jpeg")],
                initialdir=os.path.expanduser("~/Users/yanfengwu/Downloads")
            )
            if file_paths:
                self.media_paths = file_paths
                try:
                    file_label_update(f"{len(file_paths)} PICS SELECTED.")
                    status_label_update("Image selected.")
                except Exception as e:
                        print(e)
                        status_label_update("Failed.")

                
        def file_label_update(display_text):
            self.file_label.configure(text=f"{display_text}")

        self.file_label = ctk.CTkLabel(
            self.image_frame,
            text="ANY PICS?",
            text_color="white"
        )
        self.file_label.pack(expand=True, side = "left", pady=5)

        self.insert_image_button = ctk.CTkButton(
            self.image_frame, 
            corner_radius=32, 
            fg_color="black",
            hover_color="#666666",
            border_color="white",
            border_width=1,
            text="INSERT",
            command=file_uploading
            )
        self.insert_image_button.pack(expand=False, side="right",padx=5, pady=5)



        # self.insert_image_test = ctk.CTkCheckBox(self.main_frame, text="Insert Image",onvalue=True, offvalue=False)
        # self.insert_image_test.pack(expand=False, fill="both", padx=0, pady=5)
        

        #sending
        def sending():
            tweet_text = self.text_box.get("1.0", "end-1c")
            try:
                if not tweet_text.strip() and not self.media_paths:
                    print("\033[33mEmpty input, cancelled.\033[0m")
                else:
                    send_tweet_v2(tweet_text, self.media_paths)
                    status_label_update("Published.".upper())
                    
            except KeyboardInterrupt:
                print("\n\033[33mCANCELLED. SEE YA.\033[0m")
                status_label_update("Cancelled.")
            except Exception as e:
                print(e)
                status_label_update("Failed.")
        self.send_button = ctk.CTkButton(
            self.main_frame, 
            text="SEND", 
            corner_radius=32, 
            command=sending,
            fg_color="black",border_color="white",border_width=1,
            hover_color="#666666",
            font=("Microsoft YaHei", 16, "bold")
        )
        self.send_button.pack(expand=False, fill="both", padx=0, pady=5)
        


        #status
        def status_label_update(status):
            self.status_label.configure(text=f"{status}")
            
        self.status_label = ctk.CTkLabel(
        self.main_frame,
        text="READY",
        text_color="white",
        anchor="center",
        font=("Microsoft YaHei", 10, "bold"),
    )
        self.status_label.pack(expand=False, fill="both", padx=0, pady=10)



        
    def _set_window_geometry(self):
        """设置窗口位置和大小"""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 400
        window_height = 480
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 4  # 偏上方
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.minsize(300, 450)
        self.resizable(True, True)



if __name__ == "__main__":
    app = twitter_create()
    app.mainloop()
