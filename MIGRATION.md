# Migration of productivity

This course was moved from the previous slide system by `academy migrate`. The inner markup of every slide is unchanged; each `<section>` tag got an `id`, section slides a session number, lab slides their lab id, and a slide drawn with coordinates or holding a layout of the course's own stylesheet that cannot reflow `data-read="scaled"`. Each deck keeps its old file name as its unit id, so its published address keeps answering. `labs/` and `assets/` are copied as they were.

Run the engine from this folder with `node academy.mjs <command>` (`check`, `build`, `check --layout --shots`); it finds the engine in `$ACADEMY_ENGINE`, then the folder named in `.academy-engine`, then `../engine`. Or run `node <engine>/bin/academy.mjs <command> --root <this folder>`.

## What is left, and how long it takes

About **1 h 26 min** of a person's work before `academy check` passes, and about **2 h 24 min** more to clear its warnings, which the house standard also asks for. The estimate counts each task below and each finding of `academy check` as this migration found them; a coding agent does the same work faster, but a person still decides the outcomes of each session and reviews the checkpoints.

| Work | Minutes |
|---|---|
| The tasks under "Needs a person" (4) | 72 |
| 14 × `text/clock` (error) | 14 |
| 18 × `quiz/why` (warning) | 90 |
| 10 × `slide/dense` (warning) | 50 |
| 1 × `notes/ratio` (warning) | 3 |
| 1 × `text/em-dash` (warning) | 1 |

Then `node academy.mjs check --layout --shots` opens every slide in Chrome (a few minutes for a course of five decks). It reports what the static check cannot see: a slide whose content is cut off or wider than the slide (`layout/overflow`, about 5 minutes each; long lines of code are the usual case, and the old system's own `?check` reported most of them too) and slides that do not reflow in the reading view on a phone (`layout/phone-wide`, `layout/phone-text`). Compare its contact sheets (`.shots/<lang>/<deck>/sheet-<n>.png`) with the old decks.

## Slides

Counted in the old deck and in the new source; "a → b" where they differ.

| Old deck | New deck | Slides | Speaker notes | Checkpoints | Lab slides | Pictures | Fragments | Break slides dropped |
|---|---|---|---|---|---|---|---|---|
| slides/day1.html | slides/day1.html | 55 | 27 | 3 | 4 | 28 | 0 | 0 |
| slides/day2.html | slides/day2.html | 47 | 18 | 5 | 4 | 20 | 0 | 0 |
| slides/day3.html | slides/day3.html | 40 | 14 | 5 | 4 | 14 | 0 | 0 |
| slides/day4.html | slides/day4.html | 46 | 15 | 5 | 4 | 18 | 0 | 0 |
| slides/day5.html | slides/day5.html | 20 | 7 | 0 | 0 | 0 | 0 | 0 |
| All | | 208 | 81 | 18 | 16 | 80 | 0 | 0 |

## Rebuilt from the old files

- slides/day1.html → slides/day1.html: "أساسيات العمل مع الذكاء الاصطناعي", 4 sessions, 4 labs.
- slides/day2.html → slides/day2.html: "الإنتاجية في المهام اليومية", 4 sessions, 4 labs.
- slides/day3.html → slides/day3.html: "البحث والمعرفة وإعادة تصميم العمل", 4 sessions, 4 labs.
- slides/day4.html → slides/day4.html: "الوكلاء والبرمجة التوليدية والتبنّي", 4 sessions, 4 labs.
- slides/day5.html is the capstone day (no lab slides; presentation slides or a capstone title): its sessions are not sessions in the new engine, so data-session was removed from its section slides.
- 7 course outcomes from the list of outcomes on index.html (LO1 to LO7).
- The audience, from the "Audience" paragraph of index.html.
- 1 prerequisite from the "Environment" paragraph of index.html.
- The capstone summary, from the "Capstone" section of index.html (its paragraphs and its list of options).
- The capstone rubric: قيمة مقيسة في تجربتين على الأقل 25, تصميم سير العمل والتفويض 20, الوصف: الأوامر أو التعليمات أو المواصفات 20, التحقق: معيار القبول والأخطاء الملتقطة 15, المسؤولية: البيانات والإفصاح وخطة التبنّي 10, العرض والتجربة الحية 10.
- The capstone's talk_minutes (5) and qa_minutes (2), from the timers "العرض والتجربة الحية" and "الأسئلة" of the old slides/day5.html line 163.
- Title "رفع الإنتاجية بالذكاء الاصطناعي", track fluency, language ar; the id "productivity" comes from the folder name.
- 16 lab pages of the previous system (labs/D1_1_task_map.html, labs/D1_2_edges_and_safety.html, labs/D1_3_rice.html, labs/D1_4_context_library.html, labs/D2_1_inbox.html, labs/D2_2_transcript_quotes.html, labs/D2_3_inquiries_budget.html, labs/D2_4_decision_deck.html, labs/D3_1_research_brief.html, labs/D3_2_ask_our_policies.html, labs/D3_3_custom_assistant.html, labs/D3_4_workflow_redesign.html, labs/D4_1_bulletin_agent.html, labs/D4_2_idea_to_spec.html, labs/D4_3_build_it.html, labs/D4_4_adoption_plan.html) became lab fragments (<article class="lab">) that the build wraps in the lab shell: the content of each <main> as it was written, the old header's facts (.meta) and its lead where it says more than the lab's summary. The pagers went (the shell links the previous and next lab), and so did the links to lab.css and academy.js on the old site.
- labs/capstone.html, a page of the previous system, was kept whole because no lab in course.json links to it; it now loads the engine's stylesheet (_engine/academy.css) and icon instead of lab.css and icon.svg on sdaiaacademy.github.io/slides, and the old academy.js is gone, so it no longer depends on the old site.

## Needs a person

- Which outcomes each session serves: write "lo" for each of the 16 sessions in course.json (["LO1"], or more than one), from the session titles and the slides; the old decks do not say, so until then "academy check" reports every outcome as not covered (lo/uncovered). (about 32 min)
- The capstone in course.json: add "submission" (what is handed in, and when); the old course page and capstone deck do not state them in a form the migration can read. (about 5 min)
- 3 parts of index.html that the migration does not read (listed under "Left out of index.html"): keep or drop each. (about 30 min)
- The old lab pages ended with "أكاديمية سدايا · رفع الإنتاجية بالذكاء الاصطناعي · كل الأسماء والجهات والأرقام في ملفات التدريب افتراضية."; the lab shell writes its own footer, so "كل الأسماء والجهات والأرقام في ملفات التدريب افتراضية." is no longer on them. Put it into each page that needs it, or into README.md if it is true of the whole course. (about 5 min)

## What `academy check` reports

On the course as migrated, apart from the codes a task above clears (`lo/uncovered`). `node academy.mjs check` prints each place with what to do.

| Code | Level | Findings | Minutes | First places |
|---|---|---|---|---|
| `text/clock` | error | 14 | 14 | slides/day4.html:108, slides/day4.html:114, slides/day4.html:186 … |
| `quiz/why` | warning | 18 | 90 | slides/day1.html:347, slides/day1.html:540, slides/day1.html:684 … |
| `slide/dense` | warning | 10 | 50 | slides/day2.html:147, slides/day3.html:89, slides/day3.html:358 … |
| `notes/ratio` | warning | 1 | 3 | slides/day4.html |
| `text/em-dash` | warning | 1 | 1 | slides/day1.html:474 |

## Left out of index.html

- index.html line 95: "التمارين والملفات" (2 paragraphs, 11 list items, 18 links) is not on the new course page, which is generated from course.json. Move what is still true into course.json (a "sources" group for a list of links, "prerequisites" for what to prepare), README.md or a lab page, or drop it.
- index.html line 156: "لمن هذه الدورة", the paragraph "الإطار" (1 paragraph, 1 link) is not on the new course page, which is generated from course.json. Move what is still true into course.json (a "sources" group for a list of links, "prerequisites" for what to prepare), README.md or a lab page, or drop it.
- index.html line 160: "The footer" ("أسماء التطبيقات أمثلة لا توصيات، وكل الأسماء والجهات والأرقام في ملفات التدريب افتراضية.") is not on the new course page, which is generated from course.json. Move what is still true into course.json (a "sources" group for a list of links, "prerequisites" for what to prepare), README.md or a lab page, or drop it.

## Good to know

- 18 checkpoint slides written as <section class="slide quiz"> (slides/day1.html line 347, slides/day1.html line 540, slides/day1.html line 684, slides/day2.html line 14, slides/day2.html line 223, slides/day2.html line 383, slides/day2.html line 541, slides/day2.html line 691, slides/day3.html line 14, slides/day3.html line 168, slides/day3.html line 309, slides/day3.html line 454, slides/day3.html line 574, slides/day4.html line 14, slides/day4.html line 218, slides/day4.html line 397, slides/day4.html line 545, slides/day4.html line 707) are kept as written. Each is one activity, in the build and in the browser: its lead paragraph (p.lead), or else its heading, is the question; the room answers with the number keys or a click. "academy check" asks for the misconception behind each wrong option (quiz/why).
- labs/D3_3_custom_assistant.html: the old page's title was "مساعدك المخصّص"; the lab shell shows the lab's title from course.json, "ابنِ مساعدًا واختبره".

## Break slides dropped

- None.

## Markup that does not parse strictly

The build parses slide sources strictly. Fix each place below in the slide source (close the element, quote the attribute, write `&lt;` for a "<" in text).

- None: every deck parses strictly.
