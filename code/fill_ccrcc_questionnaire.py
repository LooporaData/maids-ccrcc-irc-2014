#!/usr/bin/env python3
"""One-off: fill xml/target/questionnaire.xml answers for ccrcc_irc_2014 MAIDS."""
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "xml" / "target" / "questionnaire.xml"

DATA = {
    1: [
        "Enable reproducible research, teaching, and secondary analysis on a landmark clear cell renal cell carcinoma (ccRCC) intratumor heterogeneity cohort distributed through cBioPortal (study ccrcc_irc_2014).",
        "The underlying study was produced by Gerlinger et al. (Nature Genetics 2014) and contributing institutions; cBioPortal hosts the public distribution.",
        "Funding and grants are described in the original paper (PMID 24487277); not duplicated exhaustively in this MAIDS file.",
        "This MAIDS document is maintained by Loopora Data as a transparency layer for analytics and ML use cases; it does not replace the publication or cBioPortal as primary sources.",
    ],
    2: [
        "Patient-level records, tumor samples, and genomic alteration calls as represented in cBioPortal for study ccrcc_irc_2014 (multi-region exome context).",
        "cBioPortal API reported 78 sequenced samples at documentation time; verify current counts on the study page.",
        "The cohort is the complete public study release for this study ID, not a random draw from all RCC patients worldwide.",
        "Clinical attributes plus somatic mutation and related genomic views as exposed in cBioPortal tables and visualizations.",
        "Outcome and phenotype fields depend on loaded clinical attributes; users must confirm available endpoints in the portal.",
        "Missingness follows primary data and cBioPortal loading; not all attributes are complete for every sample.",
        "Relationships between multi-region samples and patients are modeled via cBioPortal patient and sample identifiers.",
        "No recommended ML splits are provided; users must define training and evaluation with appropriate patient- or tumor-level grouping to avoid leakage.",
        "Sequencing, alignment, and variant calling introduce technical noise; harmonization across portal releases may differ slightly over time.",
        "Data are hosted on cBioPortal and described in the peer-reviewed literature; reliance on stable URLs and portal versioning applies.",
        "The data are de-identified research artifacts under controlled public sharing policies—not for casual browsing of identifiable records.",
        "Not applicable in the sense of offensive language; clinical cancer content may still be sensitive for some audiences.",
        "No—the cohort concerns people with cancer.",
        "ccRCC and clinical subgroups as encoded in cBioPortal; small n limits generalization.",
        "Direct identifiers are not published; indirect re-identification cannot be ruled out when combined with external data.",
        "Yes—genomic and clinical oncology data are sensitive categories of health information.",
        "See https://www.cbioportal.org/study/summary?id=ccrcc_irc_2014 for authoritative metadata and downloads.",
    ],
    3: [
        "Tumor tissue sampling, DNA extraction, exome sequencing, and bioinformatics per Gerlinger et al. (2014); details in the primary paper.",
        "Laboratory sequencing platforms and computational pipelines as described in the publication; cBioPortal presents derived mutation and clinical tables.",
        "Non-random purposive sampling of ten tumors with multiple regions; not a population-based series.",
        "Trained clinicians and laboratory staff per original study; compensation not documented in this MAIDS.",
        "Primary data collection timeframe per publication (~2010s era cohort); see paper for specifics.",
        "Ethical approvals are described in the original publication; this MAIDS does not store IRB documents.",
        "No—data relate to human patients.",
        "Data were collected in a clinical research context and disseminated via publication and repository mechanisms—not collected by Loopora.",
        "Participants were enrolled under study-specific consent as described in the primary paper.",
        "Consent and data sharing terms follow the original study and cBioPortal policies.",
        "Revocation and downstream use are governed by those policies; not restated here.",
        "Not attached to this repository; consult custodians for DPIA-style analyses if required.",
        "Refer to PMID 24487277 and cBioPortal documentation for collection ethics and governance.",
    ],
    4: [
        "cBioPortal applies harmonization, annotation, and quality filtering for display and export; exact steps are documented on cBioPortal.",
        "Raw sequence data are not redistributed inside this MAIDS repo; access may require dbGaP or similar when applicable.",
        "Portal pipelines and code are open source in the cBioPortal ecosystem; see their repositories for reproducibility.",
        "Loopora does not claim to reproduce MSK or cBioPortal preprocessing in this documentation-only repository.",
    ],
    5: [
        "Yes—in cancer genomics and heterogeneity research (primary publication and numerous citations).",
        "PubMed and cBioPortal link related work; no exhaustive bibliography is maintained in this MAIDS file.",
        "Exploratory analysis, method comparison, teaching, and responsible ML benchmarking with careful cohort statistics.",
        "Small sample count, single-disease focus, and evolution of genomic annotations may limit external validity.",
        "Not for clinical decision support, diagnostic use, or deployment without independent validation and regulatory clearance.",
        "Users must comply with cBioPortal terms and applicable privacy law when exporting or modeling data.",
    ],
    6: [
        "Yes—cBioPortal distributes study data broadly to registered and public users per portal policy.",
        "Primarily via cBioPortal web interface and APIs; publication supplements may provide additional files.",
        "Available continuously subject to cBioPortal uptime and policy; this MAIDS does not gate access.",
        "Use is subject to cBioPortal terms of use and any study-specific restrictions noted on the portal.",
        "Third-party restrictions follow publication, institutional, and repository policies.",
        "Export and reuse may be subject to institutional and national regulations for genomic data.",
        "Loopora mirrors documentation only; licensing of underlying data remains with custodians.",
    ],
    7: [
        "cBioPortal consortium and study custodians maintain the live dataset; Loopora maintains this MAIDS text in its GitHub repository.",
        "Contact cBioPortal help and study authors for scientific questions; Loopora via GitHub issues for MAIDS document fixes.",
        "Errata would appear via cBioPortal release notes or corrigenda; not tracked in this repo beyond best-effort updates.",
        "cBioPortal may refresh annotations; archival snapshots are the responsibility of users who need point-in-time reproducibility.",
        "Retention follows cBioPortal and originating institutions; not specified in this MAIDS.",
        "Older portal releases may not be indefinitely hosted; users should archive exports for long-term studies.",
        "Contributions to the underlying study data go through custodians; contributions to this MAIDS via pull request are welcome.",
        "Prefer citing Gerlinger et al. (2014), cBioPortal study ID ccrcc_irc_2014, and this repository for the MAIDS layer.",
    ],
}


def main() -> None:
    tree = ET.parse(path)
    el = tree.getroot()
    q = el.find("questionnaire")
    if q is None:
        raise SystemExit("questionnaire element not found")
    for cat_idx, texts in DATA.items():
        cat = q.find(f"category_{cat_idx}")
        if cat is None:
            raise SystemExit(f"missing category_{cat_idx}")
        answers = cat.find("answers")
        if answers is None:
            raise SystemExit(f"missing answers in category_{cat_idx}")
        for i, text in enumerate(texts):
            a = answers.find(f"A{i}")
            if a is None:
                raise SystemExit(f"missing A{i} in category_{cat_idx}")
            a.text = text
    ET.indent(tree, space="    ")
    tree.write(path, encoding="unicode", xml_declaration=False)


if __name__ == "__main__":
    main()
