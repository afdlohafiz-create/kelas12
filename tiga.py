import streamlit as st
import streamlit.components.v1 as components
import time
import requests
import io
import base64

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="CBT Kimia - Kelas 12 HOTS Pro", 
    page_icon="💜", 
    layout="wide", 
    initial_sidebar_state="expanded" 
)

# --- FUNGSI ANTI-GAMBAR-PECAH (BASE64 BYPASS) ---
def tampilkan_gambar_aman(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            encoded_string = base64.b64encode(response.content).decode()
            st.markdown(
                f'<div style="display: flex; justify-content: center;"><img src="data:image/png;base64,{encoded_string}" width="400" style="border-radius: 10px; border: 2px solid #D6A2E8; box-shadow: 0 4px 12px rgba(0,0,0,0.1);"></div>', 
                unsafe_allow_html=True
            )
        else:
            st.warning("⚠️ Gagal menarik data gambar dari server sumber.")
    except Exception:
        st.error("⚠️ Gangguan Koneksi Gambar.")

# --- 2. TEMA GRADASI UNGU MUDA (LILAC) ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #E0C3FC 0%, #F5F7FA 100%); }
    .block-container {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border-radius: 20px !important; padding: 30px !important;
        box-shadow: 0 10px 40px rgba(142, 68, 173, 0.15) !important;
        margin-top: 20px !important; margin-bottom: 30px !important;
    }
    h1, h2, h3, p, span, li, label { color: #2C3E50 !important; }
    div[data-testid="stAlert"] { background-color: #F4E8FF !important; border: 1px solid #D6A2E8 !important; border-radius: 10px !important; }
    div[data-testid="stAlert"] p, div[data-testid="stAlert"] span { color: #6A1B9A !important; font-weight: 500;}
    .stTextInput input, .stNumberInput input, div[data-baseweb="select"] > div {
        background-color: #FAFAFA !important; color: #4A235A !important; border: 1px solid #D6A2E8 !important; border-radius: 8px !important;
    }
    .stButton button { 
        background: linear-gradient(135deg, #9B59B6 0%, #8E44AD 100%) !important; color: white !important; 
        font-weight: bold !important; border-radius: 8px !important; border: none !important; transition: 0.3s;
    }
    .stButton button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(142, 68, 173, 0.4); }
    .ragu-checkbox { background-color: #FFF3CD; padding: 10px; border-radius: 8px; border-left: 5px solid #F1C40F; margin-bottom: 15px;}
    .hots-label { background-color: #E74C3C; color: white; padding: 3px 8px; border-radius: 5px; font-size: 12px; font-weight: bold; margin-left: 10px; }
    .matching-box { background-color: #F8F9FA; border-radius: 10px; padding: 15px; border: 1px solid #E0E0E0;}
    </style>
""", unsafe_allow_html=True)

# --- 3. DATABASE SOAL SUPER HOTS (10 Soal/Bab Lengkap) ---
DATABASE_SOAL = {
    "Bab 1: Sifat Koligatif Larutan": [
        {"topik": "Titik Didih", "hint": "Mr X = (gram/ΔTb) * (1000/p) * Kb", "tipe": "mcq", "soal": "Ke dalam 250 gram air dilarutkan 15 gram senyawa non-elektrolit X. Jika titik didih larutan terukur 100,26 °C dan Kb air = 0,52 °C/m, analisislah Mr dari zat X tersebut!", "opsi": ["A. 60", "B. 90", "C. 120", "D. 180"], "jawaban": "C. 120", "pembahasan": "ΔTb = 0,26. Mr = (15/0,26) * 4 * 0,52 = 120."},
        {"topik": "Titik Beku", "hint": "Garam NaCl i=2, Urea i=1.", "tipe": "multiselect", "soal": "Diberikan larutan: (1) Glukosa 0.3 M, (2) NaCl 0.2 M, (3) Al2(SO4)3 0.1 M, (4) Urea 0.4 M. Evaluasilah mana yang membeku pada SUHU SAMA!", "opsi": ["Glukosa 0.3 M", "NaCl 0.2 M", "Al2(SO4)3 0.1 M", "Urea 0.4 M"], "jawaban": ["NaCl 0.2 M", "Urea 0.4 M"], "pembahasan": "Keduanya punya konsentrasi efektif 0.4 M."},
        {"topik": "Antibeku", "hint": "Pelarut 2 kg. Gunakan ΔTf = m.Kf", "tipe": "numeric", "soal": "Berapa gram Etilen Glikol (Mr=62) ditambahkan ke 2 kg air agar beku pada -3,72 °C? (Kf=1,86).", "opsi": [], "jawaban": 248, "pembahasan": "3,72 = (gr/62)*(1000/2000)*1,86 -> gr = 248."},
        {"topik": "Tekanan Osmotik", "hint": "CaCl2 i=3.", "tipe": "tf", "soal": "Larutan 0.1 M CaCl2 punya tekanan osmotik lebih besar dari 0.1 M CH3COOH.", "opsi": ["Benar", "Salah"], "jawaban": "Benar", "pembahasan": "CaCl2 elektrolit kuat i=3."},
        {"topik": "Osmosis", "hint": "Plasmolisis.", "tipe": "short_answer", "soal": "Fenomena keluarnya cairan sel akar ke tanah yang sangat pekat disebut...", "opsi": [], "jawaban": "plasmolisis", "pembahasan": "Air keluar sel akar secara osmosis."},
        {"topik": "Diagram P-T", "hint": "Cek selisih vertikal garis pelarut dan larutan.", "tipe": "hotspot", "gambar": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/34/Phase_diagram_of_water.svg/300px-Phase_diagram_of_water.svg.png", "soal": "Manakah pada diagram fasa P-T yang merepresentasikan Penurunan Tekanan Uap (ΔP)?", "opsi": ["A. Titik tripel", "B. Garis sublimasi", "C. Jarak vertikal kurva P pelarut dan larutan", "D. Titik kritis"], "jawaban": "C. Jarak vertikal kurva P pelarut dan larutan", "pembahasan": "Selisih tekanan uap pada T tetap."},
        {"topik": "Eritrosit", "hint": "Hipertonik = mengkerut.", "tipe": "matching", "soal": "Pasangkan kondisi tonisitas infus dengan nasib sel darah merah!", "kiri": ["Hipertonik", "Hipotonik", "Isotonik"], "kanan": ["Krenasi", "Hemolisis", "Normal"], "jawaban": {"Hipertonik": "Krenasi", "Hipotonik": "Hemolisis", "Isotonik": "Normal"}, "pembahasan": "Osmosis air keluar/masuk sel."},
        {"topik": "Ionisasi", "hint": "i = 1 + (n-1)a", "tipe": "numeric", "soal": "Elektrolit biner (n=2) 0.1 m beku pada -0.279 °C (Kf=1.86). Hitung derajat ionisasinya (a)!", "opsi": [], "jawaban": 0.5, "pembahasan": "i = 0,279 / (0,1*1,86) = 1,5. 1,5 = 1 + a -> a = 0,5."},
        {"topik": "Reverse Osmosis", "hint": "Melawan tekanan alami.", "tipe": "tf", "soal": "Tekanan pompa alat desalinasi air laut harus lebih besar dari tekanan osmotiknya.", "opsi": ["Benar", "Salah"], "jawaban": "Benar", "pembahasan": "Melawan aliran osmosis alami."},
        {"topik": "Hukum Raoult", "hint": "Hanya perubahan yang sebanding lurus.", "tipe": "mcq", "soal": "Jika molalitas naik 2x, yang juga naik TEPAT 2x lipat adalah...", "opsi": ["A. Titik Beku", "B. Titik Didih", "C. Penurunan Titik Beku (ΔTf)", "D. Tekanan Uap Larutan"], "jawaban": "C. Penurunan Titik Beku (ΔTf)", "pembahasan": "ΔTf sebanding lurus m."}
    ],
    "Bab 2: Reaksi Redoks dan Elektrokimia": [
        {"topik": "Sel Volta", "hint": "Cari selisih E° terbesar.", "tipe": "mcq", "soal": "E°: Ag=+0.80, Cu=+0.34, Zn=-0.76, Mg=-2.37. Mana E°sel PALING BESAR?", "opsi": ["A. Cu-Ag", "B. Mg-Ag", "C. Zn-Cu", "D. Mg-Zn"], "jawaban": "B. Mg-Ag", "pembahasan": "+0.80 - (-2.37) = 3.17 V."},
        {"topik": "Anoda Korban", "hint": "E° harus lebih negatif dari Besi.", "tipe": "multiselect", "soal": "Besi (E°=-0.44) dilindungi secara katodik. Mana logam anoda korban yang pas?", "opsi": ["Magnesium (-2.37)", "Timah (-0.14)", "Seng (-0.76)", "Tembaga (+0.34)"], "jawaban": ["Magnesium (-2.37)", "Seng (-0.76)"], "pembahasan": "Mg dan Zn lebih mudah oksidasi dari Fe."},
        {"topik": "Faraday", "hint": "w = (Ar/n)*(It/96500)", "tipe": "numeric", "soal": "Arus 965A, 100 detik ke AgNO3. Berapa gram Perak (Ar=108) mengendap?", "opsi": [], "jawaban": 108, "pembahasan": "W = (108/1)*(965*100/96500) = 108."},
        {"topik": "Oksidator", "hint": "Biloks N turun dari +5 ke +2.", "tipe": "tf", "soal": "Pada Cu + HNO3, HNO3 bertindak sebagai oksidator.", "opsi": ["Benar", "Salah"], "jawaban": "Benar", "pembahasan": "N pada HNO3 mengalami reduksi."},
        {"topik": "Anoda", "hint": "Oksidasi air hasilkan O2.", "tipe": "short_answer", "soal": "Anoda Karbon pada larutan CuSO4 menghasilkan gas...", "opsi": [], "jawaban": "o2", "pembahasan": "2H2O -> 4H+ + O2 + 4e-."},
        {"topik": "Aliran e-", "hint": "Lepas dari Anoda (negatif) ke Katoda (positif).", "tipe": "hotspot", "gambar": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Galvanic_cell_labeled.svg/400px-Galvanic_cell_labeled.svg.png", "soal": "Berdasarkan gambar Sel Volta di atas, ke mana arah aliran elektron?", "opsi": ["A. Dari Cu ke Zn", "B. Dari Zn ke Cu", "C. Lewat jembatan garam", "D. Bolak balik"], "jawaban": "B. Dari Zn ke Cu", "pembahasan": "Zn anoda melepaskan e-."},
        {"topik": "Produk", "hint": "Lelehan NaCl vs Larutan Ag.", "tipe": "matching", "soal": "Pasangkan elektroda dengan produknya!", "kiri": ["Katoda Lelehan NaCl", "Anoda Larutan K2SO4", "Katoda Larutan AgNO3"], "kanan": ["Lelehan Natrium", "Gas Oksigen", "Logam Perak"], "jawaban": {"Katoda Lelehan NaCl": "Lelehan Natrium", "Anoda Larutan K2SO4": "Gas Oksigen", "Katoda Larutan AgNO3": "Logam Perak"}, "pembahasan": "Sesuai aturan deret volta dan anion/kation."},
        {"topik": "Penyetaraan", "hint": "Biloks Mn +7 ke +2.", "tipe": "numeric", "soal": "MnO4- + 8H+ + X e- -> Mn2+ + 4H2O. Berapa nilai X?", "opsi": [], "jawaban": 5, "pembahasan": "Selisih biloks Mn adalah 5."},
        {"topik": "Laju Korosi", "hint": "Asam mempercepat pengaratan.", "tipe": "tf", "soal": "Besi di tanah rawa asam berkarat lebih lambat dari tanah netral.", "opsi": ["Benar", "Salah"], "jawaban": "Salah", "pembahasan": "Asam katalisator korosi."},
        {"topik": "Sel Aki", "hint": "Dua-duanya jadi PbSO4.", "tipe": "mcq", "soal": "Saat discharging aki, kedua elektroda berubah menjadi...", "opsi": ["A. Pb", "B. PbO2", "C. PbSO4", "D. H2SO4"], "jawaban": "C. PbSO4", "pembahasan": "Reaksi pakai membentuk PbSO4."}
    ],
    "Bab 3: Kimia Unsur": [
        {"topik": "Reaktivitas", "hint": "Rb paling bawah.", "tipe": "mcq", "soal": "Urutan ledakan logam Na, K, Rb dengan air dari paling DAHSYAT:", "opsi": ["A. Rb > K > Na", "B. Na > K > Rb", "C. K > Rb > Na", "D. Identik"], "jawaban": "A. Rb > K > Na", "pembahasan": "Rb paling reaktif."},
        {"topik": "Oksidator", "hint": "Cl di atas Br.", "tipe": "tf", "soal": "Cl2 mampu mengoksidasi ion Bromida dari NaBr.", "opsi": ["Benar", "Salah"], "jawaban": "Benar", "pembahasan": "Cl2 + 2NaBr -> 2NaCl + Br2."},
        {"topik": "Sulfur", "hint": "Padat kuning korek api.", "tipe": "short_answer", "soal": "Unsur periode 3 padat kuning untuk korek api adalah...", "opsi": [], "jawaban": "belerang", "pembahasan": "Belerang/Sulfur."},
        {"topik": "Warna Ion", "hint": "d10 atau d0 tidak berwarna.", "tipe": "multiselect", "soal": "Pilih ion transisi periode 4 yang larutannya TIDAK BERWARNA!", "opsi": ["Zn2+", "Sc3+", "Cu2+", "Fe3+"], "jawaban": ["Zn2+", "Sc3+"], "pembahasan": "d terisi penuh atau kosong."},
        {"topik": "Valensi", "hint": "Oktet.", "tipe": "numeric", "soal": "Berapa elektron valensi Kripton (Kr)?", "opsi": [], "jawaban": 8, "pembahasan": "Gas mulia valensi 8."},
        {"topik": "Lokasi", "hint": "Blok d di tengah.", "tipe": "hotspot", "gambar": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3d/Periodic_table_large-id.svg/800px-Periodic_table_large-id.svg.png", "soal": "Di area blok manakah letak unsur-unsur Logam Transisi pada Tabel Periodik?", "opsi": ["A. Blok s (kiri)", "B. Blok d (tengah)", "C. Blok p (kanan)", "D. Blok f (bawah)"], "jawaban": "B. Blok d (tengah)", "pembahasan": "Logam transisi mendiami blok d."},
        {"topik": "Aplikasi", "hint": "I2 untuk luka.", "tipe": "matching", "soal": "Pasangkan unsur dengan fungsinya!", "kiri": ["Iodin", "Klorin", "Argon"], "kanan": ["Obat luka (Betadine)", "Desinfektan kolam", "Isi lampu pijar"], "jawaban": {"Iodin": "Obat luka (Betadine)", "Klorin": "Desinfektan kolam", "Argon": "Isi lampu pijar"}, "pembahasan": "Fungsi umum kimia unsur."},
        {"topik": "Kelarutan", "hint": "Mg(OH)2 sukar larut.", "tipe": "mcq", "soal": "Urutan kelarutan hidroksida alkali tanah dari MUDAH ke SUKAR:", "opsi": ["A. Mg > Ca > Ba", "B. Ba > Ca > Mg", "C. Ca > Mg > Ba", "D. Sama saja"], "jawaban": "B. Ba > Ca > Mg", "pembahasan": "Kelarutan OH- alkali tanah naik ke bawah."},
        {"topik": "Industri", "hint": "V2O5.", "tipe": "short_answer", "soal": "Proses pembuatan Asam Sulfat dengan katalis V2O5 disebut proses...", "opsi": [], "jawaban": "kontak", "pembahasan": "Proses Kontak."},
        {"topik": "Senyawa Xe", "hint": "XePtF6.", "tipe": "tf", "soal": "Sampai sekarang ilmuwan belum pernah berhasil membuat senyawa dari Gas Mulia.", "opsi": ["Benar", "Salah"], "jawaban": "Salah", "pembahasan": "Neil Bartlett berhasil mensintesis XePtF6."}
    ],
    "Bab 4: Senyawa Karbon Turunan Alkana": [
        {"topik": "Uji Alkanal", "hint": "Endapan merah bata.", "tipe": "mcq", "soal": "C3H6O bereaksi positif dengan Fehling dan Tollens. Nama senyawanya?", "opsi": ["A. Propanon", "B. 1-Propanol", "C. Propanal", "D. Etanol"], "jawaban": "C. Propanal", "pembahasan": "Aldehida bereaksi dengan Fehling/Tollens."},
        {"topik": "TD Isomer", "hint": "Rantai lurus > Bercabang.", "tipe": "multiselect", "soal": "Evaluasi pernyataan BENAR untuk isomer C4H10O:", "opsi": ["1-butanol TD tertinggi", "2-metil-2-propanol TD tertinggi", "2-metil-2-propanol tersier"], "jawaban": ["1-butanol TD tertinggi", "2-metil-2-propanol tersier"], "pembahasan": "Cabang menurunkan TD."},
        {"topik": "Kesetimbangan", "hint": "Membuang air.", "tipe": "tf", "soal": "Agar ester maksimal, air hasil esterifikasi harus terus dibuang.", "opsi": ["Benar", "Salah"], "jawaban": "Benar", "pembahasan": "Prinsip Le Chatelier."},
        {"topik": "Mekanisme", "hint": "H2SO4 170°C.", "tipe": "short_answer", "soal": "Etanol jadi Etena melepas H2O disebut reaksi...", "opsi": [], "jawaban": "eliminasi", "pembahasan": "Penghilangan molekul air."},
        {"topik": "Kiral", "hint": "Pusat asimetris.", "tipe": "numeric", "soal": "Berapa atom C kiral pada 2-butanol?", "opsi": [], "jawaban": 1, "pembahasan": "Hanya C nomor 2."},
        {"topik": "Gugus", "hint": "Sifat asam cuka.", "tipe": "hotspot", "gambar": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Aspirin-skeletal.svg/300px-Aspirin-skeletal.svg.png", "soal": "Manakah pada molekul Aspirin di atas yang merupakan gugus Asam Karboksilat?", "opsi": ["A. Cincin", "B. Gugus -COOH", "C. Gugus Ester", "D. Metil"], "jawaban": "B. Gugus -COOH", "pembahasan": "Asam karboksilat di sebelah kanan atas."},
        {"topik": "Tipe Isomer", "hint": "Fungsi vs Posisi.", "tipe": "matching", "soal": "Pasangkan hubungan isomer berikut!", "kiri": ["1-propanol vs 2-propanol", "Etanol vs Dimetil eter", "Asam vs Ester"], "kanan": ["Isomer Posisi", "Isomer Fungsi", "Isomer Fungsi"], "jawaban": {"1-propanol vs 2-propanol": "Isomer Posisi", "Etanol vs Dimetil eter": "Isomer Fungsi", "Asam vs Ester": "Isomer Fungsi"}, "pembahasan": "Jenis-jenis isomer senyawa karbon."},
        {"topik": "Uji Lucas", "hint": "Instan keruh.", "tipe": "mcq", "soal": "Alkohol yang bereaksi instan jadi keruh dengan Lucas adalah...", "opsi": ["A. Primer", "B. Sekunder", "C. Tersier", "D. Glikol"], "jawaban": "C. Alkohol Tersier", "pembahasan": "Alkohol tersier paling reaktif."},
        {"topik": "Dimer", "hint": "Ikatan hidrogen ganda.", "tipe": "tf", "soal": "Asam karboksilat punya TD lebih tinggi dari alkohol setara karena membentuk dimer.", "opsi": ["Benar", "Salah"], "jawaban": "Benar", "pembahasan": "Ikatan antarmolekulnya lebih kuat."},
        {"topik": "Sabun", "hint": "Lipid + NaOH.", "tipe": "multiselect", "soal": "Hasil reaksi Saponifikasi Trigliserida + NaOH:", "opsi": ["Sabun", "Gliserol", "Air", "Alkohol"], "jawaban": ["Sabun", "Gliserol"], "pembahasan": "Garam asam lemak dan gliserin."}
    ],
    "Bab 5: Benzena dan Turunannya": [
        {"topik": "Orientasi", "hint": "OH aktivator kuat.", "tipe": "mcq", "soal": "Nitrasi Fenol akan mengarahkan gugus nitro ke posisi...", "opsi": ["A. Meta saja", "B. Orto saja", "C. Orto dan Para", "D. Meta dan Para"], "jawaban": "C. Orto dan Para", "pembahasan": "-OH pengarah orto/para."},
        {"topik": "Rantai Samping", "hint": "Potong semua jadi COOH.", "tipe": "tf", "soal": "Oksidasi Etilbenzena menghasilkan Asam Benzoat.", "opsi": ["Benar", "Salah"], "jawaban": "Benar", "pembahasan": "Rantai samping dipotong jadi karboksilat."},
        {"topik": "Bukti", "hint": "Tidak bisa adisi Br2.", "tipe": "multiselect", "soal": "Bukti ikatan benzena beresonansi:", "opsi": ["Ikatan C-C identik", "Susah adisi Br2", "Entalpi kecil"], "jawaban": ["Ikatan C-C identik", "Entalpi kecil"], "pembahasan": "Bukan alkena biasa."},
        {"topik": "Bahan Baku", "hint": "Cincin metil.", "tipe": "short_answer", "soal": "Bahan baku pembuatan peledak TNT adalah...", "opsi": [], "jawaban": "toluena", "pembahasan": "Toluena/Metilbenzena."},
        {"topik": "Nomor", "hint": "1 dan 3.", "tipe": "numeric", "soal": "Posisi Meta adalah substitusi pada nomor 1 dan...", "opsi": [], "jawaban": 3, "pembahasan": "Meta (1,3)."},
        {"topik": "Nama Posisi", "hint": "Persis sebelah OH.", "tipe": "hotspot", "gambar": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Phenol_chemical_structure.svg/200px-Phenol_chemical_structure.svg.png", "soal": "Jika ada Cl di karbon nomor 2 fenol, posisinya disebut...", "opsi": ["A. Orto", "B. Meta", "C. Para", "D. Alkil"], "jawaban": "A. Orto", "pembahasan": "Orto adalah posisi 1,2."},
        {"topik": "Fungsi", "hint": "BHT untuk minyak.", "tipe": "matching", "soal": "Pasangkan turunan benzena dengan gunanya!", "kiri": ["Asetilsalisilat", "BHT", "Na-Benzoat"], "kanan": ["Aspirin", "Antioksidan minyak", "Pengawet minuman"], "jawaban": {"Asetilsalisilat": "Aspirin", "BHT": "Antioksidan minyak", "Na-Benzoat": "Pengawet minuman"}, "pembahasan": "Aplikasi benzena."},
        {"topik": "Elektrofil", "hint": "CH3+.", "tipe": "mcq", "soal": "Pada Alkilasi Friedel-Crafts, spesi penyerang adalah...", "opsi": ["A. Nukleofil", "B. Elektrofil", "C. Radikal", "D. Basa"], "jawaban": "B. Elektrofil", "pembahasan": "Karbokation adalah elektrofil."},
        {"topik": "Laju", "hint": "Kaya elektron.", "tipe": "tf", "soal": "Gugus -OH dan -NH2 mempercepat reaksi substitusi benzena.", "opsi": ["Benar", "Salah"], "jawaban": "Benar", "pembahasan": "Gugus aktivator."},
        {"topik": "Analgesik", "hint": "Obat demam.", "tipe": "multiselect", "soal": "Ciri Asam Salisilat:", "opsi": ["Punya OH dan COOH", "Obat jamur", "Bahan Aspirin", "Bahan PVC"], "jawaban": ["Punya OH dan COOH", "Obat jamur", "Bahan Aspirin"], "pembahasan": "Bukan bahan plastik PVC."}
    ],
    "Bab 6: Makromolekul (Polimer dan Biokimia)": [
        {"topik": "Adisi", "hint": "Pecah rangkap.", "tipe": "mcq", "soal": "Polimerisasi monomer rangkap tanpa sisa molekul disebut...", "opsi": ["A. Kondensasi", "B. Adisi", "C. Substitusi", "D. Eliminasi"], "jawaban": "B. Adisi", "pembahasan": "Adisi membuka ikatan rangkap."},
        {"topik": "Unit", "hint": "Satu saja.", "tipe": "tf", "soal": "Glukosa bisa dihidrolisis jadi unit lebih kecil.", "opsi": ["Benar", "Salah"], "jawaban": "Salah", "pembahasan": "Unit terkecil."},
        {"topik": "Uji", "hint": "Kuning vs Ungu.", "tipe": "multiselect", "soal": "Pilih uji spesifik protein!", "opsi": ["Biuret", "Iodin", "Xantoproteat", "Fehling"], "jawaban": ["Biuret", "Xantoproteat"], "pembahasan": "Biuret (ungu), Xantoproteat (kuning)."},
        {"topik": "Sabun", "hint": "Garam lemak.", "tipe": "short_answer", "soal": "Reaksi lemak + NaOH disebut...", "opsi": [], "jawaban": "saponifikasi", "pembahasan": "Penyabunan."},
        {"topik": "Ion", "hint": "Dual muatan.", "tipe": "mcq", "soal": "Asam amino amfoter karena membentuk...", "opsi": ["A. Karbokation", "B. Anion", "C. Zwitterion", "D. Radikal"], "jawaban": "C. Zwitterion", "pembahasan": "Zwitterion (kutub ganda)."},
        {"topik": "Ion Zwitter", "hint": "Menerima H+.", "tipe": "hotspot", "gambar": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/ca/Amino_Acid_Zwitterion.svg/300px-Amino_Acid_Zwitterion.svg.png", "soal": "Bagian manakah yang menerima proton dan membentuk kutub positif?", "opsi": ["A. Karboksilat", "B. Amina (-NH3+)", "C. Rantai R", "D. Hidrogen"], "jawaban": "B. Amina (-NH3+)", "pembahasan": "Amina bersifat basa menerima H+."},
        {"topik": "Monomer", "hint": "Isoprena karet.", "tipe": "matching", "soal": "Pasangkan polimer dengan monomernya!", "kiri": ["Amilum", "Karet Alam", "PVC"], "kanan": ["Glukosa", "Isoprena", "Kloroetena"], "jawaban": {"Amilum": "Glukosa", "Karet Alam": "Isoprena", "PVC": "Kloroetena"}, "pembahasan": "Balok penyusun polimer."},
        {"topik": "Panas", "hint": "Lipatan rusak.", "tipe": "mcq", "soal": "Putih telur cair jadi padat saat direbus disebut...", "opsi": ["A. Esterifikasi", "B. Denaturasi", "C. Saponifikasi", "D. Adisi"], "jawaban": "B. Denaturasi", "pembahasan": "Rusaknya struktur protein oleh panas."},
        {"topik": "Lugol", "hint": "Biru hitam.", "tipe": "tf", "soal": "Uji Iodin amilum hasilkan warna biru kehitaman.", "opsi": ["Benar", "Salah"], "jawaban": "Benar", "pembahasan": "Kompleks amilum-iodin."},
        {"topik": "Lipid", "hint": "Nabati cair.", "tipe": "multiselect", "soal": "Evaluasi perbedaan lemak hewani dan nabati:", "opsi": ["Nabati ada ikatan rangkap", "Hewani jenuh lurus rapat", "Mentega reaktif"], "jawaban": ["Nabati ada ikatan rangkap", "Hewani jenuh lurus rapat"], "pembahasan": "Lemak jenuh padat, tak jenuh cair."}
    ]
}

# --- 4. MANAJEMEN STATE DAN TIMER ---
if "kuis_aktif" not in st.session_state: st.session_state.kuis_aktif = False
if "jawaban_user" not in st.session_state: st.session_state.jawaban_user = {}
if "indeks_soal" not in st.session_state: st.session_state.indeks_soal = 0
if "waktu_mulai" not in st.session_state: st.session_state.waktu_mulai = None
if "ragu_ragu" not in st.session_state: st.session_state.ragu_ragu = []
if "hints_used" not in st.session_state: st.session_state.hints_used = []
if "nama_siswa" not in st.session_state: st.session_state.nama_siswa = ""

BATAS_WAKTU = 60 

# --- 5. HALAMAN AWAL (HOME) ---
if not st.session_state.kuis_aktif:
    st.markdown("<h1 style='text-align: center; color: #4A235A;'>🎓 CBT Kimia K12 - Level Analisis (C4-C6)</h1>", unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown("<h2 style='text-align: center; color: #8E44AD;'>🛠️ Tools Ujian</h2>", unsafe_allow_html=True)
        with st.expander("📊 Tabel Periodik Unsur"):
            tampilkan_gambar_aman("https://upload.wikimedia.org/wikipedia/commons/thumb/3/3d/Periodic_table_large-id.svg/800px-Periodic_table_large-id.svg.png")
        with st.expander("📝 Cheat Sheet Rumus"):
            st.markdown("""
            **Koligatif:** $\Delta Tf = Kf \cdot m \cdot i$ <br>
            **Redoks:** $W = \frac{e \cdot i \cdot t}{96500}$ <br>
            **Sel Volta:** $E^\circ_{sel} = E^\circ_{kat} - E^\circ_{an}$
            """, unsafe_allow_html=True)
            
    with st.container(border=True):
        st.markdown("### 📜 Aturan Mengerjakan Ujian")
        st.warning("""
        1. **Mode HOTS & Analitik:** Soal level C4-C6 (Analisis, Evaluasi, Sintesis).
        2. ⏳ **Timer 60 Detik:** Jawaban tak terekam jika lewat waktu.
        3. Gunakan **💡 Hint** (Skor -20%) & **⚠️ Ragu-Ragu** jika perlu.
        """)
        
        st.session_state.nama_siswa = st.text_input("👤 Masukkan Nama Lengkap (Untuk Rapor):", value=st.session_state.nama_siswa)
        pilih_bab = st.selectbox("📂 Pilih Bab Ujian (10 Soal per Bab):", list(DATABASE_SOAL.keys()))
        
        if st.button("Mulai Ujian Analitik Sekarang 🚀", use_container_width=True):
            if st.session_state.nama_siswa == "": st.error("Nama wajib diisi!")
            else:
                st.session_state.soal_siap = DATABASE_SOAL[pilih_bab]
                st.session_state.kuis_aktif = True
                st.session_state.indeks_soal = 0
                st.session_state.jawaban_user = {}
                st.session_state.ragu_ragu = []
                st.session_state.hints_used = []
                st.session_state.waktu_mulai = time.time()
                st.rerun()

# --- 6. MESIN KUIS AKTIF ---
else:
    daftar_soal = st.session_state.soal_siap
    idx = st.session_state.indeks_soal
    
    with st.sidebar:
        st.success("🟢 Progres Tersimpan Aman")
        st.write(f"Soal Ke: **{idx + 1} / {len(daftar_soal)}**")
        if st.session_state.ragu_ragu:
            st.warning(f"Ragu-Ragu: {', '.join([str(x+1) for x in st.session_state.ragu_ragu])}")
            
    if idx < len(daftar_soal):
        curr = daftar_soal[idx]
        waktu_berjalan = time.time() - st.session_state.waktu_mulai
        sisa_waktu = max(0, int(BATAS_WAKTU - waktu_berjalan))

        st.progress((idx)/len(daftar_soal), text=f"Sedang Menjawab: Soal {idx+1}")
        
        timer_html = f"""
        <div id="clock" style="font-size: 18px; font-weight: bold; color: #E74C3C; text-align: center; padding: 10px; background-color: #FADBD8; border-radius: 10px; border: 2px solid #E74C3C; margin-bottom: 15px;">
            ⏳ Sisa Waktu: {sisa_waktu} detik
        </div>
        <script>
            var tl = {sisa_waktu};
            var el = document.getElementById('clock');
            var tid = setInterval(function() {{
                if (tl <= 0) {{ clearInterval(tid); el.innerHTML = "🚨 WAKTU HABIS!"; el.style.background = "#E74C3C"; el.style.color = "white"; }} 
                else {{ el.innerHTML = "⏳ Sisa Waktu: " + tl + " detik"; tl--; }}
            }}, 1000);
        </script>
        """
        components.html(timer_html, height=70)

        with st.container(border=True):
            st.markdown(f"<h4 style='color: #8E44AD;'>Pertanyaan {idx+1} <span class='hots-label'>Analitik C4-C6</span></h4>", unsafe_allow_html=True)
            st.write(curr["soal"])
            if "gambar" in curr: tampilkan_gambar_aman(curr["gambar"])
            st.markdown("---")
            
            if idx not in st.session_state.hints_used:
                if st.button("💡 Butuh Petunjuk? (Skor -20%)"):
                    st.session_state.hints_used.append(idx)
                    st.rerun()
            if idx in st.session_state.hints_used:
                st.info(f"**Petunjuk:** {curr.get('hint', 'Fokus pada soal.')}")
            
            jwbn_lama = st.session_state.jawaban_user.get(idx)
            ans = None
            
            if curr["tipe"] in ["mcq", "tf", "hotspot"]:
                def_idx = curr["opsi"].index(jwbn_lama) if jwbn_lama in curr["opsi"] else None
                ans = st.radio("Jawaban Anda:", curr["opsi"], key=f"q{idx}", index=def_idx)
            elif curr["tipe"] == "matching":
                ans = {}
                default_dict = jwbn_lama if isinstance(jwbn_lama, dict) else {}
                for kiri in curr["kiri"]:
                    val = default_dict.get(kiri, "-- Pilih --")
                    list_k = ["-- Pilih --"] + curr["kanan"]
                    ans[kiri] = st.selectbox(kiri, list_k, index=list_k.index(val), key=f"m_{idx}_{kiri}")
            elif curr["tipe"] == "multiselect":
                ans = st.multiselect("Pilih SEMUA yang Benar:", curr["opsi"], key=f"q{idx}", default=jwbn_lama if isinstance(jwbn_lama, list) else [])
            elif curr["tipe"] == "numeric":
                ans = st.number_input("Input Angka:", key=f"q{idx}", value=float(jwbn_lama) if jwbn_lama is not None else 0.0)
            elif curr["tipe"] == "short_answer":
                ans = st.text_input("Jawaban Singkat:", key=f"q{idx}", value=jwbn_lama if jwbn_lama else "")
            
            st.write("")
            is_ragu = st.checkbox("⚠️ Tandai Ragu-Ragu", value=(idx in st.session_state.ragu_ragu))

            col1, col2 = st.columns(2)
            with col1:
                if idx > 0:
                    if st.button("⏪ Sebelumnya", use_container_width=True):
                        st.session_state.jawaban_user[idx] = ans
                        if is_ragu and idx not in st.session_state.ragu_ragu: st.session_state.ragu_ragu.append(idx)
                        elif not is_ragu and idx in st.session_state.ragu_ragu: st.session_state.ragu_ragu.remove(idx)
                        st.session_state.indeks_soal -= 1
                        st.session_state.waktu_mulai = time.time()
                        st.rerun()
            with col2:
                btn_txt = "Kumpulkan Ujian 🏁" if idx == len(daftar_soal) - 1 else "Simpan & Lanjut ⏭️"
                if st.button(btn_txt, use_container_width=True):
                    if (time.time() - st.session_state.waktu_mulai) > BATAS_WAKTU + 3:
                        st.session_state.jawaban_user[idx] = None
                    else:
                        if (ans is None or ans == "" or ans == []) or (curr["tipe"]=="matching" and "-- Pilih --" in ans.values()): 
                            st.error("⚠️ Lengkapi jawaban!"); st.stop()
                        st.session_state.jawaban_user[idx] = ans
                    
                    if is_ragu and idx not in st.session_state.ragu_ragu: st.session_state.ragu_ragu.append(idx)
                    elif not is_ragu and idx in st.session_state.ragu_ragu: st.session_state.ragu_ragu.remove(idx)
                    
                    if idx == len(daftar_soal) - 1 and len(st.session_state.ragu_ragu) > 0:
                        st.warning("⚠️ Ada soal Ragu-ragu! Klik kumpul lagi untuk paksa selesai."); st.session_state.ragu_ragu.clear(); st.stop()
                        
                    st.session_state.indeks_soal += 1
                    st.session_state.waktu_mulai = time.time()
                    st.rerun()

    # --- 7. HASIL & ANALISIS ---
    else:
        skor_akhir = 0
        bobot = 100 / len(daftar_soal)
        analisis_topik = {} 
        
        for i, s in enumerate(daftar_soal):
            jwbn = st.session_state.jawaban_user.get(i)
            topik = s.get("topik", "Umum")
            if topik not in analisis_topik: analisis_topik[topik] = [0, 0]
            analisis_topik[topik][1] += 1
            
            is_correct = False
            if jwbn is not None:
                if s["tipe"] in ["mcq", "tf", "hotspot"]:
                    if str(jwbn).strip().lower() == str(s["jawaban"]).strip().lower(): is_correct = True
                elif s["tipe"] == "numeric":
                    if float(jwbn) == float(s["jawaban"]): is_correct = True
                elif s["tipe"] == "multiselect":
                    if isinstance(jwbn, list) and set(jwbn) == set(s["jawaban"]): is_correct = True
                elif s["tipe"] == "short_answer":
                    if str(jwbn).strip().lower() in str(s["jawaban"]).lower(): is_correct = True
                elif s["tipe"] == "matching":
                    if isinstance(jwbn, dict) and jwbn == s["jawaban"]: is_correct = True
            
            if is_correct: 
                skor_akhir += (bobot * 0.8) if i in st.session_state.hints_used else bobot
                analisis_topik[topik][0] += 1
            
        st.session_state.skor = int(skor_akhir)
        gelar = "Mahaguru" if st.session_state.skor >= 90 else "Master" if st.session_state.skor >= 75 else "Alkemis" if st.session_state.skor >= 60 else "Pemula"

        st.balloons()
        st.markdown("<h1 style='text-align: center; color: #8E44AD;'>Ujian Selesai!</h1>", unsafe_allow_html=True)
        
        with st.container(border=True):
            st.markdown(f"<h2 style='text-align: center;'>Skor: {st.session_state.skor} / 100 ({gelar})</h2>", unsafe_allow_html=True)
            st.markdown("### 🧠 Analisis Penguasaan Topik")
            teks_analisis = ""
            for t, d in analisis_topik.items():
                persen = (d[0]/d[1])*100
                if persen >= 75: st.success(f"✅ **{t}:** Kuat ({d[0]}/{d[1]})")
                elif persen >= 50: st.warning(f"⚠️ **{t}:** Cukup ({d[0]}/{d[1]})")
                else: st.error(f"❌ **{t}:** Lemah ({d[0]}/{d[1]})")
                teks_analisis += f"{t}: {d[0]}/{d[1]} Benar\n"
            
            # FITUR PDF DIHAPUS, DIGANTI TXT AGAR 100% AMAN SAAT DEPLOY
            fallback_txt = f"SERTIFIKAT CBT KIMIA\nNama: {st.session_state.nama_siswa}\nSkor: {st.session_state.skor}\nGelar: {gelar}\n\nANALISIS NALAR:\n{teks_analisis}"
            st.download_button("📄 Unduh Rapor (TXT)", data=fallback_txt, file_name="Rapor_Siswa.txt", use_container_width=True)

            st.markdown("---")
            for i, s in enumerate(daftar_soal):
                with st.expander(f"Pembahasan Soal {i+1}"):
                    st.write(s['soal'])
                    if "gambar" in s: tampilkan_gambar_aman(s["gambar"])
                    st.info(f"Jawaban: {s['jawaban']} | Pembahasan: {s['pembahasan']}")
                
        if st.button("Selesai & Keluar 🏠", use_container_width=True):
            st.session_state.kuis_aktif = False
            st.rerun()