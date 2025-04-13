import asyncio
import aiohttp
from aiohttp import web
import aiohttp.web_request
from yarl import URL

async def handle_request(request: aiohttp.web_request.Request, remote_host, remote_port):
    try:
        base_url = f"http://{remote_host}:{remote_port}"
        # リクエストの情報を取得
        method = request.method
        url = URL(base_url + request.rel_url.path)
        headers = dict(request.headers)
        # リクエストデータ取得
        data = await request.read()
        
        # プロキシするリクエストを作成
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, headers=headers, data=data) as resp:
                data = await resp.read()
                return web.Response(
                    status=resp.status,
                    headers=resp.headers,
                    body=data
                )
    except Exception as e:
        return web.Response(text=f"Error: {str(e)}", status=500)

async def start_proxy(local_host, local_port, remote_host, remote_port):
    app = web.Application()
    app.router.add_route('*', '/{proxy_path:.*}', lambda r: handle_request(r, remote_host, remote_port))

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, local_host, local_port)
    print(f"HTTP Proxy running on {local_host}:{local_port} -> {remote_host}:{remote_port}")
    await site.start()

if __name__ == "__main__":
    local_host = "127.0.0.1"
    local_port = 3000
    remote_host = "127.0.0.1"
    remote_port = 8080

    asyncio.run(start_proxy(local_host, local_port, remote_host, remote_port))
