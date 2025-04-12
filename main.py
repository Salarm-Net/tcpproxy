import asyncio
from aiohttp import web
from tcpproxy import start_proxy
from httpserver import start_http_server


# メイン処理
async def main():
    # 並列でTCPサーバーとHTTPサーバーを起動
    await asyncio.gather(
        start_proxy('127.0.0.1', 8080, '127.0.0.1', 9999),
        start_http_server('127.0.0.1', 9999)
    )

# 実行
if __name__ == "__main__":
    asyncio.run(main())
