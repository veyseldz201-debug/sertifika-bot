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

# Tüm ekran görüntülerinden eksiksiz kurtarılan ve +1 hediye referans eklenen kullanıcı verileri
kullanici_verileri = {
    8613637517: {"referrals": 1, "username": "OwnerSiken", "first_name": "PEOPLE", "davet_eden": None, "davet_onaylandi": False},
    8421022472: {"referrals": 1, "username": "yok", "first_name": "Koller", "davet_eden": None, "davet_onaylandi": False},
    5085014674: {"referrals": 1, "username": "zirratbankasi", "first_name": "Hz.Sexkurt @bayraktarsh3", "davet_eden": None, "davet_onaylandi": False},
    9086769626: {"referrals": 1, "username": "rg7koray", "first_name": "RG7 koray", "davet_eden": None, "davet_onaylandi": False},
    7991979360: {"referrals": 1, "username": "yok", "first_name": "Demo", "davet_eden": None, "davet_onaylandi": False},
    6379047412: {"referrals": 1, "username": "Qpekfkfkf1000", "first_name": "ATATV44 Rüzgar", "davet_eden": None, "davet_onaylandi": False},
    7194006650: {"referrals": 1, "username": "RedmiNote11ProHype25", "first_name": "Note 11 Pro", "davet_eden": None, "davet_onaylandi": False},
    8851475981: {"referrals": 1, "username": "tesisatcixdd", "first_name": "Tesisatcixdd", "davet_eden": None, "davet_onaylandi": False},
    8800129298: {"referrals": 1, "username": "kaanww02", "first_name": "Kaan", "davet_eden": None, "davet_onaylandi": False},
    7420060017: {"referrals": 1, "username": "mico213", "first_name": "...", "davet_eden": None, "davet_onaylandi": False},
    8893878324: {"referrals": 1, "username": "yok", "first_name": "Q", "davet_eden": None, "davet_onaylandi": False},
    8852740082: {"referrals": 1, "username": "yok", "first_name": "vazieca", "davet_eden": None, "davet_onaylandi": False},
    8241065557: {"referrals": 1, "username": "yok", "first_name": "Names", "davet_eden": None, "davet_onaylandi": False},
    6002117683: {"referrals": 1, "username": "emirxd00", "first_name": "emirxd", "davet_eden": None, "davet_onaylandi": False},
    9192959921: {"referrals": 1, "username": "yok", "first_name": "Can", "davet_eden": None, "davet_onaylandi": False},
    442202264: {"referrals": 1, "username": "SafinHadiAziz", "first_name": "Safin", "davet_eden": None, "davet_onaylandi": False},
    8347570411: {"referrals": 1, "username": "userr143209", "first_name": "Userrr12345678900", "davet_eden": None, "davet_onaylandi": False},
    8570334539: {"referrals": 1, "username": "Prison1907", "first_name": "atatv44", "davet_eden": None, "davet_onaylandi": False},
    7348788357: {"referrals": 1, "username": "TassyStoreTR", "first_name": "Tassy Store TR", "davet_eden": None, "davet_onaylandi": False},
    8933409412: {"referrals": 1, "username": "yok", "first_name": "Ruhsuz siker", "davet_eden": None, "davet_onaylandi": False},
    7685481517: {"referrals": 1, "username": "Layzn81", "first_name": "Layzn", "davet_eden": None, "davet_onaylandi": False},
    9084976579: {"referrals": 1, "username": "yok", "first_name": ".", "davet_eden": None, "davet_onaylandi": False},
    6524080104: {"referrals": 1, "username": "yok", "first_name": "STAR • SPAIN", "davet_eden": None, "davet_onaylandi": False},
    9118924354: {"referrals": 1, "username": "yok", "first_name": "qwertypoiu9998", "davet_eden": None, "davet_onaylandi": False},
    8076638276: {"referrals": 1, "username": "URFALIFR", "first_name": "BEETHOVEN", "davet_eden": None, "davet_onaylandi": False},
    6418901414: {"referrals": 1, "username": "yok", "first_name": "7uksell", "davet_eden": None, "davet_onaylandi": False},
    8012681735: {"referrals": 1, "username": "Cicocoi", "first_name": "ᶫᵒᵛᵉᵧₒᵤഽ", "davet_eden": None, "davet_onaylandi": False},
    8955962571: {"referrals": 1, "username": "usmanawan", "first_name": "Usman", "davet_eden": None, "davet_onaylandi": False},
    8648574341: {"referrals": 1, "username": "yok", "first_name": "Jiyan", "davet_eden": None, "davet_onaylandi": False},
    7683534715: {"referrals": 1, "username": "TEAHCIW", "first_name": "John Michael", "davet_eden": None, "davet_onaylandi": False},
    8561815348: {"referrals": 1, "username": "AxentraStore", "first_name": "Axentra", "davet_eden": None, "davet_onaylandi": False},
    8593185106: {"referrals": 1, "username": "yok", "first_name": "Yusak", "davet_eden": None, "davet_onaylandi": False},
    7500586973: {"referrals": 1, "username": "yok", "first_name": "KUTSALXX🔞", "davet_eden": None, "davet_onaylandi": False},
    8951167346: {"referrals": 1, "username": "yok", "first_name": "ḈḀṾḀṆİṠ", "davet_eden": None, "davet_onaylandi": False},
    8288774951: {"referrals": 1, "username": "yok", "first_name": "Benz Fruppinn", "davet_eden": None, "davet_onaylandi": False},
    8969184491: {"referrals": 1, "username": "ahmetyildirmaz", "first_name": "YAZILI HAFTASI FULL AFK", "davet_eden": None, "davet_onaylandi": False},
    8510730640: {"referrals": 1, "username": "AlwaysXXX", "first_name": "ALWAYS", "davet_eden": None, "davet_onaylandi": False},
    8808287992: {"referrals": 1, "username": "yok", "first_name": "gakpo", "davet_eden": None, "davet_onaylandi": False},
    8761294529: {"referrals": 1, "username": "psychoo1967Xguzreszs", "first_name": "Diablo!", "davet_eden": None, "davet_onaylandi": False},
    5420522088: {"referrals": 1, "username": "Mamixre", "first_name": "Mami", "davet_eden": None, "davet_onaylandi": False},
    8891249931: {"referrals": 1, "username": "berso21", "first_name": "BERŞO", "davet_eden": None, "davet_onaylandi": False},
    7617271214: {"referrals": 1, "username": "yok", "first_name": "İsa", "davet_eden": None, "davet_onaylandi": False},
    6613410039: {"referrals": 1, "username": "Huse2012confiq", "first_name": "Hüseyn", "davet_eden": None, "davet_onaylandi": False},
    8667925297: {"referrals": 1, "username": "Alic9x963", "first_name": "علي", "davet_eden": None, "davet_onaylandi": False},
    8948322153: {"referrals": 1, "username": "deliflox31", "first_name": "DELURME FLOX", "davet_eden": None, "davet_onaylandi": False},
    1542251088: {"referrals": 1, "username": "Zoneben", "first_name": "ZONE", "davet_eden": None, "davet_onaylandi": False},
    8888104236: {"referrals": 1, "username": "RazeStoreOWNER", "first_name": "Raze Store", "davet_eden": None, "davet_onaylandi": False},
    8832378065: {"referrals": 1, "username": "sarsamazsin77", "first_name": "PASA @YxgizOtp", "davet_eden": None, "davet_onaylandi": False},
    7974542154: {"referrals": 1, "username": "OscarCALLER", "first_name": "Oscâr", "davet_eden": None, "davet_onaylandi": False},
    6406123867: {"referrals": 1, "username": "raizeneu", "first_name": "Я", "davet_eden": None, "davet_onaylandi": False},
    8662861404: {"referrals": 1, "username": "Deepyilmaz", "first_name": "Hüseyin", "davet_eden": None, "davet_onaylandi": False},
    1632985238: {"referrals": 1, "username": "yok", "first_name": "Abdulkadir", "davet_eden": None, "davet_onaylandi": False},
    6352315302: {"referrals": 1, "username": "yok", "first_name": "Çakır", "davet_eden": None, "davet_onaylandi": False},
    7304480644: {"referrals": 1, "username": "yok", "first_name": "Yook", "davet_eden": None, "davet_onaylandi": False},
    8112587073: {"referrals": 1, "username": "KuzeyDeathMagic", "first_name": "Kuzey", "davet_eden": None, "davet_onaylandi": False},
    7590849024: {"referrals": 1, "username": "GraxyAstras", "first_name": "Graxy", "davet_eden": None, "davet_onaylandi": False},
    8699112166: {"referrals": 1, "username": "yok", "first_name": "Recp", "davet_eden": None, "davet_onaylandi": False},
    8983534316: {"referrals": 1, "username": "wozyxdd", "first_name": "Wozyxdd #AFK", "davet_eden": None, "davet_onaylandi": False},
    8967675020: {"referrals": 1, "username": "bulursanseninim", "first_name": "EMRE BXBA", "davet_eden": None, "davet_onaylandi": False},
    8392620304: {"referrals": 1, "username": "Lvl99Emi", "first_name": "Lvl99Emir", "davet_eden": None, "davet_onaylandi": False},
    8882342303: {"referrals": 1, "username": "yok", "first_name": "h", "davet_eden": None, "davet_onaylandi": False},
    8955489186: {"referrals": 1, "username": "KannSaplar", "first_name": "Kaan @YxgizOtp", "davet_eden": None, "davet_onaylandi": False},
    6236992909: {"referrals": 1, "username": "aliyefff019", "first_name": "𝘈𝘭𝘪𝘺𝘦𝘷", "davet_eden": None, "davet_onaylandi": False},
    8977103833: {"referrals": 1, "username": "bpf99", "first_name": "Azo | BXBX @YxgizOtp", "davet_eden": None, "davet_onaylandi": False},
    8918536708: {"referrals": 1, "username": "blackhackcf", "first_name": "•BLACK•", "davet_eden": None, "davet_onaylandi": False},
    6113645179: {"referrals": 1, "username": "yok", "first_name": "YY", "davet_eden": None, "davet_onaylandi": False},
    8702823143: {"referrals": 1, "username": "yok", "first_name": "Deliyim", "davet_eden": None, "davet_onaylandi": False},
    5883968210: {"referrals": 1, "username": "yok", "first_name": "Emir", "davet_eden": None, "davet_onaylandi": False},
    6383517817: {"referrals": 1, "username": "yok", "first_name": "Dani", "davet_eden": None, "davet_onaylandi": False},
    8811539642: {"referrals": 1, "username": "yok", "first_name": "Gggg", "davet_eden": None, "davet_onaylandi": False},
    8733347326: {"referrals": 1, "username": "yok", "first_name": "XoceanPM", "davet_eden": None, "davet_onaylandi": False},
    9040158156: {"referrals": 1, "username": "Titanerenbaba", "first_name": "ErenBaba", "davet_eden": None, "davet_onaylandi": False},
    6841398582: {"referrals": 1, "username": "Napoleon901", "first_name": "E901 #AFK", "davet_eden": None, "davet_onaylandi": False},
    8841178825: {"referrals": 1, "username": "yok", "first_name": "..", "davet_eden": None, "davet_onaylandi": False},
    6746025987: {"referrals": 1, "username": "JawierCfg", "first_name": "JâwierBabaPuro", "davet_eden": None, "davet_onaylandi": False},
    6803785864: {"referrals": 1, "username": "yok", "first_name": "Kadir", "davet_eden": None, "davet_onaylandi": False},
    5830354612: {"referrals": 1, "username": "bypato", "first_name": "bypato", "davet_eden": None, "davet_onaylandi": False},
    8964516066: {"referrals": 1, "username": "thox127", "first_name": "Samet", "davet_eden": None, "davet_onaylandi": False},
    7964555286: {"referrals": 1, "username": "Hekatomb030", "first_name": "ḨEḰA", "davet_eden": None, "davet_onaylandi": False},
    8810090592: {"referrals": 1, "username": "yok", "first_name": "PUBG HİLE CONFIG", "davet_eden": None, "davet_onaylandi": False},
    5699057642: {"referrals": 1, "username": "yok", "first_name": "Hasanbycn", "davet_eden": None, "davet_onaylandi": False},
    8406338293: {"referrals": 1, "username": "RichiexRich0", "first_name": "Richie", "davet_eden": None, "davet_onaylandi": False},
    8874999673: {"referrals": 1, "username": "cakmayargyonetcs", "first_name": "Çakma 16", "davet_eden": None, "davet_onaylandi": False},
    8759000356: {"referrals": 1, "username": "yok", "first_name": "King", "davet_eden": None, "davet_onaylandi": False},
    8512532605: {"referrals": 1, "username": "yok", "first_name": "#HAYATSIZ-Tomiл-| 🐅✈️", "davet_eden": None, "davet_onaylandi": False},
    8888287349: {"referrals": 1, "username": "yok", "first_name": "မင်းးမှ", "davet_eden": None, "davet_onaylandi": False},
    7656783384: {"referrals": 1, "username": "yok", "first_name": "x", "davet_eden": None, "davet_onaylandi": False},
    5927880112: {"referrals": 1, "username": "yok", "first_name": "Qowdhan 🐐", "davet_eden": None, "davet_onaylandi": False},
    8645160507: {"referrals": 1, "username": "yok", "first_name": "....#⌚️", "davet_eden": None, "davet_onaylandi": False},
    9208523925: {"referrals": 1, "username": "yok", "first_name": "youkai", "davet_eden": None, "davet_onaylandi": False},
    8432977534: {"referrals": 1, "username": "zerostoremx", "first_name": "yok", "davet_eden": None, "davet_onaylandi": False}
}

if os.path.exists(VERI_DOSYASI):
    try:
        with open(VERI_DOSYASI, "r", encoding="utf-8") as f:
            dosya_verileri = {int(k): v for k, v in json.load(f).items()}
            for uid, udata in dosya_verileri.items():
                if uid not in kullanici_verileri:
                    kullanici_verileri[uid] = udata
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

# AI Asistan için 15+ maddelik kapsamlı rehber menüsü
ai_kb = {
    "inline_keyboard": [
        [{"text": "💡 iOS Sertifika Nedir?", "callback_data": "ai_nedir"}, {"text": "💰 Fiyatlandırma Bilgisi", "callback_data": "ai_fiyat"}],
        [{"text": "📱 UDID Nasıl Bulunur?", "callback_data": "ai_udid"}, {"text": "🎮 Modlu Oyun & Uygulama", "callback_data": "ai_mod"}],
        [{"text": "🛡 Sistem Güvenilir mi?", "callback_data": "ai_guven"}, {"text": "⏳ Süreç Ne Kadar Sürer?", "callback_data": "ai_sure"}],
        [{"text": "🔄 Revoke (İptal) Durumu", "callback_data": "ai_revoke"}, {"text": "⚡ E-Sign / GBox Kurulum", "callback_data": "ai_sign"}],
        [{"text": "📦 IPA Dosyası Yükleme", "callback_data": "ai_ipa"}, {"text": "🎁 15 Davet Hediyesi", "callback_data": "ai_hediye"}],
        [{"text": "🔋 Pil & Performans", "callback_data": "ai_pil"}, {"text": "🔄 Güncelleme Desteği", "callback_data": "ai_guncelle"}],
        [{"text": "👥 Aile / Çoklu Cihaz", "callback_data": "ai_aile"}, {"text": "📞 Canlı Destek Hattı", "callback_data": "ai_destek"}],
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
                            send_message(uid, f"📢 **DUYURU & BÜYÜK GÜNCELLEME**\n\n{d_metin}")
                            g += 1
                    send_message(ADMIN_ID, f"✅ Duyuru {g} kullanıcıya iletildi.")
                    continue

                if text.startswith("/admin") and chat_id == ADMIN_ID:
                    send_message(ADMIN_ID, "👑 **Yönetim Paneli:**", admin_menu)
                    continue

                if text.startswith("/start"):
                    yeni_kayit = False
                    if chat_id not in kullanici_verileri and chat_id != ADMIN_ID:
                        # Yeni kullanıcılara kıyak: +1 referans hediyesiyle başlatıyoruz!
                        kullanici_verileri[chat_id] = {"referrals": 1, "username": uname, "first_name": fname, "davet_eden": None, "davet_onaylandi": False}
                        yeni_kayit = True
                        verileri_kaydet()
                        send_message(ADMIN_ID, f"👤 Yeni Kullanıcı (Hediye 1 Puanlı): {fname} (@{uname}) - Toplam: {len(kullanici_verileri)}")
                    elif chat_id not in kullanici_verileri:
                        kullanici_verileri[chat_id] = {"referrals": 1, "username": uname, "first_name": fname, "davet_eden": None, "davet_onaylandi": False}
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
                        karsilama = "🎉 **Büyük Bot Güncellemesi & Sürpriz Hediye!**\n\nBizden size küçük bir güzellik olsun: Hesabınıza **+1 Ücretsiz Referans Puanı** tanımlandı! 🎁\n\n✨ **Ekosisteme Hoş Geldin!**" if yeni_kayit else "✨ **Ekosisteme Tekrar Hoş Geldin!** Botumuz güncellendi ve yenilendi."
                        send_message(chat_id, karsilama, main_menu)

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
                    d_sayi = kullanici_verileri.get(chat_id, {}).get("referrals", 1)
                    edit_message(chat_id, mid, f"👤 **Profil Kartı**\nID: `{chat_id}`\nDavet Puanı: {d_sayi}/15 (Hediye Dahil! 🎁)", main_back_kb)
                elif data == "vip_leaderboard":
                    sira = sorted(kullanici_verileri.items(), key=lambda x: x[1].get("referrals", 0), reverse=True)[:3]
                    lb = "🏆 **Liderlik Tablosu**\n\n" + ("\n".join([f"• {u['first_name']}: {u['referrals']} Puan" for uid, u in sira]) if sira else "Henüz veri yok.")
                    edit_message(chat_id, mid, lb, main_back_kb)
                elif data == "send_udid_info":
                    edit_message(chat_id, mid, "⚡️ UDID numaranızı destek hattına iletebilirsiniz.", main_back_kb)
                elif data == "davet_menu":
                    rlink = f"https://t.me/SertifikaMagazaBot?start={chat_id}"
                    ds = kullanici_verileri.get(chat_id, {}).get("referrals", 1)
                    edit_message(chat_id, mid, f"🎁 **Davet Et Kazan**\nLinkin:\n`{rlink}`\nDavetlerin: {ds}/15", main_back_kb)
                elif data == "ai_menu":
                    edit_message(chat_id, mid, "🤖 **AI Asistan & Bilgi Bankası:**\nMerak ettiğiniz tüm konuları aşağıdan inceleyebilirsiniz:", ai_kb)
                elif data == "benefits":
                    edit_message(chat_id, mid, "🛡 **Avantajlar:** 1 Yıl Garanti ve Revoke değişim güvencesi.", main_back_kb)
                elif data == "faq":
                    edit_message(chat_id, mid, "❓ **SSS:** İşlemler kısa sürede onaylanır ve anında teslim edilir.", main_back_kb)
                elif data == "check_subscription":
                    if kanallari_kontrol_et(chat_id):
                        send_message(chat_id, "✨ Kanallar doğrulandı!", main_menu)
                    else:
                        send_message(chat_id, "⚠️ Eksik kanallar var, lütfen tamamlayın.")
                elif data in [
                    "ai_nedir", "ai_fiyat", "ai_udid", "ai_mod", "ai_guven", "ai_sure",
                    "ai_revoke", "ai_sign", "ai_ipa", "ai_hediye", "ai_pil", "ai_guncelle",
                    "ai_aile", "ai_destek"
                ]:
                    cevaplar = {
                        "ai_nedir": "💡 **iOS Sertifika Nedir?**\nApple Geliştirici programı sayesinde cihazınıza resmi olmayan IPA dosyalarını kurmanıza olanak tanıyan özel bir profildir. Bilgisayarsız doğrudan yükleme yapar.",
                        "ai_fiyat": "💰 **Fiyatlandırma Nedir?**\nEn uygun VIP paket fiyatlarımız ve güncel kampanyalarımız için Shopier mağazamızı ziyaret edebilirsiniz.",
                        "ai_udid": "📱 **UDID Nasıl Bulunur?**\nSafari tarayıcınızdan [Get My UDID](https://get.udid.io) adresine girerek cihaz kimlik numaranızı kolayca öğrenebilirsiniz.",
                        "ai_mod": "🎮 **Modlu Oyun & Uygulama:**\nSertifika sayesinde YouTube, Instagram, Spotify gibi uygulamaların hileli/özellikli modlarını ve ücretli oyunları ücretsiz kurabilirsiniz.",
                        "ai_guven": "🛡 **Sistem Güvenilir mi?**\nKesinlikle %100 güvenlidir. Kişisel verileriniz veya Apple ID şifreniz asla istenmez, sadece cihaz UDID kaydı yapılır.",
                        "ai_sure": "⏳ **Süreç Ne Kadar Sürer?**\nUDID kaydınız iletildikten sonra işlemleriniz çok kısa süre içinde hızla tamamlanır ve aktif edilir.",
                        "ai_revoke": "🔄 **Revoke (Sertifika İptali):**\nNadiren de olsa Apple sertifikayı iptal edebilir. VIP paketlerimizde garanti kapsamında yenileme desteği sağlanır.",
                        "ai_sign": "⚡ **E-Sign / GBox Kurulumu:**\nSertifikanız aktif olduktan sonra E-Sign veya GBox gibi imzalama uygulamalarıyla cihazınızda dilediğiniz IPA'yı kurabilirsiniz.",
                        "ai_ipa": "📦 **IPA Dosyası Yükleme:**\nKanalımızdaki veya harici kaynaklardaki `.ipa` uzantılı dosyaları telefonunuza indirip doğrudan imzalayarak çalıştırabilirsiniz.",
                        "ai_hediye": "🎁 **15 Davet Hediyesi:**\nBotumuzda arkadaşlarınızı davet ederek 15 puana ulaştığınızda ücretsiz sertifika kazanma şansı yakalarsınız! (Ayrıca herkese +1 puan hediye ettik!)",
                        "ai_pil": "🔋 **Pil & Performans:**\nSertifikalar ve imza araçları cihazınızın pil ömrüne veya sistem performansına hiçbir olumsuz etki etmez.",
                        "ai_guncelle": "🔄 **Güncelleme Desteği:**\nSistemimiz ve bot altyapımız sürekli güncellenmektedir. En yeni iOS sürümleri ve araçlar desteklenmektedir.",
                        "ai_aile": "👥 **Çoklu Cihaz Desteği:**\nHer sertifika kayıt işlemi ilgili tek bir cihazın UDID kimliğine özel olarak tanımlanmaktadır.",
                        "ai_destek": "📞 **Canlı Destek Hattı:**\nTakıldığınız tüm teknik sorunlar ve sorularınız için @devolepercertificate üzerinden 7/24 destek alabilirsiniz."
                    }
                    edit_message(chat_id, mid, cevaplar[data], ai_kb)
    except Exception as e:
        print("Döngü hatası:", e)
        time.sleep(3)
