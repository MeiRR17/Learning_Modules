# -*- coding: utf-8 -*-

import subprocess
import os
import time
import random
import sys

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# ==========================================
# תצורה והגדרות מערכת (System Configuration)
# ==========================================

# תיקיית הבסיס שאליה יורדו כל התכנים.
BASE_DIR = os.path.abspath("University_Course_Data")

# ==========================================
# מבנה נתונים ראשי (Data Structure)
# ==========================================
# מבנה זה מכיל את כלל התיקיות, תתי-התיקיות, מזהי הקבצים ושמותיהם,
# בדיוק כפי שחולצו ממערך הלוגים שסופק.

COURSE_STRUCTURE = {
    "01-Linux": [
        ("1xYCk36ACkcChL67D6i2C_41nTouLr6-B", "01-intro.mp4"),
        ("1ikVUr7OJy5KZIDtGegA9jnHuTfwFfXNW", "02-HPC.mp4"),
        ("1EsGyeSZmtCYJSCXZRWPmJ4SUAN1js0E1", "03-Ubuntu_installation.mp4"),
        ("1OdI8_b7HecKZ-KmeDfP4igL1PtveyS6u", "04-examples_1_to_9.mp4"),
        ("15lxbVbaYdtxEmIjNqfR57SjGIfw0TQNe", "05-examples_10_to_17.mp4"),
        ("1VU-zwbYnMehKiAD8aN7dsFt9XzEVme2m", "06-examples_18_to_20.mp4"),
        ("1xZNU7mvVr4LLOI2O8tAIUCKoSfKvm8sh", "07-examples_21_to_22.mp4"),
        ("13ljVDk64wjs8TqihXMhV5WzpYc-BPJY8", "08-example_23.mp4"),
        ("1p3_raX6OMeqyBlLlPrQcVrVfgmJbyeCF", "09-example_24.mp4"),
        ("1LihYuxXIW7c8r1PV0SCeZ4jMW2fEAAMT", "10-example_25.mp4"),
        ("1EWfH6k7g9nbavsajai-eR-40f4Ud0hpN", "11-running_script.mp4"),
        ("1SQH-7p40a_xSk7O8sS3v4-gaJOT8jCqj", "12-conclusion.mp4")
    ],
    "02-Python/part1": [
        ("1XZywoFEyZjohxysc-zv4fbuNvU-wN2hh", "01-intro_to_Python.mp4"),
        ("1ag1L-60gfnK_e7MQ3lKigMTgn7VE1k4P", "02-jupyter_part1.mp4"),
        ("1N7FiATvujF3AZl7bVs3deFZ-1pH1-V4k", "03-jupyter_part2.mp4"),
        ("1SyFwIgVf8jse-fbHgFs5Av2E4muk0Zr0", "04.mp4"),
        ("10vMCyG8KO_xJ38WDB9FiM9TkMUqTw4Rt", "05.mp4"),
        ("1KNvS_a6iXzfKm2j3BIC9z79y0sJSZ7U5", "06.mp4"),
        ("1rEGPIdBp6GMR46DrS7oYLei49_0HSXx-", "07.mp4"),
        ("1SZ6kNBLsmIHDmYBo0DOXE33tLkC1CMF6", "08.mp4"),
        ("1AgF4mv85PtDrDzhFLmPyxKPrKj201pQZ", "09.mp4"),
        ("1NsaHLjhyrEsNdZYH1PJdsxWtgwBoKqHw", "10.mp4"),
        ("1ixdP3TWaGou5M4KfexfkhOaqOJpL1HwP", "11.mp4"),
        ("1RFYxLi3CCOz0L9_EePP2L-LfTV7_hA-Z", "12.mp4")
    ],
    "02-Python/part2": [
        ("10rVfYmuWC3k7zew9Lat0Q_VONwa3T_Ju", "part1.mp4"),
        ("1Z65GWeM2fjbNQ_deAl31_U28EhGIhXFl", "part2.mp4"),
        ("17gdU_Jwgc-D5PyjdgO7keVFEIe8Yxq6T", "part3.mp4"),
        ("1QtLzI_sxbi1uM9UcNrUI_zl3myccjqI4", "part4.mp4"),
        ("17udv7lhluoCsU0IrqWOqoop0KCs9UJyq", "part5.mp4"),
        ("18lgafGa3jMHZJD9HOiV0dEVOFlsXYf4I", "part6.mp4"),
        ("1HmeHyF8zqHLVs-AgTNgGUZ-pgwq4OUYi", "part7.mp4"),
        ("1FRCnaaflKmYA6dVS3K8lVecx5cSfWQGZ", "part8.mp4"),
        ("1zm0kxsla5aslwfrvvFRSDaNtIquvRuvf", "part9.mp4"),
        ("1ccxK4Sa7EWhRIfKQNuxS5eaUwOobOcbj", "targil.mp4")
    ],
    "03-Hadoop-MapReduce/Part 1": [
        ("1NyctjgIqSVaa-i-C2I4oDQjRNIzTdDcD", "01.mp4"),
        ("1F-U5FiHXkXJDM-onFSI29G1MwI135FTl", "02.mp4"),
        ("1cvnl505IDNAw1DlqPp0xQxx5VrYmO2si", "03.mp4"),
        ("1tY2wCQT5Hg8v9pA5MmgN3eToNHKHy9aY", "04.mp4"),
        ("1qLkFstTrtYYnJFc1l2dq7lFubolQy73x", "05.mp4"),
        ("1ja8G2vW3Z2nkkzMG80PKnAzi4FW6I092", "06.mp4"),
        ("12mJY_0qz55UbaX5vovlWFMqIq3wW1Tw5", "07.mp4"),
        ("1Bt2ogxSmz-at5EZgkgfgAojAQoOdxzUt", "08.mp4"),
        ("1ZJdQpnfFJ9nj8_PIPn5haTOmFoT8fVtb", "09.mp4"),
        ("1dwlpZ14DNPwFfzffioAA9plEJj-BMQpC", "10.mp4")
    ],
    "03-Hadoop-MapReduce/Part 2": [
        ("1pACScxva15NB3DmJjh-rzDYEmEiwesxj", "01.mp4"),
        ("1xjiUwHB9xwLJiPa95eh-Eme_P9EodgOi", "02.mp4"),
        ("1_SFNZUxdt-2mhdw_c18bPt96Q9oBExv5", "03.mp4"),
        ("1-GZgyN3lJ_V3xj7vsXz7bGTtnZsd7i5l", "04.mp4"),
        ("169YBmjYP6_yHb6KKRTx1o_cJLxodD8US", "05.mp4"),
        ("1Yl8P2GrHwi-V-Brgw9gFwEozjRdWsjWN", "06.mp4"),
        ("1JVo4iX0GgOJ-RK8wpR6OGsTursUh9B8J", "07.mp4")
    ],
    "04-Spark": [
        ("15lph9fIVMxw0FmHDLtQ_h5zYDV6jZSmc", "01.mp4"),
        ("1P4UdMoT8_REPU6BrzZwoUi3w4TKn6CRe", "02.mp4"),
        ("13BJgZhyDLzB41Jqrf1vNzcySrM2KuhAM", "03.mp4"),
        ("1x3N3s1btmu9jT0ojbm_kOha2gOfTXpK1", "04.mp4"),
        ("1Cmw9DMHb5GduV4Ku2TfI58Rq-xDAY8wp", "05.mp4"),
        ("1RFZSuxSiPIHiKufEsfvym_91ZSNr8O3h", "06.mp4"),
        ("1TrJkkFhGcL3yoZHb3lsuNOtLlGK82bT4", "07.mp4"),
        ("1g-hAq8UsqvhHZdndYZCZOcctRn-cb7Aw", "08.mp4"),
        ("1cnBai-DiUwo-usAkHnv_CtzpCUQrcg1m", "09.mp4")
    ],
    "05-RegEx": [
        ("189EJMhuqpn2tiglE9pwtHMsFq9ZfYyHS", "01.mp4"),
        ("10iM3Vpu00dFP08-SkX46hpNyA4L1ZsXR", "02.mp4"),
        ("1RrXDqoGJ9tUF_oJCBMNrSbEXYaTVH_ln", "03.mp4"),
        ("18c_-NFXUJyQrjWaGBJR3jXSpvZXH4NZr", "04.mp4"),
        ("1qedHVPca2K4cwQqEjs34yAA3grNk1Kd8", "05.mp4"),
        ("1svboam7Uj3l9BHqBdDVPj7OyOXRPa535", "06.mp4"),
        ("14c2NmKHKLQTqHTf0kcrf4Vt88TIYS40m", "07.mp4")
    ],
    "06-Data preparation": [
        ("18cKAea-jOyZH967HDJzUHTAecFut-Etm", "intro.mp4")
    ],
    "08-Tableau/Part 1": [
        ("1uagLalHR9Wmn9JzPuH04SCdFMwAWJngX", "01.mp4"),
        ("1j4YDAQCi01sBY_QtcJOHVI5ZxlzL43Dd", "02.mp4"),
        ("1Ld34y-IdsKrEA6K-fAf9Ba_PxknsAGW6", "03.mp4"),
        ("12FKTkoS5HNQFzrdjF-H_KRySR5LDHx4r", "04.mp4"),
        ("1TVq6Qw-FZOA5XIB5Q99t1M5D3wN4NvU8", "05.mp4"),
        ("1-F_khmMm4paQEsj1aywuG3u0pjjw5rnI", "06.mp4"),
        ("1ZUJUVGPhfU5Rw6fKRtXFUkAh0QGBqOzt", "07.mp4")
    ],
    "08-Tableau/Part 2": [
        ("1AEGvgy7qcPPxQpEB-B0HS-JqXN77-gnn", "01.mp4"),
        ("1X-vYff6z-_cJKeaHjlRbSCq_bXQ-K8mf", "02.mp4"),
        ("1955_Oi3BI02kKDoqcrPRbMHYs_7bFsgK", "03.mp4"),
        ("1HQpk623vCVTLeKisC-il0B1gsVCvmDGp", "04.mp4"),
        ("1K76oDn9p7t1BEibSzigCh_060RM_UqoX", "05.mp4")
    ]
}

# ==========================================
# לוגיקת ליבה (Core Engine)
# ==========================================

def create_directory_if_not_exists(path: str):
    """
    פונקציה ליצירת נתיב תיקיות מלא.
    הפרמטר exist_ok=True מונע קריסת קוד אם התיקייה כבר נוצרה בעבר.
    """
    if not os.path.exists(path):
        print(f"[*] Creating directory structure: {path}")
        os.makedirs(path, exist_ok=True)

def download_file(file_id: str, output_path: str):
    """
    פונקציה המנהלת את תהליך ההורדה מול yt-dlp ומטפלת בחריגות תקשורת.
    """
    # בדיקת אידמפוטנטיות - האם הקובץ כבר קיים פיזית (כדי לאפשר עצירה והמשך)
    if os.path.exists(output_path):
        # וידוא בסיסי שמדובר בקובץ ולא בתיקייה שנוצרה בטעות
        if os.path.isfile(output_path):
            file_size = os.path.getsize(output_path)
            if file_size > 1024:  # קובץ גדול מ-1KB סביר שהוא וידאו תקין ולא קובץ שגיאה ריק
                print(f"[-] File already exists, skipping: {output_path}")
                return True

    url = f"https://drive.google.com/file/d/{file_id}/view"
    
    # הרכבת וקטור הפקודה המלא שיישלח לטרמינל.
    # נעשה שימוש במערך אובייקטים (List) כדי למנוע בעיות של שרשור מחרוזות ורווחים בנתיבים.
    command = [
        "python", "-m", "yt_dlp",
        "--cookies", "cookies.txt",
        "--no-check-certificate",           # מעקף חיוני לסביבות מסוננות ברמת ה-SSL
        "--format", "best[ext=mp4]/best",
        "--no-part",                         # מניעת הוספת סיומות זמניות כמו f140 לשם הקובץ
        "-o", output_path,                  # הגדרת יעד השמירה המדויק (כולל שם הקובץ)
        "--quiet", "--no-warnings",         # צמצום רעשי פלט בטרמינל, נציג רק שגיאות ממשיות
        url
    ]
    
    try:
        print(f"[>] Downloading: {os.path.basename(output_path)} ... ", end="", flush=True)
        # הרצת התהליך המשני. check=True יזרוק חריגה במקרה של סטטוס שגיאה (קוד חזרה שאינו 0)
        subprocess.run(command, check=True)
        print("SUCCESS")
        return True
    except subprocess.CalledProcessError as e:
        print(f"FAILED (Process Error: {e})")
        return False
    except Exception as ex:
        print(f"FAILED (Unexpected Error: {ex})")
        return False

def main():
    print(f"==================================================")
    print(f"  Google Drive Sync Engine - Static Cookie Mode")
    print(f"  Target Root Directory: {BASE_DIR}")
    print(f"==================================================\n")

    # וידוא שקובץ העוגיות אכן קיים באותה תיקייה לפני שמתחילים את הריצה המסיבית
    if not os.path.exists("cookies.txt"):
        print("[!] ERROR: 'cookies.txt' file not found!")
        print("Please export your Chrome cookies to a file named 'cookies.txt'")
        print("and place it in the same folder as this script before running.")
        return

    create_directory_if_not_exists(BASE_DIR)
    
    total_files = sum(len(files) for files in COURSE_STRUCTURE.values())
    processed_files = 0
    failed_downloads = []

    # איטרציה על פני המילון: שליפת נתיב התיקייה ורשימת הקבצים המשויכת לה
    for folder_path, files in COURSE_STRUCTURE.items():
        # בניית הנתיב המקומי השלם (Root + Sub-folder)
        # שימוש ב-normpath כדי לוודא תאימות של הלוכסנים (Slashes) בין ווינדוס ללינוקס
        full_dir_path = os.path.normpath(os.path.join(BASE_DIR, folder_path))
        create_directory_if_not_exists(full_dir_path)
        
        for file_id, file_name in files:
            processed_files += 1
            print(f"\n[Progress: {processed_files}/{total_files}] Folder: {folder_path}")
            
            full_file_path = os.path.join(full_dir_path, file_name)
            
            success = download_file(file_id, full_file_path)
            
            if not success:
                failed_downloads.append(f"{folder_path}/{file_name} (ID: {file_id})")
            
            # ויסות עומסים מואץ (Fast Throttling) - זמן המתנה מצומצם משמעותית
            sleep_time = random.uniform(0.5, 1.5)
            time.sleep(sleep_time)

    print(f"\n==================================================")
    print(f"  Execution Completed.")
    print(f"  Processed {processed_files} files.")
    
    if failed_downloads:
        print(f"\n[!] WARNING: {len(failed_downloads)} files failed to download.")
        print("Please review the list below. You may need to re-run the script or check permissions/network.")
        for item in failed_downloads:
            print(f"    - {item}")
    else:
        print(f"\n[v] ALL FILES SUCCESSFULLY SYNCED.")
    print(f"==================================================")

if __name__ == "__main__":
    main()