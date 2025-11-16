#!/usr/bin/env python3
"""
Redirect from port 8889 to real-time dashboard on 8890
"""
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def redirect_page():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Redirecting to Real-Time Dashboard</title>
    <meta http-equiv="refresh" content="3;url=http://localhost:8890">
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            text-align: center;
            padding: 40px;
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        h1 {
            font-size: 3rem;
            margin-bottom: 20px;
        }
        p {
            font-size: 1.3rem;
            margin: 15px 0;
        }
        .url {
            font-size: 2rem;
            font-weight: bold;
            color: #fbbf24;
            margin: 20px 0;
        }
        .spinner {
            border: 4px solid rgba(255,255,255,0.3);
            border-top: 4px solid white;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 30px auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        a {
            color: #fbbf24;
            text-decoration: none;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Upgrading to Real-Time Dashboard</h1>
        <p>The IMPROVED dashboard with live cpp detection is now on:</p>
        <div class="url">http://localhost:8890</div>
        <p>Redirecting automatically in 3 seconds...</p>
        <div class="spinner"></div>
        <p>Or <a href="http://localhost:8890">click here to go now</a></p>
        <p style="font-size: 0.9rem; opacity: 0.8; margin-top: 30px;">
            ✨ NEW FEATURES:<br>
            ✅ Auto-discovers ALL running cpp tasks<br>
            ✅ Status indicators (COMPLETED/EXECUTING/WAITING)<br>
            ✅ System resources AT THE TOP<br>
            ✅ Real-time process detection<br>
            ✅ Updates every 500ms (2x faster)<br>
            ✅ Live progress tracking
        </p>
    </div>
</body>
</html>
"""

if __name__ == "__main__":
    print("\n" + "="*80)
    print("🔀 DASHBOARD REDIRECT SERVER (Port 8889)")
    print("="*80)
    print("\nRedirecting http://localhost:8889 → http://localhost:8890 (Real-Time Dashboard)")
    print("Press Ctrl+C to stop\n")
    uvicorn.run(app, host="0.0.0.0", port=8889, log_level="error")
