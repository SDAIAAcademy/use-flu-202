# الحل المرجعي: المختبر 1.2 صنّف قبل أن تشارك

نقطة البداية: `files/document_register.xlsx` و`files/accommodation_request.docx`. التحقق بالكود: `uv run labs/solutions/check.py 1.2`.

## السجل

| # | الملف | المستوى | الأداة |
|---|---|---|---|
| 1 | visual_identity_guide.pdf | عام | أي مساعد |
| 2 | report_excerpt_en.docx | عام | أي مساعد |
| 3 | hr_faq.pdf | عام | أي مساعد |
| 4 | policy_flexible_work.pdf | عام | أي مساعد |
| 5 | procurement_guide.pdf | مقيد | المساعد المعتمد فقط |
| 6 | quarterly_report_q3_2026.pdf | مقيد | المساعد المعتمد فقط |
| 7 | minutes_portal_committee.pdf | مقيد | المساعد المعتمد فقط |
| 8 | meeting_transcript_sept_review.txt | مقيد | المساعد المعتمد فقط |
| 9 | beneficiary_inquiries_q3.xlsx | سري | لا شيء (مستخلصه المرمّز مقيد) |
| 10 | accommodation_request.docx | سري | لا شيء (نسخته بعناصر نائبة) |
| 11 | quote_b_naseej.pdf | سري | لا شيء |
| 12 | C-2026-121_22oct.docx | سري | لا شيء |

الأسباب في `answer_key_files.md`. الكود يتحقق أن الأداة في كل صف تتبع قاعدة المستوى في ورقة «قواعد المركز».

## الطلب بعناصر نائبة

الأمر في `reference/D1_2_prompt.txt`. الكود يقرأ نص الطلب الأصلي، فيجد فيه رقم هوية وجوالًا وبريدًا ورقم ملف طبي، ثم يستبدل الاسم والرقم الوظيفي ورقم الطلب وتاريخه بعناصر نائبة (`reference/D1_2_placeholders.json`) ويحذف الباقي، ويثبت أن لا شيء منها بقي، وأن الأمر نفسه لا يحمل أي معرّف ولا أي تفصيل صحي.
