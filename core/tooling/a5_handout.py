#!/usr/bin/env python3
"""Adds and validates the standard footer for student-friendly A5 handouts."""

from __future__ import annotations

import argparse
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

import fitz


FOOTER_TEXT = "ki generiert - Fehler bitte ggf. melden!"
A5_WIDTH = 419.53
A5_HEIGHT = 595.28
MIN_TEXT_PAGE_RATIO = 0.9
WORD_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
DOC_REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
CONTENT_NS = "http://schemas.openxmlformats.org/package/2006/content-types"
FOOTER_REL_TYPE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer"

ET.register_namespace("w", WORD_NS)
ET.register_namespace("r", DOC_REL_NS)


def add_pdf_footer(source: Path, target: Path) -> int:
    document = fitz.open(str(source))
    for page in document:
        page.insert_textbox(
            fitz.Rect(0, page.rect.height - 22, page.rect.width, page.rect.height - 4),
            FOOTER_TEXT,
            fontsize=7,
            fontname="helv",
            color=(0.4, 0.4, 0.4),
            align=fitz.TEXT_ALIGN_CENTER,
        )
    target.parent.mkdir(parents=True, exist_ok=True)
    document.save(str(target), garbage=4, deflate=True)
    page_count = len(document)
    document.close()
    return page_count


def _word_text(value: str) -> ET.Element:
    paragraph = ET.Element(f"{{{WORD_NS}}}p")
    run = ET.SubElement(paragraph, f"{{{WORD_NS}}}r")
    properties = ET.SubElement(run, f"{{{WORD_NS}}}rPr")
    size = ET.SubElement(properties, f"{{{WORD_NS}}}sz")
    size.set(f"{{{WORD_NS}}}val", "14")
    text = ET.SubElement(run, f"{{{WORD_NS}}}t")
    text.text = value
    return paragraph


def add_docx_footer(source: Path, target: Path) -> None:
    with zipfile.ZipFile(source) as archive:
        files = {name: archive.read(name) for name in archive.namelist()}

    document = ET.fromstring(files["word/document.xml"])
    relationships = ET.fromstring(files["word/_rels/document.xml.rels"])
    content_types = ET.fromstring(files["[Content_Types].xml"])

    existing = None
    for relationship in relationships:
        if relationship.get("Type") == FOOTER_REL_TYPE:
            existing = relationship
            break

    if existing is None:
        footer_number = 1
        while f"word/footer{footer_number}.xml" in files:
            footer_number += 1
        target_name = f"word/footer{footer_number}.xml"
        relation_ids = {item.get("Id") for item in relationships}
        relation_number = 1
        while f"rId{relation_number}" in relation_ids:
            relation_number += 1
        relationship = ET.SubElement(relationships, f"{{{REL_NS}}}Relationship")
        relationship.set("Id", f"rId{relation_number}")
        relationship.set("Type", FOOTER_REL_TYPE)
        relationship.set("Target", f"footer{footer_number}.xml")
        footer_reference_id = f"rId{relation_number}"
        override = ET.SubElement(content_types, f"{{{CONTENT_NS}}}Override")
        override.set("PartName", f"/{target_name}")
        override.set("ContentType", "application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml")
    else:
        target_name = "word/" + existing.get("Target", "footer1.xml").lstrip("/")
        footer_reference_id = existing.get("Id")

    footer = ET.Element(f"{{{WORD_NS}}}ftr")
    footer.append(_word_text(FOOTER_TEXT))
    files[target_name] = ET.tostring(footer, encoding="utf-8", xml_declaration=True)

    sect_pr = document.find(f".//{{{WORD_NS}}}sectPr")
    if sect_pr is None:
        raise ValueError("DOCX enthaelt keinen Abschnitt (sectPr).")
    for reference in list(sect_pr.findall(f"{{{WORD_NS}}}footerReference")):
        if reference.get(f"{{{DOC_REL_NS}}}id") == footer_reference_id:
            sect_pr.remove(reference)
    reference = ET.Element(f"{{{WORD_NS}}}footerReference")
    reference.set(f"{{{DOC_REL_NS}}}type", "default")
    reference.set(f"{{{DOC_REL_NS}}}id", footer_reference_id)
    sect_pr.append(reference)
    files["word/document.xml"] = ET.tostring(document, encoding="utf-8", xml_declaration=True)
    files["word/_rels/document.xml.rels"] = ET.tostring(relationships, encoding="utf-8", xml_declaration=True)
    files["[Content_Types].xml"] = ET.tostring(content_types, encoding="utf-8", xml_declaration=True)

    target.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, data in files.items():
            archive.writestr(name, data)


def _validate_pdf(path: Path) -> None:
    document = fitz.open(str(path))
    for page in document:
        width = page.rect.width
        height = page.rect.height
        if abs(width - A5_WIDTH) > 2 or abs(height - A5_HEIGHT) > 2:
            raise ValueError(f"Keine A5-Seite: {path.name} ({width:.1f} x {height:.1f} pt)")
        if FOOTER_TEXT not in page.get_text():
            raise ValueError(f"Fusszeile fehlt auf einer Seite von {path.name}")
    document.close()


def _quality_check_pdf(path: Path) -> None:
    document = fitz.open(str(path))
    page_count = len(document)
    text_pages = 0
    footer_pages = 0
    link_count = 0
    all_text = []

    for page in document:
        text = page.get_text()
        all_text.append(text)
        text_pages += bool(text.strip())
        footer_pages += FOOTER_TEXT in text
        link_count += len(page.get_links())
        width, height = page.rect.width, page.rect.height
        if abs(width - A5_WIDTH) > 2 or abs(height - A5_HEIGHT) > 2:
            raise ValueError(f"Keine A5-Seite: {path.name} ({width:.1f} x {height:.1f} pt)")

    toc = document.get_toc()
    text = "\n".join(all_text)
    checklist_markers = ("☐", "[ ]", "checkliste", "check-list")
    table_markers = ("Tabelle", "Begriff Bedeutung Wozu gibt es das?", "|")
    checklist_found = any(marker.lower() in text.lower() for marker in checklist_markers)
    table_found = any(marker.lower() in text.lower() for marker in table_markers)
    print(f"A5-Qualitaetsbericht: {path}")
    print(f"  Seiten: {page_count}; Textseiten: {text_pages}/{page_count}; Fusszeilen: {footer_pages}/{page_count}")
    print(f"  Inhaltsverzeichnis/Lesezeichen: {len(toc)} Eintraege; PDF-Links: {link_count}")
    print(f"  Checklistenmarker: {'vorhanden' if checklist_found else 'nicht erkannt'}; Tabellenmarker: {'vorhanden' if table_found else 'nicht erkannt'}")

    if text_pages / max(page_count, 1) < MIN_TEXT_PAGE_RATIO:
        raise ValueError(f"Zu wenig maschinenlesbarer Text in {path.name}")
    if footer_pages != page_count:
        raise ValueError(f"Fusszeile fehlt auf mindestens einer Seite von {path.name}")
    if not toc:
        print("  WARNUNG: Kein klickbares Inhaltsverzeichnis/Lesezeichen erkannt.")
    if not link_count:
        print("  WARNUNG: Keine klickbaren PDF-Links erkannt.")
    if not checklist_found:
        print("  HINWEIS: Keine Checkliste automatisch erkannt; fachlich pruefen.")
    if not table_found:
        print("  HINWEIS: Keine Tabelle automatisch erkannt; fachlich pruefen.")
    document.close()


def _copy_with_footer(source: Path, target: Path) -> None:
    if source.suffix.lower() == ".pdf":
        add_pdf_footer(source, target)
    elif source.suffix.lower() == ".docx":
        add_docx_footer(source, target)
    else:
        raise ValueError("Unterstuetzt werden nur .pdf und .docx.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Erzeugt gepruefte A5-Handouts mit KI-Fusszeile.")
    parser.add_argument("source", type=Path, help="Quell-DOCX oder Quell-PDF")
    parser.add_argument("output", type=Path, nargs="?", help="Ziel-DOCX oder Ziel-PDF")
    parser.add_argument("--validate-only", action="store_true", help="Nur eine PDF mit Fusszeile und A5-Format pruefen")
    parser.add_argument("--quality-check", action="store_true", help="A5-Lesbarkeit, Navigation, Links, Checklisten und Tabellen berichten")
    args = parser.parse_args()

    if args.validate_only:
        _validate_pdf(args.source)
        if args.quality_check:
            _quality_check_pdf(args.source)
        print(f"OK: {args.source}")
        return

    if args.output is None:
        parser.error("output ist erforderlich, außer bei --validate-only")
    if args.source.suffix.lower() != args.output.suffix.lower():
        raise SystemExit("Quell- und Zieldatei muessen denselben Typ haben.")
    _copy_with_footer(args.source, args.output)
    if args.output.suffix.lower() == ".pdf":
        _validate_pdf(args.output)
        if args.quality_check:
            _quality_check_pdf(args.output)
    print(f"Erzeugt: {args.output}")


if __name__ == "__main__":
    main()