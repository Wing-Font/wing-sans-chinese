"""The Wing Sans families — single source for build.py, config.yaml and
gen_metadata.py. Generator flags follow wing-font-generator's
deploy-pages.yml NotoCond builds."""

# Font version; release tags must be "v" + VERSION (checked in CI).
VERSION = "1.001"

HK = "srcfonts/NotoSansHK[wght].ttf"
TC = "srcfonts/NotoSansTC[wght].ttf"
SC = "srcfonts/NotoSansSC[wght].ttf"
LATIN = "srcfonts/NotoSans[wdth,wght].ttf"
LATIN_ARGS = ["--anno-axis", "wdth=75", "-as", "0.39", "-bs", "0.70", "-y", "0.70"]

# family, base, anno, mapping, diy, extra generator args,
# GF language ids, GF subset, reading (for the article)
FAMILIES = [
    dict(family="Wing Sans Yue Jyutping", base=HK, anno=LATIN,
         mapping="mappings/cantonese/canto-lshk.csv", diy="mappings/cantonese/lshk.diy-annotation.csv",
         args=LATIN_ARGS, languages=["yue_Hant"], subset="chinese-hongkong",
         reading="Cantonese in Jyutping", data="typeduck"),
    dict(family="Wing Sans Yue Yale", base=HK, anno=LATIN,
         mapping="mappings/cantonese/canto-yale.csv", diy=None,
         args=LATIN_ARGS, languages=["yue_Hant"], subset="chinese-hongkong",
         reading="Cantonese in Yale romanization", data="typeduck"),
    dict(family="Wing Sans Guoyu Pinyin", base=TC, anno=LATIN,
         mapping="mappings/mandarin/mandarin-tw-toned.csv", diy="mappings/mandarin/pinyin.diy-annotation.csv",
         args=LATIN_ARGS, languages=["zh_Hant"], subset="chinese-traditional",
         reading="Taiwan Mandarin (Guoyu) in Hanyu Pinyin", data="moe-revised"),
    dict(family="Wing Sans Putonghua Pinyin", base=SC, anno=LATIN,
         mapping="mappings/mandarin/mandarin-cn-toned-trimmed.csv", diy="mappings/mandarin/pinyin.diy-annotation.csv",
         args=LATIN_ARGS, languages=["zh_Hans"], subset="chinese-simplified", script="Hans",
         reading="Standard Mandarin (Putonghua) in Hanyu Pinyin", data="mozillazg"),
    dict(family="Wing Sans Taigi Tailo", base=TC, anno=LATIN,
         mapping="mappings/taiwanese/taigi-tl-toned.csv", diy="mappings/taiwanese/sutian.diy-annotation.csv",
         args=LATIN_ARGS, languages=["nan_Hant"], subset="chinese-traditional",
         reading="Taiwanese Hokkien in Tâi-lô", data="moe-taigi"),
]


def gf_dir(f):
    """Folder name google/fonts uses under ofl/ (e.g. wingsansyuejyutping)."""
    return f["family"].replace(" ", "").lower()


def ps_name(f):
    return f["family"].replace(" ", "") + "-Regular"
