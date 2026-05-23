import flet as ft
import requests
import urllib.parse
import time
import os

def main(page: ft.Page):
    page.title = "Hussein AI"
    page.theme_mode = ft.ThemeMode.DARK
    page.rtl = True
    page.padding = 20
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    current_image_url = [""]

    app_title = ft.Text(
        "Hussein AI",
        size=32,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLUE_ACCENT
    )

    app_subtitle = ft.Text(
        "اكتب وصفا وسيتكفل الذكاء الاصطناعي بالباقي",
        size=14,
        color=ft.Colors.GREY_400,
        text_align=ft.TextAlign.CENTER
    )

    prompt_input = ft.TextField(
        label="اكتب وصف الصورة هنا",
        hint_text="مثال: رائد فضاء على المريخ",
        border_radius=15,
        border_color=ft.Colors.BLUE_ACCENT,
        multiline=True,
        min_lines=2,
        max_lines=4,
    )

    # بقية كود الأزرار والـ Layout المتبقية سنقوم بحقنها تلقائياً
    # (تأكيد نهاية الملف بالطريقة القياسية لأندرويد)
