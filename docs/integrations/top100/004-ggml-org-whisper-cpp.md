# 4. ggml-org/whisper.cpp — תוכנית מימוש ייעודית

> סטטוס: EXISTING_BASELINE; עדיפות מחקר: P0; מקור: https://github.com/ggml-org/whisper.cpp; מאגר יעד: MeiRR17/Learning_Modules. מסמך זה אינו אישור התקנה או רישוי.

## צורך ונחיצות בפרויקט
Keep the existing Apple Silicon transcription scripts reliable; do not duplicate the engine.

מיקום בארכיטקטורה הנוכחית: Public source repository with established whisper.cpp helpers. Keep all media, subtitles, licensed fonts and model weights outside Git.

## תפקוד, חוזה אינטגרציה ובעלות נתונים
Existing Learning_Modules shell workflow -> WAV, TXT/SRT/VTT using pinned Whisper.cpp revision and explicitly licensed model.

המתאם שייבנה חייב להחזיר תוצאה מובנית עם מזהה פעולה, גרסת מקור, סטטוס הצלחה/כשל, זמני עיבוד, ושיוך למקור קלט מורשה. יש להפריד תוצרי עבודה זמניים מתשתיות פעילות ולחשוף מתג הפעלה כבוי כברירת מחדל, פלט JSON ניתן לביקורת ושגיאות ללא סודות. אם הכלי הוא פלטפורמה שלמה או חלופה למערכת קיימת, יש לבודד אותו כ־spike ולא כחיבור קבוע.

## תוכנית עבודה מחולקת לשלבים
**שלב 0 — בדיקת התאמה:** להשוות את היכולת המבוקשת לקוד, לענפים ול־PRים הקיימים במאגר היעד. לציין מי הרכיב הקיים ומה יהיה היתרון המדיד על פניו. לכתוב החלטת ADR קצרה אם צריך שינוי תשתיתי.

**שלב 1 — בטיחות ותאימות:** לבדוק גרסת upstream מדויקת ו־commit קבוע, רישיון קוד (תצפית קודמת: MIT), תלויות, רישיונות מודלים/דאטה, SBOM, מפת רשת, הרשאות, עלות, התאמה לחומרת המחשב ויכולת rollback. אין לבצע התקנת upstream אוטומטית לפני אישור הבדיקות.

**שלב 2 — פיילוט:** Run current shell with a short local owned clip; verify Metal acceleration, UTF-8 RTL output, timestamp stability and failure behavior. להכין נתוני דוגמה סינתטיים או מורשים, לבצע הרצה מקומית מבודדת, ולאסוף baseline מאותו קלט ללא הרכיב.

**שלב 3 — מתאם ייעודי:** לממש את חוזה הקלט־פלט שלעיל במודול מקומי עם הגבלת גדלים/זמנים, תיעוד גרסאות, מתג opt-in והפרדת backend מהלוגיקה העסקית. אין להעתיק קוד שלם או ליצור שירות מתחרה אם כבר קיימת חלופה טובה.

**שלב 4 — אימות וקבלה:** Measure media fidelity, Hebrew RTL rendering or transcription CER/WER where applicable, timestamps, reproducibility, and zero unapproved media uploads. לכלול בדיקות יחידה, תרחישי כשל, מקרי הרשאות חסרות, רגרסיה בהפעלת רכיבים קיימים והדגמה ניתנת לשחזור. מדידות הן של הפיילוט, ולא נתונים משוערים מתוך README.

**שלב 5 — הדרגתיות ותחזוקה:** להתחיל במשתמש/מכונה אחת ובקריאה בלבד כשאפשר, לתעד ניטור ועלויות, להצמיד גרסה, לספק כיבוי מהיר וליצור PR נפרד שמכיל את הבדיקות. לפרוס רק לאחר אימות סביבת היעד ואישור בעלים.

## החלטת אימוץ, תנאי סף וחלופות
Baseline engine; do not reinstall or replace unless faster-whisper wins real benchmarks.

סיכון ייחודי: A prior import already references this upstream; check version drift and license for models.

החלטה נוכחית: **EXISTING_BASELINE** — תעדוף והחלטת רישוי, לא אישור לפריסה אוטומטית. יש להציג מדוע הכלי נחוץ על פני החלופות ברשימת ה־57, כולל עלות תפעולית, רישוי, רמת אמון ותלות בשירות חיצוני.
טרם קיים פיילוט מאומת של הרכיב הזה בריפו; אל תסמן אותו כממומש.

## הגדרת סיום (Definition of Done)
החלטת רישוי ותלות חתומה; מתאם או דוח השוואה ממשי לפי ההחלטה; fixture שחזור; תוצאות בדיקות מדווחות עם פקודות ולוגים; מקור קלט וקישור לפלט; rollback מוכח; PR בענף המתאים; ורק לאחר מכן שינוי סטטוס ל־pilot-tested או enabled. אם תנאי סף נכשל — סטטוס rejected/deferred עם נימוק ותאריך בדיקה מחדש, ולא התקנה בכוח.
