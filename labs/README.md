# إنتاجية العمل المعرفي بالذكاء الاصطناعي: المختبرات

ستة عشر مختبرًا لمقرر أكاديمية سدايا **USE-FLU-202**، مدة كل منها 25 دقيقة. المختبرات صفحات إرشادية بالعربية: الهدف،
والملفات، وخطوات بدقائقها وطلبات تُنسخ، وأسئلة تحقق، وتمرين إضافي ✱، وملاحظات للمدرب. لا كود يكتبه المشارك.

كل المختبرات في جهة واحدة: **مركز الواحة للخدمات المشتركة**، مركز حكومي افتراضي. كل الأسماء والأرقام والجهات والعناوين
البريدية وهمية.

## ما يحتاجه المشارك

- متصفح، وحساب مجاني في مساعد ذكاء اصطناعي عام واحد على الأقل. الخطط المجانية تكفي، ولا يُنزَّل أي نموذج على الجهاز.
- دفتر مستند إلى المصادر أو مساحة مشروع (اليوم 3)، ومساحة عمل للوكلاء ومنصة للبرمجة التوليدية (اليوم 4). لكل مختبر
  بديل مكتوب في صفحته حين لا تتاح الأداة: مشروع في مساعد عام، أو ملف جاهز.
- حزمة مكتبية لجداول البيانات والعروض.
- سجل القياس: `files/my_productivity_kit.xlsx`، ويبقى مفتوحًا طوال المقرر.

## نقطة البداية والحل

كل مختبر يبدأ من ملفات جاهزة ولا يعتمد على مختبر آخر في اليوم نفسه. حين يبني مختبر على يوم سابق، له ملف بديل في
`files/start/` يبدأ منه من لم يكمل.

| المختبر | الصفحة | يبدأ من | الحل المرجعي |
|---|---|---|---|
| 1.1 | `D1_1_task_map.html` | `weekly_tasks.xlsx` | `solutions/D1_1_task_map.md` |
| 1.2 | `D1_2_classify.html` | `document_register.xlsx`، `accommodation_request.docx` | `solutions/D1_2_classify.md` |
| 1.3 | `D1_3_rice.html` | `minutes_portal_committee.pdf` | `solutions/D1_3_rice.md` |
| 1.4 | `D1_4_context_library.html` | `start/context_sample.md` | `solutions/D1_4_context_library.md` |
| 2.1 | `D2_1_letter.html` | `letter_points.txt`، `glossary_en_ar.xlsx` | `solutions/D2_1_letter.md` |
| 2.2 | `D2_2_forms.html` | `forms/` (عشرون نموذجًا)، `hr_faq.pdf` | `solutions/D2_2_forms.md` |
| 2.3 | `D2_3_reconcile.html` | `beneficiary_inquiries_q3_coded.xlsx` | `solutions/D2_3_reconcile.md` |
| 2.4 | `D2_4_decision_deck.html` | `deck_brief.txt`، `quarterly_report_q3_2026.pdf` | `solutions/D2_4_decision_deck.md` |
| 3.1 | `D3_1_research_brief.html` | `start/research_brief.txt`، `start/verification_log.csv`، `start/research_report_sample.md` | `solutions/D3_1_research_brief.md` |
| 3.2 | `D3_2_ask_our_policies.html` | `policy_flexible_work.pdf`، `hr_faq.pdf`، `procurement_guide.pdf` | `solutions/D3_2_ask_our_policies.md` |
| 3.3 | `D3_3_custom_assistant.html` | `frequent_questions.xlsx` | `solutions/D3_3_custom_assistant.md` |
| 3.4 | `D3_4_workflow_redesign.html` | `monthly_report_workflow.xlsx` | `solutions/D3_4_workflow_redesign.md` |
| 4.1 | `D4_1_agent_connector.html` | `start/agent_task.txt`، `shared_mailbox/`، `circulars/` | `solutions/D4_1_agent_connector.md` |
| 4.2 | `D4_2_idea_to_spec.html` | `start/tracker_need.txt` | `solutions/D4_2_idea_to_spec.md` |
| 4.3 | `D4_3_build_it.html` | `start/tracker_requirements.md`، `start/tracker_AGENTS.md` | `solutions/D4_3_build_it.md` |
| 4.4 | `D4_4_adoption_plan.html` | `start/adoption_plan_template.md` | `solutions/D4_4_adoption_plan.md` |

## تشغيل الحلول

```bash
uv run labs/solutions/check.py            # كل المختبرات
uv run labs/solutions/check.py 2.3 4.1    # بعضها
```

ملف واحد يعلن اعتمادياته، ويحتاج [uv](https://docs.astral.sh/uv/)، ويحتاج Node.js للمختبر 4.3. يطبع لكل مختبر ما أعاد
حسابه و`PASS`، ولا يكتب شيئًا على القرص ولا يتصل بأي نموذج.

**ما يُشغَّل فعلًا:** كل حساب على الملفات: مجاميع خريطة المهام، وإزالة البيانات الشخصية، وقراءة النماذج العشرين وتحويل
التاريخ الهجري، وإعادة حساب الاستفسارات، ووجود كل رقم في صفحته من التقرير، ودليل كل إجابة في وثائق السياسات، وتوقيت
سير العمل، وطبقة صلاحيات الوكيل، وفحوص القبول الثلاثة للنموذج الأولي.

**ما يُشغَّل بنموذج بديل:** كل خطوة يؤديها المشارك في مساعد محادثة. النموذج البديل (`solutions/standin.json`) ردود
مكتوبة فيها الأخطاء التي يقع فيها مساعد حقيقي، ليُظهر كل فحص أن خطوة التحقق في المختبر تلتقطها. لم تُشغَّل الحلول على
نموذج حقيقي، ولم تُجرَّب المختبرات في أدوات البحث المعمق والدفاتر والوكلاء ومنصات البناء: هذه تتغير، ويجربها المدرب قبل
كل دفعة.

## الملفات

| الملف | ما هو | المزروع فيه |
|---|---|---|
| `weekly_tasks.xlsx` | ست عشرة مهمة أسبوعية بأوقاتها | ست مهام خارج الحد المتعرج |
| `document_register.xlsx` | سجل اثني عشر ملفًا وقواعد المركز | أربعة عام، وأربعة مقيد، وأربعة سري |
| `accommodation_request.docx` | طلب تسهيلات وظيفية | بيانات شخصية وصحية تُزال قبل أي مساعد |
| `minutes_portal_committee.pdf` | محضر لجنة من أربع صفحات | مقترح لم يُقر، ومهمة بلا موعد |
| `letter_points.txt`، `glossary_en_ar.xlsx` | نقاط خطاب ومسرد المركز | أرقام تُطابق، ومصطلحات معتمدة |
| `forms/` | عشرون نموذج طلب تدريب | تكلفة بالحروف، وتاريخ هجري، واعتماد فارغ، ومكرر، وتكلفة معدلة، وطلب فوق الحد |
| `beneficiary_inquiries_q3_coded.xlsx` | 458 صفًا مرمّزًا | ستة صفوف مكررة، وتهجئتان للقناة الواحدة |
| `beneficiary_inquiries_q3.xlsx` | الأصل ببيانات شخصية وهمية | يُصنَّف «سريًّا» ولا يدخل أي مساعد |
| `quarterly_report_q3_2026.pdf`، `deck_brief.txt`، `visual_identity_guide.pdf` | تقرير ربعي من 12 صفحة، وموجز عرض، ودليل هوية | الرضا 84% في الملخص و81% في الجدول |
| `policy_flexible_work.pdf`، `hr_faq.pdf`، `procurement_guide.pdf` | دليل الموظفين | تعارض في بداية مهلة التظلم؛ ولا ذكر لبدل العمل عن بعد |
| `frequent_questions.xlsx` | عشرة أسئلة اختبار بإجاباتها | سؤال خارج المصادر، وافتراض خاطئ، وحالة تصعيد |
| `monthly_report_workflow.xlsx` | عشر خطوات بأوقاتها | خطوتا تحقق وقتهما صفر في الطريقة الحالية |
| `shared_mailbox/`، `circulars/` | خمس رسائل، وستة تعاميم وقالب نشرة | تعليمة مزروعة في الرسالة 03، وتعميم سري، وتعميم مكرر |
| `start/` | نقاط بداية مكتوبة باليد | التقرير التدريبي فيه خمسة ادعاءات: اثنان يصمدان |
| `quote_*.pdf`، `training_budget_2026.xlsx`، `service_kpis_2026.xlsx`، `inbox_week43.txt`، `meeting_transcript_sept_review.txt`، `report_excerpt_en.docx` | مواد للتمارين الإضافية ولسجل التصنيف | مفتاحها في `solutions/answer_key_files.md` |

## إعادة توليد الملفات

ملفات `files/` مولّدة ببذرة ثابتة، عدا `files/start/` المكتوب باليد. النصوص في `_tools/texts.py`، والمولّد:

```bash
uv run labs/_tools/prepare_files.py            # الجداول والمستندات والنصوص وملفات PDF ومفتاح الإجابات
uv run labs/_tools/prepare_files.py --no-pdf   # دون متصفح Chrome
```

ملفات PDF يطبعها Chrome دون واجهة ليصح تشكيل العربية. إعادة التوليد تعيد كتابة `solutions/answer_key_files.md`.
