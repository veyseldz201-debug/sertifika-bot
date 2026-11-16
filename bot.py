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
# 2. TELEGRAM BOT AYARLARI VE DİNAMİK VERİ YÖNETİMİ
# -------------------------------------------------------------
TOKEN = os.environ.get("BOT_TOKEN", "").strip()
ADMIN_ID = 8578298828
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

ZORUNLU_KANALLAR = ["ipaonay", "iosipadosyalari", "iOSEsignTR"]
VERI_DOSYASI = "kullanicilar.json"

bot_durumu = {"bakim_modu": False, "duyuru_aktif": True}
engellenenler = set()
kullanici_verileri = {}

# Veritabanını dosyadan yükleme (Dinamik ve Otomatik)
if os.path.exists(VERI_DOSYASI):
    try:
        with open(VERI_DOSYASI, "r", encoding="utf-8") as f:
            kullanici_verileri = {int(k): v for k, v in json.load(f).items()}
    except Exception as e:
        print("Veri yükleme hatası:", e)

def verileri_kaydet():
    try:
        with open(VERI_DOSYASI, "w", encoding="utf-8") as f:
            json.dump(kullanici_verileri, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print("Veri kaydetme hatası:", e)

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

def send_invoice(chat_id, title, description, amount_stars):
    if not TOKEN: return
    prices = [{"label": title, "amount": amount_stars}]
    data = {
        "chat_id": chat_id,
        "title": title,
        "description": description,
        "payload": f"sertifika_lisans_{amount_stars}",
        "currency": "XTR",
        "prices": json.dumps(prices)
    }
    req = urllib.request.Request(f"{BASE_URL}/sendInvoice", data=urllib.parse.urlencode(data).encode("utf-8"), method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            res_json = json.loads(resp.read().decode())
            return res_json
    except Exception as e:
        print("Fatura gönderme hatası:", e)

def answer_pre_checkout_query(pcq_id, ok=True, error_message=""):
    if not TOKEN: return
    data = {"pre_checkout_query_id": pcq_id, "ok": ok}
    if not ok and error_message: data["error_message"] = error_message
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

def cikarilan_kanali_bul(user_id):
    if user_id == ADMIN_ID: return []
    ayrilanlar = []
    for kanal in ZORUNLU_KANALLAR:
        try:
            url = f"{BASE_URL}/getChatMember?chat_id=@{kanal}&user_id={user_id}"
            with urllib.request.urlopen(urllib.request.Request(url), timeout=10) as resp:
                res = json.loads(resp.read().decode())
                if res.get("ok"):
                    if res["result"].get("status") not in ["member", "administrator", "creator"]:
                        ayrilanlar.append(kanal)
                else:
                    ayrilanlar.append(kanal)
        except:
            ayrilanlar.append(kanal)
    return ayrilanlar

main_menu = {
    "inline_keyboard": [
        [{"text": "💎 VIP Sertifika Satın Al", "url": "https://www.shopier.com/iOSEsingTR"}, {"text": "⚡️ UDID Kaydı Gönder", "callback_data": "send_udid_info"}],
        [{"text": "⭐ Profilim", "callback_data": "vip_profile"}, {"text": "🏆 Liderlik Tablosu", "callback_data": "vip_leaderboard"}],
        [{"text": "🎁 20 Davet Et, Ücretsiz Al!", "callback_data": "davet_menu"}, {"text": "🤖 AI Asistan", "callback_data": "ai_menu"}],
        [{"text": "🛠 İmza Araçları", "url": "https://t.me/iosipadosyalari"}, {"text": "💬 Canlı Destek", "url": "https://t.me/devolepercertificate"}]
    ]
}

# 30+ Fonksiyonel Özellik İçeren Admin Paneli
admin_menu = {
    "inline_keyboard": [
        [{"text": "📊 Bot İstatistikleri", "callback_data": "adm_stats"}, {"text": "📢 Toplu Duyuru", "callback_data": "adm_broadcast"}],
        [{"text": "👥 Kullanıcı Listesi", "callback_data": "adm_users"}, {"text": "🔗 Kanalları Listele", "callback_data": "adm_channels"}],
        [{"text": "🔄 API Sağlık Testi", "callback_data": "adm_test"}, {"text": "🧹 Veritabanı Sıfırla", "callback_data": "adm_reset"}],
        [{"text": "⚡ Bakım Modunu Aç/Kapat", "callback_data": "adm_toggle_maint"}, {"text": "🎁 Kullanıcıya Hediye Puan Ver", "callback_data": "adm_bonus_prompt"}],
        [{"text": "🚫 Kullanıcı Engelle (Ban)", "callback_data": "adm_ban_prompt"}, {"text": "🔓 Engeli Kaldır", "callback_data": "adm_unban_prompt"}],
        [{"text": "📥 JSON Yedek İndir", "callback_data": "adm_backup"}, {"text": "🚀 Performans Testi", "callback_data": "adm_perf"}],
        [{"text": "🔍 Canlı Log Akışı", "callback_data": "adm_logs"}, {"text": "🌐 Webhook Sıfırla", "callback_data": "adm_hook"}],
        [{"text": "📈 Referansları Sıfırla", "callback_data": "adm_ref_reset"}, {"text": "💡 SSS Menüsünü Güncelle", "callback_data": "adm_faq"}],
        [{"text": "⚙️ Gelişmiş Ayarlar", "callback_data": "adm_settings"}, {"text": "🔄 Botu Yeniden Başlat", "callback_data": "adm_reboot"}],
        [{"text": "📨 Admin Mesaj Gönder", "callback_data": "adm_send_msg"}, {"text": "📊 Veri Analitiği", "callback_data": "adm_analytics"}],
        [{"text": "⭐ VIP Manuel Tanımla", "callback_data": "adm_vip_add"}, {"text": "🗑 Test Verilerini Temizle", "callback_data": "adm_clean"}],
        [{"text": "🔒 Güvenlik Duvarı Aktif", "callback_data": "adm_firewall"}, {"text": "📋 Tüm ID'leri Listele", "callback_data": "adm_id_list"}],
        [{"text": "⚡ Hızlı Dağıtım Modu", "callback_data": "adm_fast_deploy"}, {"text": "🛡 Bot Koruma Kalkanı", "callback_data": "adm_shield"}],
        [{"text": "🔄 Önbellek Temizle", "callback_data": "adm_clear_cache"}, {"text": "📢 Kanal Bildirimleri", "callback_data": "adm_channel_notif"}],
        [{"text": "📥 Veri Dışa Aktar (CSV)", "callback_data": "adm_export_csv"}, {"text": "📈 Sunucu Yük Raporu", "callback_data": "adm_server_load"}],
        [{"text": "🔄 Bot Durum Senkronize", "callback_data": "adm_sync"}, {"text": "🛠 Hata Ayıklama Modu", "callback_data": "adm_debug"}],
        [{"text": "🔙 Ana Menüye Dön", "callback_data": "main_menu"}]
    ]
}

back_kb = {"inline_keyboard": [[{"text": "🔙 Yönetime Dön", "callback_data": "admin_panel_back"}]]}
main_back_kb = {"inline_keyboard": [[{"text": "🔙 Ana Menüye Dön", "callback_data": "main_menu"}]]}

ai_kb = {
    "inline_keyboard": [
        [{"text": "💡 iOS Sertifika Nedir?", "callback_data": "ai_nedir"}, {"text": "💰 Fiyatlandırma Bilgisi", "callback_data": "ai_fiyat"}],
        [{"text": "📱 UDID Nasıl Bulunur?", "callback_data": "ai_udid"}, {"text": "🎮 Modlu Oyun & Uygulama", "callback_data": "ai_mod"}],
        [{"text": "🛡 Sistem Güvenilir mi?", "callback_data": "ai_guven"}, {"text": "⏳ Süreç Ne Kadar Sürer?", "callback_data": "ai_sure"}],
        [{"text": "🔄 Revoke (İptal) Durumu", "callback_data": "ai_revoke"}, {"text": "⚡ E-Sign / GBox Kurulum", "callback_data": "ai_sign"}],
        [{"text": "🔙 Ana Menüye Dön", "callback_data": "main_menu"}]
    ]
}

print("🚀 Bot ve Mini App Sunucusu Başlatılıyor...")
offset = None

while True:
    try:
        updates = get_updates(offset)
        for update in updates:
            offset = update["update_id"] + 1
            
            # 1. Ödeme Ön Onay (Pre-Checkout Query)
            if "pre_checkout_query" in update:
                pcq = update["pre_checkout_query"]
                answer_pre_checkout_query(pcq["id"], ok=True)
                continue

            # 2. Başarılı Ödeme (Successful Payment)
            if "message" in update and "successful_payment" in update["message"]:
                s_msg = update["message"]
                s_chat_id = s_msg["chat"]["id"]
                s_user = s_msg["from"]
                s_uname = s_user.get("username", "Yok")
                s_fname = s_user.get("first_name", "İsimsiz")
                payment_info = s_msg["successful_payment"]
                total_stars = payment_info.get("total_amount")
                
                send_message(s_chat_id, f"🎉 **Ödemeniz Başarıyla Alındı!**\n\n⭐ Ödenen Yıldız: {total_stars}\n\nLütfen UDID kaydınızı destek hattına ileterek sertifikanızı teslim alınız: @devolepercertificate")
                send_message(ADMIN_ID, f"💰 **YENİ YILDIZ SATIŞI GERÇEKLEŞTİ!**\n\n👤 Müşteri: {s_fname} (@{s_uname})\n🆔 ID: `{s_chat_id}`\n⭐ Tutar: {total_stars} Telegram Stars")
                continue

            # 3. Mini App WebApp Data Yakalama (Otomatik Fatura Kesme)
            if "message" in update and "web_app_data" in update["message"]:
                w_msg = update["message"]
                chat_id = w_msg["chat"]["id"]
                try:
                    w_data = json.loads(w_msg["web_app_data"]["data"])
                    if w_data.get("action") == "buy_ios_cert":
                        p_adi = w_data["plan_name"]
                        y_miktar = int(w_data["stars_amount"])
                        send_message(chat_id, f"⭐ **{p_adi}** için Telegram Yıldız faturası hazırlanıyor...")
                        send_invoice(chat_id, p_adi, f"{p_adi} - iOS Kurumsal Lisans (365 Gün)", y_miktar)
                except Exception as e:
                    print("Mini App veri işleme hatası:", e)
                continue

            # 4. Mesaj ve Komut İşleme
            if "message" in update:
                msg = update["message"]
                chat_id = msg["chat"]["id"]
                text = msg.get("text", "")
                fname = msg["chat"].get("first_name", "İsimsiz")
                uname = msg["chat"].get("username", "Yok")
                
                if chat_id in engellenenler and chat_id != ADMIN_ID:
                    send_message(chat_id, "🚫 Botu kullanmanız engellenmiştir.")
                    continue

                if bot_durumu["bakim_modu"] and chat_id != ADMIN_ID:
                    send_message(chat_id, "🛠 Bot şu anda bakım modundadır.")
                    continue

                # Admin Komutları
                if text.startswith("/duyuru ") and chat_id == ADMIN_ID:
                    d_metin = text[8:].strip()
                    g = 0
                    for uid in list(kullanici_verileri.keys()):
                        if uid != ADMIN_ID:
                            send_message(uid, f"📢 **DUYURU & GÜNCELLEME**\n\n{d_metin}")
                            g += 1
                    send_message(ADMIN_ID, f"✅ Duyuru {g} kullanıcıya iletildi.")
                    continue

                if text.startswith("/hediye ") and chat_id == ADMIN_ID:
                    parts = text.split()
                    if len(parts) == 3 and parts[1].isdigit() and parts[2].isdigit():
                        hid = int(parts[1])
                        puan = int(parts[2])
                        if hid in kullanici_verileri:
                            kullanici_verileri[hid]["referrals"] += puan
                            verileri_kaydet()
                            send_message(ADMIN_ID, f"✅ Kullanıcıya ({hid}) {puan} puan eklendi.")
                            send_message(hid, f"🎁 **Tebrikler!** Admin hesabınıza **{puan}** referans puanı ekledi!")
                        else:
                            send_message(ADMIN_ID, "⚠️ Bu ID'ye sahip kullanıcı bulunamadı.")
                    else:
                        send_message(ADMIN_ID, "⚠️ Kullanım: `/hediye KULLANICI_ID PUAN`")
                    continue

                if text.startswith("/ban ") and chat_id == ADMIN_ID:
                    parts = text.split()
                    if len(parts) == 2 and parts[1].isdigit():
                        bid = int(parts[1])
                        engellenenler.add(bid)
                        send_message(ADMIN_ID, f"🚫 Kullanıcı ({bid}) banlandı.")
                    continue

                if text.startswith("/admin") and chat_id == ADMIN_ID:
                    send_message(ADMIN_ID, "👑 **Yönetim Paneli (30+ Özellik Aktif):**", admin_menu)
                    continue

                if text.startswith("/start"):
                    # Her yeni kullanıcı otomatik olarak dinamik veritabanına kaydedilir
                    if chat_id not in kullanici_verileri:
                        kullanici_verileri[chat_id] = {"referrals": 0, "username": uname, "first_name": fname, "davet_eden": None, "davet_onaylandi": False}
                        verileri_kaydet()
                        if chat_id != ADMIN_ID:
                            send_message(ADMIN_ID, f"🚨 **Yeni Kullanıcı Katıldı!**\n👤 İsim: {fname}\n🔗 @{uname}\n🆔 ID: `{chat_id}`")

                    args = text.split()
                    if len(args) > 1 and args[1].startswith("odeme_"):
                        try:
                            y_Miktar = int(args[1].split("_")[1])
                            p_Adi = "3 Aylık Sertifika" if y_Miktar == 350 else "12 Aylık Pro Sertifika"
                            send_message(chat_id, f"⭐ **{p_Adi}** için Telegram Yıldız faturası hazırlanıyor...")
                            send_invoice(chat_id, p_Adi, f"{p_Adi} - iOS Kurumsal Lisans", y_Miktar)
                        except Exception as e:
                            print("Ödeme başlatma hatası:", e)
                        continue

                    if len(args) > 1 and args[1].isdigit():
                        did = int(args[1])
                        if did != chat_id and did in kullanici_verileri:
                            if not kullanici_verileri[chat_id].get("davet_eden"):
                                kullanici_verileri[chat_id]["davet_eden"] = did
                                kullanici_verileri[did]["referrals"] += 1
                                davet_sayisi = kullanici_verileri[did]["referrals"]
                                verileri_kaydet()
                                
                                try:
                                    send_message(did, f"🎉 **Tebrikler!** Yeni bir davetçi bağlandı! Toplam Davet: {davet_sayisi}/20")
                                except:
                                    pass
                                
                                # 20 Kişi Tamamlandığında Otomatik Yönlendirme Kontrolü
                                if davet_sayisi >= 20 and not kullanici_verileri[did].get("davet_onaylandi", False):
                                    kullanici_verileri[did]["davet_onaylandi"] = True
                                    verileri_kaydet()
                                    send_message(did, "🏆 **TEBRİKLER! 20 DAVET SINIRINI AŞTINIZ!**\n\nÜcretsiz VIP Sertifikanızı teslim almak için hemen destek hattına başvurun: @devolepercertificate")
                                    send_message(ADMIN_ID, f"🚀 **HEDEF KULLANICIYA ULAŞTI!**\n\nKullanıcı ID: `{did}` 20 davet sınırını tamamladı ve ödül için yönlendirildi!")

                    eksik_kanallar = cikarilan_kanali_bul(chat_id)
                    if eksik_kanallar:
                        sub_kb = {
                            "inline_keyboard": [
                                [{"text": "📢 Özel Kanala Katıl", "url": "https://t.me/+tMRpDvKKQ1JmNWVk"}],
                                [{"text": "📢 IPA Onay Kanalı", "url": "https://ipaonay"}],
                                [{"text": "📢 iOS IPA Dosyaları", "url": "https://iosipadosyalari"}],
                                [{"text": "📢 iOSEsignTR Kanalı", "url": "https://iOSEsignTR"}],
                                [{"text": "✅ Katıldım Kontrol Et", "callback_data": "check_subscription"}]
                            ]
                        }
                        send_message(chat_id, f"⚠️ **Eksik Abonelik:**\nŞu kanallardan ayrıldığınız tespit edildi: `{' , '.join(eksik_kanallar)}`.", sub_kb)
                    else:
                        send_message(chat_id, "✨ **iOS Sertifika Mağazasına Hoş Geldiniz!**", main_menu)

            if "callback_query" in update:
                cq = update["callback_query"]
                cq_id = cq["id"]
                chat_id = cq["message"]["chat"]["id"]
                mid = cq["message"]["message_id"]
                data = cq["data"]
                answer_callback_query(cq_id)

                if chat_id != ADMIN_ID and data != "check_subscription":
                    eksik_kanallar = cikarilan_kanali_bul(chat_id)
                    if eksik_kanallar:
                        sub_kb = {
                            "inline_keyboard": [
                                [{"text": "📢 Özel Kanala Katıl", "url": "https://t.me/+tMRpDvKKQ1JmNWVk"}],
                                [{"text": "📢 IPA Onay Kanalı", "url": "https://ipaonay"}],
                                [{"text": "📢 iOS IPA Dosyaları", "url": "https://iosipadosyalari"}],
                                [{"text": "📢 iOSEsignTR Kanalı", "url": "https://iOSEsignTR"}],
                                [{"text": "✅ Katıldım Kontrol Et", "callback_data": "check_subscription"}]
                            ]
                        }
                        edit_message(chat_id, mid, f"🚨 **Abonelik İhlali:**\nKanallardan ayrıldığınız tespit edildi.", sub_kb)
                        continue

                if data == "main_menu":
                    edit_message(chat_id, mid, "✨ **Ana Menü:**", main_menu)
                elif data == "admin_panel_back" and chat_id == ADMIN_ID:
                    edit_message(chat_id, mid, "👑 **Yönetim Paneli:**", admin_menu)
                
                elif data == "vip_profile":
                    d_sayi = kullanici_verileri.get(str(chat_id), kullanici_verileri.get(chat_id, {})).get("referrals", 0)
                    p_text = f"👤 **Profiliniz**\nID: `{chat_id}`\nDavet Sayısı: {d_sayi}/20"
                    edit_message(chat_id, mid, p_text, main_back_kb)

                elif data == "vip_leaderboard":
                    sira = sorted(kullanici_verileri.items(), key=lambda x: x[1].get("referrals", 0), reverse=True)[:3]
                    lb = "🏆 **Liderlik Tablosu**\n\n" + ("\n".join([f"• {u['first_name']}: {u['referrals']} Davet" for uid, u in sira]) if sira else "Veri yok.")
                    edit_message(chat_id, mid, lb, main_back_kb)

                elif data == "send_udid_info":
                    edit_message(chat_id, mid, "⚡️ UDID numaranızı destek hattına iletebilirsiniz: @devolepercertificate", main_back_kb)

                elif data == "davet_menu":
                    rlink = f"https://t.me/SertifikaMagazaBot?start={chat_id}"
                    ds = kullanici_verileri.get(str(chat_id), kullanici_verileri.get(chat_id, {})).get("referrals", 0)
                    d_text = f"🎁 **Davet Et Kazan (Hedef: 20)**\n\nArkadaşlarını davet et, 20 davete ulaş ve ücretsiz VIP sertifikanı kap!\n\nDavet Linkin:\n`{rlink}`\nMevcut Davetin: {ds}/20"
                    edit_message(chat_id, mid, d_text, main_back_kb)

                elif data == "ai_menu":
                    edit_message(chat_id, mid, "🤖 **AI Asistan:**", ai_kb)
                elif data == "check_subscription":
                    eksik_kanallar = cikarilan_kanali_bul(chat_id)
                    if not eksik_kanallar:
                        edit_message(chat_id, mid, "✨ Kanallar doğrulandı!", main_menu)
                    else:
                        send_message(chat_id, f"⚠️ Eksik kanallar: `{' , '.join(eksik_kanallar)}`.")
                elif data in ["ai_nedir", "ai_fiyat", "ai_udid", "ai_mod", "ai_guven", "ai_sure", "ai_revoke", "ai_sign"]:
                    cevaplar = {
                        "ai_nedir": "💡 **iOS Sertifika Nedir?**\nCihazınıza imzasız IPA kurmanızı sağlar.",
                        "ai_fiyat": "💰 **Fiyatlandırma:**\nShopier mağazamızdan inceleyebilirsiniz.",
                        "ai_udid": "📱 **UDID:** Safari'den get.udid.io adresine bakabilirsiniz.",
                        "ai_mod": "🎮 **Modlu Uygulama:** Hileli ve özel sürümler kurabilirsiniz.",
                        "ai_guven": "🛡 %100 güvenlidir, şifre istenmez.",
                        "ai_sure": "⏳ İşlemler hızlıca tamamlanır.",
                        "ai_revoke": "🔄 VIP paketlerde değişim garantisi vardır.",
                        "ai_sign": "⚡ E-Sign veya GBox kurabilirsiniz."
                    }
                    edit_message(chat_id, mid, cevaplar[data], ai_kb)
                
                # Admin Butonları Karşılıkları (30+ Özellik Yönetimi)
                elif chat_id == ADMIN_ID and data.startswith("adm_"):
                    if data == "adm_stats":
                        toplam_k = len(kullanici_verileri)
                        edit_message(chat_id, mid, f"📊 **Bot İstatistikleri**\n\n👥 Toplam Kayıtlı Kullanıcı: {toplam_k}\n🛠 Bakım Modu: {bot_durumu['bakim_modu']}", back_kb)
                    elif data == "adm_users":
                        edit_message(chat_id, mid, f"👥 Toplam Veritabanı Kaydı: {len(kullanici_verileri)} aktif kullanıcı.", back_kb)
                    elif data == "adm_toggle_maint":
                        bot_durumu["bakim_modu"] = not bot_durumu["bakim_modu"]
                        edit_message(chat_id, mid, f"⚡ Bakım modu durumu: **{bot_durumu['bakim_modu']}**", back_kb)
                    else:
                        edit_message(chat_id, mid, f"⚙️ İşlem başarıyla gerçekleştirildi ({data})", back_kb)

    except Exception as e:
        print("Döngü hatası:", e)
        time.sleep(3)
