import time
import os
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import schedule  
import config

pytesseract.pytesseract.tesseract_cmd = config.TESSERACT_PATH

def run_bot():
    print("\n=========================================")
    print("🤖 شروع اجرای خودکار ربات...")
    print("=========================================")

    try:
        # تنظیمات مخصوص سرور ابری (بدون مانیتور و نامرئی)
        options = webdriver.ChromeOptions()
        options.add_argument('--headless=new') 
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-software-rasterizer')
        options.add_argument('--disable-dev-tools')
        options.add_argument('--no-zygote')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--remote-debugging-port=9222')
        
        driver = webdriver.Chrome(options=options)
        driver.maximize_window()
        
        for student in config.STUDENTS:
            print(f"\n>>> شروع کار برای دانشجو: {student['id']}")
            
            driver.delete_all_cookies()
            driver.get(config.UNIVERSITY_URL)
            time.sleep(4) 

            # --- بررسی هوشمند صفحه لاگین ---
            try:
                driver.find_element(By.ID, "UserName")
                print("✅ فرم ورود آماده است.")
            except:
                try:
                    login_button = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".btn.btn-warning.btn-sm.mx-1"))
                    )
                    driver.execute_script("arguments[0].click();", login_button)
                    print("✅ دکمه ورود با موفقیت کلیک شد.")
                    time.sleep(4)
                except Exception as e:
                    print(f"❌ دکمه ورود پیدا نشد. پرش به دانشجوی بعدی.")
                    continue 
            
            # --- حلقه عبور از کپچا ---
            max_tries = 20
            for attempt in range(1, max_tries + 1):
                print(f"\n--- 🔄 تلاش شماره {attempt} برای عبور از کپچا ---")
                
                try: 
                    # ۱. عکس گرفتن از کپچا
                    captcha_img = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//img[contains(@src, "data:image")]'))
                    )
                    
                    if not os.path.exists(config.DATA_DIR):
                        os.makedirs(config.DATA_DIR)
                        
                    captcha_path = os.path.join(config.DATA_DIR, "captcha.png")
                    captcha_img.screenshot(captcha_path)
                    
                    # پردازش تصویر
                    img = Image.open(captcha_path)
                    img = img.convert('L') 
                    img = img.resize((img.width * 4, img.height * 4), Image.Resampling.LANCZOS)
                    enhancer = ImageEnhance.Contrast(img)
                    img = enhancer.enhance(3.5)
                    img = img.filter(ImageFilter.SHARPEN)
                    
                    clean_captcha_path = os.path.join(config.DATA_DIR, "clean_captcha.png")
                    img.save(clean_captcha_path)

                    captcha_text = pytesseract.image_to_string(
                        Image.open(clean_captcha_path), 
                        config='--psm 6 -c tessedit_char_whitelist=0123456789'
                    )
                    
                    captcha_text = ''.join(filter(str.isdigit, captcha_text))
                    
                    if len(captcha_text) > 6:
                        captcha_text = captcha_text[:6]
                        
                    if len(captcha_text) < 4:
                        print("⚠️ تصویر کپچا ناخوانا بود. رفرش صفحه و تلاش مجدد...")
                        driver.refresh()
                        time.sleep(3)
                        continue 
                        
                    # ۲. صید تازه فیلدها در هر بار اجرای حلقه
                    username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "UserName")))
                    password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password")))
                    captcha_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "CaptchaCode")))

                    # پاک کردن و پر کردن فیلدها
                    driver.execute_script("arguments[0].value = '';", username_field)
                    driver.execute_script("arguments[0].value = '';", password_field)
                    driver.execute_script("arguments[0].value = '';", captcha_field)

                    username_field.send_keys(student['id'])
                    password_field.send_keys(student['password'])
                    captcha_field.send_keys(captcha_text)

                    typed_code = captcha_field.get_attribute('value')
                    if not typed_code:
                        print("⚠️ فیلد کپچا به دلایلی پر نشد! تلاش مجدد...")
                        driver.refresh()
                        time.sleep(3)
                        continue
                    
                    # کلیک روی دکمه ورود
                    submit_button = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".btn.btn-primary.btn-sm"))
                    )
                    driver.execute_script("arguments[0].click();", submit_button)
                    time.sleep(4) 
                    
                    # بررسی وضعیت لاگین
                    check_login = driver.find_elements(By.ID, "UserName")
                    
                    if len(check_login) == 0:
                        print("🎉 تبریک! لاگین موفقیت آمیز بود.")
                        print("⏳ در حال صبر برای لود شدن کامل داشبورد...")
                        time.sleep(5)
                        
                        # ========================================================
                        # شروع استخراج اطلاعات به صورت کاملاً تفکیک‌شده و مقاوم
                        # ========================================================
                        try:
                            classes_data, exams_data, hw_data = [], [], []

                            # ۱. بررسی جلسات آنلاین
                            print("\n--- 🔍 در حال بررسی جلسات آنلاین ---")
                            try:
                                online_icon = WebDriverWait(driver, 10).until(
                                    EC.presence_of_element_located((By.CSS_SELECTOR, ".bi-mic"))
                                )
                                driver.execute_script("arguments[0].click();", online_icon)
                                time.sleep(5) 
                                rows = driver.find_elements(By.TAG_NAME, "tr")
                                classes_data = [row.text.strip() for row in rows if row.text.strip()]
                                driver.back() 
                                time.sleep(5)
                            except:
                                print("⚠️ بخش جلسات آنلاین پیدا نشد یا پاپ‌آپ مانع شد.")
                                driver.get(config.UNIVERSITY_URL + "/Dashboard")
                                time.sleep(4)

                            # ۲. بررسی آزمون‌ها
                            print("\n--- 🔍 در حال بررسی آزمون‌ها ---")
                            try:
                                exams_icon = WebDriverWait(driver, 10).until(
                                    EC.presence_of_element_located((By.CSS_SELECTOR, ".bi-question-diamond"))
                                )
                                driver.execute_script("arguments[0].click();", exams_icon)
                                time.sleep(5)
                                exam_rows = driver.find_elements(By.TAG_NAME, "tr")
                                exams_data = [row.text.strip() for row in exam_rows if row.text.strip()]
                                driver.back()
                                time.sleep(5) 
                            except:
                                print("⚠️ بخش آزمون‌ها پیدا نشد یا پاپ‌آپ مانع شد.")
                                driver.get(config.UNIVERSITY_URL + "/Dashboard")
                                time.sleep(4)
                            
                            # ۳. بررسی تکالیف
                            print("\n--- 🔍 در حال بررسی تکالیف ---")
                            try:
                                homework_icon = WebDriverWait(driver, 10).until(
                                    EC.presence_of_element_located((By.CSS_SELECTOR, ".bi-journal-bookmark-fill"))
                                )
                                driver.execute_script("arguments[0].click();", homework_icon)
                                time.sleep(5)
                                hw_rows = driver.find_elements(By.TAG_NAME, "tr")
                                hw_data = [row.text.strip() for row in hw_rows if row.text.strip()]
                                driver.back()
                                time.sleep(5)
                            except:
                                print("⚠️ بخش تکالیف پیدا نشد یا پاپ‌آپ مانع شد.")
                                driver.get(config.UNIVERSITY_URL + "/Dashboard")
                                time.sleep(4)
                            
                            print("\n🏁 استخراج اطلاعات با موفقیت به پایان رسید!")
                            
                            # مقایسه با حافظه و ارسال نوتیفیکیشن
                            MEMORY_FILE = os.path.join(config.DATA_DIR, f"memory_{student['id']}.json")
                            current_data = {"classes": classes_data, "exams": exams_data, "homework": hw_data}
                            new_alerts = []
                            
                            if os.path.exists(MEMORY_FILE):
                                with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                                    old_data = json.load(f)
                                    
                                for cls in current_data["classes"]:
                                    if cls not in old_data.get("classes", []): new_alerts.append(f"👨‍🏫 کلاس جدید: {cls}")
                                        
                                for exm in current_data["exams"]:
                                    if exm not in old_data.get("exams", []): new_alerts.append(f"📝 آزمون جدید: {exm}")
                                        
                                for hw in current_data["homework"]:
                                    if hw not in old_data.get("homework", []): new_alerts.append(f"📚 تکلیف جدید: {hw}")
                            else:
                                print("\n🧠 اولین اجرای ربات: در حال ساخت حافظه اولیه...")
                                
                            with open(MEMORY_FILE, "w", encoding="utf-8") as f:
                                json.dump(current_data, f, ensure_ascii=False, indent=4)
                                
                            print("\n=========================================")
                            print("🔔 گزارش تغییرات سامانه:")
                            
                            if not new_alerts:
                                message_text = f"🎓 وضعیت دانشجو {student['id']}:\n\n✅ هیچ تغییر جدیدی در سامانه یافت نشد."
                                print(message_text)
                            else:
                                message_text = f"🎓 آپدیت جدید برای {student['id']}:\n\n" + "\n\n".join(new_alerts)
                                for alert in new_alerts:
                                    print(f"👉 {alert}")

                            # ارسال پیام به تلگرام
                            print("\n📲 در حال ارسال گزارش به تلگرام...")
                            try:
                                url = f"https://api.telegram.org/bot{config.TELEGRAM_TOKEN}/sendMessage"
                                payload = {"chat_id": student['chat_id'], "text": message_text}
                                response = requests.post(url, data=payload)
                                if response.status_code == 200:
                                    print("✅ پیام با موفقیت به تلگرام ارسال شد!")
                                else:
                                    print(f"⚠️ خطا در ارسال پیام به تلگرام: {response.text}")
                            except Exception as e:
                                print(f"❌ خطای ارتباط با تلگرام: {e}")
                                    
                            print("=========================================")
                            
                        except Exception as e:
                            print(f"❌ مشکلی در بخش استخراج اطلاعات سایت پیش آمد: {e}")
                        
                        # شکستن حلقه کپچا برای این دانشجو و رفتن سراغ نفر بعدی
                        break 
                        
                    else:
                        print("❌ کپچا یا رمز اشتباه بود. صفحه را رفرش می‌کنیم...")
                        driver.refresh()
                        time.sleep(3)
                        
                except Exception as loop_error:
                    print(f"⚠️ مشکلی در این تلاش رخ داد، ۵ ثانیه مکث و تلاش مجدد... (خطا: {loop_error})")
                    try:
                        driver.refresh()
                    except:
                        pass
                    time.sleep(5)
                    continue
                    
            else:
                print(f"\nمتاسفانه ربات بعد از {max_tries} بار تلاش برای {student['id']} موفق نشد.")
                
    except Exception as e:
        print(f"❌ خطای کلی مرورگر:\n {e}")

    finally:
        print("\n❌ در حال بستن مرورگر و آزادسازی منابع...")
        if 'driver' in locals():
            try:
                driver.quit() 
            except:
                pass
        print("✅ منابع این مرحله آزاد شدند.")

# --- بخش زمان‌بندی دائم سرور ابری بر اساس تایم UTC سرور ---

# توجه: خط run_bot() مستقیم حذف شد تا با ری‌استارت شدن کانتینر الکی پیام اضافه نیاید.
# زمان‌های زیر به وقت UTC تنظیم شده‌اند که دقیقاً معادل ساعت‌های ایران است:
schedule.every().day.at("04:30").do(run_bot)  # ساعت ۸:۰۰ صبح ایران
schedule.every().day.at("14:30").do(run_bot)  # ساعت ۱۸:۰۰ (۶ عصر) ایران
schedule.every().day.at("19:30").do(run_bot)  # ساعت ۲۳:۰۰ (۱۱ شب) ایران

print("\n⏳ ربات با موفقیت مستقر شد و دقیقاً راس ساعت‌های ۸ صبح، ۶ عصر و ۱۱ شب به وقت ایران کار خواهد کرد...")

while True:
    schedule.run_pending()
    time.sleep(60)
