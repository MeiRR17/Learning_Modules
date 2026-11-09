# תוכנית מימוש 36: chidiwilliams/buzz

> **מאגר יעד:** `MeiRR17/Learning_Modules` | **עדיפות:** P2 | **החלטה:** REFERENCE | **מקור:** https://github.com/chidiwilliams/buzz

## נחיצות ופער מוצר
Offer manual review UI for local transcription outputs.
מיקומו של הרכיב בפרויקט: public learning tools and existing local Apple Silicon whisper transcription; media/models never committed. יש לבדוק את ה־HEAD, ענפי העבודה, ה־CI והקוד הקיים לפני שינוי כדי שלא תיווצר תשתית שנייה הפועלת במקביל.

## ארכיטקטורה, API וגבולות
Authorized local audio -> reviewed transcription/subtitles without background auto-sync.
ליצור adapter מאחורי feature flag כבוי, עם מזהה מקור מורשה, גרסת upstream/מודל, סטטוס, זמני ריצה, SHA-256 של קלט/פלט כשמתאים, וקישור ראיות. תוצרי ביניים יישמרו מחוץ ל־Git ולנתונים הקנוניים. אין ענן, שינוי מערכת, השבתה או חיבור הרשאות ללא אישור נפרד.

## תוכנית הגרסאות
**0.1 — אימות היתכנות:** זיהוי הפער המדויק והחלופה הקיימת, ADR החלטה, הגדרת צרכן/בעלים, ביצוע מיפוי תלויות.
**0.2 — אבטחה ורישוי:** לנעול commit/release ומודל, לבדוק LICENSE (תצפית: MIT), תלויות, רישיונות מודלים/מידע, SBOM, תחומי רשת, זיכרון ו־CPU.
**0.3 — Vertical slice:** On Mac, measure Hebrew editor usability with one owned 2-minute recording. הרצה על נתונים סינתטיים/מורשים בלבד. לתעד baseline ללא הכלי והשוואה מדידה.
**0.4 — אינטגרציה:** קוד מתאם ואירועים, טיפול ב־timeouts ובשגיאות, גבולות משאבים, מתג הפעלה, בדיקות רכיב/תאימות והרשאות מינימליות.
**0.5 — איכות:** לאמת מקרי כשל, נתונים שגויים, מסמכים/טקסטים בעברית כשיש לכך קשר, שימור מקור, השפעת ביצועים והימנעות משינוי לרכיבי ליבה.
**1.0 — השקה מותנית:** רק אחרי PR, תיעוד, בעלות תפעולית, בדיקות בסביבה המתאימה, rollback והחלטת בעלים; לא כל P2 מצדיק שלב זה.

## תרחיש קבלה ומדדים
בפיילוט: On Mac, measure Hebrew editor usability with one owned 2-minute recording.
במבחן קבלה נדרשים נכונות פלט בהשוואת אמת, אפס גישה בלתי מורשית, שחזור תוצאה, מדידת latency/זיכרון/טוקנים אם רלוונטי, התנהגות offline וחזרה נקייה לנתיב הישן. אין להסתמך על ציונים שמופיעים בשיווק של upstream.

## בחירה, חלופות ובלמים
Optional desktop tool; not part of server transcription pipeline.
**סיכון ממוקד:** Avoid duplicate installers, hidden transcription APIs, or model downloads.
אם התועלת הנמדדת אינה מוכחת או שהרישוי אינו מתאים, יש לתעד defer/reject במקום להתקין. מצב `REFERENCE` הוא סטטוס תכנון, **לא הודעת הצלחה בהטמעה**.

## Checklist להשלמה
- [ ] רישיון קוד+מודל+מידע הוכח; גרסה מוצמדת
- [ ] סודיות/הרשאות/משאבים מאושרים ו־flag כבוי כברירת מחדל
- [ ] קוד או ניסוי השוואתי ותוצאות מדודות
- [ ] בדיקות יחידה, אינטגרציה, קצה ורגרסיה
- [ ] תיעוד הפעלה, ניטור, rollback וקישור ל־PR בעל ראיות
