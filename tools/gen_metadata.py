"""Write the Google Fonts files for every Wing Sans family into
ofl/<family>/ (METADATA.pb, OFL.txt, article/ARTICLE.en_us.html) — the same
layout as google/fonts, so a folder can be copied into an onboarding PR — plus the repo-level OFL.txt,
AUTHORS.txt and CONTRIBUTORS.txt. Layout follows the Bpmf families.

Run after build.py (it calls this):  python3 tools/gen_metadata.py
"""
import datetime
import re
import pathlib
import sys

from fontTools.ttLib import TTFont

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from families import FAMILIES, VERSION, gf_dir, ps_name  # noqa: E402

REPO = "https://github.com/Wing-Font/wing-sans-chinese"
AUTHOR = "Wai-Chun Law"
DESIGNER = "Wing Font, Adobe"
OURS = f"Copyright 2026 The Wing Sans Project Authors ({REPO})"
BASE_NAME = {"HK": "Noto Sans HK", "TC": "Noto Sans TC", "SC": "Noto Sans SC"}
CREDIT = {
    "typeduck": (f'<a href="https://github.com/TypeDuck-HK/schema">TypeDuck</a> (CC BY 4.0); '
                 f'see <a href="{REPO}#data-attribution">data attribution</a>'),
    "moe-revised": ('中華民國教育部（Ministry of Education, R.O.C.）'
                    '<a href="https://dict.revised.moe.edu.tw/">《重編國語辭典修訂本》</a> and '
                    '<a href="https://dict.concised.moe.edu.tw/">《國語辭典簡編本》</a> (CC BY-ND 3.0 TW); '
                    f'see <a href="{REPO}#data-attribution">data attribution</a>'),
    "mozillazg": ('<a href="https://github.com/mozillazg/pinyin-data">pinyin-data</a> and '
                  '<a href="https://github.com/mozillazg/phrase-pinyin-data">phrase-pinyin-data</a> (MIT, from Unicode Unihan); '
                  f'see <a href="{REPO}#data-attribution">data attribution</a>'),
    "moe-taigi": ('中華民國教育部（Ministry of Education, R.O.C.）'
                  '<a href="https://sutian.moe.edu.tw/">《臺灣台語常用詞辭典》</a> (CC BY-ND 3.0 TW); '
                  f'see <a href="{REPO}#data-attribution">data attribution</a>'),
}


def copyright_of(f):
    """One copyright per line (callers join with "; " for METADATA / OFL.txt:
    FontBakery wants it single-line). Same composition as the generator's nameID 0: ours, then base, then anno lines."""
    lines = [OURS]
    for src in (f["base"], f["anno"]):
        for line in TTFont(ROOT / src, lazy=True)["name"].getDebugName(0).split("\n"):
            line = line.strip().rstrip(".")  # as the generator: "A. B. C." on one line
            if line and line not in lines:
                lines.append(line)
    return "\n".join(f"{line}." for line in lines)


def q(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n") + '"'


def metadata(f, copyright, date_added):
    ps = ps_name(f)
    return "\n".join([
        f"name: {q(f['family'])}",
        f"designer: {q(DESIGNER)}",
        'license: "OFL"',
        'category: "SANS_SERIF"',
        f'date_added: "{date_added}"',
        "fonts {",
        f"  name: {q(f['family'])}",
        '  style: "normal"',
        "  weight: 400",
        f'  filename: "{ps}.ttf"',
        f'  post_script_name: "{ps}"',
        f"  full_name: {q(f['family'] + ' Regular')}",
        f"  copyright: {q(copyright)}",
        "}",
        f'subsets: "{f["subset"]}"',
        'subsets: "latin"',
        'subsets: "latin-ext"',
        'subsets: "menu"',
        *[f'languages: "{l}"' for l in f["languages"]],
        f'primary_script: "{f.get("script", "Hant")}"',
        # gftools packager takes these files from the release zip (build.yml);
        # it matches source_file by suffix, so paths must be unique in the zip.
        "source {",
        f'  repository_url: "{REPO}"',
        f'  archive_url: "{REPO}/releases/download/v{VERSION}/WingSans-v{VERSION}.zip"',
        *[f'  files {{\n    source_file: "{src}"\n    dest_file: "{dst}"\n  }}' for src, dst in (
            (f"fonts/ttf/{ps}.ttf", f"{ps}.ttf"),
            (f"ofl/{gf_dir(f)}/OFL.txt", "OFL.txt"),
            (f"ofl/{gf_dir(f)}/article/ARTICLE.en_us.html", "article/ARTICLE.en_us.html"),
            (f"ofl/{gf_dir(f)}/article/sample.png", "article/sample.png"),
        )],
        "}",
        "",
    ])


# Per family: the word pair shown in article/sample.png, and the sentence explaining it.
EXAMPLE = {
    "Wing Sans Yue Jyutping": "行 is hong4 in 銀行 (bank) but hang4 in 行人 (pedestrian)",
    "Wing Sans Yue Yale": "長 is cheung4 in 長短 (length) but jeung2 in 長大 (to grow up)",
    "Wing Sans Guoyu Pinyin": "重 is zhòng in 重要 (important) but chóng in 重複 (to repeat)",
    "Wing Sans Putonghua Pinyin": "觉 is jiào in 睡觉 (to sleep) but jué in 觉得 (to feel)",
    "Wing Sans Taigi Tailo": "上 is tsiūnn in 上山 (to go up a mountain) but siōng in 上課 (to attend class)",
}


def article(f):
    base = next(v for k, v in BASE_NAME.items() if f"NotoSans{k}" in f["base"])
    anno = "Noto Sans" if f["anno"] != f["base"] else base
    return f"""<p>
  {f['family']} prints the reading of every Chinese character — {f['reading']} — right above it,
  so learners can read text aloud without looking anything up. The reading is part of the glyph,
  so no extra typesetting or annotation tools are needed: it works in applications with OpenType
  support, such as Microsoft Word, Canva, Affinity and modern web browsers.
</p>
<img src="sample.png" alt="{f['family']}: the same character read differently in two words">
<p>
  Many characters have more than one reading. The font picks the right one from the surrounding word
  through OpenType contextual alternates: {EXAMPLE[f['family']]}. When the automatic choice is wrong,
  typing a digit after the character selects another reading.
</p>
<p>
  Wing Sans is made for students, teachers and self-learners who can read Chinese but are unsure how to
  say it, and for anyone preparing handouts, slides or signage that should be read aloud.
</p>
<p>
  Built with <a href="https://wing-font.chunlaw.io">Wing Font</a> from
  <a href="https://fonts.google.com/noto/specimen/{base.replace(' ', '+')}">{base}</a> (characters)
  and <a href="https://fonts.google.com/noto/specimen/{anno.replace(' ', '+')}">{anno}</a> (annotations).
  Reading data: {CREDIT[f['data']]}.
</p>
<p>
  To contribute, see <a href="{REPO}">{REPO[len("https://"):]}</a>.
</p>
"""


def main():
    ofl_body = (ROOT / "tools" / "OFL-1.1-body.txt").read_text(encoding="utf-8")
    all_lines = [OURS + "."]
    for f in FAMILIES:
        c = copyright_of(f)
        all_lines += [l for l in c.split("\n")[1:] if l not in all_lines]
        out = ROOT / "ofl" / gf_dir(f)
        (out / "article").mkdir(parents=True, exist_ok=True)
        old = out / "METADATA.pb"
        # Keep the first date_added; GF treats it as the onboarding date.
        m = re.search(r'date_added: "([^"]+)"', old.read_text(encoding="utf-8")) if old.exists() else None
        old.write_text(metadata(f, c.replace("\n", " "), m.group(1) if m else datetime.date.today().isoformat()), encoding="utf-8")
        (out / "OFL.txt").write_text(c.replace("\n", " ") + "\n\n" + ofl_body, encoding="utf-8")
        (out / "article" / "ARTICLE.en_us.html").write_text(article(f), encoding="utf-8")
        print("wrote", out.relative_to(ROOT))
    (ROOT / "OFL.txt").write_text(" ".join(all_lines) + "\n\n" + ofl_body, encoding="utf-8")
    (ROOT / "AUTHORS.txt").write_text(
        "# This is the official list of project authors for copyright purposes.\n"
        "# The first name appears as \"Principal design\" on Google Fonts.\n"
        "# Name or Organization <email address>\n\n"
        f"{AUTHOR}\nAdobe (Noto Sans HK, Noto Sans TC, Noto Sans SC)\nGoogle (Noto Sans)\n", encoding="utf-8")
    (ROOT / "CONTRIBUTORS.txt").write_text(
        "# People who contributed to The Wing Sans Project, including those not\n"
        "# listed in AUTHORS.txt.\n\n"
        f"{AUTHOR}\n", encoding="utf-8")


if __name__ == "__main__":
    main()
