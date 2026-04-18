#!/usr/bin/env python3
"""
Merge xml/target/feature_description.cbioportal.xml into the legacy MAIDS Template
shape expected by code/build_site/xml2html.py (root name=FEATURE + Subset_Feature_Dataset).

Usage (from repo root):
  python3 code/transform_cbioportal_feature_xml.py
  python3 code/transform_cbioportal_feature_xml.py -i xml/target/feature_description.cbioportal.xml \\
      -o xml/target/feature_description.xml
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import date
from pathlib import Path
from xml.etree import ElementTree as ET


def local_tag(tag: str) -> str:
    if tag.startswith("{"):
        return tag.split("}", 1)[1]
    return tag


def parse_cbioportal(path: Path) -> tuple[str, dict[str, str], list[dict], list[dict]]:
    root = ET.parse(path).getroot()
    dataset_id = ""
    cohort: dict[str, str] = {}
    subset_defs: list[dict] = []
    features: list[dict] = []

    for ch in root:
        t = local_tag(ch.tag)
        if t == "dataset_id":
            dataset_id = (ch.text or "").strip()
        elif t == "cohort_metrics":
            for m in ch:
                cohort[local_tag(m.tag)] = (m.text or "").strip()
        elif t == "subsets":
            for s in ch:
                if local_tag(s.tag) != "subset":
                    continue
                subset_defs.append(
                    {
                        "id": s.get("id", ""),
                        "name": s.get("name", ""),
                        "description": s.get("description", ""),
                    }
                )
        elif t == "feature":
            fd: dict[str, str] = {"xml_id": ch.get("id", "")}
            for el in ch:
                fd[local_tag(el.tag)] = (el.text or "").strip()
            features.append(fd)

    return dataset_id, cohort, subset_defs, features


def subset_row_size(subset_id: str, cohort: dict[str, str]) -> str:
    if subset_id == "cohort_overview":
        return cohort.get("total_samples") or cohort.get("total_patients") or ""
    if subset_id == "clinical":
        return cohort.get("total_patients") or ""
    if subset_id == "sample_annotation":
        return cohort.get("total_samples") or ""
    if subset_id == "genomic":
        return cohort.get("profiled_samples") or ""
    return ""


def build_values_field(fd: dict[str, str]) -> str:
    parts: list[str] = []
    if fd.get("type"):
        parts.append(f"type={fd['type']}")
    if fd.get("value"):
        parts.append(fd["value"])
    if fd.get("values"):
        parts.append(fd["values"])
    if fd.get("statistics"):
        parts.append(fd["statistics"])
    if fd.get("missing_rate"):
        parts.append(f"missing_rate={fd['missing_rate']}")
    return "; ".join(parts)


def add_text(parent: ET.Element, tag: str, text: str) -> None:
    el = ET.SubElement(parent, tag)
    el.text = text


def build_legacy_tree(
    skeleton_path: Path,
    dataset_id: str,
    cohort: dict[str, str],
    subset_defs: list[dict],
    features_by_subset: dict[str, list[dict]],
    study_url: str,
    last_update: str,
) -> ET.ElementTree:
    tree = ET.parse(skeleton_path)
    root = tree.getroot()
    for i, child in enumerate(list(root)):
        if local_tag(child.tag) == "Subset_Feature_Dataset":
            root.remove(child)
            break

    dataset_el = ET.SubElement(root, "Subset_Feature_Dataset")

    for si, sdef in enumerate(subset_defs, start=1):
        sid = sdef["id"]
        subset_el = ET.SubElement(dataset_el, f"Subset_{si}")
        add_text(subset_el, "ID", str(si))
        add_text(subset_el, "Name", sdef["name"])
        add_text(subset_el, "LastUpdate", last_update)
        add_text(subset_el, "Modality", "TABULAR")
        add_text(subset_el, "Format", "cBioPortal (feature_description.cbioportal.xml)")
        add_text(subset_el, "Size", subset_row_size(sid, cohort) or "—")
        add_text(subset_el, "ParentID", "0")
        add_text(subset_el, "Purpose", sdef["description"])
        add_text(subset_el, "Link", study_url)
        add_text(subset_el, "Covmat", "Not computed in this MAIDS repository.")
        add_text(subset_el, "Modsys", "Not bundled in this MAIDS repository.")

        features_el = ET.SubElement(subset_el, "Features")
        bucket = features_by_subset.get(sid, [])
        for fi, fd in enumerate(bucket, start=1):
            fe = ET.SubElement(features_el, f"Feature_{fi}")
            add_text(fe, "ID", str(fi))
            add_text(fe, "Introduction", last_update)
            add_text(fe, "Name", fd.get("name", fd.get("xml_id", "")))
            add_text(fe, "Values", build_values_field(fd))
            add_text(fe, "Unit", "")
            add_text(fe, "Definition", fd.get("description", ""))
            add_text(fe, "Purpose", fd.get("role", ""))
            add_text(fe, "Encoding", fd.get("type", ""))
            add_text(fe, "Meaning_NA_NULL_NONE_OTHER", fd.get("missing_rate", ""))
            add_text(fe, "Meaning_Zero", "N/A")
            add_text(fe, "Meaning_BlankVoid", "")
            add_text(fe, "Sparsity", "")
            add_text(fe, "Mean", "")
            add_text(fe, "Std", "")
            add_text(fe, "Modality", "")
            add_text(fe, "Median", "")
            add_text(fe, "IQR", "")
            add_text(fe, "ParentIDs", "")

    ET.indent(tree.getroot(), space="    ")
    return tree


def main() -> None:
    ap = argparse.ArgumentParser(description="Transform cBioPortal MAIDS XML to legacy feature_description.xml")
    repo = Path(__file__).resolve().parents[1]
    ap.add_argument(
        "-i",
        "--input",
        type=Path,
        default=repo / "xml" / "target" / "feature_description.cbioportal.xml",
    )
    ap.add_argument(
        "-o",
        "--output",
        type=Path,
        default=repo / "xml" / "target" / "feature_description.xml",
    )
    ap.add_argument(
        "--skeleton",
        type=Path,
        default=repo / "xml" / "empty" / "feature_description.xml",
    )
    ap.add_argument("--study-url", type=str, default="", help="Override cBioPortal study URL")
    args = ap.parse_args()

    dataset_id, cohort, subset_defs, features = parse_cbioportal(args.input)
    study_url = args.study_url.strip() or (
        f"https://www.cbioportal.org/study/summary?id={dataset_id}" if dataset_id else ""
    )

    by_subset: dict[str, list[dict]] = defaultdict(list)
    orphan: list[dict] = []
    for fd in features:
        sid = fd.get("subset", "")
        if sid and any(s["id"] == sid for s in subset_defs):
            by_subset[sid].append(fd)
        else:
            orphan.append(fd)
    if orphan:
        bucket = by_subset[subset_defs[0]["id"]] if subset_defs else []
        for fd in orphan:
            bucket.append(fd)

    last_update = date.today().isoformat().replace("-", "/")
    tree = build_legacy_tree(
        args.skeleton,
        dataset_id,
        cohort,
        subset_defs,
        by_subset,
        study_url,
        last_update,
    )

    out_lines = [
        "<!-- AUTO-GENERATED by code/transform_cbioportal_feature_xml.py — edit feature_description.cbioportal.xml and re-run. -->",
        ET.tostring(tree.getroot(), encoding="unicode"),
        "",
    ]
    args.output.write_text("\n".join(out_lines), encoding="utf-8")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
