import flet as ft
import requests
import urllib.parse
import time

def main(page: ft.Page):
    # --- إعدادات الصفحة والواجهة ---
    page.title = "مُولد الصور الذكي - Hussein AI"
    page.theme_mode = ft.ThemeMode.DARK # وضع داكن فخم
    page.rtl = True # دعم اللغة العربية بالكامل
    page.padding = 30
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    # تحسين استجابة الواجهة على شاشات الهواتف
    page.window_width = 400
    page.window_height = 750

    # --- عناصر الواجهة (UI Components) ---
    
    # عنوان التطبيق العلوي
    app_title = ft.Text(
        "Hussein AI 🌟",
        size=32,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLUE_ACCENT
    )
    
    app_subtitle = ft.Text(
        "اكتب وصفاً وسيقوم الذكاء الاصطناعي بتحويله إلى لوحة فنية",
        size=14,
        color=ft.Colors.GREY_400,
        text_align=ft.TextAlign.CENTER
    )

    # حقل إدخال النص (وصف الصورة)
    prompt_input = ft.TextField(
        label="ما الذي تتخيله؟",
        hint_text="مثال: رائد فضاء يركب حصاناً على كوكب المريخ، واقعي، 4k...",
        border_radius=15,
        border_color=ft.Colors.BLUE_ACCENT,
        multiline=True,
        min_lines=2,
        max_lines=4,
    )

    # عنصر عرض الصورة (مخفي في البداية)
    result_image = ft.Image(
        src="",
        width=350,
        height=350,
        fit=ft.ImageFit.COVER,
        border_radius=20,
        visible=False
    )
    
    # بطاقة أنيقة تحتوي على الصورة لإعطائها ظلالاً وجمالية
    image_card = ft.Card(
        content=ft.Container(
            content=result_image,
            padding=5,
        ),
        elevation=10,
        visible=False
    )

    # مؤشر التحميل (يظهر أثناء التوليد)
    loading_indicator = ft.ProgressRing(
        width=40,
        height=40,
        stroke_width=4,
        visible=False
    )
    
    loading_text = ft.Text(
        "يتم الآن رسم لوحتك الفنية... انتظر قليلاً",
        color=ft.Colors.BLUE_200,
        visible=False
    )

    # --- دالة توليد الصورة (The Logic) ---
    def generate_image(e):
        # التأكد من أن المستخدم كتب شيئاً
        if not prompt_input.value:
            prompt_input.error_text = "الرجاء كتابة وصف أولاً!"
            page.update()
            return
        
        # تفعيل وضع التحميل وإخفاء الصور السابقة
        prompt_input.error_text = None
        generate_btn.disabled = True
        image_card.visible = False
        result_image.visible = False
        loading_indicator.visible = True
        loading_text.visible = True
        page.update()

        try:
            # تجهيز النص وترميزه ليتوافق مع الروابط (URL Encoding)
            user_prompt = prompt_input.value
            encoded_prompt = urllib.parse.quote(user_prompt)
            
            # رابط الـ API المجاني المعتمد على نماذج تجميعية متطورة (Flux/Stable Diffusion)
            # نقوم بإضافة تايم-ستامب عشوائي لمنع الكاش وجلب صورة جديدة دائماً
            seed = int(time.time())
            image_url = f"https://image.pollinations.ai/p/{encoded_prompt}?width=1024&height=1024&nologo=true&seed={seed}"
            
            # تحديث مصدر الصورة وجعلها مرئية
            result_image.src = image_url
            
            # حيلة برمجية صغيرة للتأكد من أن الصورة تم تحميلها بنجاح قبل عرضها
            requests.get(image_url, timeout=15)
            
            # إخفاء مؤشر التحميل وعرض النتيجة
            loading_indicator.visible = False
            loading_text.visible = False
            image_card.visible = True
            result_image.visible = True
            
        except Exception as ex:
            # في حال حدوث خطأ في الاتصال
            prompt_input.error_text = "فشل الاتصال بالخادم، تحقق من الإنترنت."
            loading_indicator.visible = False
            loading_text.visible = False
            
        # إعادة تفعيل زر التوليد
        generate_btn.disabled = False
        page.update()

    # زر التوليد السحري
    generate_btn = ft.ElevatedButton(
        text="توليد الصورة السحرية",
        icon=ft.Icons.AUTO_AWESOME,
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BLUE_ACCENT,
            padding=20,
            shape=ft.RoundedRectangleBorder(radius=15),
        ),
        on_click=generate_image
    )

    # --- بناء الهيكل النهائي وتوزيع العناصر عمودياً ---
    page.add(
        ft.Column(
            [
                app_title,
                app_subtitle,
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT), # مسافة فارغة
                prompt_input,
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                generate_btn,
                ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                loading_indicator,
                loading_text,
                image_card
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        )
    )

# تشغيل التطبيق
if __name__ == "__main__":
    ft.app(target=main)
