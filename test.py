import requests

dc_webhook_url = "https://discord.com/api/webhooks/1344548206566182952/suQOjXaEthEAWs_tbN3aXEZUaX00SQ2qVI_XDuqQd1pl_nzbA9AdQAmi6Zvgdp6xJcan"

def send_discord_notification(subject, days_left):
    message = f"⚠️ 注意！{subject} 考試只剩 {days_left} 天！請準備好！"
    data = {"content": message}
    
    try:
        response = requests.post(dc_webhook_url, json=data)
        response.raise_for_status()  # 如果請求失敗，會拋出錯誤
        print("✅ 訊息發送成功！")
    except requests.exceptions.RequestException as e:
        print(f"❌ 發送失敗: {e}")

# 測試發送通知
send_discord_notification("數學", 3)