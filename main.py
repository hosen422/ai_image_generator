import flet as ft
import requests
import urllib.parse
import time
import os

def main(page: ft.Page):
    page.title = "مُولد الصور الذكي - Hussein AI"
    page.theme_mode = ft.ThemeMode.DARK 
    page.rtl = True 
    page.padding = 30
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    current_image_url = [""]

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

    prompt_input = ft.TextField(
        label="ما الذي تتخيله؟",
        hint_text="مثال: رائد فضاء يركب حصاناً على كوكب المريخ، واقعي، 4k...",
        border_radius=15,
        border_color=ft.Colors.BLUE_ACCENT,
        multiline=True,
        min_lines=2,
        max_lines=4,
    )

    result_image = ft.Image(
        src="",
        width=350,
        height=350,
        fit=ft.ImageFit.COVER,
        border_radius=20,
        visible=False
    )

    image_card = ft.Card(
        content=ft.Container(
            content=result_image,
            padding=5,
        ),
        elevation=10,
        visible=False
    )

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

    status_text = ft.Text("", size=14, weight=ft.FontWeight.BOLD)

    def generate_image(e):
        if not prompt_input.value:
            prompt_input.error_text = "الرجاء كتابة وصف أولاً!"
            page.update()
            return

        prompt_input.error_text = None
        generate_btn.disabled = True
        save_btn.visible = False 
        image_card.visible = False
        result_image.visible = False
        loading_indicator.visible = True
        loading_text.visible = True
        status_text.value = ""
        page.update()

        try:
            user_prompt = prompt_input.value
            encoded_prompt = urllib.parse.quote(user_prompt)
            seed = int(time.time())
            image_url = f"https://image.pollinations.ai/p/{encoded_prompt}?width=1024&height=1024&seed={seed}"
            
            current_image_url[0] = image_url
            requests.get(image_url, timeout=15)

            result_image.src = image_url
            loading_indicator.visible = False
            loading_text.visible = False
            image_card.visible = True
            result_image.visible = True
            save_btn.visible = True 

        except Exception as ex:
            prompt_input.error_text = "فشل الاتصال بالخادم، تحقق من الإنترنت."
            loading_indicator.visible = False
            loading_text.visible = False

        generate_btn.disabled = False
        page.update()

    def save_image_to_device(e):
        if not current_image_url[0]:
            return
        
        save_btn.disabled = True
        status_text.value = "جاري تحميل وحفظ الصورة..."
        status_text.color = ft.Colors.BLUE_200
        page.update()

        try:
            response = requests.get(current_image_url[0], timeout=20)
            if response.status_code == 200:
                download_path = "/sdcard/Download"
                if not os.path.exists(download_path):
                    download_path = os.path.expanduser("~")

                filename = f"Hussein_AI_{int(time.time())}.jpg"
                full_path = os.path.join(download_path, filename)

                with open(full_path, "wb") as f:
                    f.write(response.content)

                status_text.value = f"✅ تم حفظ الصورة بنجاح في مجلد Downloads باسم {filename}"
                status_text.color = ft.Colors.GREEN_ACCENT
            else:
                status_text.value = "❌ فشل تحميل الصورة من السيرفر."
                status_text.color = ft.Colors.RED_ACCENT
        except Exception as ex:
            status_text.value = f"❌ خطأ أثناء الحفظ: {str(ex)}"
            status_text.color = ft.Colors.RED_ACCENT

        save_btn.disabled = False
        page.update()

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

    save_btn = ft.ElevatedButton(
        text="حفظ الصورة في الجهاز",
        icon=ft.Icons.DOWNLOAD,
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.GREEN_700,
            padding=15,
            shape=ft.RoundedRectangleBorder(radius=12),
        ),
        visible=False,
        on_click=save_image_to_device
    )

    page.add(
        ft.Column(
            [
                app_title,
                app_subtitle,
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT), 
                prompt_input,
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                generate_btn,
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                loading_indicator,
                loading_text,
                image_card,
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                save_btn,
                status_text
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
