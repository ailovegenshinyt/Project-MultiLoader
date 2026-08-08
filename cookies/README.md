# 🍪 Cookies Directory

Place your platform cookie files here.

## How to Export Cookies

1. Install a browser extension:
   - **Chrome:** [Get cookies.txt LOCALLY](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)
   - **Firefox:** [cookies.txt](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/)

2. Log into the platform in your browser

3. Navigate to the platform's website

4. Click the extension and export as `cookies.txt`

5. Save the file here with the correct name

## Expected File Names

| File | Platform | Env Var |
|------|----------|---------|
| `instagram_cookies.txt` | Instagram | `INSTAGRAM_COOKIES` |
| `tiktok_cookies.txt` | TikTok | `TIKTOK_COOKIES` |
| `x_cookies.txt` | X (Twitter) | `X_COOKIES` |
| `facebook_cookies.txt` | Facebook | `FACEBOOK_COOKIES` |
| `reddit_cookies.txt` | Reddit | `REDDIT_COOKIES` |
| `pornhub_cookies.txt` | PornHub | `PORNHUB_COOKIES` |
| `twitch_cookies.txt` | Twitch | `TWITCH_COOKIES` |
| `bilibili_cookies.txt` | Bilibili | `BILIBILI_COOKIES` |
| `snapchat_cookies.txt` | Snapchat | `SNAPCHAT_COOKIES` |
| `pinterest_cookies.txt` | Pinterest | `PINTEREST_COOKIES` |
| `linkedin_cookies.txt` | LinkedIn | `LINKEDIN_COOKIES` |

## Then Enable in .env

Uncomment and set the path in your `.env` file:

```env
INSTAGRAM_COOKIES=./cookies/instagram_cookies.txt
X_COOKIES=./cookies/x_cookies.txt
```

## ⚠️ Security Note

**Never commit cookie files to Git!** They contain your login sessions.
The `.gitignore` should already exclude `*.txt` files in this folder.

## Global Fallback

You can also place a single `cookies.txt` in the **project root** 
(not this folder). MultiLoader will use it as a fallback for all 
platforms when no platform-specific cookie file is configured.
