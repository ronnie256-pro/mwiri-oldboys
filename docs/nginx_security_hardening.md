# Nginx Security Hardening & Rate Limiting Guide

This document provides production hardening rules for Nginx reverse proxy serving MOBA Portal at `https://mwirioldboys.com`.

---

## 1. Updated `/etc/nginx/sites-available/oldboys` Configuration

```nginx
server {
    server_name 187.7.19.28 mwirioldboys.com www.mwirioldboys.com;

    # Allow up to 120MB media uploads
    client_max_body_size 120M;

    location /static/ {
        alias /var/www/oldboys/static/;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }

    # Serve uploaded media safely (Disable directory listing)
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

    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/mwirioldboys.com/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/mwirioldboys.com/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot
}

server {
    if ($host = www.mwirioldboys.com) {
        return 301 https://$host$request_uri;
    } # managed by Certbot

    if ($host = mwirioldboys.com) {
        return 301 https://$host$request_uri;
    } # managed by Certbot

    listen 80;
    server_name 187.7.19.28 mwirioldboys.com www.mwirioldboys.com;
    return 404; # managed by Certbot
}
```

---

## 2. Server UFW Firewall Hardening

Run these commands on your VPS terminal to ensure only SSH and Web ports are exposed:

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing

sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

sudo ufw enable
```
