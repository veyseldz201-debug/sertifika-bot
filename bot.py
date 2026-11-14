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

kullanici_verileri = {
    8613637517: {"referrals": 1, "username": "OwnerSiken", "first_name": "PEOPLE", "davet_eden": None, "davet_onaylandi": False},
    8421022472: {"referrals": 1, "username": "yok", "first_name": "Koller", "davet_eden": None, "davet_onaylandi": False},
    5085014674: {"referrals": 1, "username": "zirratbankasi", "first_name": "Hz.Sexkurt", "davet_eden": None, "davet_onaylandi": False},
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
    8347570411: {"referrals": 1, "username": "userr143209", "first_name": "Userrr", "davet_eden": None, "davet_onaylandi": False},
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
    8969184491: {"referrals": 1, "username": "ahmetyildirmaz", "first_name": "YAZILI HAFTASI", "davet_eden": None, "davet_onaylandi": False},
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
    8832378065: {"referrals": 1, "username": "sarsamazsin77", "first_name": "PASA", "davet_eden": None, "davet_onaylandi": False},
    7974542154: {"referrals": 1, "username": "OscarCALLER", "first_name": "Oscâr", "davet_eden": None, "davet_onaylandi": False},
    6406123867: {"referrals": 1, "username": "raizeneu", "first_name": "Я", "davet_eden": None, "davet_onaylandi": False},
    
