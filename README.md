## AI-Powered News Aggregator & Digest Agent

Bu layihə, süni intellekt dünyasındakı yenilikləri avtomatik izləyən, analiz edən və istifadəçinin maraqlarına uyğun olaraq fərdiləşdirilmiş xəbərlərin məcmusunu hazırlayan və e-mail vasitəsilə istifadəçiyə göndərilən çox-agentli (multi-agent) bir sistemdir.

---

## Əsas Özəlliklər

* **Avtomatik Məlumat Toplama:** OpenAI, Anthropic və seçilmiş YouTube kanallarından ən son xəbərləri və videoları avtomatik skan edir.
* **Məlumatların analiz eidlməsi:** Toplanan məlumatlar **Groq (Llama 3.3)** vasitəsilə analiz edilir, xülasələr hazırlanır və mövzularına görə kateqoriyalara ayrılır.
* **Fərdiləşdirilmiş Sıralama (Curator Agent):** Xəbərlər istifadəçinin profilinə və maraq dairəsinə görə "Curator Agent" tərəfindən sıralanır.
* **E-mail vasitəsilə xəbərlərin məcmusu:** İstifadəçinin maraqlarına uyğun olan əsas xəbərlər və videolar HTML formatında tərtib olunur və Gmail vasitəsilə göndərilir.

---

## İstifadə edilən texnologiyalar:

| Texnologiya | İstifadə Sahəsi |
| :--- | :--- |
| **Python 3.14+** | Əsas proqramlaşdırma dili |
| **Groq API** | Llama-3.3-70b modeli ilə sürətli LLM emalı |
| **SQLite** | Verilənlərin saxlanılması (Repository pattern) |
| **Pydantic** | Məlumatların validasiyası və strukturlaşdırılması |
| **uv** | Müasir Python paket və asılılıq idarəetməsi |
| **SMTP / SSL** | Təhlükəsiz e-mail göndərişi |

---

## Qovluq Strukturu

ai-news-aggregator/
├── app/
│   ├── agent/          # LLM Agentləri (Curator, Digest, Email)
│   ├── database/       # DB modelləri, Connection və Repository
│   ├── scrapers/       # YouTube, OpenAI və Anthropic məlumat çəkən vasitələr
│   ├── services/       # Biznes məntiqi, emal və e-mail xidməti
│   └── config.py       # Sistem sazlamaları və kanallar
├── main.py             # Proqramın əsas giriş nöqtəsi
├── daily_runner.py     # Bütün konveyeri (pipeline) idarə edən skript
└── pyproject.toml      # Layihə asılılıqları (Dependencies)

---

## Necə İşləyir?

Sistem 5 əsas mərhələdən ibarət konveyer (**pipeline**) üzərində qurulub:

*  **Scraping:** Mənbələrdən (RSS, YouTube API, Markdown) məlumatlar yığılır.
*  **Processing:** Videoların mətnləri (transcripts) və məqalələr təmizlənərək bazaya yazılır.
*  **Digesting:** AI hər bir məlumatı oxuyub xülasə hazırlayır.
*  **Ranking:** İstifadəçinin maraq dairəsinə uyğun olaraq ən vacib 10 xəbər seçilir.
*  **Emailing:** Seçilmiş xəbərlər HTML şablonuna salınaraq istifadəçiyə göndərilir.

---

## Quraşdırma və İstifadə

1. **Repozitoriyanı kopyalayın:**
   git clone [https://github.com/istifadeci_adiniz/ai-news-aggregator.git](https://github.com/istifadeci_adiniz/ai-news-aggregator.git)
   cd ai-news-aggregator

2. **Asılılıqları yükləyin:**
   uv sync

3. **Environment (.env) faylını hazırlayın:**
   GROQ_API_KEY=groq_acariniz
   MY_EMAIL=gmail_adresiniz
   APP_PASSWORD=google_app_password

4. **Sistemi başladın:**
   Bütün konveyeri (pipeline) işə salmaq üçün **main.py** faylını icra edin


* **Qeyd:** Opsional olaraq saat və xəbər sayını tənzimləyə bilərsiniz: **python main.py 48 20**