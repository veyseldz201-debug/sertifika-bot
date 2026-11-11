import json
import urllib.request
import urllib.parse
import time
import threading
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is active and running 24/7!")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

threading.Thread(target=run_server, daemon=True).start()

TOKEN = "8989644682:AAGBeZGT-XZgTaYMXYEoMr2me8sNIjoGzzE".strip()
ADMIN_ID = 8578298828
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

ZORUNLU_KANALLAR = ["ipaonay", "iosipadosyalari", "iOSEsignTR"]
kullanici_verileri = {}

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

def answer_callback_query(callback_query_id, text=""):
    data = {"callback_query_id": callback_query_id, "text": text, "show_alert": False}
    req = urllib.request.Request(f"{BASE_URL}/answerCallbackQuery", data=urllib.parse.urlencode(data).encode("utf-8"), method="POST")
    try:
        with urllib.request.urlopen(req):
            pass
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
    for kanal in ZORUNLU_KANALLAR:
        try:
            url = f"{BASE_URL}/getChatMember?chat_id=@{kanal}&user_id={user_id}"
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=10) as response:
                res = json.loads(response.read().decode())
                if res.get("ok"):
                    status = res["result"].get("status")
                    if status not in ["member", "administrator", "creator"]:
                        return False
                else:
                    return False
        except Exception as e:
            return False
    return True

def daveti_onayla_ve_ver(chat_id, first_name, username):
    if chat_id in kullanici_verileri:
        davet_eden = kullanici_verileri[chat_id].get("davet_eden")
        if davet_eden and not kullanici_verileri[chat_id].get("davet_onaylandi", False):
            if davet_eden in kullanici_verileri:
                kullanici_verileri[chat_id]["davet_onaylandi"] = True
                kullanici_verileri[davet_eden]["referrals"] += 1
                ref_sayisi = kullanici_verileri[davet_eden]["referrals"]
                
                send_message(davet_eden, f"💎 **ULTRA VIP DAVET SİSTEMİ**\n\n🎉 Davet ettiğin kullanıcı resmi kanallara katıldı ve doğrulandı!\n➕ **Hesabına +1 VIP Puan Eklendi.**\n🔥 Toplam İlerlemen: **{ref_sayisi} / 15**")
                
                if ref_sayisi >= 15:
                    send_message(ADMIN_ID, f"🏆 **KRİTİK BAŞARI: 15 DAVET TAMAMLANDI!**\n\n👤 Kullanıcı: {first_name} (@{username})\n🆔 ID: `{davet_eden}`\n🔥 Ücretsiz VIP Sertifika hakkını kazandı!")

def check_bot():
    try:
        req = urllib.request.Request(f"{BASE_URL}/getMe")
        with urllib.request.urlopen(req, timeout=10) as response:
            res = json.loads(response.read().decode())
            if res.get("ok"):
                print(f"✅ Bot Aktif: @{res['result'].get('username')}")
                return True
            return False
    except Exception as e:
        print("❌ Bağlantı Hatası:", e)
        return False

main_menu = {
    "inline_keyboard": [
        [{"text": "💎 VIP Sertifika Satın Al", "url": "https://www.shopier.com/iOSEsingTR"}, {"text": "⚡️ UDID Kaydı Gönder", "callback_data": "send_udid_info"}],
        [{"text": "⭐ VIP Profilim & Kartım", "callback_data": "vip_profile"}, {"text": "🏆 Liderlik Tablosu", "callback_data": "vip_leaderboard"}],
        [{"text": "🎁 15 Davet Et, Ücretsiz Al!", "callback_data": "davet_menu"}, {"text": "🤖 VIP AI Asistan", "callback_data": "ai_menu"}],
        [{"text": "🛠 İmza Araçları & IPA", "callback_data": "tools"}, {"text": "🛡 VIP Avantajları & Garanti", "callback_data": "benefits"}],
        [{"text": "❓ SSS", "callback_data": "faq"}, {"text": "💬 Canlı VIP Destek", "url": "https://t.me/devolepercertificate"}]
    ]
}

admin_menu = {
    "inline_keyboard": [
        [{"text": "📊 VIP Bot İstatistikleri", "callback_data": "admin_stats"}, {"text": "📢 Toplu VIP Duyurusu", "callback_data": "admin_broadcast_prompt"}],
        [{"text": "🔗 Zorunlu Kanalları İncele", "callback_data": "admin_channels"}, {"text": "🔄 API Sağlık Testi", "callback_data": "admin_test"}],
        [{"text": "🔙 Normal Ana Menüye Dön", "callback_data": "main_menu"}]
