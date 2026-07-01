# 🚀 Deploy Хүслэн AI Online (Free on Render)

## Quick Steps

### 1. **Push to GitHub**
```bash
cd /Users/Khuslen/Desktop/PathFinder
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/PathFinder.git
git push -u origin main
```
*(Replace `YOUR_USERNAME` with your GitHub username)*

### 2. **Create Render Account**
Go to https://render.com and sign up with GitHub.

### 3. **Deploy**
- Click **New Web Service**
- Select your PathFinder repo
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app`
- Add Environment Variable:
  - Key: `SECRET_KEY`
  - Value: *(generate a random string like: `a7f3k9x2m4b8c1d5e6g9h0j2k3l4m5n6`)*
- Click **Deploy**

### 4. **Done!**
Your app will be live at: `https://pathfinder-xxxxx.onrender.com`

---

## Local Testing Before Deploy
```bash
pip install -r requirements.txt
python app.py
```
Visit: http://127.0.0.1:5001

## Notes
- Database auto-resets on Render (free tier). For persistent data, upgrade to Render's PostgreSQL.
- First deploy may take 2-3 minutes to build.
- Cold starts may be slow (free tier sleeps after 15 min inactivity).
