import requests

url = 'http://127.0.0.1:8080/upload'  # サーバーのURLを指定
file_path = 'send_sample.txt'  # 送信するファイルのパス

with open(file_path, 'rb') as file:
    response = requests.post(url, files={'file': file})

# レスポンスを表示
print(f"Status Code: {response.status_code}")
print(f"Response Text: {response.text}")