import requests
from flask import Flask, send_file
import requests
import matplotlib.pyplot as plt
import io

app = Flask(__name__)

dc_webhook_url = "https://discord.com/api/webhooks/1344548206566182952/suQOjXaEthEAWs_tbN3aXEZUaX00SQ2qVI_XDuqQd1pl_nzbA9AdQAmi6Zvgdp6xJcan"

def send_discord_notification(image_data):
    """
    發送圖片到 Discord 伺服器
    """
    # 構建要發送的資料
    data = {"content": "這是你的課表圖表！"}
    
    # 使用 multipart/form-data 發送圖片
    files = {"file": ("chart.png", image_data, "image/png")}
    
    # 發送 POST 請求到 Discord Webhook
    response = requests.post(dc_webhook_url, data=data, files=files)
    
    # 輸出是否成功
    if response.status_code == 204:
        print("圖片已成功發送到 Discord!")
    else:
        print(f"發送失敗: {response.status_code}, {response.text}")

@app.route('/')
def index():
    """
    生成圖表並發送到 Discord
    """
    # 生成圖表
    labels = ['Math', 'Science', 'English', 'History']
    sizes = [30, 30, 20, 20]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%')
    ax.axis('equal')  # 圓形顯示

    # 儲存圖表為內存中的圖片
    img_io = io.BytesIO()
    plt.savefig(img_io, format='PNG')
    img_io.seek(0)  # 重設讀取指標

    # 發送圖片到 Discord
    send_discord_notification(img_io)

    # 返回成功訊息
    return "圖表已發送到 Discord！"

if __name__ == '__main__':
    app.run(debug=True)
