#!/usr/bin/env bash
# Local pre-push check: build the fonts with a local wing-font-generator
# checkout (not the PyPI pin), then run FontBakery on them.
#   tools/check.sh                 # all families
#   tools/check.sh jyutping        # build.py family filter
# Generator path: $WING_FONT_GENERATOR (default ../wing-font-generator).
# Note: leaves the editable generator installed; `pip install -r requirements.txt`
# goes back to the PyPI pin.
set -euo pipefail
cd "$(dirname "$0")/.."
GEN=${WING_FONT_GENERATOR:-../wing-font-generator}
python3 -m pip install -q -e "$GEN/python" "fontbakery[googlefonts]==1.1.0"
python3 build.py "$@"
bash tools/fontbakery.sh
