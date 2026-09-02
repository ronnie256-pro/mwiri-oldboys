# Nginx Security Hardening & Rate Limiting Guide

This document provides production hardening rules for Nginx reverse proxy serving MOBA Portal at `https://mwirioldboys.com`.

---

## 1. Upload Size & Media Execution Protection

Add these directives inside `/etc/nginx/sites-available/oldboys`:

```nginx
server {
    listen 80;
    listen 443 ssl;
    server_name mwirioldboys.com www.mwirioldboys.com 187.7.19.28;

    # Allow up to 120MB file/media uploads
    client_max_body_size 120M;

    # Serve static files
    location /static/ {
        alias /var/www/oldboys/static/;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }

    # Serve uploaded media files safely (Disable directory listing)
    location /media/ {
        alias /var/www/oldboys/media/;
        autoindex off;
    }

    # BLOCK EXECUTABLE SCRIPT EXECUTION IN MEDIA UPLOADS
    location ~* ^/media/.*\.(py|sh|php|pl|cgi|bash|exe|bat)$ {
        deny all;
        return 403;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## 2. Authentication Rate Limiting

Add rate limiting zone definition at the top of `/etc/nginx/nginx.conf` (inside `http { ... }` block):

```nginx
# Limit authentication requests to 5 requests per minute per IP
limit_req_zone $binary_remote_addr zone=auth_limit:10m rate=5r/m;
```

Apply the rate limit to login endpoints inside `/etc/nginx/sites-available/oldboys`:

```nginx
location /admin-dashboard/login/ {
    limit_req zone=auth_limit burst=5 nodelay;
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}

location /accounts/login/ {
    limit_req zone=auth_limit burst=5 nodelay;
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

---

## 3. Server UFW Firewall Hardening

Run these commands on your VPS terminal to ensure only SSH and Web ports are exposed:

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing

sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

sudo ufw enable
```
