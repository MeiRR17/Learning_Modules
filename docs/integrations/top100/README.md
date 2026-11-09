# תוכניות שילוב כלי GitHub — MeiRR17/Learning_Modules

הספרייה כוללת **6 תוכניות מימוש עצמאיות** שהוקצו למאגר הזה מתוך רשימה גלובלית של 57 מועמדים. תחום האחריות: תמלול ומדיה מקורית בלבד, ללא מודלים/הקלטות/תמלולים פרטיים בתוך Git.

**הבחנה מחייבת:** קיום תוכנית אינו התקנה, הפעלה, אישור רישוי או מוכנות לפרודקשן. `P0/P1/P2` מציין עדיפות לבדיקה; `PILOT/COMPARE/GATED/REFERENCE` הוא סוג החלטה, ולא סטטוס הצלחה. קוד פיילוט קיים אינו מופעל אוטומטית.

## אינדקס מימוש לפי כלי

| # | מאגר המקור ותוכנית מפורטת | עדיפות | החלטת שילוב | נחיצות |
|---:|---|:---:|---|---|
| 3 | [SYSTRAN/faster-whisper](./003-systran-faster-whisper.md) | P0 | PILOT | Provide a local transcription alternative when Whisper.cpp is slow or lacks timing quality. |
| 4 | [ggml-org/whisper.cpp](./004-ggml-org-whisper-cpp.md) | P0 | EXISTING_BASELINE | Keep the existing Apple Silicon transcription scripts reliable; do not duplicate the engine. |
| 36 | [chidiwilliams/buzz](./036-chidiwilliams-buzz.md) | P2 | REFERENCE | Offer manual review UI for local transcription outputs. |
| 41 | [heygen-com/hyperframes](./041-heygen-com-hyperframes.md) | P0 | GATED_PILOT | Generate professionally consistent original branded video intros and captions. |
| 51 | [OpenMontageInc/OpenMontage](./051-openmontageinc-openmontage.md) | P2 | REFERENCE | Assess integrated video studio only after HyperFrames proves insufficient. |
| 57 | [koala73/worldmonitor](./057-koala73-worldmonitor.md) | P2 | REFERENCE | Study geopolitical monitoring UI for independent evidence-led media design. |

## כללי פעולה

1. **אין התקנה גורפת.** בוחרים לפי פער מוצר אמיתי, בודקים את הרישיון המדויק וגרסאות מודלים/דאטה, ומריצים fixture סינתטי או מורשה.
2. **אין שני מנועים שווים לפרודקשן ללא הצדקה.** מתעדים בדיקת A/B והשוואת accuracy/latency/cost/maintenance ומחליטים על engine יחיד או fallback לפי סוג קלט.
3. **הגנת המידע:** אין להעלות ספרים, תמלולים, הקלטות, מודלי שפה, קובצי הרשאות או נתוני מחקר מוגנים ל־GitHub או לשירות AI חיצוני.
4. **הטמעה ממוקדת:** מתאם נקודתי בנתיב הקוד המתאים, opt-in/feature-flag, תוצאות מובנות ו־read-only ברירת מחדל, בדיקות ורישום ראיות.
5. **מיזוג רק לאחר אימות:** PR, CI ממוקד, תוצאות אמיתיות, תיעוד rollback, וסקירה של ענפים/גרסאות קודמות. פריט שאינו נחוץ עובר ל־deferred ולא להתקנה מאולצת.

## אימות מסירה

השלמה של **תוכנית** דורשת קובץ Markdown ייחודי לכל כלי ברשימה. השלמה של **אינטגרציה** דורשת קוד, ריצת בדיקות, החלטת רישוי, ראיות מדודות ו־PR; אין לערבב בין שני המצבים.
