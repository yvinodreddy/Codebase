#!/bin/bash

   dig ai.paragroup.com
   nslookup ai.paragroup.com
   ```

5. **Update web server configuration:**
   - Apache: Add VirtualHost for ai.paragroup.com
   - Nginx: Add server block for ai.paragroup.com

6. **SSL Certificate:**
   ```bash
   # Using Let's Encrypt
   certbot --nginx -d ai.paragroup.com
   ```

**Estimated Time:** 15-30 minutes (+ up to 48 hours for DNS propagation)