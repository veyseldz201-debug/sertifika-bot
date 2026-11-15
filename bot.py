import json
import urllib.request
import urllib.parse
import time
import threading
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler

# -------------------------------------------------------------
# 1. SAF PYTHON İLE MINI APP SUNUCUSU (24/7 Render Destekli)
# -------------------------------------------------------------
def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

threading.Thread(target=run_server, daemon=True).start()

# -------------------------------------------------------------
# 2. TELEGRAM BOT AYARLARI VE LİSTE
# -------------------------------------------------------------
TOKEN = os.environ.get("BOT_TOKEN", "").strip()
ADMIN_ID = 8578298828
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

ZORUNLU_KANALLAR = ["ipaonay", "iosipadosyalari", "iOSEsignTR"]
VERI_DOSYASI = "kullanicilar.json"

bot_durumu = {"bakim_modu": False, "duyuru_aktif": True}
engellenenler = set()

kullanici_verileri = {}

if os.path.exists(VERI_DOSYASI):
    try:
        with open(VERI_DOSYASI, "r", encoding="utf-8") as f:
            dosya_verileri = {int(k): v for k, v in json.load(f).items()}
            kullanici_verileri.update(dosya_verileri)
    except:
        pass

def verileri_kaydet():
    try:
        with open(VERI_DOSYASI, "w", encoding="utf-8") as f:
            json.dump(kullanici_verileri, f, ensure_ascii=False, indent=4)
    except:
        pass

def send_message(chat_id, text, reply_markup=None):
    if not TOKEN: return
    data = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    if reply_markup: data["reply_markup"] = json.dumps(reply_markup)
    req = urllib.request.Request(f"{BASE_URL}/sendMessage", data=urllib.parse.urlencode(data).encode("utf-8"), method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print("Mesaj hatası:", e)

def edit_message(chat_id, message_id, text, reply_markup=None):
    if not TOKEN: return
    data = {"chat_id": chat_id, "message_id": message_id, "text": text, "parse_mode": "Markdown"}
    if reply_markup: data["reply_markup"] = json.dumps(reply_markup)
    req = urllib.request.Request(f"{BASE_URL}/editMessageText", data=urllib.parse.urlencode(data).encode("utf-8"), method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print("Düzenleme hatası:", e)

def answer_callback_query(cq_id):
    if not TOKEN: return
    data = {"callback_query_id": cq_id, "text": "", "show_alert": False}
    req = urllib.request.Request(f"{BASE_URL}/answerCallbackQuery", data=urllib.parse.urlencode(data).encode("utf-8"), method="POST")
    try:
        with urllib.request.urlopen(req): pass
    except: pass

# Telegram Yıldız (Stars) Fatura Gönderme Fonksiyonu
def send_invoice(chat_id, title, description, amount_stars):
    if not TOKEN: return
    prices = [{"label": title, "amount": amount_stars}]
    data = {
        "chat_id": chat_id,
        "title": title,
        "description": description,
        "payload": f"sertifika_lisans_{amount_stars}",
        "currency": "XTR",  # Telegram Stars resmi birimi
        "prices": json.dumps(prices)
    }
    req = urllib.request.Request(f"{BASE_URL}/sendInvoice", data=urllib.parse.urlencode(data).encode("utf-8"), method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        print("Fatura gönderme hatası:", e)

def answer_pre_checkout_query(pcq_id, ok=True):
    if not TOKEN: return
    data = {"pre_checkout_query_id": pcq_id, "ok": ok}
    req = urllib.request.Request(f"{BASE_URL}/answerPreCheckoutQuery", data=urllib.parse.urlencode(data).encode("utf-8"), method="POST")
    try:
        with urllib.request.urlopen(req): pass
    except: pass

def get_updates(offset=None):
    if not TOKEN:
        time.sleep(3)
        return []
    url = f"{BASE_URL}/getUpdates?timeout=30"
    if offset: url += f"&offset={offset}"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=35) as resp:
            return json.loads(resp.read().decode()).get("result", [])
    except:
        return []

main_menu = {
    "inline_keyboard": [
        [{"text": "💎 VIP Sertifika Satın Al", "url": "https://www.shopier.com/iOSEsingTR"}, {"text": "⚡️ UDID Kaydı Gönder", "callback_data": "send_udid_info"}],
        [{"text": "⭐ Profilim", "callback_data": "vip_profile"}, {"text": "🏆 Liderlik Tablosu", "callback_data": "vip_leaderboard"}],
        [{"text": "🎁 15 Davet Et, Ücretsiz Al!", "callback_data": "davet_menu"}, {"text": "🤖 AI Asistan", "callback_data": "ai_menu"}],
        [{"text": "🛠 İmza Araçları", "url": "https://t.me/iosipadosyalari"}, {"text": "💬 Canlı Destek", "url": "https://t.me/devolepercertificate"}]
    ]
}

main_back_kb = {"inline_keyboard": [[{"text": "🔙 Ana Menüye Dön", "callback_data": "main_menu"}]]}

print("🚀 Bot ve Mini App Sunucusu Başlatılıyor...")
offset = None

while True:
    try:
        updates = get_updates(offset)
        for update in updates:
            offset = update["update_id"] + 1
            
            # 1. Ödeme Ön Onay İstemi (Pre-Checkout Query)
            if "pre_checkout_query" in update:
                pcq = update["pre_checkout_query"]
                answer_pre_checkout_query(pcq["id"], ok=True)
                continue

            # 2. Başarılı Ödeme Yakalama -> Sana Bildirim Gider
            if "message" in update and "successful_payment" in update["message"]:
                s_msg = update["message"]
                s_chat_id = s_msg["chat"]["id"]
                s_user = s_msg["from"]
                s_uname = s_user.get("username", "Yok")
                s_fname = s_user.get("first_name", "İsimsiz")
                payment_info = s_msg["successful_payment"]
                total_stars = payment_info.get("total_amount")
                
                send_message(s_chat_id, f"🎉 **Ödemeniz Başarıyla Alındı!**\n\n⭐ Ödenen Yıldız: {total_stars}\n\nLütfen UDID kaydınızı iletin: @devolepercertificate")
                send_message(ADMIN_ID, f"💰 **YENİ YILDIZ SATIŞI GERÇEKLEŞTİ!**\n\n👤 Müşteri: {s_fname} (@{s_uname})\n🆔 ID: `{s_chat_id}`\n⭐ Tutar: {total_stars} Telegram Stars")
                continue

            # 3. Mini App'ten gelen veriyi yakala ve fatura gönder
            if "message" in update:
                msg = update["message"]
                chat_id = msg["chat"]["id"]
                
                if "web_app_data" in msg:
                    try:
                        w_data = json.loads(msg["web_app_data"]["data"])
                        if w_data.get("action") == "buy_stars":
                            p_adi = w_data.get("package")
                            p_yildiz = int(w_data.get("stars"))
                            send_message(chat_id, f"⭐ **{p_adi}** için ödeme faturası oluşturuluyor...")
                            send_invoice(chat_id, p_adi, f"{p_adi} - iOS Kurumsal Sertifika Lisansı", p_yildiz)
                    except Exception as e:
                        print("Web App veri işleme hatası:", e)
                    continue

                text = msg.get("text", "")
                fname = msg["chat"].get("first_name", "İsimsiz")
                uname = msg["chat"].get("username", "Yok")

                if text.startswith("/start"):
                    if chat_id not in kullanici_verileri:
                        kullanici_verileri[chat_id] = {"referrals": 1, "username": uname, "first_name": fname}
                        verileri_kaydet()
                    send_message(chat_id, "✨ **iOS Sertifika Botuna Hoşgeldiniz!**", main_menu)

            if "callback_query" in update:
                cq = update["callback_query"]
                cq_id = cq["id"]
                chat_id = cq["message"]["chat"]["id"]
                mid = cq["message"]["message_id"]
                data = cq["data"]
                answer_callback_query(cq_id)

                if data == "main_menu":
                    edit_message(chat_id, mid, "✨ **Ana Menü:**", main_menu)
                elif data == "vip_profile":
                    edit_message(chat_id, mid, f"👤 **Profil**\nID: `{chat_id}`", main_back_kb)
                elif data == "send_udid_info":
                    edit_message(chat_id, mid, "⚡️ UDID numaranızı destek hattına iletebilirsiniz.", main_back_kb)
    except Exception as e:
        print("Döngü hatası:", e)
        time.sleep(3)
