# Deployment Guide for All Fours Game

## Quick Start: Deploy to Railway (Recommended for Beginners)

### Step 1: Prepare Your Code
```bash
# Make sure git is initialized
git init
git add .
git commit -m "Initial commit for production"

# Create a GitHub repository
# Push your code to GitHub
```

### Step 2: Deploy to Railway
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your all-fours-game repository
5. Railway auto-detects Node.js and deploys automatically
6. Set environment variables in Railway dashboard

**Cost:** $5/month or free trial

---

## Deploy to Heroku (Most Popular)

### Step 1: Setup
```bash
npm install -g heroku
heroku login
heroku create your-game-name
```

### Step 2: Deploy
```bash
git push heroku main
```

### Step 3: Configure
```bash
heroku config:set NODE_ENV=production
heroku config:set JWT_SECRET=your-secret-key
heroku open
```

**Cost:** Was free, now $5-50/month

---

## Deploy to DigitalOcean (Best for Control)

### Step 1: Create Droplet
1. Go to DigitalOcean.com
2. Create new Ubuntu 22.04 Droplet ($5/month)
3. SSH into your server

### Step 2: Setup Server
```bash
# Update packages
sudo apt update && sudo apt upgrade -y

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Install PM2 (process manager)
sudo npm install -g pm2

# Install Nginx (reverse proxy)
sudo apt install -y nginx

# Clone your repository
git clone your-repo-url
cd all-fours-game
npm install --production
```

### Step 3: Start Application
```bash
pm2 start server.js --name "all-fours"
pm2 startup
pm2 save
```

### Step 4: Configure Nginx
```bash
sudo nano /etc/nginx/sites-available/default
```

Add:
```nginx
server {
    listen 80 default_server;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Step 5: Enable HTTPS
```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

---

## Deploy with Docker (Advanced)

### Step 1: Build Docker Image
```bash
docker build -t all-fours-game:latest .
```

### Step 2: Test Locally
```bash
docker run -p 3000:3000 all-fours-game:latest
```

### Step 3: Push to Registry
```bash
# Docker Hub
docker tag all-fours-game:latest your-username/all-fours-game:latest
docker push your-username/all-fours-game:latest
```

### Step 4: Deploy to Any Docker Host
- AWS ECS
- Google Cloud Run
- Azure Container Instances
- Heroku Container Registry

---

## Domain Setup

1. **Buy a domain:**
   - Namecheap ($2-3/year)
   - Google Domains ($12/year)
   - Cloudflare ($0-12/year)

2. **Point domain to your server:**
   - Update DNS settings
   - Add CNAME record pointing to your hosting provider
   - Enable SSL certificate

3. **Example domain setup:**
   ```
   all-fours.com → game.railway.app
   or
   play.mygame.com → your-server-ip
   ```

---

## Environment Variables Checklist

Before deploying, make sure to set:

```
NODE_ENV=production
PORT=3000
API_BASE_URL=https://your-domain.com
JWT_SECRET=generate-a-secure-random-string
SESSION_SECRET=generate-another-secure-random-string
```

Generate secure secrets:
```bash
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
```

---

## Post-Deployment

### Monitor Your Server
- **Railway Dashboard** - Built-in monitoring
- **Heroku Dashboard** - Logs and metrics
- **DigitalOcean** - Droplet metrics
- **UptimeRobot** - Uptime monitoring (free)

### Setup Logging
```bash
# View logs
heroku logs --tail
# or
pm2 logs all-fours
```

### Auto-Restart
- Railway/Heroku restart automatically on crashes
- DigitalOcean: Use PM2 with `pm2 startup`

### Backup Database
- Regular backups of your database
- Set up automated backups
- Test restore procedures

---

## Scaling

As your game grows:

1. **Database:** Add caching (Redis)
2. **Load balancing:** Multiple server instances
3. **CDN:** Serve static assets faster (Cloudflare)
4. **WebSockets optimization:** Fine-tune Socket.io

---

## Security After Deploy

- [ ] Change all default passwords
- [ ] Enable HTTPS everywhere
- [ ] Set up firewall rules
- [ ] Regular security updates
- [ ] Monitor for suspicious activity
- [ ] Backup frequently
- [ ] Rate limit API endpoints
- [ ] Enable CORS properly
