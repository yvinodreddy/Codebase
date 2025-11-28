#!/bin/bash
# phase6_redirects.sh
# CHANGE 6.2: Configure 301 redirects for SEO

set -e

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="/home/user01/claude-test/ParaGroupAI/rebranding_logs/phase6_redirects_${TIMESTAMP}.log"

echo "==================================================================" | tee -a "$LOG_FILE"
echo "PHASE 6.2: 301 Redirects Configuration" | tee -a "$LOG_FILE"
echo "==================================================================" | tee -a "$LOG_FILE"

# Create .htaccess file with redirects (Apache)
cat > /home/user01/claude-test/ParaGroupAI/.htaccess << 'EOF'
# Para Group AI Orchestrator® - 301 Redirects
# Preserve SEO value from old URLs

RewriteEngine On

# Redirect old ClaudePrompt URLs to new Para Group URLs
RewriteRule ^claudeprompt/(.*)$ https://ai.paragroup.com/$1 [R=301,L]
RewriteRule ^cpp/(.*)$ https://ai.paragroup.com/prsg/$1 [R=301,L]

# Redirect old domain (if applicable)
# RewriteCond %{HTTP_HOST} ^oldomain\.com$ [NC]
# RewriteRule ^(.*)$ https://ai.paragroup.com/$1 [R=301,L]
EOF

echo "✅ Created .htaccess with 301 redirects" | tee -a "$LOG_FILE"

# Create nginx redirect config
cat > /home/user01/claude-test/ParaGroupAI/nginx_redirects.conf << 'EOF'
# Para Group AI Orchestrator® - Nginx 301 Redirects

server {
    listen 80;
    server_name old-domain.com;

    # Permanent redirects to new domain
    rewrite ^/claudeprompt/(.*)$ https://ai.paragroup.com/$1 permanent;
    rewrite ^/cpp/(.*)$ https://ai.paragroup.com/prsg/$1 permanent;
    rewrite ^/(.*)$ https://ai.paragroup.com/$1 permanent;
}
EOF

echo "✅ Created nginx_redirects.conf" | tee -a "$LOG_FILE"
echo "✅ PHASE 6.2 COMPLETE" | tee -a "$LOG_FILE"