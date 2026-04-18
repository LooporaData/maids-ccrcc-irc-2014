![](banner.png?raw=true)

# Medical AI Datasheet (MAIDS) — cBioPortal `ccrcc_irc_2014`

This repository is based on the official MAIDS template from **[PERSIMUNE/MAIDS-Template](https://github.com/PERSIMUNE/MAIDS-Template)** (*v0.2-alpha*) and documents the public cBioPortal study:

**[Kidney Renal Clear Cell Carcinoma (IRC, Nat Genet 2014)](https://www.cbioportal.org/study/summary?id=ccrcc_irc_2014)** (`ccrcc_irc_2014`)

Upstream publication: Gerlinger et al., *Nature Genetics* 2014, PMID [24487277](https://pubmed.ncbi.nlm.nih.gov/24487277/).

## Contents

| Path | Purpose |
|------|---------|
| `xml/target/` | Filled MAIDS XML (questionnaire, about, features, keywords, provenance) for this study |
| `docs/index.html` | Generated single-page MAIDS site (run build below) |
| `code/fill_ccrcc_questionnaire.py` | Helper used to populate questionnaire answers (optional for updates) |

## Build the HTML site

From the repository root (Python 3 + `beautifulsoup4`):

```bash
pip install beautifulsoup4
python3 code/build_site/xml2html.py -u target
```

Optional: copy `docs/images/figures/thematic.png` to `supplementary/figures/thematic.png` to silence missing-figure warnings during build.

## Git remote (Loopora SSH alias)

Clone with your GitHub SSH host alias:

```bash
git clone git@looporadata.ai:LooporaData/maids-ccrcc-irc-2014.git
```

Web: `https://github.com/LooporaData/maids-ccrcc-irc-2014`

## Specification submodule

The `specification/` directory tracks **[MAIDS-Specification](https://github.com/PERSIMUNE-Health-Informatics/MAIDS-Specification)** as a git submodule (see `.gitmodules`).

---

*Original template README text:* MAIDS is being prototyped in the context of the [Copenhagen Ultrathon on Precision Medicine](https://ultrathon.online). Please watch/star **[PERSIMUNE/MAIDS-Template](https://github.com/PERSIMUNE/MAIDS-Template)** for upstream updates.
