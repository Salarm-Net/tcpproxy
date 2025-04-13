import asyncio
from aiohttp import web
import tcpproxy
import httpproxy
import httpserver


# メイン処理
async def main():
    # 並列でTCPサーバーとHTTPサーバーを起動
    await asyncio.gather(
        tcpproxy.start_proxy('127.0.0.1', 2000, '127.0.0.1', 8080),
        httpproxy.start_proxy('127.0.0.1', 3000, '127.0.0.1', 8080),
        httpserver.start_http_server('127.0.0.1', 8080)
    )

# 実行
if __name__ == "__main__":
    asyncio.run(main())

'''
サンプル
curl -v http://localhost:3000/
curl -v http://localhost:3000/upload -F filename=@send_sample.txt 

'''