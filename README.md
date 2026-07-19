# Nafaq VPN — خادم قائمة السيرفرات السريعة

هذا المستودع يحوّل قائمة VPN Gate الضخمة (~5900 سيرفر / ~6MB) إلى ملف صغير
(`servers.csv`) يحوي **أسرع 25 سيرفراً فقط** (~150KB)، ويُحدَّث تلقائياً كل 10 دقائق
عبر GitHub Actions. التطبيق يقرأ هذا الملف الصغير من CDN بدل الاتصال المباشر
بـ VPN Gate — فيصبح فتح القائمة شبه فوري.

## المحتويات

```
.
├── .github/workflows/update-servers.yml   # المهمة المجدولة (كل 10 دقائق)
├── scripts/fetch_servers.py               # سكربت الجلب والفلترة
├── servers.csv                            # الناتج (يُملأ تلقائياً)
├── .gitignore
└── README.md
```

## خطوات الرفع على GitHub

### أ) عبر الموقع (الأسهل)

1. أنشئ مستودعاً جديداً على https://github.com/new — مثلاً باسم `nafaq-servers`
   واجعله **Public** (ضروري كي يعمل رابط jsDelivr المجاني).
2. اضغط **uploading an existing file** ثم اسحب كل ملفات هذا المجلد
   (مع الحفاظ على المسارات `.github/workflows/` و `scripts/`).
3. اضغط **Commit changes**.
4. افتح تبويب **Actions** ووافق على تشغيل الـ workflows إن طُلب منك.
5. شغّل المهمة يدوياً أول مرة: **Actions → Update VPN Servers → Run workflow**.
6. بعد دقيقة، تأكد أن ملف `servers.csv` امتلأ بالسيرفرات.

### ب) عبر Git (سطر الأوامر)

```bash
cd nafaq-servers
git init
git add .
git commit -m "init: خادم قائمة سيرفرات نفق"
git branch -M main
git remote add origin https://github.com/USERNAME/nafaq-servers.git
git push -u origin main
```

ثم فعّل الـ Actions من تبويب **Actions** وشغّلها يدوياً أول مرة.

## ربط التطبيق

غيّر رابط الجلب في التطبيق (`REMOTE_CONTENT_URL`) إلى أحد الرابطين:

- **jsDelivr (أسرع عالمياً، مع تفريغ كاش تلقائي):**

  ```
  https://cdn.jsdelivr.net/gh/USERNAME/nafaq-servers@main/servers.csv
  ```

- **raw مباشر (أحدث تحديثاً، كاش أقصر):**

  ```
  https://raw.githubusercontent.com/USERNAME/nafaq-servers/main/servers.csv
  ```

استبدل `USERNAME` باسم حسابك. **لا حاجة لتعديل المحلّل أو النموذج** لأن صيغة
الملف مطابقة تماماً لصيغة VPN Gate.

## ملاحظات

- عدد السيرفرات في `scripts/fetch_servers.py` عبر المتغيّر `LIMIT` (افتراضي 25).
- الفلترة: يُستبعد أي سيرفر بلا إعداد OpenVPN، تُزال التكرارات حسب IP،
  ثم تُرتَّب حسب: أقل Ping ← أعلى Speed ← أعلى Score.
- المهمة المجدولة تعمل على الفرع الافتراضي (`main`) فقط.
