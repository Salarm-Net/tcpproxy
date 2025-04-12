import asyncio
import os
from aiohttp import web

UPLOAD_DIR = './upload'

# HTTPサーバーのPUTメソッドでファイルをアップロードするハンドラー
async def handle_put_request(request):
    # アップロードされたファイルを取得
    reader = await request.multipart()
    
    # ファイルの受け取り処理
    file_field = await reader.next()  # 最初のファイルフィールドを取得
    
    if file_field is None:
        return web.Response(status=400, text="No file uploaded")
    
    # ファイル名を取得
    filename = file_field.filename
    filepath = os.path.join(UPLOAD_DIR, filename)
    
    # ファイルを保存
    with open(filepath, 'wb') as f:
        while True:
            chunk = await file_field.read_chunk()  # ファイルのチャンクを読み取る
            if not chunk:
                break
            f.write(chunk)
    
    return web.Response(status=200, text=f"File '{filename}' uploaded successfully")

# HTTPサーバーを起動
async def start_http_server(local_host, local_port):
    app = web.Application()
    app.router.add_post('/upload', handle_put_request)
    
    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, local_host, local_port)
    print(f"HTTP Server running on http://{local_host}:{local_port}")
    await site.start()


# 実行
if __name__ == "__main__":
    local_host = "127.0.0.1"
    local_port = 8888

    asyncio.run(start_http_server(local_host, local_port))
