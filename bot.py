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
ADMIN_ID = 8578298882
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

# Zorunlu Kanallar Listesi (Kanal kullanıcı adları)
# NOT: Botun bu kanallarda YÖNETİCİ olması gerekir!
ZORUNLU_KANALLAR = ["iosipadosyalari", "iOSEsignTR"] 

# Bellek tabanlı veritabanı (Davet ve kayıtlar için)
# {user_id: {"referrals": 0, "username": "...", "first_name": "..."}}
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
        [{"text": "💎 VIP Sertifika (250₺)", "callback_data": "vip_cert"}, {"text": "⚡️ UDID Gönder", "callback_data": "send_udid_info"}],
        [{"text": "🔗 Davet Et & Kazan", "callback_data": "davet_menu"}, {"text": "🤖 AI Asistan Soru Sor", "callback_data": "ai_menu"}],
        [{"text": "🛠 Araçlar", "callback_data": "tools"}, {"text": "🛡 Avantajlar", "callback_data": "benefits"}],
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
    print("🚀 Havalı VIP AI Bot Davet ve Zorunlu Kanal Sistemiyle Dinliyor...")
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
                                # Davet eden kişiye bilgi ver
                                send_message(davet_eden_id, f"🎉 **Tebrikler!** Linkiniz üzerinden yeni biri katıldı.\n🔥 Toplam davet sayınız: **{ref_sayisi}**")

                    if chat_id not in kullanici_verileri:
                        kullanici_verileri[chat_id] = {"referrals": 0, "username": username, "first_name": first_name}

                    # 2. Zorunlu Kanal Kontrolü
                    if not kanallari_kontrol_et(chat_id):
                        sub_keyboard = {
                            "inline_keyboard": [
                                [{"text": "📢 Özel Kanala Katıl", "url": "https://t.me/+tMRpDvKKQ1JmNWVk"}],
                                [{"text": "📢 iOS IPA Dosyaları Katıl", "url": "https://t.me/iosipadosyalari"}],
                                [{"text": "📢 iOS E-Sign TR Katıl", "url": "https://t.me/iOSEsignTR"}],
                                [{"text": "✅ Katıldım, Kontrol Et", "callback_data": "kontrol_et"}]
                            ]
                        }
                        send_message(chat_id, "⚠️ **Botu kullanabilmek için aşağıdaki kanallarımıza abone olmanız gerekmektedir:**\n\nLütfen sırasıyla kanallara katıldıktan sonra aşağıdaki **'✅ Katıldım, Kontrol Et'** butonuna tıklayın.", sub_keyboard)
                        continue

                    # Kanallardaysa ve ilk kez tam giriş yapıyorsa admin'e bildirim at
                    if ADMIN_ID != 0 and chat_id != ADMIN_ID:
                        davet_bilgi = f"\n🔗 Davet Eden ID: `{davet_eden_id}`" if davet_eden_id else ""
                        send_message(ADMIN_ID, f"🔔 **Yeni Kullanıcı Botu Başlattı ve Kanallara Katıldı!**\n\n👤 İsim: {first_name}\nkünyesi: @{username}\n🆔 ID: `{chat_id}`{davet_bilgi}")

                    send_message(chat_id, f"✨ Merhaba **{first_name}**!\n\n👑 **Apple Developer VIP Ekosistemine** hoş geldin.\n\n🚀 Cihazını özgürleştirmek için aşağıdaki modern menüyü kullanabilir veya **AI Asistan** ile merak ettiklerini anında sorabilirsin:", main_menu)
                    
                elif user_states.get(chat_id) == "waiting_udid":
                    udid = text.strip()
                    if len(udid) < 20:
                        send_message(chat_id, "⚠️ Geçersiz UDID! Lütfen Safari'den `get.ud.me` adresine girip doğru kodu kopyala.")
                    else:
                        user_states.pop(chat_id, None)
                        if ADMIN_ID != 0:
                            send_message(ADMIN_ID, f"🚨 **Yeni UDID Gönderildi!**\n\n👤 Kullanıcı: @{username} ({first_name})\n🆔 ID: `{chat_id}`\n📲 UDID: `{udid}`")
                        send_message(chat_id, f"✅ **UDID Başarıyla Alındı!**\n`{udid}`\n\n🔥 İşlemi sonuçlandırmak için bu kodla birlikte yöneticimize yaz:\n👉 **@devolepercertificate**", back_keyboard)
                
                else:
                    # AI Chat / Soru Yanıtlama
                    q = text.lower()
                    if any(w in q for w in ["fiyat", "ne kadar", "ücret", "kaç tl"]):
                        reply = "💰 **Fiyat:** 1 Yıllık Tam Yetkili VIP Sertifika yalnızca **250₺**'dir.\n🛒 Satın alım: @devolepercertificate"
                    elif any(w in q for w in ["udid", "nasıl", "bulunur"]):
                        reply = "📱 **UDID:** Safari'den **`get.ud.me`** adresine girerek kolayca öğrenebilirsin."
                    elif any(w in q for w in ["güvenilir", "garanti", "patlar mı"]):
                        reply = "🛡 **Garanti:** 1 yıl boyunca tam güvence ve kesintisiz destek sağlanır."
                    elif any(w in q for w in ["süre", "saat", "ne kadar sürer"]):
                        reply = "⏳ **Teslimat Süresi:** UDID sisteme eklendikten sonra ortalama **1-3 saat** içinde hızlıca hazırlanır ve teslim edilir."
                    else:
                        reply = "🤖 **AI Asistan:** Detaylı bilgi almak ve işlem başlatmak için yetkili yöneticimizle görüşebilirsin:\n👉 **@devolepercertificate**"
                    send_message(chat_id, reply, back_keyboard)

            elif "callback_query" in update:
                query = update["callback_query"]
                chat_id = query["message"]["chat"]["id"]
                message_id = query["message"]["message_id"]
                data = query["data"]
                first_name = query["from"].get("first_name", "Kullanıcı")
                username = query["from"].get("username", "Yok")
                
                if data == "kontrol_et":
                    if kanallari_kontrol_et(chat_id):
                        delete_message(chat_id, message_id)
                        send_message(chat_id, "🎉 Tebrikler, kanallara katılımınız onaylandı!")
                        
                        # Admin'e kanalları geçtiğine dair bildirim
                        if ADMIN_ID != 0 and chat_id != ADMIN_ID:
                            send_message(ADMIN_ID, f"🚨 **Kullanıcı Kanalları Tamamladı ve Giriş Yaptı!**\n\n👤 İsim: {first_name}\nkünyesi: @{username}\n🆔 ID: `{chat_id}`")
                        
                        send_message(chat_id, f"✨ Merhaba **{first_name}**!\n\n👑 **Apple Developer VIP Ekosistemine** hoş geldin. Menüyü kullanmaya başlayabilirsin:", main_menu)
                    else:
                        # Uyarı bildirimi (Alert)
                        answer_data = {"callback_query_id": query["id"], "text": "❌ Henüz tüm kanallara katılmadınız! Lütfen kontrol edip tekrar deneyin.", "show_alert": True}
                        req = urllib.request.Request(f"{BASE_URL}/answerCallbackQuery", data=urllib.parse.urlencode(answer_data).encode("utf-8"), method="POST")
                        try:
                            with urllib.request.urlopen(req): pass
                        except: pass

                elif data == "main_menu":
                    user_states.pop(chat_id, None)
                    edit_message(chat_id, message_id, "✨ **VIP Ana Kontrol Paneli:**\nLütfen yapmak istediğiniz işlemi seçin:", main_menu)
                elif data == "ai_menu":
                    edit_message(chat_id, message_id, "🤖 **Yapay Zeka Bilgi Asistanı**\nAşağıdaki hızlı sorulara tıklayarak veya sohbete yazarak bilgi alabilirsin!", ai_chat_keyboard)
                elif data == "ai_fiyat":
                    edit_message(chat_id, message_id, "💰 **Fiyat:** 1 Yıllık VIP Sertifika **250₺**'dir.\n🛒 İletişim: @devolepercertificate", ai_chat_keyboard)
                elif data == "ai_udid":
                    edit_message(chat_id, message_id, "📱 **UDID:** Safari'den **`get.ud.me`** adresine gidip öğrenebilirsin.", ai_chat_keyboard)
                elif data == "ai_guven":
                    edit_message(chat_id, message_id, "🛡 **Güvenilirlik:** Sertifikalarımız 1 yıl tam garantilidir.", ai_chat_keyboard)
                elif data == "ai_sure":
                    edit_message(chat_id, message_id, "⏳ **Süreç:** UDID gönderildikten sonra ortalama **1-3 saat** içinde hızlıca teslim edilir.", ai_chat_keyboard)
                elif data == "vip_cert":
                    edit_message(chat_id, message_id, "💎 **1 Yıllık VIP Sertifika**\n• Fiyat: `250₺`\n• Garanti: 1 Yıl\n• Teslimat: 1-3 Saat\n\n🚀 İletişim: **@devolepercertificate**", back_keyboard)
                elif data == "send_udid_info":
                    user_states[chat_id] = "waiting_udid"
                    edit_message(chat_id, message_id, "⚡️ **UDID Gönderim Ekranı**\n\nSafari'den **`get.ud.me`** adresine girip UDID'ni kopyala ve **doğrudan bu sohbete mesaj olarak yaz!**", back_keyboard)
                elif data == "davet_menu":
                    bot_info_req = urllib.request.Request(f"{BASE_URL}/getMe")
                    try:
                        with urllib.request.urlopen(bot_info_req) as resp:
                            bot_username = json.loads(resp.read().decode())["result"]["username"]
                    except:
                        bot_username = "bot"
                    
                    ref_link = f"https://t.me/{bot_username}?start={chat_id}"
                    ref_sayisi = kullanici_verileri.get(chat_id, {"referrals": 0})["referrals"]
                    edit_message(chat_id, message_id, f"📌 **Davet Et - Kazan Sistemi:**\n\nArkadaşlarınızı davet ederek ödüller kazanabilirsiniz!\n\n🔗 **Kişisel Davet Linkiniz:**\n`{ref_link}`\n\n📊 Toplam Davet Ettiğiniz Kişi: **{ref_sayisi}**", back_keyboard)
                elif data == "benefits":
                    edit_message(chat_id, message_id, "🛡 **Avantajlar:**\n• Bilgisayarsız IPA kurulumu\n• Sınırsız uygulama\n• Esign, Scarlet ve GBox uyumu", back_keyboard)
                elif data == "tools":
                    edit_message(chat_id, message_id, "🛠 **Araçlar:**\n1️⃣ Esign\n2️⃣ Scarlet\n3️⃣ GBox", back_keyboard)
                elif data == "faq":
                    edit_message(chat_id, message_id, "❓ **SSS:**\nSertifikanız 1-3 saat içinde aktifleşir.\n\nİletişim: @devolepercertificate", back_keyboard)

        time.sleep(1)
else:
    print("⚠️ Botu başlatılamadı.")
