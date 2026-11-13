# /// script
# requires-python = ">=3.11"
# dependencies = ["openpyxl>=3.1", "python-docx>=1.1", "pypdf>=5.0", "hijridate>=2.5"]
# ///
"""Run the reference solution of every lab and check it against the course files.

    uv run labs/solutions/check.py            # all labs
    uv run labs/solutions/check.py 2.3 4.1    # some labs

What runs for real: every computation on the files (counts, recalculations, extraction from the
twenty forms, retrieval over the policies, the classification rules, the agent's permission
layer, the timing of the workflow). What runs against a stand-in: every step that a participant
does in a chat assistant. The stand-in is a scripted model (standin.json): fixed replies that
contain the mistakes a real assistant makes, so each check shows that the lab's verification
step catches them. No model is called and nothing is written to disk.
"""
from __future__ import annotations

import json
import random
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

import openpyxl
from docx import Document
from pypdf import PdfReader

HERE = Path(__file__).resolve().parent
LABS = HERE.parent
FILES = LABS / "files"
REF = HERE / "reference"
STANDIN = json.loads((HERE / "standin.json").read_text(encoding="utf-8"))
LABS_RUN: dict[str, callable] = {}


def lab(lab_id):
    def wrap(fn):
        LABS_RUN[lab_id] = fn
        return fn
    return wrap


def ref(name: str) -> str:
    return (REF / name).read_text(encoding="utf-8")


def norm(text: str) -> str:
    """Arabic text as compared here: presentation forms folded, diacritics and tatweel removed."""
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"[ً-ْـ]", "", text)
    return text.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا").replace("ة", "ه").replace("ى", "ي")


def sheet_rows(path: Path, sheet: str | None = None):
    wb = openpyxl.load_workbook(path, data_only=False)
    ws = wb[sheet] if sheet else wb.worksheets[0]
    rows = list(ws.iter_rows(values_only=True))
    return rows[0], rows[1:]


def docx_text(path: Path) -> str:
    d = Document(path)
    parts = [p.text for p in d.paragraphs]
    for t in d.tables:
        for row in t.rows:
            parts.append(" | ".join(c.text for c in row.cells))
    return "\n".join(parts)


def pdf_pages(path: Path) -> list[str]:
    return [norm(p.extract_text() or "") for p in PdfReader(path).pages]


def words(text: str) -> int:
    return len(re.findall(r"\S+", text))


# =============================================================== Day 1
@lab("1.1")
def lab_1_1():
    head, rows = sheet_rows(FILES / "weekly_tasks.xlsx", "مهام الأسبوع")
    assert len(rows) == 16, len(rows)
    key = {int(r[0]): (r[1], r[2]) for r in (l.split(",") for l in ref("D1_1_map.csv").strip().splitlines()[1:])}
    assert sorted(key) == list(range(1, 17))
    minutes = Counter()
    for r in rows:
        minutes[key[r[0]][0]] += r[3] * r[4]
        assert r[5] == f"=D{r[0] + 1}*E{r[0] + 1}", r[5]  # the weekly minutes are a formula, not a typed number
    print(f"  weekly minutes: inside {minutes['داخل']:g}, outside {minutes['خارج']:g}, mixed {minutes['مختلط']:g}, "
          f"total {sum(minutes.values()):g}")
    assert (minutes["داخل"], minutes["خارج"], minutes["مختلط"]) == (590, 197.5, 95)
    outside = sorted(n for n, (z, _) in key.items() if z == "خارج")
    assert outside == [3, 5, 6, 9, 13, 15], outside
    modes = Counter(m for _, m in key.values())
    print("  modes:", dict(modes))
    # Step 4: the same request twice to the stand-in; the acceptance criterion is checked by code
    for i, reply in enumerate(STANDIN["1.1"]["replies"], 1):
        promised = bool(re.search(r"\d", reply))
        n = words(reply)
        ok = n <= 80 and not promised
        print(f"  reply {i}: {n} words, promises a figure or date: {promised} -> {'accepted' if ok else 'rejected'}")
    verdicts = [words(r) <= 80 and not re.search(r"\d", r) for r in STANDIN["1.1"]["replies"]]
    assert verdicts == [True, False], verdicts  # the same request gave one acceptable and one unacceptable reply


ID_RE = re.compile(r"\b[12]\d{9}\b")
MOBILE_RE = re.compile(r"\b05\d{8}\b")
EMAIL_RE = re.compile(r"\S+@\S+")
MRN_RE = re.compile(r"MRN-\d+")


@lab("1.2")
def lab_1_2():
    _, rows = sheet_rows(FILES / "document_register.xlsx", "سجل الملفات")
    _, rules = sheet_rows(FILES / "document_register.xlsx", "قواعد المركز")
    levels = [r[0] for r in rules]
    assert levels == ["عام", "مقيد", "سري", "سري للغاية"], levels
    key = [l.split(",") for l in ref("D1_2_register.csv").strip().splitlines()[1:]]
    assert [k[1] for k in key] == [r[1] for r in rows], "the reference lists the register's files in order"
    allowed = {"عام": "أي مساعد", "مقيد": "المساعد المعتمد فقط", "سري": "لا شيء", "سري للغاية": "لا شيء"}
    for n, name, level, tool in key:
        assert (FILES / name).exists() or (FILES / "circulars" / name).exists(), name
        assert allowed[level] == tool, (name, level, tool)  # the tool follows the centre's rule for the level
    print("  levels:", dict(Counter(k[2] for k in key)))
    # Step 4: de-identify the accommodation request by code and prove nothing identifying is left
    text = docx_text(FILES / "accommodation_request.docx")
    found = {"national id": ID_RE.findall(text), "mobile": MOBILE_RE.findall(text), "email": EMAIL_RE.findall(text),
             "medical file": MRN_RE.findall(text)}
    print("  identifiers in the original:", {k: len(v) for k, v in found.items()})
    assert all(found.values())
    mapping = json.loads(ref("D1_2_placeholders.json"))
    safe = text
    for real, ph in mapping.items():
        safe = safe.replace(real, ph)
    safe = ID_RE.sub("", MOBILE_RE.sub("", EMAIL_RE.sub("", MRN_RE.sub("", safe))))
    for real in mapping:
        assert real not in safe, real
    assert not (ID_RE.search(safe) or MOBILE_RE.search(safe) or EMAIL_RE.search(safe) or MRN_RE.search(safe))
    prompt = ref("D1_2_prompt.txt")
    leaked = [w for w in ("العمود الفقري", "علاج", "تقرير طبي", "مستشفى") + tuple(mapping) if w in prompt]
    assert not leaked, leaked
    print("  the prompt carries no identifier and no health detail")


@lab("1.3")
def lab_1_3():
    pages = pdf_pages(FILES / "minutes_portal_committee.pdf")
    minutes_numbers = set(re.findall(r"\d[\d,]*", " ".join(pages)))
    def invented(text):
        return sorted(n for n in set(re.findall(r"\d[\d,]*", text)) if n not in minutes_numbers)
    generic = STANDIN["1.3"]["generic"]
    final = ref("D1_3_update.txt")
    print("  generic request, numbers not in the minutes:", invented(generic))
    print("  RICE request, numbers not in the minutes:", invented(final))
    assert invented(generic), "the stand-in's reply to the vague request invents a date"
    assert not invented(final)
    n = words(final)
    print(f"  final update: {n} words")
    assert n <= 180
    for must in ("186,000", "22 أكتوبر", "غير محدد في المحضر", "المرحلة الثانية", "25 أكتوبر"):
        assert must in final, must
    assert "الإطلاق التجريبي" not in final or "لم يُقر" in final  # the soft launch is not a decision


@lab("1.4")
def lab_1_4():
    context = ref("D1_4_context.txt")
    assert words(context) < 150, words(context)
    assert not (ID_RE.search(context) or MOBILE_RE.search(context) or EMAIL_RE.search(context))
    templates = [t.strip() for t in ref("D1_4_templates.txt").split("\n---\n")]
    assert len(templates) == 3
    for t in templates:
        fields = dict(line.split(": ", 1) for line in t.splitlines() if ": " in line[:30])
        for f in ("الاسم", "متى أستخدمه", "الأمر", "معيار القبول", "أخطاء شائعة"):
            assert f in fields, (f, t[:40])
        ph = re.findall(r"\[[^\]]+\]", fields["الأمر"])
        assert len(ph) >= 2, fields["الاسم"]
        print(f"  {fields['الاسم']}: {len(ph)} placeholders, {words(fields['الأمر'])} words")
    sample = (FILES / "start" / "context_sample.md").read_text(encoding="utf-8")
    assert words(sample.split("\n\n", 2)[2]) < 150

# =============================================================== Day 2
def inquiries(dedupe=True):
    head, rows = sheet_rows(FILES / "beneficiary_inquiries_q3_coded.xlsx")
    recs = [dict(zip(head, r)) for r in rows]
    if dedupe:
        seen, out = set(), []
        for r in recs:
            if r["رقم الطلب"] not in seen:
                seen.add(r["رقم الطلب"])
                out.append(r)
        recs = out
    return recs


CHANNELS = {"البوابه": "البوابة", "بريد إلكتروني": "البريد الإلكتروني"}


@lab("2.1")
def lab_2_1():
    rows = [r for r in inquiries() if r["الجهة"] == "هيئة المرجان للسياحة الساحلية" and r["تاريخ الاستلام"].startswith("2026-09")]
    closed = [r["مدة المعالجة (يوم)"] for r in rows if r["مدة المعالجة (يوم)"] not in (None, "")]
    n, c, avg = len(rows), len(closed), round(sum(closed) / len(closed), 1)
    print(f"  recomputed from the coded file: {n} inquiries, {c} closed, average {avg} days")
    points = (FILES / "letter_points.txt").read_text(encoding="utf-8")
    for v in (f"{n} ", f"({c} ", f"{avg} "):
        assert v in points, v
    figures = [str(n), str(c), str(avg)]
    letter, note, summary = ref("D2_1_letter.txt"), ref("D2_1_note.txt"), ref("D2_1_summary_en.txt")
    for name, text in (("letter", letter), ("note", note), ("summary", summary)):
        found = set(re.findall(r"\d+(?:\.\d+)?", text))
        need = [f for f in figures if not (name == "note" and f == str(c))]
        assert all(f in found for f in need), (name, need, found)
    formal = ("سعادة", "تفضلوا بقبول", "إشارة إلى")
    assert "إشارة إلى" in letter and not any(m in note for m in formal)
    glossary = ("shared-service centre", "processing time")
    assert words(summary) <= 80 and all(g in summary for g in glossary), words(summary)
    print(f"  letter {words(letter)} words, note {words(note)} words, summary {words(summary)} words")
    bad = STANDIN["2.1"]["summary_en"]
    hedges = [w for w in ("reduced", "improved", "faster", "trend") if w in bad.lower()]
    wrong = sorted(set(re.findall(r"\d+(?:\.\d+)?", bad)) - set(figures) - {"2026"})
    print(f"  stand-in summary: certainty words {hedges}, figures not in the points {wrong}")
    assert hedges and wrong


def form_fields(path):
    d = Document(path)
    kv = {}
    for t in d.tables:
        for row in t.rows:
            cells = [c.text.strip() for c in row.cells]
            if len(cells) >= 2:
                kv[cells[0]] = cells[1]
    notes = " ".join(p.text for p in d.paragraphs)
    return kv, notes


def to_number(text, words_map):
    digits = re.sub(r"[^\d]", "", text)
    if digits:
        return int(digits)
    return words_map.get(text)


def to_gregorian(text):
    from hijridate import Hijri
    months = {"محرم": 1, "صفر": 2, "ربيع الأول": 3, "ربيع الآخر": 4, "جمادى الأولى": 5, "جمادى الآخرة": 6, "رجب": 7,
              "شعبان": 8, "رمضان": 9, "شوال": 10, "ذو القعدة": 11, "ذو الحجة": 12}
    if "هـ" in text:
        m = re.match(r"(\d+) (.+) (\d{4})هـ", text)
        return Hijri(int(m.group(3)), months[m.group(2)], int(m.group(1))).to_gregorian().isoformat()
    m = re.match(r"(\d+) نوفمبر (\d{4})م", text)
    return f"{m.group(2)}-11-{int(m.group(1)):02d}"


@lab("2.2")
def lab_2_2():
    words_map = json.loads(ref("D2_2_words.json"))
    faq = " ".join(pdf_pages(FILES / "hr_faq.pdf"))
    assert "12,000" in faq
    cap = 12000
    truth = {}
    for path in sorted((FILES / "forms").glob("TR-2026-*.docx")):
        kv, notes = form_fields(path)
        cost = to_number(kv["التكلفة"], words_map)
        revised = re.search(r"المعدلة[^:]*: ([\d,]+)", notes)
        if revised:
            cost = int(revised.group(1).replace(",", ""))
        truth[kv["رقم الطلب"]] = {"emp": kv["الرقم الوظيفي"], "course": kv["اسم الدورة"],
                                  "start": to_gregorian(kv["تاريخ البداية"]), "cost": cost,
                                  "approved": kv["اعتماد المدير المباشر"]}
    assert len(truth) == 20
    seen, flags, dup = {}, [], []
    for no, t in truth.items():
        k = (t["emp"], t["course"], t["start"])
        if k in seen:
            flags.append(f"{no} duplicates {seen[k]}")
            dup.append(no)
        seen.setdefault(k, no)
        if t["cost"] > cap:
            flags.append(f"{no} cost {t['cost']:,} above {cap:,}")
        if not t["approved"]:
            flags.append(f"{no} has no manager approval")
    print("  needs a decision:", "; ".join(flags))
    assert len(flags) == 3
    total = sum(t["cost"] for no, t in truth.items() if no not in dup)
    print(f"  total cost of the {20 - len(dup)} distinct requests: {total:,}")
    assert truth["TR-2026-307"]["start"] == "2026-11-16"
    assert truth["TR-2026-318"]["cost"] == 7200 and truth["TR-2026-304"]["cost"] == 9500
    errors = []
    for row in STANDIN["2.2"]["extraction"]:
        t = truth[row["no"]]
        for f in ("start", "cost", "approved"):
            if str(row[f]) != str(t[f]):
                errors.append((row["no"], f))
    print(f"  stand-in extraction: {len(errors)} wrong cells:", ", ".join(f"{n} {f}" for n, f in errors))
    assert len(errors) == 4
    sample = sorted(random.Random(5).sample(sorted(truth), 5))
    in_sample = [e for e in errors if e[0] in sample]
    rows = {r["no"]: r for r in STANDIN["2.2"]["extraction"]}
    by_rule = [e for e in errors if (e[1] == "cost" and rows[e[0]]["cost"] in ("", None))
               or (e[1] == "start" and not str(rows[e[0]]["start"]).startswith("2026-11"))]
    rest = [e for e in errors if e not in in_sample and e not in by_rule]
    print(f"  random sample {', '.join(x[-3:] for x in sample)} catches {len(in_sample)}: {in_sample}")
    print(f"  column rules (empty cost, start outside November) catch {len(by_rule)}: {by_rule}")
    print(f"  caught only by reading the form: {rest}")


@lab("2.3")
def lab_2_3():
    raw = inquiries(dedupe=False)
    rows = inquiries()
    assert (len(raw), len(rows)) == (458, 452)
    channel = Counter(CHANNELS.get(r["القناة"], r["القناة"]) for r in rows)
    month = Counter(r["تاريخ الاستلام"][:7] for r in rows)
    entity = Counter(r["الجهة"] for r in rows).most_common(1)[0]
    days = [r["مدة المعالجة (يوم)"] for r in rows if r["مدة المعالجة (يوم)"] not in (None, "")]
    avg = round(sum(days) / len(days), 1)
    recomputed = {"total": len(rows), "portal": channel["البوابة"], "top_entity": entity[0],
                  "september": month["2026-09"], "avg_days": avg}
    print("  recomputed:", recomputed, "| channels:", dict(channel), "| months:", dict(sorted(month.items())))
    report = " ".join(pdf_pages(FILES / "quarterly_report_q3_2026.pdf"))
    assert "452" in report
    claimed = STANDIN["2.3"]["summary_figures"]
    wrong = 0
    print("  reconciliation:")
    for k, v in claimed.items():
        ok = str(v) == str(recomputed[k])
        wrong += not ok
        print(f"    {k}: summary {v} | recomputed {recomputed[k]} | {'matches' if ok else 'corrected'}")
    assert wrong == 3, wrong


@lab("2.4")
def lab_2_4():
    pages = pdf_pages(FILES / "quarterly_report_q3_2026.pdf")

    def check_outline(lines):
        problems = []
        for line in lines:
            title, figure, page = [x.strip() for x in line.split("|")]
            number = figure.strip("%")  # the PDF text keeps the digits; the percent sign may sit on either side
            if figure and number not in pages[int(page) - 1]:
                problems.append(f"{figure} not on page {page}")
            if "الرضا" in title and (figure != "81%" or page != "3"):
                problems.append(f"satisfaction must be the KPI table figure (81%, page 3), not {figure} on page {page}")
        return problems

    outline = [l for l in ref("D2_4_outline.txt").splitlines() if l.strip()]
    assert len(outline) == 6
    p = check_outline(outline)
    print("  reference outline:", p or "every figure is on its cited page")
    assert not p
    bad = check_outline(STANDIN["2.4"]["outline"])
    print("  stand-in outline:", bad)
    assert bad

# =============================================================== Day 3
_SOURCES: dict[str, str] = {}


def source_text(name: str) -> str:
    """The text of a pack document as compared here: normalised and lower case."""
    if name not in _SOURCES:
        path = FILES / name
        text = docx_text(path) if name.endswith(".docx") else " ".join(pdf_pages(path))
        _SOURCES[name] = norm(text).lower()
    return _SOURCES[name]


def has_all(name: str, tokens) -> bool:
    text = source_text(name)
    return all(norm(t).lower() in text for t in tokens)


def numbers_in(text: str) -> set[str]:
    return set(re.findall(r"\d[\d,]*", text))


@lab("3.1")
def lab_3_1():
    for start in ("research_brief.txt", "verification_log.csv", "research_report_sample.md"):
        assert (FILES / "start" / start).exists(), start
    report = (FILES / "start" / "research_report_sample.md").read_text(encoding="utf-8")
    listed = re.findall(r"^(\d)\. .+المصدر: (\S+?)\.$", report, flags=re.M)
    claims = json.loads(ref("D3_1_claims.json"))
    assert [(str(c["n"]), c["cited"]) for c in claims] == listed, listed  # the key follows the sample report
    sources = sorted({c["cited"] for c in claims})
    decisions = {}
    for c in claims:
        if has_all(c["cited"], c["tokens"]):
            finding, decision = "the cited source supports it", "يُعتمد"
        else:
            elsewhere = [s for s in sources if s != c["cited"] and has_all(s, c["tokens"])]
            if elsewhere:
                finding, decision = f"not in the cited source; found in {elsewhere[0]}", "يُعدَّل"
            elif c.get("weaker") and has_all(c["cited"], [c["weaker"]]):
                finding, decision = f"the source only says \"{c['weaker']}\"", "يُعدَّل"
            else:
                finding, decision = "no source supports it", "يُحذف"
        decisions[c["n"]] = decision
        print(f"  claim {c['n']} ({c['cited']}): {finding} -> {decision}")
    log = [l.split(",") for l in ref("D3_1_log.csv").strip().splitlines()[1:]]
    assert {int(r[0]): r[-1] for r in log} == decisions, decisions  # the reference log reaches the same decisions
    kept = Counter(decisions.values())
    print("  decisions:", dict(kept))
    assert kept == {"يُعتمد": 2, "يُعدَّل": 2, "يُحذف": 1}


NOTEBOOK_SOURCES = ("policy_flexible_work.pdf", "hr_faq.pdf", "procurement_guide.pdf")


@lab("3.2")
def lab_3_2():
    questions = json.loads(ref("D3_2_questions.json"))
    assert Counter(q["type"] for q in questions) == {"عادي": 5, "خارج المصادر": 1, "تجميع": 1, "تعارض": 1, "افتراض خاطئ": 1}
    for q in questions:
        for doc, tokens in q["evidence"].items():
            assert has_all(doc, tokens), (q["q"], doc, tokens)  # the evidence of every answer is in its source
        for doc, tokens in q.get("absent", {}).items():
            assert not has_all(doc, tokens), (q["q"], doc, tokens)
    print(f"  {len(questions)} questions: the evidence of each answer is in its source")
    all_numbers = set().union(*(numbers_in(source_text(s)) for s in NOTEBOOK_SOURCES))
    outside = STANDIN["3.2"]["outside"]
    invented = sorted(numbers_in(outside) - all_numbers)
    print(f"  stand-in on the allowance: figures in no source {invented}")
    assert invented == ["500"]
    conflict = norm(STANDIN["3.2"]["conflict"])
    both = norm("القرار") in conflict and norm("إبلاغ") in conflict
    print(f"  stand-in on the grievance deadline: names both dates {both}")
    assert not both  # it answers from one source and misses the planted conflict
    reference = norm(ref("D3_2_answers.txt"))
    assert norm("إبلاغ") in reference and norm("القرار") in reference and not (numbers_in(reference) - all_numbers)


def grade(answer: str, rule: dict) -> bool:
    text = norm(answer)
    ok = all(norm(m) in text for m in rule["must"]) and not any(norm(m) in text for m in rule.get("must_not", []))
    return ok and words(answer) <= rule.get("max_words", 80)


@lab("3.3")
def lab_3_3():
    head, rows = sheet_rows(FILES / "frequent_questions.xlsx")
    assert len(rows) == 10 and all(r[5] is None for r in rows)  # ten questions, the result columns empty
    rubric = json.loads(ref("D3_3_rubric.json"))
    for r in rows:
        rule = rubric[str(r[0])]
        assert has_all(rule["doc"], rule["evidence"]), (r[0], rule["evidence"])
    print("  the evidence of the ten expected answers is in the reference files")
    instructions = ref("D3_3_instructions.txt")
    for part in ("المنتج", "العملية", "الأداء", "لا ", "التصعيد"):
        assert part in instructions, part
    before = STANDIN["3.3"]["before"]
    assert len(before) == 10
    failed = [n for n in range(1, 11) if not grade(before[n - 1], rubric[str(n)])]
    print(f"  before the edit: {10 - len(failed)} of 10 pass; failed {failed}")
    assert failed == [6, 8, 10], failed
    after = STANDIN["3.3"]["after"]
    still = [n for n in failed if not grade(after[str(n)], rubric[str(n)])]
    print(f"  after one added rule: {10 - len(still)} of 10 pass; still failing {still}")
    assert still == [8, 10], still


@lab("3.4")
def lab_3_4():
    head, rows = sheet_rows(FILES / "monthly_report_workflow.xlsx", "خط الأساس")
    steps = [r for r in rows if r[0]]
    total_row = rows[-1]
    assert len(steps) == 10 and total_row[2] == "=SUM(C2:C11)" and all(r[3] is None for r in steps)
    baseline = {r[0]: r[2] for r in steps}
    redesign = {}
    who = {}
    for line in ref("D3_4_redesign.csv").strip().splitlines()[1:]:
        n, w, minutes = line.split(",")
        redesign[int(n)], who[int(n)] = int(minutes), w
    assert sorted(redesign) == sorted(baseline)
    b, a = sum(baseline.values()), sum(redesign.values())
    print(f"  baseline {b} min, redesign {a} min, saving {round(100 * (b - a) / b)}%")
    print(f"  classification alone: {baseline[3]} -> {redesign[3]} min ({round(100 * (baseline[3] - redesign[3]) / baseline[3])}%)")
    checking = (4, 6, 9)
    cb, ca = sum(baseline[n] for n in checking), sum(redesign[n] for n in checking)
    print(f"  checking steps 4, 6, 9: {cb} of {b} min ({round(100 * cb / b)}%) -> {ca} of {a} min ({round(100 * ca / a)}%)")
    assert (b, a) == (245, 105) and (cb, ca) == (30, 55)
    assert all(who[n] == "لي وحدي" for n in checking)  # the checks are not delegated to the assistant
    print("  who:", dict(Counter(who.values())))


def main(argv):
    wanted = argv or list(LABS_RUN)
    failed = 0
    for lab_id in wanted:
        print(f"Lab {lab_id}")
        try:
            LABS_RUN[lab_id]()
            print(f"  PASS {lab_id}")
        except Exception as e:  # report and continue with the next lab
            failed += 1
            print(f"  FAIL {lab_id}: {type(e).__name__}: {e}")
    print(f"{len(wanted) - failed} of {len(wanted)} labs pass")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
