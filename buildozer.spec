[app]
title = Hussein AI
package.name = husseinai
package.domain = org.hosin.ai
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# المكتبات البرمجية التي يحتاجها تطبيقك ليعمل داخل الأندرويد
requirements = python3,flet,requests,urllib3,certifi,idna,charset-normalizer

orientation = portrait
fullscreen = 0
android.archs = arm64-v8a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
