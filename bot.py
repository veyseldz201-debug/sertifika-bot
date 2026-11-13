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

# Token gizli olarak Render Environment Variables içerisinden alınır (GitHub uyarısı almazsın)
TOKEN = os.environ.get("BOT_TOKEN", "").strip()
ADMIN_ID = 8578298828
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

ZORUNLU_KANALLAR = ["ipaonay", "iosipadosyalari", "iOSEsignTR"]
VERI_DOSYASI = "kullanicilar.json"

def verileri_yukle():
    if os.path.exists(VERI_DOSYASI):
        try:
            with open(VERI_DOSYASI, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def verileri_kaydet():
    try:
        with open(VERI_DOSYASI, "w", encoding="utf-8") as f:
            json.dump(kullanici_verileri, f, ensure_ascii=False, indent=4)
    except:
        pass

kullanici_verileri = {int(k): v for k, v in verileri_yukle().items()}

def send_message(chat_id, text, reply_markup=None):
    if not TOKEN:
        return
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
    if not TOKEN:
        return
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
    if not TOKEN:
        return
    data = {"chat_id": chat_id, "message_id": message_id}
    req = urllib.request.Request(f"{BASE_URL}/deleteMessage", data=urllib.parse.urlencode(data).encode("utf-8"), method="POST")
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except:
        pass

def answer_callback_query(callback_query_id, text=""):
    if not TOKEN:
        return
    data = {"callback_query_id": callback_query_id, "text": text, "show_alert": False}
    req = urllib.request.Request(f"{BASE_URL}/answerCallbackQuery", data=urllib.parse.urlencode(data).encode("utf-8"), method="POST")
    try:
        with urllib.request.urlopen(req):
            pass
    except:
        pass

def get_updates(offset=None):
    if not TOKEN:
        time.sleep(3)
        return []
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
                verileri_kaydet()
                ref_sayisi = kullanici_verileri[davet_eden]["referrals"]
                
                send_message(davet_eden, f"💎 **DAVET SİSTEMİ**\n\n🎉 Davet ettiğin kullanıcı resmi kanallara katıldı ve doğrulandı!\n➕ **Hesabına +1 Puan Eklendi.**\n🔥 Toplam İlerlemen: **{ref_sayisi} / 15**")
                
                if ref_sayisi >= 15:
                    send_message(ADMIN_ID, f"🏆 **KRİTİK BAŞARI: 15 DAVET TAMAMLANDI!**\n\n👤 Kullanıcı: {first_name} (@{username})\n🆔 ID: `{davet_eden}`\n🔥 Ücretsiz Sertifika hakkını kazandı!")

def check_bot():
    if not TOKEN:
        print("❌ HATA: BOT_TOKEN çevre değişkeni (Environment Variable) tanımlanmamış!")
        return False
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
        [{"text": "👥 Kullanıcı Listesi (Son 5)", "callback_data": "admin_users"}, {"text": "🧹 Verileri Sıfırla", "callback_data": "admin_reset_confirm"}],
        [{"text": "🔙 Normal Ana Menüye Dön", "callback_data": "main_menu"}]
    ]
}

back_keyboard = {
    "inline_keyboard": [[{"text": "🔙 Yönetim Paneline Dön", "callback_data": "admin_panel_back"}]]
}

main_back_keyboard = {
    "inline_keyboard": [[{"text": "🔙 Ana Menüye Dön", "callback_data": "main_menu"}]]
}

ai_chat_keyboard = {
    "inline_keyboard": [
        [{"text": "💰 Fiyatlandırma Nedir?", "callback_data": "ai_fiyat"}, {"text": "📱 UDID Nasıl Bulunur?", "callback_data": "ai_udid"}],
        [{"text": "🛡 Sistem Güvenilir mi?", "callback_data": "ai_guven"}, {"text": "⏳ Süreç Ne Kadar Sürer?", "callback_data": "ai_sure"}],
        [{"text": "🔙 Ana Menüye Dön", "callback_data": "main_menu"}]
    ]
}

if check_bot():
    print("🚀 Bot Aktif ve Çalışıyor...")
    send_message(ADMIN_ID, "🚀 **Sertifika Botu Başlatıldı!**\n\nGüvenli token mimarisi ve tüm özellikler aktif.")

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
                    first_name = msg["chat"].get("first_name", "İsimsiz")
                    username = msg["chat"].get("username", "Kullanıcı adı yok")
                    
                    if text.startswith("/duyuru ") and chat_id == ADMIN_ID:
                        duyuru_metni = text[8:].strip()
                        gonderilen = 0
                        for uid in list(kullanici_verileri.keys()):
                            if uid != ADMIN_ID:
                                send_message(uid, f"📢 **DUYURU & GÜNCELLEME**\n\n{duyuru_metni}")
                                gonderilen += 1
                        send_message(ADMIN_ID, f"✅ Duyuru başarıyla **{gonderilen}** aktif kullanıcıya iletildi.")
                        continue

                    if text.startswith("/admin") and chat_id == ADMIN_ID:
                        send_message(ADMIN_ID, "👑 **Yönetim Paneline Hoş Geldin!**\n\nSistemi tam yetkiyle yönetmek için aşağıdaki paneli kullanabilirsin:", admin_menu)
                        continue

                    if text.startswith("/start"):
                        args = text.split()
                        
                        if chat_id not in kullanici_verileri and chat_id != ADMIN_ID:
                            kullanici_verileri[chat_id] = {"referrals": 0, "username": username, "first_name": first_name, "davet_eden": None, "davet_onaylandi": False}
                            verileri_kaydet()
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
                            verileri_kaydet()

                        if len(args) > 1 and args[1].isdigit():
                            davet_eden_id = int(args[1])
                            if davet_eden_id != chat_id and davet_eden_id in kullanici_verileri:
                                if not kullanici_verileri[chat_id].get("davet_eden"):
                                    kullanici_verileri[chat_id]["davet_eden"] = davet_eden_id
                                    verileri_kaydet()

                        if chat_id == ADMIN_ID:
                            send_message(ADMIN_ID, "👑 **Admin Olarak Oturum Açıldı!**\n\nPaneli açmak için /admin komutunu gönderebilirsin.", main_menu)
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
                            send_message(chat_id, "⚠️ **Eksik Abonelik!** Botun özelliklerinden faydalanabilmek için yukarıdaki resmi kanallarımıza abone olmalısınız.", sub_keyboard)
                        else:
                            daveti_onayla_ve_ver(chat_id, first_name, username)
                            send_message(chat_id, "✨ **Apple Developer Ekosistemine Hoş Geldin!**\n\n👑 Cihazını tamamen özgürleştirmek, imza araçlarına erişmek ve özel ayrıcalıklardan yararlanmak için aşağıdaki menüyü kullanabilirsin:", main_menu)

                if "callback_query" in update:
                    cq = update["callback_query"]
                    cq_id = cq["id"]
                    chat_id = cq["message"]["chat"]["id"]
                    message_id = cq["message"]["message_id"]
                    data = cq["data"]
                    first_name = cq["from"].get("first_name", "İsimsiz")
                    username = cq["from"].get("username", "Kullanıcı adı yok")
                    
                    answer_callback_query(cq_id)
                    
                    if chat_id != ADMIN_ID and not kanallari_kontrol_et(chat_id) and data != "check_subscription":
                        sub_keyboard = {
                            "inline_keyboard": [
                                [{"text": "📢 Özel Kanala Katıl", "url": "https://t.me/+tMRpDvKKQ1JmNWVk"}],
                                [{"text": "📢 IPA Onay Kanalı", "url": "https://t.me/ipaonay"}],
                                [{"text": "📢 iOS IPA Dosyaları", "url": "https://t.me/iosipadosyalari"}],
                                [{"text": "📢 iOSEsignTR Kanalı", "url": "https://t.me/iOSEsignTR"}],
                                [{"text": "✅ Katıldım Kontrol Et", "callback_data": "check_subscription"}]
                            ]
                        }
                        edit_message(chat_id, message_id, "⚠️ **Güvenlik Uyarısı: Kanallardan ayrıldığınız tespit edildi!** Botu kullanmaya devam edebilmek için lütfen tekrar katılın:", sub_keyboard)
                        continue

                    if data == "main_menu":
                        if chat_id == ADMIN_ID:
                            edit_message(chat_id, message_id, "✨ **Ana Menü (Admin Görünümü):**\n\nYönetim paneline dönmek için /admin yazabilirsin.", main_menu)
                        else:
                            edit_message(chat_id, message_id, "✨ **Ana Menü:**\n\nCihazını özgürleştirmek için aşağıdaki seçenekleri kullanabilirsin:", main_menu)
                    
                    elif data == "admin_panel_back" and chat_id == ADMIN_ID:
                        edit_message(chat_id, message_id, "👑 **Yönetim Paneli:**", admin_menu)

                    elif data == "admin_stats" and chat_id == ADMIN_ID:
                        toplam_kullanici = len(kullanici_verileri)
                        istatistik_metni = (
                            f"📊 **İstatistik ve Durum Paneli**\n\n"
                            f"👥 Toplam Tekil Kullanıcı: **{toplam_kullanici}**\n"
                            f"🛡 Kalıcı Hafıza: **Aktif (JSON)**\n"
                        )
                        edit_message(chat_id, message_id, istatistik_metni, back_keyboard)

                    elif data == "admin_broadcast_prompt" and chat_id == ADMIN_ID:
                        edit_message(chat_id, message_id, "📢 **Toplu Duyuru Gönderimi:**\n\nTüm kullanıcılara anlık bildirim göndermek için sohbete:\n`/duyuru Mesajınız`\nşeklinde yazıp gönderebilirsin.", back_keyboard)

                    elif data == "admin_channels" and chat_id == ADMIN_ID:
                        kanal_listesi = "\n".join([f"• @{k}" for k in ZORUNLU_KANALLAR])
                        edit_message(chat_id, message_id, f"🔗 **Aktif Zorunlu Kanal Denetimi:**\n\n{kanal_listesi}\n\n🛡 Otomatik denetim mekanizması devrede.", back_keyboard)

                    elif data == "admin_test" and chat_id == ADMIN_ID:
                        durum = "✅ Kararlı ve Çalışıyor" if check_bot() else "❌ Kritik Hata"
                        edit_message(chat_id, message_id, f"🔄 **API & Sunucu Sağlık Testi:**\n\nDurum: {durum}\nBağlantı Türü: HTTPS / 24/7 Render", back_keyboard)

                    elif data == "admin_users" and chat_id == ADMIN_ID:
                        son_kullanicilar = list(kullanici_verileri.items())[-5:]
                        u_metni = "👥 **Son Kayıt Olan 5 Kullanıcı:**\n\n"
                        if not son_kullanicilar:
                            u_metni += "Henüz kayıtlı kullanıcı yok."
                        else:
                            for uid, udata in son_kullanicilar:
                                u_metni += f"• {udata['first_name']} (@{udata['username']}) - Davet: {udata['referrals']}\n"
                        edit_message(chat_id, message_id, u_metni, back_keyboard)

                    elif data == "admin_reset_confirm" and chat_id == ADMIN_ID:
                        reset_kb = {
                            "inline_keyboard": [
                                [{"text": "⚠️ EVET, VERİLERİ SIFIRLA", "callback_data": "admin_reset_exec"}],
                                [{"text": "🔙 Vazgeç / Geri Dön", "callback_data": "admin_panel_back"}]
                            ]
                        }
                        edit_message(chat_id, message_id, "⚠️ **DİKKAT:** Tüm kullanıcı kayıtları silinecek. Emin misiniz?", reset_kb)

                    elif data == "admin_reset_exec" and chat_id == ADMIN_ID:
                        kullanici_verileri.clear()
                        verileri_kaydet()
                        edit_message(chat_id, message_id, "🧹 **Veritabanı Sıfırlandı!** Tüm kullanıcı verileri temizlendi.", back_keyboard)

                    elif data == "vip_profile":
                        davet_sayisi = kullanici_verileri.get(chat_id, {}).get("referrals", 0)
                        profil_metni = (
                            f"👤 **Kullanıcı Profil Kartı**\n\n"
                            f"🆔 Telegram ID: `{chat_id}`\n"
                            f"⭐ Üyelik Seviyesi: **Standart Üye**\n"
                            f"🎁 Mevcut Davet Puanın: **{davet_sayisi} / 15**\n"
                            f"🛡 Sertifika Hakkı Limiti: **1 / 1**\n\n"
                            f"💎 *Sistem tarafından güvenliğiniz onaylanmıştır.*"
                        )
                        edit_message(chat_id, message_id, profil_metni, main_back_keyboard)

                    elif data == "vip_leaderboard":
                        sirali_kullanicilar = sorted(kullanici_verileri.items(), key=lambda x: x[1].get("referrals", 0), reverse=True)[:3]
                        lb_metni = "🏆 **Liderlik Tablosu**\n\nEn çok arkadaşını davet eden üyelerimiz:\n\n"
                        if not sirali_kullanicilar or sirali_kullanicilar[0][1].get("referrals", 0) == 0:
                            lb_metni += "📌 Henüz liderlik tablosunda listelenen aktif veri bulunmuyor. İlk sıra senin olabilir!"
                        else:
                             sira = 1
                             emojiler = ["🥇", "🥈", "🥉"]
                             for uid, udata in sirali_kullanicilar:
                                 if udata.get("referrals", 0) > 0:
                                     lb_metni += f"{emojiler[sira-1]} {udata['first_name']} — **{udata['referrals']} Davet**\n"
                                     sira += 1
                        edit_message(chat_id, message_id, lb_metni, main_back_keyboard)

                    elif data == "send_udid_info":
                        edit_message(chat_id, message_id, "⚡️ **UDID Kayıt & Gönderim Rehberi:**\n\nSertifikanın Apple sistemlerine kusursuz tanımlanabilmesi için UDID numaranızı destek hattımıza iletmeniz gerekmektedir.", main_back_keyboard)
                    elif data == "udid_nasil_bakilir":
                        edit_message(chat_id, message_id, "📱 **UDID Nereden ve Nasıl Bulunur?**\n\nCihazınızın 40 haneli UDID numarasını öğrenmek için [Get My UDID](https://get.udid.io) veya benzeri güvenli tarayıcı araçlarını kullanabilirsiniz.", main_back_keyboard)
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
                                f"Arkadaşlarını davet et, 15 kişiye ulaştığında 1 Yıl Garantili Sertifikan bizden hediye!\n\n"
                                f"🔗 **Senin Davet Linkin:**\n`{ref_link}`\n\n"
                                f"🔥 **Mevcut Davetlerin:** {davet_sayisi} / 15\n\n"
                                f"ℹ️ *Herkesin yalnızca 1 sertifika kazanma hakkı mevcuttur.*"
                            )
                        edit_message(chat_id, message_id, davet_metni, main_back_keyboard)
                    elif data == "ai_menu":
                        edit_message(chat_id, message_id, "🤖 **AI Destek Asistanı:**\n\nAşağıdaki akıllı konu başlıklarından birini seçerek anında bilgi alabilirsin:", ai_chat_keyboard)
                    elif data == "benefits":
                        edit_message(chat_id, message_id, "🛡 **Avantajlar & Garanti Paketi:**\n\n• **1 Yıl Kesintisiz Garanti:** Süre boyunca güvenli kullanım.\n• **Ücretsiz Revoke Değişimi:** Olası iptallerde anında yeni sertifika.\n• **Öncelikli Destek:** 7/24 hat üzerinden hızlı çözüm.", main_back_keyboard)
                    elif data == "faq":
                        edit_message(chat_id, message_id, "❓ **Sık Sorulan Sorular (SSS):**\n\nSertifikanız ödeme veya ödül onayı sonrasında çok kısa bir süre içinde aktif edilmektedir.", main_back_keyboard)
                    elif data == "check_subscription":
                        if kanallari_kontrol_et(chat_id):
                            daveti_onayla_ve_ver(chat_id, first_name, username)
                            delete_message(chat_id, message_id)
                            send_message(chat_id, "✨ **Harika! Kanallara katılımınız başarıyla doğrulandı.**", main_menu)
                        else:
                            send_message(chat_id, "⚠️ Henüz tüm zorunlu kanallara abone olmamış görünüyorsun. Lütfen eksikleri tamamlayıp tekrar dene.")
                    elif data in ["ai_fiyat", "ai_udid", "ai_guven", "ai_sure"]:
                        cevaplar = {
                            "ai_fiyat": "💰 Sertifika fiyatlarımız ve avantajlı paketlerimiz Shopier mağazamızda güvenle sunulmaktadır.",
                            "ai_udid": "📱 UDID, Apple cihazınıza özel olarak atanan 40 haneli eşsiz bir donanım kimliğidir. Öğrenmek için [Get My UDID](https://get.udid.io) sitesini ziyaret edebilirsiniz.",
                            "ai_guven": "🛡 Altyapımız ve ödeme sistemimiz %100 güvenlidir. Binlerce mutlu kullanıcımız bulunmaktadır.",
                            "ai_sure": "⏳ İşlemleriniz güvenlik doğrulamaları tamamlandıktan sonra çok kısa sürede sonuçlandırılır."
                        }
                        edit_message(chat_id, message_id, cevaplar[data], ai_chat_keyboard)
        except Exception as loop_err:
            print("Döngü hatası:", loop_err)
            time.sleep(3)
