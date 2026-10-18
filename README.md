# FINAL JAGRUK AUTOBOT - @jagruk_aadmi

## YOUR CONFIG ALREADY FILLED:
- Page IDs: 1439845869203465 (CA and JOBS update - MAIN), 1355122084357809 (Current Affair Daily), 61595230657784
- Token: EAAqCj1D94a4BS8D... (inside FINAL_JAGRUK_BOT.py)

## QUICK START - Local (Post NOW):
1. pip install -r requirements.txt
2. Edit FINAL_JAGRUK_BOT.py:
   - CLOUDINARY_CLOUD_NAME: from cloudinary.com
   - CLOUDINARY_UPLOAD_PRESET: meme_upload (create unsigned)
   - GROQ_API_KEY: from console.groq.com/keys (FREE, no billing)
3. python FINAL_JAGRUK_BOT.py
-> Auto-finds IG_USER_ID, creates viral meme, posts as REELS to @jagruk_aadmi

## FULL AUTOMATION - GitHub Actions (8x/day, no PC needed):

### Step 1: Create GitHub Repo
- Go to github.com -> New repo -> jagruk-bot -> Public -> Create

### Step 2: Upload files
- Upload ALL files from this zip: FINAL_JAGRUK_BOT.py, requirements.txt, .github/workflows/auto-post.yml, trending_audios/
- Or: git clone, copy files, git push

### Step 3: Add Secrets (VERY IMPORTANT)
Repo -> Settings -> Secrets and variables -> Actions -> New repository secret:

1. PAGE_ACCESS_TOKEN = EAAqCj1D94a4BS8DfmZCWYWtJ7U1ur05ZALpL0wlNp21yZBGhCdrmLs7tJYFRiAovQLol3YVZB2LG6UMCtOGBjkj9R2aUCQgJRiMqfeGRAlA06GpDZBqm2S2cWaYJ78MCLLsB76fZBF3ZAZBiDzCZBq6Y4j5WH0oOJETXAaf7rQQ5NMzgZB9VUZCtWWvxF5EwID6flUCFRsNyBzIHpvgYAw6XZBGSfPGsfyw4GnZADHteggLUW
2. IG_USER_ID = (bot will auto-find on first run, then copy from logs and add here for faster)
3. CLOUDINARY_CLOUD_NAME = your cloud name from cloudinary.com dashboard
4. CLOUDINARY_UPLOAD_PRESET = meme_upload
5. GROQ_API_KEY = gsk_... from console.groq.com

### Step 4: Cloudinary Setup (2 min)
- cloudinary.com -> Sign up free -> Dashboard -> copy Cloud Name
- Settings -> Upload -> Upload presets -> Add upload preset -> Unsigned -> Name: meme_upload -> Save

### Step 5: Groq Setup (1 min, FREE no billing)
- console.groq.com/keys -> Create API key -> copy gsk_...

### Step 6: Trending Songs (Optional but VIRAL)
- Put mp3 files in trending_audios/ folder (e.g., trending1.mp3, viral_song.mp3)
- Bot auto-picks one and adds to video

### Step 7: Run
- Actions tab -> Auto Meme Post @jagruk_aadmi - 8x Daily -> Run workflow -> Run
- Check logs: Should print ✅✅✅ FOUND IG_USER_ID: 1784...
- If IG ID found, it will post!

### Automation Schedule (IST):
- 5:30 AM, 8:30 AM, 11:30 AM, 2:30 PM, 5:30 PM, 8:30 PM, 11:30 PM, 2:30 AM = 8x/day

### Features:
- Auto-finds IG_USER_ID from Page token (fixes Invalid platform app error)
- Scrapes Reddit, Meme APIs -> Unique Hinglish (Groq AI or fallback)
- Creates 1080x1920 viral image + adds trending song
- No repeat (posted_history.json)
- Auto-commits history
- v26.0 API

### Security:
After first successful post, regenerate Page token in developers.facebook.com -> your app pybot -> Tools -> Access Token Debugger -> Extend -> Replace in Secrets.

### Troubleshooting:
- If IG ID not found: Instagram -> Edit Profile -> Page -> Select CA and JOBS update (1439845869203465) -> Wait 3 min -> Run again
- If Cloudinary fail: Check preset is Unsigned
- If post fail: Check token not expired, Page connected to Instagram Business

Enjoy! @jagruk_aadmi will grow on autopilot.
