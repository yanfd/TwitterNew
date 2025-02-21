# Twitter的小型Cli应用
english version [ENG](https://github.com/yanfd/TwitterNew/blob/main/README_EN.md) 

[TOC]



## Update Available V1.1.0 🚀

使用Twitter的X API v2。

### version

- main branch
  - twitter_new.py 以Cli方式运行
- feature
  - GUI_CTkinter.py 以桌面程式运行

### 功能

- [x] greetings
- [x] 推文发送
- [x] 图像插入
- [x] GUI
- [x] mockup背景

![](https://p.ipic.vip/eo9v36.png)

![](https://p.ipic.vip/5t3qjo.png)

---

Feb22 update(CTkinter版本)

import PIL实现mockup

Feb20 updated.  

import PyQT

Feb17更新，加装GUI玩玩，未merge于main branch. 

import CTkinter

Feb 10更新，增加图像插入功能:)

已满足本人需求，有其他问题欢迎提交issue

---



其他如查看回复/转发等操作较为繁琐，效率不如网站。

方便的话可以集成Alfred的workflow



### 使用

#### 下载项目

```
git clone https://github.com/yanfd/TwitterNew.git
```

cd切换到对应目录



#### 安装依赖库

安装前建议启动虚拟环境。

```shell
source twienv/bin/activate
```

- tweepy：X的官方开发库
- pyfiglet：用于banner生成
- prompt_toolkit：文字编辑区域，比input好使

```shell
pip3 install tweepy pyfiglet prompt_toolkit
```



#### 获取自己的推特密钥

登陆[X Developer Portal](https://developer.twitter.com/en/portal/projects/) ，注册/登陆/创建应用

生成 API_KEY，API_SECRET，ACCESS_TOKEN，ACCESS_TOKEN_SECRET

在setting中将

![](https://p.ipic.vip/ld3oje.png)

设置为**可读并可写**

![](https://p.ipic.vip/cft2y9.png)

下面三个required随便填写。



程序为安全需要把推特密钥放置到了环境变量里。

获取完的keys，添加至.bashrc或.zshrc环境配置文件中(取决于你用的shell是哪种类型)

```
export 'BEARER_TOKEN'='$YOUR_BEARER'
export 'API_KEY'='$your_api_key'
export 'API_SECRET'='$your_api_secret'
export 'ACCESS_TOKEN'='$your_access_token'
export 'ACCESS_TOKEN_SECRET'='$your_access_token_secret'
```

source ~/.bashrc 

⬆️加载配置文件



**运行**

```
python3 twitter_new.py
```

- 输入文本后，ESC+Enter下一步

- 插入图片，需绝对路径（可选）

- 继续ESC+Enter结束

  

![](https://p.ipic.vip/a0r0x6.png)

![](https://p.ipic.vip/t17eoa.png)

deactivate退出虚拟环境



### 可能出现的问题

- apikeys在生成时一般只会出现一次。请自己备份好
- 提示权限不足只能读取有限endpoint，说明没有设置为**可读并可写**
- 依赖库建议安装在虚拟环境中。如果是全剧环境可能会报危
- 其他请进行issues提交
