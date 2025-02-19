import sys
import os
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QFileDialog, QHBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QTextCursor
import tweepy

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

class TwitterWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.media_paths = []
        self.init_ui()

    def init_ui(self):
        # 窗口设置
        self.setWindowTitle("TwitterNew")
        self.setGeometry(100, 100, 400, 480)
        self.setWindowFlags(Qt.FramelessWindowHint)  # 无边框窗口
        self.setAttribute(Qt.WA_TranslucentBackground)  # 透明背景

        # 主布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)

        # 问候语
        greetings = show_banner()
        self.label1 = QLabel(greetings)
        self.label1.setFont(QFont("Monospace", 18, QFont.Bold))
        self.label1.setStyleSheet("color: white;")
        layout.addWidget(self.label1)

        # 文本输入框
        self.text_box = QTextEdit()
        self.text_box.setFont(QFont("Microsoft YaHei", 25, QFont.Bold))
        self.text_box.setStyleSheet("""
            background-color: transparent;
            border: 2px solid white;
            border-radius: 8px;
            color: white;
            padding: 10px;
        """)
        self.text_box.setAcceptRichText(False)  # 禁用富文本粘贴
        layout.addWidget(self.text_box)

        # 图片插入框架
        self.image_frame = QWidget()
        image_layout = QHBoxLayout(self.image_frame)
        image_layout.setContentsMargins(0, 0, 0, 0)

        # 图片标签
        self.file_label = QLabel("ANY PICS?")
        self.file_label.setStyleSheet("color: white;")
        image_layout.addWidget(self.file_label)

        # 图片插入按钮
        self.insert_image_button = QPushButton("INSERT")
        self.insert_image_button.setStyleSheet("""
            QPushButton {
                background-color: #FBD35A;
                color: black;
                border: 1px solid white;
                border-radius: 8px;  # 圆角半径
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FFA500;  # 悬停颜色
            }
        """)
        self.insert_image_button.clicked.connect(self.file_uploading)
        image_layout.addWidget(self.insert_image_button)

        layout.addWidget(self.image_frame)

        # 发送按钮
        self.send_button = QPushButton("SEND")
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #FBD35A;
                color: black;
                border: 1px solid white;
                border-radius: 8px;  # 圆角半径
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FFA500;  # 悬停颜色
            }
        """)
        self.send_button.clicked.connect(self.sending)
        layout.addWidget(self.send_button)
        # 状态标签
        self.status_label = QLabel("READY")
        self.status_label.setStyleSheet("""
            color: white;
            font-size: 10px;
            font-weight: bold;
            text-align: center;
        """)
        layout.addWidget(self.status_label)

    def file_uploading(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select the pic you wanna share:",
            os.path.expanduser("~/Users/yanfengwu/Downloads"),
            "Images (*.jpg *.png *.jpeg)"
        )
        if file_path:
            self.media_paths = [file_path]
            if len(file_path) > 10:
                file_path = "..." + file_path[-10:]
            self.file_label.setText(f"{file_path} selected.")
            self.status_label.setText("Image selected.")

    def sending(self):
        tweet_text = self.text_box.toPlainText()
        try:
            if not tweet_text.strip() and not self.media_paths:
                print("\033[33mEmpty input, cancelled.\033[0m")
                self.status_label.setText("Cancelled.")
            else:
                send_tweet_v2(tweet_text, self.media_paths)
                self.status_label.setText("Published.")
        except Exception as e:
            print(e)
            self.status_label.setText("Failed.")

    def mousePressEvent(self, event):
        # 实现窗口拖动
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.globalPos()

    def mouseMoveEvent(self, event):
        # 实现窗口拖动
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.drag_start_position)
            self.drag_start_position = event.globalPos()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TwitterWindow()
    window.show()
    sys.exit(app.exec_())