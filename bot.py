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

TOKEN = os.environ.get("BOT_TOKEN", "").strip()
ADMIN_ID = 8578298828
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

ZORUNLU_KANALLAR = ["ipaonay", "iosipadosyalari", "iOSEsignTR"]
VERI_DOSYASI = "kullanicilar.json"
kullanici_verileri = {}

if os.path.exists(VERI_DOSYASI):
    try:
        with open(VERI_DOSYASI, "r", encoding="utf-8") as f:
            kullanici_verileri = {int(k): v for k, v in json.load(f).items()}
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

def kanallari_kontrol_et(user_id):
    for kanal in ZORUNLU_KANALLAR:
        try:
            url = f"{BASE_URL}/getChatMember?chat_id=@{kanal}&user_id={user_id}"
            with urllib.request.urlopen(urllib.request.Request(url), timeout=10) as resp:
                res = json.loads(resp.read().decode())
                if res.get("ok"):
                    if res["result"].get("status") not in ["member", "administrator", "creator"]:
                        return False
                else:
                    return False
        except:
            return False
    return True

main_menu = {
    "inline_keyboard": [
        [{"text": "💎 VIP Sertifika Satın Al", "url": "https://www.shopier.com/iOSEsingTR"}, {"text": "⚡️ UDID Kaydı Gönder", "callback_data": "send_udid_info"}],
        [{"text": "⭐ Profilim & Kartım", "callback_data": "vip_profile"}, {"text": "🏆 Liderlik Tablosu", "callback_data": "vip_leaderboard"}],
        [{"text": "🎁 15 Davet Et, Ücretsiz Al!", "callback_data": "davet_menu"}, {"text": "🤖 AI Asistan", "callback_data": "ai_menu"}],
        [{"text": "🛠 İmza Araçları & IPA", "url": "https://t.me/iosipadosyalari"}, {"text": "🛡 Avantajlar & Garanti", "callback_data": "benefits"}],
        [{"text": "❓ SSS", "callback_data": "faq"}, {"text": "💬 Canlı Destek", "url": "https://t.me/devolepercertificate"}]
    ]
}

admin_menu = {
    "inline_keyboard": [
        [{"text": "📊 Bot İstatistikleri", "callback_data": "admin_stats"}, {"text": "📢 Toplu Duyuru", "callback_data": "admin_broadcast_prompt"}],
        [{"text": "🔗 Zorunlu Kanallar", "callback_data": "admin_channels"}, {"text": "🔄 API Sağlık Testi", "callback_data": "admin_test"}],
        [{"text": "👥 Kullanıcı Listesi", "callback_data": "admin_users"}, {"text": "🧹 Verileri Sıfırla", "callback_data": "admin_reset_confirm"}],
        [{"text": "🔙 Ana Menüye Dön", "callback_data": "main_menu"}]
    ]
}

back_kb = {"inline_keyboard": [[{"text": "🔙 Yönetime Dön", "callback_data": "admin_panel_back"}]]}
main_back_kb = {"inline_keyboard": [[{"text": "🔙 Ana Menüye Dön", "callback_data": "main_menu"}]]}
ai_kb = {
    "inline_keyboard": [
        [{"text": "💰 Fiyatlandırma Nedir?", "callback_data": "ai_fiyat"}, {"text": "📱 UDID Nasıl Bulunur?", "callback_data": "ai_udid"}],
        [{"text": "🛡 Sistem Güvenilir mi?", "callback_data": "ai_guven"}, {"text": "⏳ Süreç Ne Kadar Sürer?", "callback_data": "ai_sure"}],
        [{"text": "🔙 Ana Menüye Dön", "callback_data": "main_menu"}]
    ]
}

print("🚀 Bot Başlatılıyor...")
offset = None

while True:
    try:
        updates = get_updates(offset)
        for update in updates:
            offset = update["update_id"] + 1
            
            if "message" in update:
                msg = update["message"]
                chat_id = msg["chat"]["id"]
                text = msg.get("text", "")
                fname = msg["chat"].get("first_name", "İsimsiz")
                uname = msg["chat"].get("username", "Yok")
                
                if text.startswith("/duyuru ") and chat_id == ADMIN_ID:
                    d_metin = text[8:].strip()
                    g = 0
                    for uid in list(kullanici_verileri.keys()):
                        if uid != ADMIN_ID:
                            send_message(uid, f"📢 **DUYURU & GÜNCELLEME**\n\n{d_metin}")
                            g += 1
                    send_message(ADMIN_ID, f"✅ Duyuru {g} kullanıcıya iletildi.")
                    continue

                if text.startswith("/admin") and chat_id == ADMIN_ID:
                    send_message(ADMIN_ID, "👑 **Yönetim Paneli:**", admin_menu)
                    continue

                if text.startswith("/start"):
                    if chat_id not in kullanici_verileri and chat_id != ADMIN_ID:
                        kullanici_verileri[chat_id] = {"referrals": 0, "username": uname, "first_name": fname, "davet_eden": None, "davet_onaylandi": False}
                        verileri_kaydet()
                        send_message(ADMIN_ID, f"👤 Yeni Kullanıcı: {fname} (@{uname}) - Toplam: {len(kullanici_verileri)}")
                    elif chat_id not in kullanici_verileri:
                        kullanici_verileri[chat_id] = {"referrals": 0, "username": uname, "first_name": fname, "davet_eden": None, "davet_onaylandi": False}
                        verileri_kaydet()

                    args = text.split()
                    if len(args) > 1 and args[1].isdigit():
                        did = int(args[1])
                        if did != chat_id and did in kullanici_verileri:
                            if not kullanici_verileri[chat_id].get("davet_eden"):
                                kullanici_verileri[chat_id]["davet_eden"] = did
                                verileri_kaydet()

                    if chat_id == ADMIN_ID:
                        send_message(ADMIN_ID, "👑 Admin olarak oturum açıldı. /admin yazabilirsin.", main_menu)
                        continue

                    if not kanallari_kontrol_et(chat_id):
                        sub_kb = {
                            "inline_keyboard": [
                                [{"text": "📢 Özel Kanala Katıl", "url": "https://t.me/+tMRpDvKKQ1JmNWVk"}],
                                [{"text": "📢 IPA Onay Kanalı", "url": "https://t.me/ipaonay"}],
                                [{"text": "📢 iOS IPA Dosyaları", "url": "https://t.me/iosipadosyalari"}],
                                [{"text": "📢 iOSEsignTR Kanalı", "url": "https://t.me/iOSEsignTR"}],
                                [{"text": "✅ Katıldım Kontrol Et", "callback_data": "check_subscription"}]
                            ]
                        }
                        send_message(chat_id, "⚠️ **Eksik Abonelik!** Devam etmek için kanallarımıza katılmalısın.", sub_kb)
                    else:
                        send_message(chat_id, "✨ **Ekosisteme Hoş Geldin!**", main_menu)

            if "callback_query" in update:
                cq = update["callback_query"]
                cq_id = cq["id"]
                chat_id = cq["message"]["chat"]["id"]
                mid = cq["message"]["message_id"]
                data = cq["data"]
                answer_callback_query(cq_id)

                if data == "main_menu":
                    edit_message(chat_id, mid, "✨ **Ana Menü:**", main_menu)
                elif data == "admin_panel_back" and chat_id == ADMIN_ID:
                    edit_message(chat_id, mid, "👑 **Yönetim Paneli:**", admin_menu)
                elif data == "admin_stats" and chat_id == ADMIN_ID:
                    edit_message(chat_id, mid, f"📊 Toplam Kullanıcı: {len(kullanici_verileri)}", back_kb)
                elif data == "admin_broadcast_prompt" and chat_id == ADMIN_ID:
                    edit_message(chat_id, mid, "📢 Duyuru için: `/duyuru Mesajınız` yazın.", back_kb)
                elif data == "admin_channels" and chat_id == ADMIN_ID:
                    edit_message(chat_id, mid, "🔗 Kanallar: " + ", ".join(ZORUNLU_KANALLAR), back_kb)
                elif data == "admin_test" and chat_id == ADMIN_ID:
                    edit_message(chat_id, mid, "🔄 Durum: Aktif", back_kb)
                elif data == "admin_users" and chat_id == ADMIN_ID:
                    son = list(kullanici_verileri.items())[-5:]
                    txt = "👥 Son Kullanıcılar:\n" + "".join([f"• {u['first_name']} (@{u['username']})\n" for uid, u in son]) if son else "Kayıt yok."
                    edit_message(chat_id, mid, txt, back_kb)
                elif data == "admin_reset_confirm" and chat_id == ADMIN_ID:
                    r_kb = {"inline_keyboard": [[{"text": "⚠️ EVET SIFIRLA", "callback_data": "admin_reset_exec"}], [{"text": "🔙 Vazgeç", "callback_data": "admin_panel_back"}]]}
                    edit_message(chat_id, mid, "⚠️ Tüm veriler silinecek?", r_kb)
                elif data == "admin_reset_exec" and chat_id == ADMIN_ID:
                    kullanici_verileri.clear()
                    verileri_kaydet()
                    edit_message(chat_id, mid, "🧹 Veritabanı sıfırlandı.", back_kb)
                elif data == "vip_profile":
                    d_sayi = kullanici_verileri.get(chat_id, {}).get("referrals", 0)
                    edit_message(chat_id, mid, f"👤 **Profil Kartı**\nID: `{chat_id}`\nDavet Puanı: {d_sayi}/15", main_back_kb)
                elif data == "vip_leaderboard":
                    sira = sorted(kullanici_verileri.items(), key=lambda x: x[1].get("referrals", 0), reverse=True)[:3]
                    lb = "🏆 **Liderlik Tablosu**\n\n" + ("\n".join([f"• {u['first_name']}: {u['referrals']} Davet" for uid, u in sira]) if sira else "Henüz veri yok.")
                    edit_message(chat_id, mid, lb, main_back_kb)
                elif data == "send_udid_info":
                    edit_message(chat_id, mid, "⚡️ UDID numaranızı destek hattına iletebilirsiniz.", main_back_kb)
                elif data == "davet_menu":
                    rlink = f"https://t.me/SertifikaMagazaBot?start={chat_id}"
                    ds = kullanici_verileri.get(chat_id, {}).get("referrals", 0)
                    edit_message(chat_id, mid, f"🎁 **Davet Et Kazan**\nLinkin:\n`{rlink}`\nDavetlerin: {ds}/15", main_back_kb)
                elif data == "ai_menu":
                    edit_message(chat_id, mid, "🤖 **AI Asistan Menüsü:**", ai_kb)
                elif data == "benefits":
                    edit_message(chat_id, mid, "🛡 **Avantajlar:** 1 Yıl Garanti ve Revoke değişimi.", main_back_kb)
                elif data == "faq":
                    edit_message(chat_id, mid, "❓ **SSS:** İşlemler kısa sürede onaylanır.", main_back_kb)
                elif data == "check_subscription":
                    if kanallari_kontrol_et(chat_id):
                        delete_message(chat_id, mid)
                        send_message(chat_id, "✨ Kanallar doğrulandı!", main_menu)
                    else:
                        send_message(chat_id, "⚠️ Eksik kanallar var, lütfen tamamlayın.")
                elif data in ["ai_fiyat", "ai_udid", "ai_guven", "ai_sure"]:
                    cevaplar = {
                        "ai_fiyat": "💰 Fiyatlar Shopier mağazamızda yer almaktadır.",
                        "ai_udid": "📱 UDID bulmak için [Get My UDID](https://get.udid.io) kullanabilirsiniz.",
                        "ai_guven": "🛡 Sistemimiz %100 güvenlidir.",
                        "ai_sure": "⏳ İşlemler hızla tamamlanır."
                    }
                    edit_message(chat_id, mid, cevaplar[data], ai_kb)
    except Exception as e:
        print("Döngü hatası:", e)
        time.sleep(3)
