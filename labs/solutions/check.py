# /// script
# requires-python = ">=3.11"
# dependencies = ["openpyxl>=3.1", "python-docx>=1.1", "pypdf>=5.0"]
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
