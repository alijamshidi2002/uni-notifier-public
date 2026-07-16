# 🤖 University Assistant Bot

> [!NOTE]
> 🇮🇷 **برای مطالعه توضیحات فارسی به پایین صفحه مراجعه کنید.** 👇

This project is a smart automation bot built with Python, designed to regularly monitor students' university portals. The bot automatically logs into accounts, bypasses CAPTCHA challenges using image processing (OCR), and sends real-time Telegram notifications if there are any updates regarding online classes, assignments, or exams.

## ✨ Key Features

*   **Automated Login:** Seamlessly logs into the university portal without user intervention.
*   **CAPTCHA Bypass (OCR):** Processes, cleans, and reads CAPTCHA images using `Pillow` and `Tesseract`.
*   **Resilient Web Scraping:** Extracts accurate data about online classes, assignments, and exams using `Selenium`.
*   **State Management:** Saves the previous dashboard state for each student (in `JSON` format) to detect new updates.
*   **Real-time Notifications:** Sends categorized messages to each student's Telegram account upon detecting new events.
*   **Cloud Scheduling:** Optimized for scheduled execution on cloud servers.

## 🛠 Tech Stack

*   **Language:** Python 3
*   **Browser Automation:** Selenium WebDriver (Headless mode)
*   **Image Processing & OCR:** Pillow (PIL) and Tesseract-OCR
*   **API & Networking:** `requests` module for Telegram Bot API
*   **Scheduling:** `schedule` library

## 🚀 Installation & Setup

1. Clone the repository:
```bash
git clone [https://github.com/YOUR-USERNAME/YOUR-REPOSITORY-NAME.git](https://github.com/YOUR-USERNAME/YOUR-REPOSITORY-NAME.git)
cd YOUR-REPOSITORY-NAME
```

2.	Install the required Python packages:
```Bash
pip install selenium pillow pytesseract requests schedule
```
3.	Install Tesseract-OCR on your system/server and ensure it is added to your system's PATH.
4.	Create a config.py file in the root directory and add the following details (this file is excluded from GitHub for security reasons):
```Python
## config.py
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
UNIVERSITY_URL = "UNIVERSITY_PORTAL_URL"
TESSERACT_PATH = r"YOUR_TESSERACT_INSTALLATION_PATH"
DATA_DIR = "data"

STUDENTS = [
    {
        "id": "STUDENT_ID",
        "password": "STUDENT_PASSWORD",
        "chat_id": "STUDENT_TELEGRAM_CHAT_ID"
    }
]
```
## 🔒 Security
To keep your sensitive information secure, ensure the following files and directories are added to your .gitignore file:
•	config.py (Contains tokens and passwords)
•	*.json (Bot memory and state files)
•	*.png (Downloaded CAPTCHA images)
•	__pycache__/
## ☁️ Deployment
This bot is optimized for cloud environments like Railway. It runs Chrome in headless mode with specific arguments (e.g., --disable-dev-shm-usage) to bypass memory limits. The scheduling is based on UTC time.
👨‍💻 Developer
•	Ali
•	My GitHub Profile : https://github.com/alijamshidi2002

## 🇮🇷 توضیحات فارسی
# 🤖 ربات هوشمند دستیار دانشگاه #
این پروژه یک ربات اتوماسیون هوشمند با پایتون است که برای بررسی منظم سامانه دانشگاهی دانشجویان طراحی شده است. این ربات به صورت خودکار وارد حساب کاربری دانشجویان شده، چالش‌های امنیتی (CAPTCHA) را با پردازش تصویر حل می‌کند و در صورت وجود تغییرات در کلاس‌های آنلاین، تکالیف یا آزمون‌ها، از طریق تلگرام به دانشجو نوتیفیکیشن می‌فرستد.
## ✨ ویژگی‌های کلیدی #
•	لاگین کاملاً خودکار: ورود به سیستم بدون نیاز به دخالت کاربر.
•	تشخیص و دور زدن کپچا (OCR): پردازش، پاک‌سازی و خواندن تصاویر کپچا با استفاده از کتابخانه‌های Pillow و Tesseract.
•	خزنده وب (Web Scraping) مقاوم: استخراج اطلاعات دقیق کلاس‌های آنلاین، تکالیف و آزمون‌ها با استفاده از Selenium.
•	سیستم مدیریت حافظه (State Management): ذخیره وضعیت قبلی داشبورد هر دانشجو (در قالب فایل‌های JSON) برای تشخیص آپدیت‌های جدید.
•	اطلاع‌رسانی بلادرنگ: ارسال پیام‌های تفکیک‌شده به حساب تلگرام هر دانشجو در صورت وجود رویداد جدید.
•	زمان‌بندی ابری: تنظیم‌شده برای اجرای خودکار در ساعات مشخص (بدون نیاز به روشن بودن سیستم شخصی).
## 🛠 تکنولوژی‌های استفاده شده ##
•	زبان برنامه‌نویسی: Python 3
•	اتوماسیون مرورگر: Selenium WebDriver (حالت Headless)
•	پردازش تصویر و OCR: Pillow (PIL) و Tesseract-OCR
•	ارتباطات و API: ماژول requests برای اتصال به Telegram Bot API
•	زمان‌بندی: کتابخانه schedule
## 🚀 پیش‌نیازها و نصب ##
۱. ابتدا مخزن را کلون کنید:
```Bash
git clone [https://github.com/YOUR-USERNAME/YOUR-REPOSITORY-NAME.git](https://github.com/YOUR-USERNAME/YOUR-REPOSITORY-NAME.git)
cd YOUR-REPOSITORY-NAME
```
۲. کتابخانه‌های مورد نیاز پایتون را نصب کنید:
```Bash
pip install selenium pillow pytesseract requests schedule
```
۳. نرم‌افزار Tesseract-OCR را روی سیستم/سرور خود نصب کرده و مسیر آن را در سیستم تنظیم کنید.
۴. یک فایل به نام config.py در روت پروژه بسازید و اطلاعات زیر را در آن قرار دهید (این فایل به دلایل امنیتی در گیت‌هاب آپلود نشده است):
```Python
# config.py
TELEGRAM_TOKEN = "توکن_ربات_تلگرام_شما"
UNIVERSITY_URL = "آدرس_پورتال_دانشگاه"
TESSERACT_PATH = r"مسیر_نصب_تسرکت"
DATA_DIR = "دایرکتوری_ذخیره_فایل_ها"

STUDENTS = [
    {
        "id": "شماره_دانشجویی",
        "password": "رمز_عبور",
        "chat_id": "آیدی_عددی_تلگرام_دانشجو"
    }
]
```
## 🔒 امنیت ##
برای حفظ امنیت اطلاعات، اطمینان حاصل کنید که فایل‌های زیر در فایل .gitignore شما قرار داشته باشند تا در گیت‌هاب آپلود نشوند:
•	config.py (حاوی توکن‌ها و رمزهای عبور)
•	*.json (فایل‌های حافظه ربات)
•	*.png (تصاویر کپچای دانلود شده)
•	پوشه‌های کش پایتون (__pycache__/)
## ☁️ استقرار روی سرور ##
این ربات برای اجرا در محیط‌های ابری مانند Railway بهینه‌سازی شده است. مرورگر کروم در حالت headless و با تنظیمات دور زدن محدودیت‌های حافظه اجرا می‌شود. زمان‌بندی‌های اسکریپت نیز بر اساس ساعت هماهنگ جهانی (UTC) معادل‌سازی شده‌اند.
👨‍💻 توسعه‌دهنده
•	علی
•	پروفایل گیت‌هاب من : https://github.com/alijamshidi2002

