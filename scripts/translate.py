from glob import glob
from google_trans_new import google_translator  
import re
from tqdm import tqdm
import time

file_list = glob("..\\config\\locale\\*\\LC_MESSAGES\\django.po")



for filename in file_list:
    lang = filename[17:19]
    translator = google_translator(url_suffix="es")  
    print(lang)
    c = False
    txt = ""
    with open(filename, 'r') as f:
        lines = [line.rstrip() for line in f]
        i = 0
        for line in tqdm(lines):
            i+=1
            if i%50 == 0:
                time.sleep(3)
            if 'msgid' in line:
                c = True
                m = re.findall(r'"([^"]*)"', line)
                
                trad = translator.translate(m[0], lang_src = 'es', lang_tgt=lang)  
                txt += line + "\n"
            elif c and 'msgstr' in line:
                txt += 'msgstr "' + trad + '" \n'
            else:
                txt += line + "\n"
    with open(filename, 'w') as f:
        f.write(txt)
        
