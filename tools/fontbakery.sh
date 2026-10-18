#!/usr/bin/env bash
# FontBakery (Google Fonts profile) on fonts/ttf. Each font is checked next to
# its ofl/<family>/METADATA.pb, the layout google/fonts uses, so the METADATA /
# copyright / OFL checks run too. Report only: writes fontbakery/<family>.{md,html,log},
# prints each family's FAILs, never exits non-zero. Shared by CI and tools/check.sh.
set -u
cd "$(dirname "$0")/.."
mkdir -p fontbakery
# Outline checks walk every glyph in pure Python (hours on CJK) and are aimed
# at Latin drawing; ttx_roundtrip is ~5 min per font and redundant (the
# generator already writes via fontTools).
SKIP=(-x outline_ -x overlapping_path_segments -x contour_count -x caps_vertically_centered -x ttx_roundtrip)
# macOS has no `timeout` unless coreutils is installed (gtimeout).
T=$(command -v timeout || command -v gtimeout || true)
for dir in ofl/*/; do
  fam=$(basename "$dir")
  ttf=$(sed -n 's/.*filename: "\(.*\)".*/\1/p' "$dir/METADATA.pb")
  cp "fonts/ttf/$ttf" "$dir"
  echo "### $fam"
  ${T:+$T 30m} fontbakery check-googlefonts "${SKIP[@]}" \
    --ghmarkdown "fontbakery/$fam.md" --html "fontbakery/$fam.html" \
    "$dir/METADATA.pb" "$dir/$ttf" > "fontbakery/$fam.log" 2>&1
  grep -o '🔥 <b>FAIL</b> [^<]*' "fontbakery/$fam.md" 2>/dev/null | sed 's/^🔥 <b>FAIL<\/b> /- FAIL: /' \
    || echo "- no FAIL (or no report: see fontbakery/$fam.log)"
done
