# Twitter Mini CLI Application
中文版本 [CN](https://github.com/yanfd/TwitterNew/blob/main/README.md)

[TOC]



Using Twitter's X API v2.

Feb10 update, adding image insertion function:)
My needs have been met. If you have any other questions, please feel free to submit an issue

---

- [x] Greetings
- [x] Tweet Posting
- [x] Image Insertion

Other operations like viewing replies/retweets are cumbersome and less efficient than the website.

Here, an Alfred workflow is integrated to enable one-click posting, though the program itself still needs to be run from the command line.

### Usage

#### Download the Project

```
git clone https://github.com/yanfd/TwitterNew.git
```

Navigate to the corresponding directory using `cd`.

#### Install Dependencies

It is recommended to activate a virtual environment before installation.

```shell
source twienv/bin/activate
```

- **tweepy**: Official development library for X
- **pyfiglet**: Used for banner generation
- **prompt_toolkit**: Text editing area, better than `input`

```shell
pip3 install tweepy pyfiglet prompt_toolkit
```

#### Obtain Your Twitter Keys

Log in to the [X Developer Portal](https://developer.twitter.com/en/portal/projects/), register/log in, and create an application.

Generate `API_KEY`, `API_SECRET`, `ACCESS_TOKEN`, and `ACCESS_TOKEN_SECRET`.

In the settings, set the following:

![](https://p.ipic.vip/ld3oje.png)

to **Read and Write**.

![](https://p.ipic.vip/cft2y9.png)

Fill in the three required fields as you like.

For security reasons, the program stores Twitter keys in environment variables.

After obtaining the keys, add them to your `.bashrc` or `.zshrc` configuration file (depending on your shell type):

```
export 'BEARER_TOKEN'='$YOUR_BEARER'
export 'API_KEY'='$your_api_key'
export 'API_SECRET'='$your_api_secret'
export 'ACCESS_TOKEN'='$your_access_token'
export 'ACCESS_TOKEN_SECRET'='$your_access_token_secret'
```

Run `source ~/.bashrc` to load the configuration file.

**Successful Run Example:**

```
python3 twitter_new.py
```

![](https://p.ipic.vip/t17eoa.png)

Use `deactivate` to exit the virtual environment.

### Potential Issues

- API keys are generally displayed only once upon generation. Please back them up.
- If you encounter insufficient permissions and can only access limited endpoints, ensure the settings are set to **Read and Write**.
- It is recommended to install dependencies in a virtual environment. Global installation may cause issues.
- For other issues, please submit them via the Issues section.