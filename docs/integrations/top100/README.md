# מפת תוכניות האינטגרציה ב־MeiRR17/Learning_Modules

מיפוי הבעלות עבר סקירה שנייה לפי תוכן המאגר, לא רק לפי שם הכלי. **3 תוכניות עצמאיות** משויכות למאגר הזה. הקשר: Optional local transcription methods; public repo cannot store user recordings.

| # | מאגר המקור ותוכנית מימוש | עדיפות | החלטה | צורך |
|---:|---|---|---|---|
| 3 | [SYSTRAN/faster-whisper](./003-systran-faster-whisper.md) | P0 | PILOT | Provide a local transcription alternative when Whisper.cpp is slow or lacks timing quality. |
| 4 | [ggml-org/whisper.cpp](./004-ggml-org-whisper-cpp.md) | P0 | EXISTING_BASELINE | Keep the existing Apple Silicon transcription scripts reliable; do not duplicate the engine. |
| 36 | [chidiwilliams/buzz](./036-chidiwilliams-buzz.md) | P2 | REFERENCE | Offer manual review UI for local transcription outputs. |

## הוראות יישום

1. לוודא חסר יכולת נוכחית לפי קוד אמיתי והענפים הפעילים; לא להסתמך רק על כוכבים או תיאור upstream.
2. לבדוק commit/release, LICENSE, זכויות מודלים ונתונים, שרשרת תלויות, עלות והרשאות. אין פטור מרישוי כשהקוד קיים ב־GitHub.
3. לבצע פיילוט עם fixture מורשה, baseline והשוואה מדידה. אם כלי אחר כבר פועל היטב, לשקול defer.
4. להטמיע קוד רק behind opt-in flag, בלי כתיבה אוטומטית למקורות/פרסום/שליחת סודות, ועם אפשרות rollback.
5. להעלות קוד + בדיקות ותוצאות מדודות ל־Draft PR ולהפעיל רק לאחר אימות בעלים.

**חשוב:** תוכניות קיימות ≠ ספריות מותקנות ≠ בדיקות שעברו ≠ פריסה עובדת. כלי במצב REFERENCE/COMPARE/GATED לא נחשב כחיבור פעיל.

קובצי המדדים ותוצאות הבדיקות של כל כלי צריכים להיכנס ל־PR של אותו מוצר; אין להעלות תוצרי קבצים פרטיים, תמלולים או קרדנציאלים לגיטהאב.
