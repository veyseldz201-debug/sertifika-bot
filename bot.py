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
                
                send_message(davet_eden, f"🎉 **Tebrikler!** Davet ettiğin kişi kanallara katıldı ve doğrulandı **(+1 Davet Eklendi)**.\n🔥 Toplam davet sayın: **{ref_sayisi} / 15**")
                
                if ref_sayisi >= 15:
                    send_message(ADMIN_ID, f"🏆 **ÖDÜL KAZANAN ÇIKTI!**\n\n👤 Kullanıcı: {first_name} (@{username})\n🆔 ID: `{davet_eden}`\n🔥 15 arkadaşını davet etti ve ücretsiz sertifika hakkı kazandı!")

main_menu = {
    "inline_keyboard": [
        [{"text": "💎 Vip Sertifika Al", "url": "https://www.shopier.com/iOSEsingTR"}, {"text": "⚡️ UDID Gönder", "callback_data": "send_udid_info"}],
        [{"text": "📱 UDID Nereden Bakılır?", "callback_data": "udid_nasil_bakilir"}],
        [{"text": "🎁 15 Davet Et, Ücretsiz Al!", "callback_data": "davet_menu"}, {"text": "🤖 AI Asistan", "callback_data": "ai_menu"}],
        [{"text": "🛠 Araçlar & Uygulamalar", "callback_data": "tools"}, {"text": "🛡 Avantajlar", "callback_data": "benefits"}],
        [{"text": "❓ SSS", "callback_data": "faq"}, {"text": "💬 Canlı Destek (Admin)", "url": "https://t.me/devolepercertificate"}]
    ]
}

admin_menu = {
    "inline_keyboard": [
        [{"text": "📊 Bot İstatistikleri", "callback_data": "admin_stats"}],
        [{"text": "📢 Toplu Mesaj Duyurusu", "callback_data": "admin_broadcast_info"}],
        [{"text": "🔙 Ana Menüye Dön", "callback_data": "main_menu"}]
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
    print("🚀 Bot Aktif ve Çalışıyor...")
    send_message(ADMIN_ID, "🚀 **Bot Başlatıldı!**\n\nAdmin paneli aktif (`/admin` yazarak erişebilirsin).")
    
    offset = None

    while True:
        updates = get_updates(offset)
        for update in updates:
            offset = update["update_id"] + 1
            
            if "message" in update:
                msg = update["message"]
                chat_id = msg["chat"]["id"]
                text = msg.get("text", "")
                first_name = msg["chat"].get("first_name", "İsimsiz")
                username = msg["chat"].get("username", "Kullanıcı adı yok")
                
                if text.startswith("/admin") and chat_id == ADMIN_ID:
                    send_message(ADMIN_ID, "👑 **Admin Paneline Hoş Geldin!**\n\nAşağıdaki yönetim panelinden botu kontrol edebilirsin:", admin_menu)
                    continue

                if text.startswith("/start"):
                    args = text.split()
                    
                    if chat_id not in kullanici_verileri and chat_id != ADMIN_ID:
                        kullanici_verileri[chat_id] = {"referrals": 0, "username": username, "first_name": first_name, "davet_eden": None, "davet_onaylandi": False}
                        toplam_kullanici = len(kullanici_verileri)
                        admin_mesaji = (
                            f"👤 **Yeni Kullanıcı Katıldı!**\n\n"
                            f"📌 Sıra: **{toplam_kullanici}. Kullanıcı**\n"
                            f"İsim: {first_name}\n"
                            f"Kullanıcı Adı: @{username}\n"
                            f"ID: `{chat_id}`"
                        )
                        send_message(ADMIN_ID, admin_mesaji)
                    elif chat_id not in kullanici_verileri:
                        kullanici_verileri[chat_id] = {"referrals": 0, "username": username, "first_name": first_name, "davet_eden": None, "davet_onaylandi": False}

                    if len(args) > 1 and args[1].isdigit():
                        davet_eden_id = int(args[1])
                        if davet_eden_id != chat_id and davet_eden_id in kullanici_verileri:
                            if not kullanici_verileri[chat_id].get("davet_eden"):
                                kullanici_verileri[chat_id]["davet_eden"] = davet_eden_id

                    if chat_id == ADMIN_ID:
                        send_message(ADMIN_ID, "👑 **Admin Olarak Botu Başlattın!**\n\nYönetim paneline erişmek için /admin yazabilirsin.", main_menu)
                        continue

                    if not kanallari_kontrol_et(chat_id):
                        sub_keyboard = {
                            "inline_keyboard": [
                                [{"text": "📢 Özel Kanala Katıl", "url": "https://t.me/+tMRpDvKKQ1JmNWVk"}],
                                [{"text": "📢 IPA Onay Kanalı", "url": "https://t.me/ipaonay"}],
                                [{"text": "📢 iOS IPA Dosyaları", "url": "https://t.me/iosipadosyalari"}],
                                [{"text": "📢 iOSEsignTR Kanalı", "url": "https://t.me/iOSEsignTR"}],
                                [{"text": "✅ Katıldım Kontrol Et", "callback_data": "check_subscription"}]
                            ]
                        }
                        send_message(chat_id, "⚠️ Botu kullanabilmek için yukarıdaki kanallarımıza abone olmanız gerekmektedir.", sub_keyboard)
                    else:
                        daveti_onayla_ve_ver(chat_id, first_name, username)
                        send_message(chat_id, "✨ **Merhaba !**\n\n👑 Apple Developer VIP Ekosistemine hoş geldin.\n\n🚀 Cihazını özgürleştirmek için aşağıdaki modern menüyü kullanabilir veya AI Asistan ile merak ettiklerini anında sorabilirsin:", main_menu)

            elif "callback_query" in update:
                cq = update["callback_query"]
                cq_id = cq["id"]
                chat_id = cq["message"]["chat"]["id"]
                message_id = cq["message"]["message_id"]
                data = cq["data"]
                first_name = cq["from"].get("first_name", "İsimsiz")
                username = cq["from"].get("username", "Kullanıcı adı yok")
                
                answer_callback_query(cq_id)
                
                if data == "main_menu":
                    if chat_id == ADMIN_ID:
                        edit_message(chat_id, message_id, "✨ **Ana Menü (Admin Görünümü):**", main_menu)
                    else:
                        edit_message(chat_id, message_id, "✨ **Ana Menü:**\n\nCihazını özgürleştirmek için aşağıdaki seçenekleri kullanabilirsin:", main_menu)
                
                elif data == "admin_stats" and chat_id == ADMIN_ID:
                    toplam_kullanici = len(kullanici_verileri)
                    istatistik_metni = (
                        f"📊 **Admin İstatistik Paneli**\n\n"
                        f"👥 Toplam Tekil Kullanıcı: **{toplam_kullanici}**\n\n"
                        f"📌 **Son Kayıt Olanlar:**\n"
                    )
                    son_kullanicilar = list(kullanici_verileri.items())[-10:]
                    for uid, udata in son_kullanicilar:
                        istatistik_metni += f"• {udata['first_name']} (@{udata['username']}) - Ref: {udata['referrals']}\n"
                    edit_message(chat_id, message_id, istatistik_metni, admin_menu)

                elif data == "admin_broadcast_info" and chat_id == ADMIN_ID:
                    edit_message(chat_id, message_id, "📢 **Toplu Mesaj Bilgilendirmesi:**\n\nŞu an sistem hafıza tabanlı çalıştığı için tüm kullanıcılara anlık duyuru göndermek üzere /stats panelinden kullanıcı sayısını takip edebilirsin.", admin_menu)

                elif data == "send_udid_info":
                    edit_message(chat_id, message_id, "⚡️ **UDID Gönderme Rehberi:**\n\nSertifikanın tanımlanabilmesi için cihazının UDID numarasını bize iletmen gerekiyor.", back_keyboard)
                elif data == "udid_nasil_bakilir":
                    edit_message(chat_id, message_id, "📱 **UDID Nereden Bakılır?**\n\nSafari tarayıcından UDID öğrenme sitelerine girerek kolayca öğrenebilirsin.", back_keyboard)
                elif data == "davet_menu":
                    ref_link = f"https://t.me/SertifikaMagazaBot?start={chat_id}"
                    davet_sayisi = kullanici_verileri.get(chat_id, {}).get("referrals", 0)
                    
                    if davet_sayisi >= 15:
                        davet_metni = (
                            f"🎁 **15 Davet Et, Ücretsiz Sertifika Al!**\n\n"
                            f"🎉 **Tebrikler! 15 Davet Hedefine Ulaştın!**\n"
                            f"✅ Başarılı bir şekilde tamamladın.\n"
                            f"💬 Ödülünü alabilmek için **@devolepercertificate** ile iletişime geç!\n\n"
                            f"🔥 **Mevcut Davetlerin:** {davet_sayisi} / 15\n\n"
                            f"ℹ️ *Herkesin yalnızca 1 sertifika kazanma hakkı mevcuttur.*"
                        )
                    else:
                        davet_metni = (
                            f"🎁 **15 Davet Et, Ücretsiz Sertifika Al!**\n\n"
                            f"Arkadaşlarını davet et, 15 kişiye ulaştığında VIP Sertifikan bizden hediye!\n\n"
                            f"🔗 **Senin Davet Linkin:**\n`{ref_link}`\n\n"
                            f"🔥 **Mevcut Davetlerin:** {davet_sayisi} / 15\n\n"
                            f"ℹ️ *Herkesin yalnızca 1 sertifika kazanma hakkı mevcuttur.*"
                        )
                    edit_message(chat_id, message_id, davet_metni, back_keyboard)
                elif data == "ai_menu":
                    edit_message(chat_id, message_id, "🤖 **AI Asistan'a Hoş Geldin!**\n\nAşağıdaki hazır sorulardan birini seçerek anında bilgi alabilirsin:", ai_chat_keyboard)
                elif data == "tools":
                    edit_message(chat_id, message_id, "🛠 **Araçlar & Uygulamalar:**\n\nSiedloading ve imzalama araçları hakkında bilgi alabilirsin.", back_keyboard)
                elif data == "benefits":
                    edit_message(chat_id, message_id, "🛡 **VIP Avantajları:**\n\n• 1 Yıl Garantili Sertifika\n• Revoke durumunda ücretsiz değişim", back_keyboard)
                elif data == "faq":
                    edit_message(chat_id, message_id, "❓ **Sık Sorulan Sorular (SSS):**\n\nSertifikanız ödeme sonrası kısa sürede aktif edilir.", back_keyboard)
                elif data == "check_subscription":
                    if kanallari_kontrol_et(chat_id):
                        daveti_onayla_ve_ver(chat_id, first_name, username)
                        delete_message(chat_id, message_id)
                        send_message(chat_id, "✨ **Harika! Kanallara katılımınız onaylandı.**", main_menu)
                    else:
                        send_message(chat_id, "⚠️ Henüz tüm açık kanallara abone olmamış görünüyorsun. Lütfen kontrol edip tekrar dene.")
                elif data in ["ai_fiyat", "ai_udid", "ai_guven", "ai_sure"]:
                    cevaplar = {
                        "ai_fiyat": "💰 VIP Sertifika fiyatımız Shopier mağazamızda sunulmaktadır.",
                        "ai_udid": "📱 UDID, Apple cihazınıza ait özel 40 haneli bir kimlik numarasıdır.",
                        "ai_guven": "🛡 Sistemimiz tamamen güvenlidir ve binlerce mutlu müşterimiz bulunmaktadır.",
                        "ai_sure": "⏳ İşlemler genellikle ödeme onayından sonra kısa sürede tamamlanır."
                    }
                    edit_message(chat_id, message_id, cevaplar[data], ai_chat_keyboard)
