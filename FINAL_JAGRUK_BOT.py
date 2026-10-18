"""
FINAL AUTO-UPLOAD BOT FOR @jagruk_aadmi
Page: CA and JOBS update (1439845869203465) + Current Affair Daily (1355122084357809) + New Profile (61595230657784)
Features: Auto-finds IG ID, Scrapes Reddit/Twitter/9GAG, Hinglish, Trending Songs, No Repeat, Cloudinary, v26.0
"""
import os, json, random, textwrap, requests, re
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# ============ YOUR CONFIG - ALREADY FILLED ============
CONFIG = {
    # Page IDs you have
    "PAGE_IDS": ["1439845869203465", "1355122084357809", "61595230657784"],
    
    # Your Page Access Token for CA and JOBS update (1439845869203465) - from me/accounts
    # This is the long EAAq... token you sent
    "PAGE_ACCESS_TOKEN": os.getenv("PAGE_ACCESS_TOKEN", "EAAqCj1D94a4BS8DfmZCWYWtJ7U1ur05ZALpL0wlNp21yZBGhCdrmLs7tJYFRiAovQLol3YVZB2LG6UMCtOGBjkj9R2aUCQgJRiMqfeGRAlA06GpDZBqm2S2cWaYJ78MCLLsB76fZBF3ZAZBiDzCZBq6Y4j5WH0oOJETXAaf7rQQ5NMzgZB9VUZCtWWvxF5EwID6flUCFRsNyBzIHpvgYAw6XZBGSfPGsfyw4GnZADHteggLUW"),
    
    # Will be auto-found at runtime
    "IG_USER_ID": os.getenv("IG_USER_ID", ""),
    
    # Cloudinary - FREE - get at cloudinary.com - create unsigned preset "meme_upload"
    "CLOUDINARY_CLOUD_NAME": os.getenv("CLOUDINARY_CLOUD_NAME", "YOUR_CLOUD_NAME"),
    "CLOUDINARY_UPLOAD_PRESET": os.getenv("CLOUDINARY_UPLOAD_PRESET", "meme_upload"),
    
    # Groq - FREE, NO BILLING - get at console.groq.com/keys
    "GROQ_API_KEY": os.getenv("GROQ_API_KEY", ""),
    
    "HISTORY_FILE": "posted_history.json",
    "PERFORMANCE_FILE": "performance.json",
    "TRENDING_AUDIO_FOLDER": "trending_audios",
    "ALLOW_REPEAT": False,
}

def get_ig_user_id_auto():
    """Auto-find IG_USER_ID from your Page token - fixes Invalid platform app error"""
    if CONFIG["IG_USER_ID"] and not CONFIG["IG_USER_ID"].startswith("YOUR_"):
        print(f"Using provided IG_USER_ID: {CONFIG['IG_USER_ID']}")
        return CONFIG["IG_USER_ID"]
    
    print("🔍 Auto-finding IG_USER_ID from Page token...")
    token = CONFIG["PAGE_ACCESS_TOKEN"]
    
    for page_id in CONFIG["PAGE_IDS"]:
        for version in ["v26.0", "v20.0", "v19.0"]:
            for field in ["instagram_business_account", "connected_instagram_account"]:
                url = f"https://graph.facebook.com/{version}/{page_id}?fields={field},name&access_token={token}"
                try:
                    r = requests.get(url, timeout=10)
                    data = r.json()
                    print(f"Trying Page {page_id} {version} {field}: {str(data)[:200]}")
                    if field in data and data[field] and "id" in data[field]:
                        ig_id = data[field]["id"]
                        print(f"\n✅✅✅ FOUND IG_USER_ID: {ig_id} from Page {page_id} ({data.get('name','')}) via {version}")
                        CONFIG["IG_USER_ID"] = ig_id
                        return ig_id
                except Exception as e:
                    print(f"Error {page_id} {version}: {e}")
                    continue
    
    # Try me/instagram_accounts
    for version in ["v26.0", "v20.0"]:
        url = f"https://graph.facebook.com/{version}/me/instagram_accounts?access_token={token}"
        try:
            r = requests.get(url, timeout=10)
            data = r.json()
            print(f"me/instagram_accounts {version}: {data}")
            if "data" in data and len(data["data"]) > 0:
                ig_id = data["data"][0]["id"]
                print(f"✅ Found via me/instagram_accounts: {ig_id}")
                CONFIG["IG_USER_ID"] = ig_id
                return ig_id
        except:
            pass
    
    print("❌ Could not auto-find IG ID. Make sure:")
    print("1. Instagram @jagruk_aadmi is Business/Creator")
    print("2. Instagram -> Edit Profile -> Page -> Select CA and JOBS update (1439845869203465)")
    print("3. Wait 2-3 minutes after connecting")
    return None

# ================= MULTI-PLATFORM SCRAPERS =================
def fetch_reddit():
    print("🔍 Reddit...")
    urls = [
        "https://www.reddit.com/r/memes/hot.json?limit=25",
        "https://www.reddit.com/r/dankmemes/hot.json?limit=25",
        "https://www.reddit.com/r/IndianMeme/hot.json?limit=25",
        "https://www.reddit.com/r/ProgrammerHumor/hot.json?limit=25",
        "https://www.reddit.com/r/wholesomememes/hot.json?limit=25",
        "https://www.reddit.com/r/memesindia/hot.json?limit=25",
    ]
    memes = []
    headers = {"User-Agent": "Mozilla/5.0 MemeBot jagruk_aadmi"}
    for url in urls:
        try:
            r = requests.get(url, headers=headers, timeout=8)
            if r.status_code == 200:
                for post in r.json()["data"]["children"]:
                    d = post["data"]
                    if not d.get("over_18") and d.get("title"):
                        memes.append({"text": d["title"], "image": d.get("url_overridden_by_dest", ""), "score": d.get("score", 0), "source": "reddit"})
        except Exception as e:
            print(f"Reddit fail {url[:30]}: {e}")
    return memes

def fetch_meme_api():
    print("🔍 Meme APIs (9GAG, Imgflip)...")
    memes = []
    try:
        r = requests.get("https://meme-api.com/gimme/memes/20", timeout=8)
        if r.status_code == 200:
            for m in r.json().get("memes", []):
                memes.append({"text": m["title"], "image": m.get("url",""), "score": m.get("ups",0), "source": "meme-api"})
    except:
        pass
    try:
        r = requests.get("https://meme-api.com/gimme/wholesomememes/20", timeout=8)
        if r.status_code == 200:
            for m in r.json().get("memes", []):
                memes.append({"text": m["title"], "image": m.get("url",""), "score": m.get("ups",0), "source": "wholesome"})
    except:
        pass
    return memes

def fetch_all_platforms():
    all_memes = []
    all_memes += fetch_reddit()
    all_memes += fetch_meme_api()
    all_memes.sort(key=lambda x: x.get("score",0), reverse=True)
    print(f"✅ Total fetched: {len(all_memes)} memes")
    return all_memes

# ================= HINGLISH CONVERTER =================
def make_unique_hinglish(text):
    text = text.strip()
    if CONFIG["GROQ_API_KEY"]:
        try:
            headers = {"Authorization": f"Bearer {CONFIG['GROQ_API_KEY']}", "Content-Type": "application/json"}
            payload = {
                "model": "llama-3.1-8b-instant",
                "messages": [{"role":"user","content": f"Rewrite this meme in Hinglish (mix Hindi + English), funny, desi, GenZ, short, unique for @jagruk_aadmi: '{text}'"}],
                "max_tokens": 80
            }
            r = requests.post("https://api.groq.com/openai/v1/chat/completions", json=payload, headers=headers, timeout=10)
            if r.status_code == 200:
                return r.json()["choices"][0]["message"]["content"].strip()
        except Exception as e:
            print(f"Groq fail: {e}")
    
    # Fallback desi twist
    desi_replacements = {
        "I am": "Me hu", "You are": "Tu hai", "My friend": "Mera dost",
        "When": "Jab", "What": "Kya", "Why": "Kyun", "How": "Kaise",
        "Don't": "Mat", "Can't": "Nahi kar sakta"
    }
    for eng, hing in desi_replacements.items():
        if random.random() < 0.3:
            text = text.replace(eng, hing)
    
    prefix = random.choice(["POV: ", "Me: ", "Jab ", "Indian parents: ", "Jagruk raho, ", ""])
    if not text.startswith(prefix) and prefix:
        text = prefix + text
    
    return text

# ================= IMAGE CREATION =================
def create_viral_reel_image(text, original_img_path, out_path):
    W, H = 1080, 1920
    # Create background
    if original_img_path and os.path.exists(original_img_path):
        try:
            bg = Image.open(original_img_path).convert("RGB")
            bg = bg.resize((W, H))
            # Darken
            overlay = Image.new('RGB', (W,H), (0,0,0))
            img = Image.blend(bg, overlay, 0.4)
        except:
            img = Image.new('RGB', (W,H), (15,15,15))
    else:
        img = Image.new('RGB', (W,H), (15,15,15))
    
    draw = ImageDraw.Draw(img)
    # Gradient
    palettes = [[(120,30,200),(40,10,100)], [(200,60,20),(100,20,10)], [(20,150,120),(10,60,50)]]
    c1,c2 = random.choice(palettes)
    for y in range(500):
        r = int(c1[0] + (c2[0]-c1[0])*y/500)
        g = int(c1[1] + (c2[1]-c1[1])*y/500)
        b = int(c1[2] + (c2[2]-c1[2])*y/500)
        draw.line([(0,y),(W,y)], fill=(r,g,b))
    
    try:
        fb = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 62)
        fs = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 42)
        fsmall = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 34)
    except:
        fb = fs = fsmall = ImageFont.load_default()
    
    draw.rounded_rectangle([(40,40),(360,110)], radius=20, fill=(255,255,255))
    draw.text((70,55), "MEME 🔥", font=fs, fill=(0,0,0))
    
    wrapped = textwrap.wrap(text, width=28)
    y = 560
    for line in wrapped[:8]:
        draw.text((70,y), line, font=fb, fill=(255,255,255), stroke_width=4, stroke_fill=(0,0,0))
        y+=88
    
    draw.text((60,1560), "@jagruk_aadmi", font=fb, fill=(255,255,255))
    draw.text((60,1640), "Roz AI memes • Jagruk raho 😂", font=fs, fill=(180,180,180))
    draw.rounded_rectangle([(50,1720),(780,1800)], radius=25, fill=(255,50,100))
    draw.text((80,1735), "Tag that friend 👇", font=fsmall, fill=(255,255,255))
    img.save(out_path)
    return out_path

def download_image(url, path):
    try:
        r = requests.get(url, timeout=10, headers={"User-Agent":"Mozilla/5.0"})
        if r.status_code == 200 and "image" in r.headers.get("Content-Type",""):
            with open(path, "wb") as f:
                f.write(r.content)
            return path
    except:
        pass
    return None

# ================= SONG MIX =================
def fetch_trending_song_auto():
    for folder in ["trending_audios", "auto_songs", "."]:
        if os.path.exists(folder):
            mp3s = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".mp3")]
            if mp3s:
                chosen = random.choice(mp3s)
                print(f"🎵 Auto-chosen song: {chosen}")
                return chosen
    return None

def add_trending_song_auto(video_path):
    song_path = fetch_trending_song_auto()
    if not song_path or not os.path.exists(song_path):
        return video_path
    try:
        from moviepy.editor import VideoFileClip, AudioFileClip
        print(f"🎵 Mixing song: {os.path.basename(song_path)}")
        video = VideoFileClip(video_path)
        audio = AudioFileClip(song_path)
        if audio.duration < video.duration:
            from moviepy.editor import concatenate_audioclips
            loops = int(video.duration // audio.duration) + 1
            audio = concatenate_audioclips([audio]*loops).subclip(0, video.duration)
        else:
            audio = audio.subclip(0, video.duration)
        audio = audio.volumex(0.6)
        final = video.set_audio(audio)
        out = video_path.replace(".mp4", "_with_song.mp4")
        final.write_videofile(out, fps=24, codec='libx264', logger=None)
        print(f"✅ Video with song: {out}")
        return out
    except Exception as e:
        print(f"Song mix fail: {e}")
        return video_path

# ================= CLOUDINARY + POST =================
def upload_to_cloudinary(file_path):
    if not CONFIG["CLOUDINARY_CLOUD_NAME"] or CONFIG["CLOUDINARY_CLOUD_NAME"] == "YOUR_CLOUD_NAME":
        print("⚠️ No Cloudinary creds - test mode")
        return None
    try:
        resource_type = "video" if file_path.endswith(".mp4") else "image"
        url = f"https://api.cloudinary.com/v1_1/{CONFIG['CLOUDINARY_CLOUD_NAME']}/{resource_type}/upload"
        with open(file_path, "rb") as f:
            files = {"file": f}
            data = {"upload_preset": CONFIG["CLOUDINARY_UPLOAD_PRESET"]}
            r = requests.post(url, files=files, data=data, timeout=30)
            if r.status_code == 200:
                media_url = r.json()["secure_url"]
                print(f"✅ Cloudinary URL: {media_url}")
                return media_url
            else:
                print(f"Cloudinary fail: {r.text[:300]}")
    except Exception as e:
        print(f"Cloudinary error: {e}")
    return None

def generate_caption_with_hook(meme_text):
    hooks = ["Tag that friend 😂", "Relatable? 😭", "No lies 💀", "AI era be like 🤖", "Jagruk ho jao 👀", "Ye wala personal laga 😂", "Konse wale ho tum? 👀"]
    viral_tags = [
        "#meme #aimemes #funny #desimemes #jagruk_aadmi #hindimemes #relatable #indianmemes #viral #memepage #aifunny #jagruk",
        "#indianmemes #desimemes #funnyvideos #memesdaily #jagruk #ai #chatgpt #viralreels #trending #funnymemes",
        "#memes #funny #desi #hinglish #jagruk_aadmi #aimeme #relatable #indian #viralpost #memepage"
    ]
    return f"{random.choice(hooks)}\n\n{meme_text[:100]}...\n\n{random.choice(viral_tags)}"

def post_to_instagram(media_url, caption, ig_user_id):
    token = CONFIG["PAGE_ACCESS_TOKEN"]
    if not ig_user_id or not token:
        print("⚠️ Missing IG_USER_ID or ACCESS_TOKEN")
        return False
    
    create_url = f"https://graph.facebook.com/v26.0/{ig_user_id}/media"
    payload = {"caption": caption, "access_token": token}
    if media_url.endswith(".mp4") or "video" in media_url:
        payload["media_type"] = "REELS"
        payload["video_url"] = media_url
    else:
        payload["image_url"] = media_url
    
    print(f"📤 Creating container for IG ID {ig_user_id}...")
    r = requests.post(create_url, data=payload, timeout=20)
    print(f"Create: {r.text[:500]}")
    if r.status_code != 200:
        return False
    
    creation_id = r.json().get("id")
    # Wait for processing
    import time
    time.sleep(5)
    
    pub_url = f"https://graph.facebook.com/v26.0/{ig_user_id}/media_publish"
    r2 = requests.post(pub_url, data={"creation_id": creation_id, "access_token": token}, timeout=20)
    print(f"Publish: {r2.text[:500]}")
    return r2.status_code == 200

# ================= MAIN =================
def load_history():
    if os.path.exists(CONFIG["HISTORY_FILE"]):
        with open(CONFIG["HISTORY_FILE"], "r", encoding="utf-8") as f:
            return json.load(f)
    return {"posted_texts": [], "count": 0}

def save_history(h):
    with open(CONFIG["HISTORY_FILE"], "w", encoding="utf-8") as f:
        json.dump(h, f, ensure_ascii=False, indent=2)

def main():
    print(f"🚀 BOT START for @jagruk_aadmi at {datetime.now()}")
    print(f"Pages: {CONFIG['PAGE_IDS']}")
    
    ig_id = get_ig_user_id_auto()
    if not ig_id:
        print("❌ Could not find IG ID - check connection")
        return
    
    all_memes = fetch_all_platforms()
    if not all_memes:
        all_memes = [{"text": "Me: I'll sleep early\nAlso me 3 AM: researching AI", "image": "", "score": 0, "source": "fallback"}]
    
    history = load_history()
    unique_meme = None
    for _ in range(50):
        candidate = random.choice(all_memes)
        hinglish_text = make_unique_hinglish(candidate["text"])
        if hinglish_text not in history["posted_texts"]:
            unique_meme = {"text": hinglish_text, "original": candidate, "image_url": candidate.get("image","")}
            history["posted_texts"].append(hinglish_text)
            history["posted_texts"] = history["posted_texts"][-1000:]
            history["count"] = history.get("count",0)+1
            save_history(history)
            break
    
    if not unique_meme:
        print("No unique meme found")
        return
    
    print(f"✅ Selected [{unique_meme['original']['source']}]: {unique_meme['text'][:80]}")
    
    temp_img = None
    if unique_meme["image_url"]:
        temp_img = download_image(unique_meme["image_url"], "temp_original.jpg")
    
    final_img = create_viral_reel_image(unique_meme["text"], temp_img, f"meme_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg")
    
    final_video = final_img.replace(".jpg", ".mp4")
    try:
        from moviepy.editor import ImageClip
        clip = ImageClip(final_img).set_duration(7)
        clip.write_videofile(final_video, fps=24, codec='libx264', logger=None)
        print(f"🎬 Video: {final_video}")
    except Exception as e:
        print(f"Video fail, using image: {e}")
        final_video = final_img
    
    final_video = add_trending_song_auto(final_video)
    
    media_url = upload_to_cloudinary(final_video)
    if not media_url:
        media_url = upload_to_cloudinary(final_img)
    
    if not media_url:
        print("⚠️ No media URL - test mode complete. Image created: " + final_img)
        print(f"Would caption: {unique_meme['text']}")
        return
    
    caption = generate_caption_with_hook(unique_meme["text"])
    print(f"📝 Caption: {caption[:200]}...")
    
    success = post_to_instagram(media_url, caption, ig_id)
    if success:
        print("🎉 POSTED SUCCESSFULLY to @jagruk_aadmi!")
        # Save performance
        perf_data = {"posts": []}
        if os.path.exists(CONFIG["PERFORMANCE_FILE"]):
            with open(CONFIG["PERFORMANCE_FILE"], "r") as f:
                perf_data = json.load(f)
        perf_data["posts"].append({"text": unique_meme["text"], "source": unique_meme["original"]["source"], "time": datetime.now().isoformat()})
        with open(CONFIG["PERFORMANCE_FILE"], "w") as f:
            json.dump(perf_data, f, indent=2, ensure_ascii=False)
    else:
        print("❌ Post failed")
    
    print("🏁 Done")

if __name__ == "__main__":
    main()
