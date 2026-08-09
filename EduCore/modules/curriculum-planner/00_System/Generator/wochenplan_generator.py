#!/usr/bin/env python3
"""Erzeugt Wochenplaene als XLS und PDF auf Basis einer JSON-Konfiguration.

Architektur (leichtgewichtig):
- Model: Datenobjekte und Kalenderlogik
- Controller: Orchestrierung pro Klasse
- View: Export nach XLS/PDF
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple
from xml.sax.saxutils import escape

import xlrd
import xlwt
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


DEFAULT_LAYOUT_TEMPLATE = {
    "name": "v003",
    "header_bg_hex": "#D9E2F3",
    "vacation_row": {
        "enabled": True,
        "keywords": ["FERIEN", "FASNET", "FEIERTAG", "SCHULFREI", "BRUECKENTAG"],
        "pdf_bg_hex": "#FDE9D9",
        "xls_palette_index": 33,
        "xls_palette_rgb": [253, 233, 217],
    },
    "xls": {
        "import_col_widths": [2300, 4200, 4200, 17000, 5200, 5200],
    },
    "pdf": {
        "single_import_meta_col_widths": [210, 600],
        "single_import_table_col_widths": [34, 70, 70, 370, 135, 130],
    },
}


def load_layout_template(template_path: Optional[Path]) -> dict:
    if template_path is None or not template_path.exists():
        return json.loads(json.dumps(DEFAULT_LAYOUT_TEMPLATE))

    with template_path.open("r", encoding="utf-8") as f:
        loaded = json.load(f)

    merged = json.loads(json.dumps(DEFAULT_LAYOUT_TEMPLATE))
    _deep_update(merged, loaded)
    return merged


def _deep_update(target: dict, source: dict) -> None:
    for key, value in source.items():
        if isinstance(value, dict) and isinstance(target.get(key), dict):
            _deep_update(target[key], value)
        else:
            target[key] = value


def is_vacation_row(row: WeekRow, layout_template: dict) -> bool:
    vacation_cfg = layout_template.get("vacation_row", {})
    if not vacation_cfg.get("enabled", True):
        return False

    keywords = [str(k).upper() for k in vacation_cfg.get("keywords", [])]
    haystack = f"{row.topic} {row.system} {row.notes}".upper()
    return any(keyword and keyword in haystack for keyword in keywords)


def parse_iso_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


@dataclass(frozen=True)
class SchoolYear:
    label: str
    start_date: date
    end_date: date
    vacation_ranges: Sequence[Tuple[date, date]]
    holidays: Sequence[date]


@dataclass(frozen=True)
class ClassProfile:
    name: str
    weekly_hours: int
    theme_pool: Sequence[str]


@dataclass(frozen=True)
class WeekSlot:
    index: int
    week_start: date
    week_end: date


@dataclass(frozen=True)
class WeekRow:
    week_no: int
    date_span: str
    weekly_hours: int
    topic: str
    weekly_task: str
    system: str
    notes: str


@dataclass(frozen=True)
class SheetMeta:
    title: str
    subtitle: str
    themes_label: str
    themes_text: str
    material_label: str
    material_text: str
    process_label: str
    process_text: str
    hints_label: str
    hints_text: str


@dataclass(frozen=True)
class ImportedSheet:
    sheet_name: str
    class_name: str
    weekly_hours: int
    meta: SheetMeta
    rows: List[WeekRow]


class CalendarModel:
    def __init__(self, school_year: SchoolYear) -> None:
        self.school_year = school_year

    def generate_teaching_weeks(self) -> List[WeekSlot]:
        weeks: List[WeekSlot] = []
        current = self._to_monday(self.school_year.start_date)
        idx = 1

        while current <= self.school_year.end_date:
            week_end = current + timedelta(days=4)
            if self._is_teaching_week(current):
                weeks.append(WeekSlot(index=idx, week_start=current, week_end=week_end))
                idx += 1
            current += timedelta(days=7)

        return weeks

    def _to_monday(self, d: date) -> date:
        return d - timedelta(days=d.weekday())

    def _is_teaching_week(self, monday: date) -> bool:
        if monday < self.school_year.start_date or monday > self.school_year.end_date:
            return False

        if monday in self.school_year.holidays:
            return False

        for start, end in self.school_year.vacation_ranges:
            if start <= monday <= end:
                return False

        return True


class WeeklyPlanController:
    def __init__(self, assignment_templates: Sequence[str]) -> None:
        self.assignment_templates = assignment_templates

    def build_rows(self, profile: ClassProfile, week_slots: Sequence[WeekSlot]) -> List[WeekRow]:
        rows: List[WeekRow] = []
        for i, slot in enumerate(week_slots):
            topic = profile.theme_pool[i % len(profile.theme_pool)]
            assignment_tpl = self.assignment_templates[i % len(self.assignment_templates)]
            weekly_task = assignment_tpl.format(topic=topic, class_name=profile.name, week=slot.index)
            date_span = f"{slot.week_start.strftime('%d.%m.%Y')} - {slot.week_end.strftime('%d.%m.%Y')}"

            rows.append(
                WeekRow(
                    week_no=slot.index,
                    date_span=date_span,
                    weekly_hours=profile.weekly_hours,
                    topic=topic,
                    weekly_task=weekly_task,
                    system="Teams, Blogbeitrag",
                    notes="",
                )
            )

        return rows


class TransferWorkbookImporter:
    DATA_HEADER_ROW = 6

    def __init__(self, source_file: Path, target_school_year: str) -> None:
        self.source_file = source_file
        self.target_school_year = target_school_year
        self.target_start_year = self._parse_target_start_year(target_school_year)
        self.source_start_year: Optional[int] = None
        self.target_start_date: Optional[date] = None
        self.target_end_date: Optional[date] = None
        if self.target_start_year is not None:
            self.target_start_date = date(self.target_start_year, 9, 1)
            self.target_end_date = date(self.target_start_year + 1, 8, 31)

    def import_sheets(self) -> List[ImportedSheet]:
        book = xlrd.open_workbook(str(self.source_file))
        imported: List[ImportedSheet] = []

        for sheet_name in book.sheet_names():
            sheet = book.sheet_by_name(sheet_name)
            if sheet.nrows == 0:
                continue
            if not self._looks_like_weekplan(sheet):
                continue

            raw_subtitle = self._cell_text(sheet, 1, 0)
            self._capture_source_start_year(raw_subtitle)
            meta = self._extract_meta(sheet, raw_subtitle)
            class_name = self._extract_class_name(meta.subtitle, sheet_name)
            weekly_hours = self._extract_weekly_hours(meta.subtitle)
            rows = self._extract_rows(sheet, weekly_hours)

            if not rows:
                continue

            imported.append(
                ImportedSheet(
                    sheet_name=sheet_name,
                    class_name=class_name,
                    weekly_hours=weekly_hours,
                    meta=meta,
                    rows=rows,
                )
            )

        if not imported:
            raise ValueError("Keine auswertbaren Wochenplan-Sheets in der Transferdatei gefunden.")

        return imported

    def _looks_like_weekplan(self, sheet: xlrd.sheet.Sheet) -> bool:
        title = str(sheet.cell_value(0, 0)).strip().upper() if sheet.nrows > 0 and sheet.ncols > 0 else ""
        return "WOCHENPLAN" in title

    def _extract_meta(self, sheet: xlrd.sheet.Sheet, raw_subtitle: str) -> SheetMeta:
        def cell(row: int, col: int) -> str:
            if row >= sheet.nrows or col >= sheet.ncols:
                return ""
            return str(sheet.cell_value(row, col)).strip()

        subtitle = self._rewrite_school_year_in_subtitle(raw_subtitle)

        return SheetMeta(
            title=cell(0, 0) or "WOCHENPLAN",
            subtitle=subtitle,
            themes_label=cell(2, 0) or "Themen:",
            themes_text=cell(2, 3),
            material_label=cell(3, 0) or "Arbeitsmaterial und Hilfsmittel:",
            material_text=cell(3, 3),
            process_label=cell(4, 0) or "Vorgehensweise:",
            process_text=cell(4, 3),
            hints_label=cell(5, 0) or "Hinweise:",
            hints_text=cell(5, 3),
        )

    def _rewrite_school_year_in_subtitle(self, subtitle: str) -> str:
        return re.sub(r"Schuljahr:\s*\d{4}/\d{4}", f"Schuljahr: {self.target_school_year}", subtitle)

    def _capture_source_start_year(self, subtitle: str) -> None:
        if self.source_start_year is not None:
            return
        match = re.search(r"Schuljahr:\s*(\d{4})/\d{4}", subtitle)
        if match:
            self.source_start_year = int(match.group(1))

    def _parse_target_start_year(self, target_school_year: str) -> Optional[int]:
        match = re.match(r"\s*(\d{4})/\d{4}\s*$", target_school_year)
        if not match:
            return None
        return int(match.group(1))

    def _extract_class_name(self, subtitle: str, fallback_sheet_name: str) -> str:
        match = re.search(r"Klasse:\s*([^\s]+)", subtitle)
        if match:
            raw = match.group(1).strip()
            if raw.isdigit() and fallback_sheet_name.upper().startswith("BG"):
                return fallback_sheet_name.upper()
            return raw
        # Sheet-Name ohne Suffixe als Fallback
        return re.split(r"[_\s]", fallback_sheet_name.strip())[0]

    def _extract_weekly_hours(self, subtitle: str) -> int:
        match = re.search(r"WoStd\.:\s*(\d+)", subtitle)
        if not match:
            return 0
        return int(match.group(1))

    def _extract_rows(self, sheet: xlrd.sheet.Sheet, weekly_hours: int) -> List[WeekRow]:
        rows: List[WeekRow] = []

        for r in range(self.DATA_HEADER_ROW + 1, sheet.nrows):
            nr_raw = self._cell_value(sheet, r, 0)
            from_raw = self._cell_value(sheet, r, 1)
            to_raw = self._cell_value(sheet, r, 2)
            topic = self._cell_text(sheet, r, 3)
            system = self._cell_text(sheet, r, 4)
            note = self._cell_text(sheet, r, 5)

            if not topic and not system and not note:
                continue

            # Ferien-/sonderwochen ohne Nummer werden uebernommen, aber nicht gezaehlt.
            if not self._is_number(nr_raw):
                week_no = 0
            else:
                week_no = int(float(nr_raw))

            from_dt, to_dt = self._normalize_dates(from_raw, to_raw)
            if not self._is_within_target_schoolyear(from_dt, to_dt):
                continue

            date_span = self._format_date_span(from_dt, to_dt)

            rows.append(
                WeekRow(
                    week_no=week_no,
                    date_span=date_span,
                    weekly_hours=weekly_hours,
                    topic=topic,
                    weekly_task=topic,
                    system=system,
                    notes=note,
                )
            )

        return rows

    def _cell_value(self, sheet: xlrd.sheet.Sheet, row: int, col: int):
        if row >= sheet.nrows or col >= sheet.ncols:
            return ""
        return sheet.cell_value(row, col)

    def _cell_text(self, sheet: xlrd.sheet.Sheet, row: int, col: int) -> str:
        value = self._cell_value(sheet, row, col)
        return str(value).strip()

    def _is_number(self, value) -> bool:
        try:
            float(value)
            return True
        except (TypeError, ValueError):
            return False

    def _format_date_span(self, from_dt: Optional[date], to_dt: Optional[date]) -> str:
        if not from_dt and not to_dt:
            return ""
        if from_dt and to_dt:
            return f"{from_dt.strftime('%d.%m.%Y')} - {to_dt.strftime('%d.%m.%Y')}"
        if from_dt:
            return from_dt.strftime('%d.%m.%Y')
        return to_dt.strftime('%d.%m.%Y') if to_dt else ""

    def _normalize_dates(self, from_value, to_value) -> Tuple[Optional[date], Optional[date]]:
        from_dt = self._shift_to_target_school_year(self._excel_date_to_date(from_value))
        to_dt = self._shift_to_target_school_year(self._excel_date_to_date(to_value))

        if from_dt and to_dt:
            delta = (to_dt - from_dt).days
            if delta < 0 or delta > 7:
                to_dt = from_dt + timedelta(days=4)
        elif from_dt and not to_dt:
            to_dt = from_dt + timedelta(days=4)
        elif to_dt and not from_dt:
            from_dt = to_dt - timedelta(days=4)

        return from_dt, to_dt

    def _is_within_target_schoolyear(self, from_dt: Optional[date], to_dt: Optional[date]) -> bool:
        if self.target_start_date is None or self.target_end_date is None:
            return True

        reference = from_dt or to_dt
        if reference is None:
            return True

        return self.target_start_date <= reference <= self.target_end_date

    def _excel_date_to_date(self, value) -> Optional[date]:
        if not self._is_number(value):
            return None
        try:
            dt = xlrd.xldate_as_datetime(float(value), 0)
            return dt.date()
        except (ValueError, OverflowError):
            return None

    def _shift_to_target_school_year(self, value: Optional[date]) -> Optional[date]:
        if value is None:
            return None
        if self.source_start_year is None or self.target_start_year is None:
            return value

        year_delta = self.target_start_year - self.source_start_year
        if year_delta == 0:
            return value

        target_year = value.year + year_delta
        try:
            return value.replace(year=target_year)
        except ValueError:
            # Robustes Verhalten fuer Sonderfaelle wie 29.02.
            if value.month == 2 and value.day == 29:
                return value.replace(year=target_year, day=28)
            return value


class XlsView:
    def __init__(self, layout_template: Optional[dict] = None) -> None:
        self.layout_template = layout_template or load_layout_template(None)

    def export_from_import(self, output_file: Path, sheets: Sequence[ImportedSheet]) -> None:
        wb = xlwt.Workbook()

        vacation_cfg = self.layout_template.get("vacation_row", {})
        palette_index = int(vacation_cfg.get("xls_palette_index", 33))
        palette_rgb = vacation_cfg.get("xls_palette_rgb", [253, 233, 217])
        if isinstance(palette_rgb, list) and len(palette_rgb) == 3:
            wb.set_colour_RGB(palette_index, int(palette_rgb[0]), int(palette_rgb[1]), int(palette_rgb[2]))

        header_style = xlwt.easyxf("font: bold on; align: horiz center, vert center; pattern: pattern solid, fore_colour gray25;")
        label_style = xlwt.easyxf("font: bold on;")
        body_style = xlwt.easyxf("align: vert top, wrap on;")
        vacation_style = xlwt.easyxf(f"align: vert top, wrap on; pattern: pattern solid, fore_colour {palette_index};")

        for item in sheets:
            ws = wb.add_sheet(item.sheet_name[:31])

            import_col_widths = self.layout_template.get("xls", {}).get("import_col_widths", [2300, 4200, 4200, 17000, 5200, 5200])
            for idx, width in enumerate(import_col_widths[:6]):
                ws.col(idx).width = int(width)

            ws.write(0, 0, item.meta.title, label_style)
            ws.write(1, 0, item.meta.subtitle)

            ws.write(2, 0, item.meta.themes_label, label_style)
            ws.write(2, 3, item.meta.themes_text, body_style)
            ws.write(3, 0, item.meta.material_label, label_style)
            ws.write(3, 3, item.meta.material_text, body_style)
            ws.write(4, 0, item.meta.process_label, label_style)
            ws.write(4, 3, item.meta.process_text, body_style)
            ws.write(5, 0, item.meta.hints_label, label_style)
            ws.write(5, 3, item.meta.hints_text, body_style)

            headers = ["Nr.", "vom", "bis", "Inhalte/Thema/Aufgabe", "System", "Anmerkung"]
            for col, header in enumerate(headers):
                ws.write(6, col, header, header_style)

            out_row = 7
            for row in item.rows:
                week_value = "" if row.week_no == 0 else row.week_no
                start_text, end_text = self._split_span(row.date_span)
                row_style = vacation_style if is_vacation_row(row, self.layout_template) else body_style

                ws.write(out_row, 0, week_value, row_style)
                ws.write(out_row, 1, start_text, row_style)
                ws.write(out_row, 2, end_text, row_style)
                ws.write(out_row, 3, row.topic, row_style)
                ws.write(out_row, 4, row.system, row_style)
                ws.write(out_row, 5, row.notes, row_style)
                ws.row(out_row).height = 620
                out_row += 1

            # Druck-Setup: eine Seite breit.
            ws.fit_num_pages = 1
            ws.set_panes_frozen(True)
            ws.set_horz_split_pos(7)
            ws.set_remove_splits(True)

        wb.save(str(output_file))

    def _split_span(self, date_span: str) -> Tuple[str, str]:
        if " - " not in date_span:
            return date_span, ""
        start, end = date_span.split(" - ", 1)
        return start, end

    def export(self, output_file: Path, school_year_label: str, plans: Dict[str, List[WeekRow]]) -> None:
        wb = xlwt.Workbook()

        header_style = xlwt.easyxf("font: bold on; align: horiz center, vert center; pattern: pattern solid, fore_colour gray25;")
        meta_style = xlwt.easyxf("font: bold on;")
        cell_style = xlwt.easyxf("align: vert top, wrap on;")

        for class_name, rows in plans.items():
            ws = wb.add_sheet(class_name[:31])

            ws.col(0).width = 2300
            ws.col(1).width = 5500
            ws.col(2).width = 2600
            ws.col(3).width = 9000
            ws.col(4).width = 14000
            ws.col(5).width = 7000

            ws.write(0, 0, "Wochenplan", meta_style)
            ws.write(0, 1, class_name, meta_style)
            ws.write(0, 3, "Schuljahr", meta_style)
            ws.write(0, 4, school_year_label, meta_style)

            headers = ["Woche", "Zeitraum", "Wochenstunden", "Thema", "Wochenaufgabe", "Hinweise"]
            for col, header in enumerate(headers):
                ws.write(2, col, header, header_style)

            for row_idx, row in enumerate(rows, start=3):
                ws.write(row_idx, 0, row.week_no, cell_style)
                ws.write(row_idx, 1, row.date_span, cell_style)
                ws.write(row_idx, 2, row.weekly_hours, cell_style)
                ws.write(row_idx, 3, row.topic, cell_style)
                ws.write(row_idx, 4, row.weekly_task, cell_style)
                ws.write(row_idx, 5, row.notes, cell_style)
                ws.row(row_idx).height = 550

            # Druck-Setup: auf eine Seite breit, bis zu zwei Seiten hoch.
            ws.set_panes_frozen(True)
            ws.set_horz_split_pos(3)
            ws.set_remove_splits(True)
            ws.fit_num_pages = 1

        wb.save(str(output_file))


class PdfView:
    def __init__(self, layout_template: Optional[dict] = None) -> None:
        self.layout_template = layout_template or load_layout_template(None)

    def export_single_from_import(self, output_file: Path, item: ImportedSheet, print_mode: bool = True) -> None:
        output_file.parent.mkdir(parents=True, exist_ok=True)

        if not print_mode:
            self._render_single_pdf(output_file, item, body_font_size=8.5, table_font_size=8.0, paddings=2.5)
            return

        # Ziel: auf 1 Seite breit, wenn moeglich max. 2 Seiten hoch.
        attempts = [
            (8.5, 8.0, 2.5),
            (8.0, 7.4, 2.0),
            (7.2, 6.8, 1.5),
        ]

        best_file = output_file
        for body_font_size, table_font_size, paddings in attempts:
            self._render_single_pdf(best_file, item, body_font_size, table_font_size, paddings)
            pages = self._count_pdf_pages(best_file)
            if pages <= 2:
                break

    def _render_single_pdf(
        self,
        output_file: Path,
        item: ImportedSheet,
        body_font_size: float,
        table_font_size: float,
        paddings: float,
    ) -> None:
        doc = SimpleDocTemplate(
            str(output_file),
            pagesize=landscape(A4),
            leftMargin=16,
            rightMargin=16,
            topMargin=14,
            bottomMargin=14,
        )
        styles = getSampleStyleSheet()
        heading = styles["Heading2"]
        heading.fontName = "Helvetica-Bold"
        heading.fontSize = 13
        heading.leading = 15

        body = styles["BodyText"]
        body.fontName = "Helvetica"
        body.fontSize = body_font_size
        body.leading = max(body_font_size + 1.2, 8.0)

        meta_label_style = ParagraphStyle(
            "MetaLabel",
            parent=body,
            fontName="Helvetica-Bold",
            fontSize=body_font_size,
            leading=body.leading,
        )

        table_cell_style = ParagraphStyle(
            "TableCell",
            parent=body,
            fontName="Helvetica",
            fontSize=table_font_size,
            leading=max(table_font_size + 1.1, 7.6),
            wordWrap="CJK",
        )

        table_head_style = ParagraphStyle(
            "TableHead",
            parent=table_cell_style,
            fontName="Helvetica-Bold",
        )

        elements = []
        elements.append(Paragraph(item.meta.title, heading))
        elements.append(Spacer(1, 2))

        # Kopfblock wie in der Vorlage: Labels links, Inhalte rechts, inkl. Leerfelder.
        meta_data = [
            [self._to_paragraph(item.meta.subtitle, body), ""],
            [self._to_paragraph(item.meta.themes_label, meta_label_style), self._to_paragraph(item.meta.themes_text, body)],
            [self._to_paragraph(item.meta.material_label, meta_label_style), self._to_paragraph(item.meta.material_text, body)],
            [self._to_paragraph(item.meta.process_label, meta_label_style), self._to_paragraph(item.meta.process_text, body)],
            [self._to_paragraph(item.meta.hints_label, meta_label_style), self._to_paragraph(item.meta.hints_text, body)],
        ]

        meta_col_widths = self.layout_template.get("pdf", {}).get("single_import_meta_col_widths", [210, 600])
        meta_table = Table(meta_data, colWidths=meta_col_widths)
        meta_table.setStyle(
            TableStyle(
                [
                    ("SPAN", (0, 0), (1, 0)),
                    ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 4),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                    ("TOPPADDING", (0, 0), (-1, -1), 3),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                    ("BACKGROUND", (0, 1), (0, -1), colors.whitesmoke),
                ]
            )
        )

        elements.append(meta_table)
        elements.append(Spacer(1, 6))

        data = [[
            self._to_paragraph("Nr.", table_head_style),
            self._to_paragraph("vom", table_head_style),
            self._to_paragraph("bis", table_head_style),
            self._to_paragraph("Inhalte/Thema/Aufgabe", table_head_style),
            self._to_paragraph("System", table_head_style),
            self._to_paragraph("Anmerkung", table_head_style),
        ]]
        for row in item.rows:
            start_text, end_text = self._split_span(row.date_span)
            data.append([
                self._to_paragraph("" if row.week_no == 0 else str(row.week_no), table_cell_style),
                self._to_paragraph(start_text, table_cell_style),
                self._to_paragraph(end_text, table_cell_style),
                self._to_paragraph(row.topic, table_cell_style),
                self._to_paragraph(row.system, table_cell_style),
                self._to_paragraph(row.notes, table_cell_style),
            ])

        table_col_widths = self.layout_template.get("pdf", {}).get("single_import_table_col_widths", [34, 70, 70, 370, 135, 130])
        table = Table(
            data,
            repeatRows=1,
            colWidths=table_col_widths,
        )
        header_bg_hex = self.layout_template.get("header_bg_hex", "#D9E2F3")
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(header_bg_hex)),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("ALIGN", (0, 0), (2, -1), "CENTER"),
                    ("ALIGN", (4, 1), (5, -1), "LEFT"),
                    ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
                    ("LEFTPADDING", (0, 0), (-1, -1), paddings),
                    ("RIGHTPADDING", (0, 0), (-1, -1), paddings),
                    ("TOPPADDING", (0, 0), (-1, -1), paddings),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), paddings),
                ]
            )
        )

        vacation_cfg = self.layout_template.get("vacation_row", {})
        vacation_bg_hex = vacation_cfg.get("pdf_bg_hex", "#FDE9D9")
        for idx, row in enumerate(item.rows, start=1):
            if is_vacation_row(row, self.layout_template):
                table.setStyle(TableStyle([("BACKGROUND", (0, idx), (-1, idx), colors.HexColor(vacation_bg_hex))]))

        elements.append(table)
        doc.build(elements)

    def _to_paragraph(self, text: str, style: ParagraphStyle) -> Paragraph:
        safe_text = escape(text or "")
        safe_text = safe_text.replace("\n", "<br/>")
        return Paragraph(safe_text, style)

    def _count_pdf_pages(self, pdf_file: Path) -> int:
        try:
            from pypdf import PdfReader

            reader = PdfReader(str(pdf_file))
            return len(reader.pages)
        except Exception:
            # Fallback: wenn Seitenzahl nicht bestimmbar ist, keine weitere Verdichtung erzwingen.
            return 1

    def export_from_import(self, output_file: Path, school_year_label: str, sheets: Sequence[ImportedSheet]) -> None:
        output_file.parent.mkdir(parents=True, exist_ok=True)

        doc = SimpleDocTemplate(
            str(output_file),
            pagesize=landscape(A4),
            leftMargin=16,
            rightMargin=16,
            topMargin=16,
            bottomMargin=16,
        )
        styles = getSampleStyleSheet()

        elements = []
        for item in sheets:
            elements.append(Paragraph(f"{item.meta.title} | {item.meta.subtitle}", styles["Heading2"]))
            elements.append(Spacer(1, 6))

            if item.meta.themes_text:
                elements.append(Paragraph(f"<b>{item.meta.themes_label}</b> {item.meta.themes_text}", styles["BodyText"]))
                elements.append(Spacer(1, 4))
            if item.meta.material_text:
                elements.append(Paragraph(f"<b>{item.meta.material_label}</b> {item.meta.material_text}", styles["BodyText"]))
                elements.append(Spacer(1, 3))
            if item.meta.process_text:
                elements.append(Paragraph(f"<b>{item.meta.process_label}</b> {item.meta.process_text}", styles["BodyText"]))
                elements.append(Spacer(1, 3))
            if item.meta.hints_text:
                elements.append(Paragraph(f"<b>{item.meta.hints_label}</b> {item.meta.hints_text}", styles["BodyText"]))
                elements.append(Spacer(1, 6))

            data = [["Nr.", "vom", "bis", "Inhalte/Thema/Aufgabe", "System", "Anmerkung"]]
            for row in item.rows:
                start_text, end_text = self._split_span(row.date_span)
                data.append([
                    "" if row.week_no == 0 else str(row.week_no),
                    start_text,
                    end_text,
                    row.topic,
                    row.system,
                    row.notes,
                ])

            table = Table(
                data,
                repeatRows=1,
                colWidths=[35, 64, 64, 340, 110, 110],
            )
            table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#D9E2F3")),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, -1), 7.5),
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
                        ("LEFTPADDING", (0, 0), (-1, -1), 3),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                        ("TOPPADDING", (0, 0), (-1, -1), 2),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                    ]
                )
            )

            elements.append(table)
            elements.append(Spacer(1, 12))

        doc.build(elements)

    def _split_span(self, date_span: str) -> Tuple[str, str]:
        if " - " not in date_span:
            return date_span, ""
        start, end = date_span.split(" - ", 1)
        return start, end

    def export(self, output_file: Path, school_year_label: str, plans: Dict[str, List[WeekRow]]) -> None:
        output_file.parent.mkdir(parents=True, exist_ok=True)

        doc = SimpleDocTemplate(
            str(output_file),
            pagesize=landscape(A4),
            leftMargin=18,
            rightMargin=18,
            topMargin=20,
            bottomMargin=18,
        )
        styles = getSampleStyleSheet()

        elements = []
        for class_name, rows in plans.items():
            title = Paragraph(f"Wochenplan {class_name} | Schuljahr {school_year_label}", styles["Heading2"])
            elements.append(title)
            elements.append(Spacer(1, 8))

            data = [["Woche", "Zeitraum", "Stunden", "Thema", "Wochenaufgabe", "Hinweise"]]
            for row in rows:
                data.append([
                    str(row.week_no),
                    row.date_span,
                    str(row.weekly_hours),
                    row.topic,
                    row.weekly_task,
                    row.notes,
                ])

            table = Table(
                data,
                repeatRows=1,
                colWidths=[36, 88, 52, 160, 280, 120],
            )
            table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#D9E2F3")),
                        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                        ("FONTSIZE", (0, 0), (-1, -1), 8),
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                        ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
                        ("LEFTPADDING", (0, 0), (-1, -1), 4),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                        ("TOPPADDING", (0, 0), (-1, -1), 3),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                    ]
                )
            )

            elements.append(table)
            elements.append(Spacer(1, 18))

        doc.build(elements)


class WeeklyPlanApp:
    def __init__(self, config_path: Path) -> None:
        self.config_path = config_path
        self.config = self._load_config(config_path)
        template_path_cfg = self.config.get("layout_template")
        template_path = None
        if template_path_cfg:
            raw_template_path = Path(template_path_cfg)
            template_path = raw_template_path if raw_template_path.is_absolute() else (Path(__file__).parent / raw_template_path).resolve()
        self.layout_template = load_layout_template(template_path)

    def run(self) -> Tuple[Path, Path]:
        school_year = self._build_school_year(self.config)
        classes = self._build_classes(self.config)

        calendar = CalendarModel(school_year)
        week_slots = calendar.generate_teaching_weeks()

        controller = WeeklyPlanController(self.config["assignment_templates"])
        plans: Dict[str, List[WeekRow]] = {}
        for profile in classes:
            plans[profile.name] = controller.build_rows(profile, week_slots)

        output_dir = self._resolve_output_dir(self.config)
        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        school_year_label = school_year.label
        prefix = self.config.get("output_prefix", "Wochenplaene")
        version_tag = self._next_version_tag(output_dir, school_year_label)

        xls_path = output_dir / f"{prefix}_{school_year_label}_{version_tag}_{timestamp}.xls"
        pdf_path = output_dir / f"{prefix}_{school_year_label}_{version_tag}_{timestamp}.pdf"

        XlsView(self.layout_template).export(xls_path, school_year_label, plans)
        PdfView(self.layout_template).export(pdf_path, school_year_label, plans)

        return xls_path, pdf_path

    def run_from_transfer(self, transfer_file: Path, target_school_year: str) -> Tuple[Path, Path]:
        importer = TransferWorkbookImporter(transfer_file, target_school_year)
        sheets = importer.import_sheets()

        output_dir = self._resolve_output_dir(self.config)
        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        prefix = self.config.get("output_prefix", "Wochenplaene")
        label_sanitized = target_school_year.replace("/", "_")
        version_tag = self._next_version_tag(output_dir, label_sanitized)

        xls_path = output_dir / f"{prefix}_{label_sanitized}_{version_tag}_{timestamp}.xls"
        pdf_path = output_dir / f"{prefix}_{label_sanitized}_{timestamp}.pdf"

        XlsView(self.layout_template).export_from_import(xls_path, sheets)

        pdf_view = PdfView(self.layout_template)
        generated_pdf_files: List[Path] = []
        print_mode = bool(self.config.get("print_mode", True))
        for item in sheets:
            class_pdf = output_dir / f"Wochenplan_{item.class_name}_{label_sanitized}_{version_tag}_{timestamp}.pdf"
            pdf_view.export_single_from_import(class_pdf, item, print_mode=print_mode)
            generated_pdf_files.append(class_pdf)

        # Fuer Rueckwaertskompatibilitaet bleibt der zweite Rueckgabewert ein PDF-Pfad.
        if generated_pdf_files:
            pdf_path = generated_pdf_files[0]

        return xls_path, pdf_path

    def _next_version_tag(self, output_dir: Path, school_year_label: str) -> str:
        escaped = re.escape(school_year_label)
        pattern = re.compile(rf"_{escaped}_v(\d{{3}})_")

        max_version = 0
        for candidate in output_dir.glob(f"*{school_year_label}*.*"):
            match = pattern.search(candidate.name)
            if not match:
                continue
            max_version = max(max_version, int(match.group(1)))

        return f"v{max_version + 1:03d}"

    def _load_config(self, config_path: Path) -> dict:
        if not config_path.exists():
            raise FileNotFoundError(f"Konfiguration nicht gefunden: {config_path}")
        with config_path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def _build_school_year(self, config: dict) -> SchoolYear:
        school_year_cfg = config["school_year"]
        vacations = [
            (parse_iso_date(block["start"]), parse_iso_date(block["end"]))
            for block in config.get("vacation_ranges", [])
        ]
        holidays = [parse_iso_date(v) for v in config.get("holidays", [])]
        return SchoolYear(
            label=school_year_cfg["label"],
            start_date=parse_iso_date(school_year_cfg["start_date"]),
            end_date=parse_iso_date(school_year_cfg["end_date"]),
            vacation_ranges=vacations,
            holidays=holidays,
        )

    def _build_classes(self, config: dict) -> List[ClassProfile]:
        classes = []
        for item in config["classes"]:
            classes.append(
                ClassProfile(
                    name=item["name"],
                    weekly_hours=int(item["weekly_hours"]),
                    theme_pool=item["theme_pool"],
                )
            )
        return classes

    def _resolve_output_dir(self, config: dict) -> Path:
        configured = config.get("output_dir", "08_Ausgaben/Jahresuebersichten")
        configured_path = Path(configured)
        if configured_path.is_absolute():
            return configured_path

        module_root = Path(__file__).resolve().parents[2]
        return (module_root / configured_path).resolve()


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generiert Wochenplaene als XLS und PDF")
    parser.add_argument(
        "--config",
        default="config/probe_2026_2027.json",
        help="Pfad zur JSON-Konfiguration",
    )
    parser.add_argument(
        "--transfer-xls",
        default="",
        help="Optional: vorhandene Transfer-XLS als Quelle (Layout bleibt erhalten)",
    )
    parser.add_argument(
        "--target-school-year",
        default="2026/2027",
        help="Zielschuljahr fuer Transfermodus, z. B. 2026/2027",
    )
    parser.add_argument(
        "--print-mode",
        choices=["auto", "off"],
        default="auto",
        help="PDF-Druckoptimierung: auto (Standard) oder off",
    )
    parser.add_argument(
        "--layout-template",
        default="config/layout_template_v003.json",
        help="JSON-Template fuer Layout/Formatierung (Standard: v003)",
    )
    return parser


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()

    cfg_path = Path(args.config)
    if not cfg_path.is_absolute():
        cfg_path = (Path(__file__).parent / cfg_path).resolve()

    app = WeeklyPlanApp(cfg_path)
    app.config["print_mode"] = args.print_mode == "auto"
    app.config["layout_template"] = args.layout_template
    raw_template_path = Path(args.layout_template)
    resolved_template = raw_template_path if raw_template_path.is_absolute() else (Path(__file__).parent / raw_template_path).resolve()
    app.layout_template = load_layout_template(resolved_template)
    if args.transfer_xls:
        transfer_path = Path(args.transfer_xls)
        if not transfer_path.is_absolute():
            transfer_path = (Path(__file__).parent / transfer_path).resolve()
        xls_file, pdf_file = app.run_from_transfer(transfer_path, args.target_school_year)
    else:
        xls_file, pdf_file = app.run()

    print(f"XLS erzeugt: {xls_file}")
    print(f"PDF erzeugt: {pdf_file}")


if __name__ == "__main__":
    main()
