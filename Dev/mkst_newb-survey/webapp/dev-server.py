#!/usr/bin/env python3
"""
로컬 개발 서버 - 배포 없이 웹앱을 바로 확인할 수 있습니다.
사용법: python3 dev-server.py
"""

import http.server
import socketserver
import webbrowser
import os
import sys
from pathlib import Path

# 현재 디렉토리를 기준으로 HTML 파일 찾기
current_dir = Path(__file__).parent
html_file = current_dir / "index.html"

if not html_file.exists():
    print("❌ index.html 파일을 찾을 수 없습니다.")
    sys.exit(1)

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # CORS 헤더 추가 (Google Apps Script API 호출을 위해)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        # CORS preflight 요청 처리
        self.send_response(200)
        self.end_headers()

def start_server(port=8000):
    """로컬 서버 시작"""
    try:
        with socketserver.TCPServer(("", port), CustomHTTPRequestHandler) as httpd:
            print(f"🚀 로컬 개발 서버가 시작되었습니다!")
            print(f"📱 브라우저에서 확인: http://localhost:{port}")
            print(f"📁 서빙 디렉토리: {current_dir}")
            print(f"⏹️  서버 중지: Ctrl+C")
            print("-" * 50)
            
            # 자동으로 브라우저 열기
            webbrowser.open(f"http://localhost:{port}")
            
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 서버가 중지되었습니다.")
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ 포트 {port}이 이미 사용 중입니다. 다른 포트를 시도합니다...")
            start_server(port + 1)
        else:
            print(f"❌ 서버 시작 오류: {e}")

if __name__ == "__main__":
    start_server()
