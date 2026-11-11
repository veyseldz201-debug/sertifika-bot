import json
import urllib.request
import urllib.parse
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# --- Mini Web Sunucusu (Render Port Uyarısını Çözmek İçin) ---
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is active and running 24/7!")

def run_server():
    server = HTTPServer(('0.0.0.0', 10000), SimpleHandler)
    server.serve_forever()

# Web sunucusunu arka planda başlatıyoruz
threading.Thread(target=run_server, daemon=True).start()
# -------------------------------------------------------------

TOKEN = "8989644682:AAGBeZGT-XZgTaYMXYEoMr2me8sNIjoGzzE".strip()
ADMIN_ID = 8578298828  # Senin ID'n
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

# Zorunlu Kanallar Listesi (Kanal kullanıcı adları - Bot bu kanallarda yönetici olmalı)
ZORUNLU_KANALLAR = ["iosipadosyalari", "iOSEsignTR"] 

# Bellek tabanlı veritabanı (Davet ve kayıtlar için)
kullanici_verileri = {}

def check_bot():
    try:
        req = urllib.request.Request(f"{BASE_URL}/getMe")
        with urllib.request.urlopen(req, timeout=10) as response:
            res = json.loads(response.read().decode())
            if res.get("ok"):
                print(f"✅ VIP AI Bot Aktif: @{res['result'].get('username')}")
                return True
            return False
    except Exception as e:
        print("❌ Bağlantı Hatası:", e)
        return False

def send_message(chat_id, text, reply_markup=None):
    data = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    if reply_markup:
        data["reply_markup"] = json.dumps(reply_markup)
    req = urllib.request.Request(f"{BASE_URL}/sendMessage", data=urllib.parse.urlencode(data).encode("utf-8"), method="POST")
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print("Mesaj hatası:", e)

def edit_message(chat_id, message_id, text, reply_markup=None):
    data = {"chat_id": chat_id, "message_id": message_id, "text": text, "parse_mode": "Markdown"}
    if reply_markup:
        data["reply_markup"] = json.dumps(reply_markup)
    req = urllib.request.Request(f"{BASE_URL}/editMessageText", data=urllib.parse.urlencode(data).encode("utf-8"), method="POST")
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print("Düzenleme hatası:", e)

def delete_message(chat_id, message_id):
    data = {"chat_id": chat_id, "message_id": message_id}
    req = urllib.request.Request(f"{BASE_URL}/deleteMessage", data=urllib.parse.urlencode(data).encode("utf-8"), method="POST")
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except:
        pass

def get_updates(offset=None):
    url = f"{BASE_URL}/getUpdates?timeout=30"
    if offset:
        url += f"&offset={offset}"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=35) as response:
            return json.loads(response.read().decode()).get("result", [])
    except Exception as e:
        return []

def kanallari_kontrol_et(user_id):
    """Kullanıcının zorunlu kanallara katılıp katılmadığını kontrol eder"""
    for kanal in ZORUNLU_KANALLAR:
        try:
            url = f"{BASE_URL}/getChatMember?chat_id=@{kanal}&user_id={user_id}"
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=10) as response:
                res = json.loads(response.read().decode())
                if res.get("ok"):
                    status = res["result"].get("status")
                    if status in ["left", "kicked"]:
                        return False
                else:
                    return False
        except Exception as e:
            print(f"Kanal kontrol hatası (@{kanal}): {e}")
            return False
    return True

# --- MENÜLER ---
main_menu = {
    "inline_keyboard": [
        [{"text": "💎 Vip Sertifika Al", "url": "https://www.shopier.com/iOSEsingTR"}, {"text": "⚡️ UDID Gönder", "callback_data": "send_udid_info"}],
        [{"text": "📱 UDID Nereden Bakılır?", "callback_data": "udid_nasil_bakilir"}],
        [{"text": "🎁 10 Davet Et, Ücretsiz Al!", "callback_data": "davet_menu"}, {"text": "🤖 AI Asistan", "callback_data": "ai_menu"}],
        [{"text": "🛠 Araçlar & Uygulamalar", "callback_data": "tools"}, {"text": "🛡 Avantajlar", "callback_data": "benefits"}],
        [{"text": "❓ SSS", "callback_data": "faq"}, {"text": "💬 Canlı Destek (Admin)", "url": "https://t.me/devolepercertificate"}]
    ]
}

back_keyboard = {
    "inline_keyboard": [[{"text": "🔙 Ana Menüye Dön", "callback_data": "main_menu"}]]
}

ai_chat_keyboard = {
    "inline_keyboard": [
        [{"text": "💰 Fiyat Nedir?", "callback_data": "ai_fiyat"}, {"text": "📱 UDID Nasıl Bulunur?", "callback_data": "ai_udid"}],
        [{"text": "🛡 Güvenilir mi?", "callback_data": "ai_guven"}, {"text": "⏳ Süreç Kaç Saat?", "callback_data": "ai_sure"}],
        [{"text": "🔙 Ana Menüye Dön", "callback_data": "main_menu"}]
    ]
}


if check_bot():
    print("🚀 VIP Ekosistem Botu Aktif ve Çalışıyor...")
    
    # 🔔 Bot açıldığı anda Admin'e Telegram üzerinden bildirim gönderir:
    send_message(ADMIN_ID, "🚀 **Bot Başlatıldı!**\n\nSunucu başarıyla aktif hale geldi ve bot döngüsü çalışmaya başladı.")
    
    offset = None
    user_states = {}

    while True:
        updates = get_updates(offset)
        for update in updates:
            offset = update["update_id"] + 1
            
            if "message" in update:
                msg = update["message"]
                chat_id = msg["chat"]["id"]
                text = msg.get("text", "")
                first_name = msg["chat"].get("first_name", "Değerli Müşterimiz")
                username = msg["chat"].get("username", "Yok")
                
                if text.startswith("/start"):
                    user_states.pop(chat_id, None)
                    args = text.split()
                    
                    # 1. Davet (Referral) Kontrolü
                    davet_eden_id = None
                    if len(args) > 1 and args[1].isdigit():
                        davet_eden_id = int(args[1])
                        if davet_eden_id != chat_id and chat_id not in kullanici_verileri:
                            if davet_eden_id in kullanici_verileri:
                                kullanici_verileri[davet_eden_id]["referrals"] += 1
                                ref_sayisi = kullanici_verileri[davet_eden_id]["referrals"]
                                
                                # Davet edene haber ver
                                send_message(davet_eden_id, f"🎉 **Tebrikler!** Linkiniz üzerinden yeni biri katıldı.\n🔥 Toplam davet sayınız: **{ref_sayisi} / 10**")
                                
                                # Eğer tam 10 kişiye ulaştıysa Admin'e özel acil bildirim gönder!
                                if ref_sayisi >= 10:
                                    send_message(ADMIN_ID, f"🏆 **ÖDÜL KAZANAN ÇIKTI!**\n\n👤 Kullanıcı: {first_name} (@{username})\n🆔 ID: `{davet_eden_id}`\n🔥 10 arkadaşını başarıyla davet etti ve ücretsiz sertifika hakkı kazandı!\n👉 Onaylamak için iletişime geçin.")

                    if chat_id not in kullanici_verileri:
                        kullanici_verileri[chat_id] = {"referrals": 0, "username": username, "first_name": first_name}

                    # 2. Zorunlu Kanal Kontrolü
                    if not kanallari_kontrol_et(chat_id):
                        sub_keyboard = {
                            "inline_keyboard": [
                                [{"text": "📢 Özel Kanala Katıl", "url": "https://t.me/+tMRpDvKKQ1JmNWVk"}],
                                [{"text": "📢 iOS IPA Dosyaları Katıl", "url": "https://t.me/iosipadosyalari"}],
                                [{"text": "✅ Katıldım Kontrol Et", "callback_data": "check_subscription"}]
                            ]
                        }
                        send_message(chat_id, "⚠️ Botu kullanabilmek için yukarıdaki kanallarımıza abone olmanız gerekmektedir.", sub_keyboard)
                    else:
                        send_message(chat_id, "✨ **Merhaba !**\n\n👑 Apple Developer VIP Ekosistemine hoş geldin.\n\n🚀 Cihazını özgürleştirmek için aşağıdaki modern menüyü kullanabilir veya AI Asistan ile merak ettiklerini anında sorabilirsin:", main_menu)
