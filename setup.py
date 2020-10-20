from django.utils.crypto import get_random_string

chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'

def generate_key():
    return get_random_string(50, chars)


local_settings_file = open("config/settings/local_settings.py", "w+")
local_settings_file.write(f"SECRET_KEY = '{generate_key()}'\n")
local_settings_file.write(f"SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = 'ID_GOOGLE'\n")
local_settings_file.write(f"SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'KEY_GOOGLE'\n")

local_settings_file.close()
