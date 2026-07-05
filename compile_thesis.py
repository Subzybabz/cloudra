import os
import re
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# 1. Custom Canvas to handle two-pass Page Numbering
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, page_count):
        # Do not draw page number on cover page (page 1)
        if self._pageNumber == 1:
            return
        self.saveState()
        self.setFont("Times-Roman", 10)
        # Centered at bottom (page width is 612 pt)
        self.drawCentredString(306, 45, str(self._pageNumber))
        self.restoreState()

def compile_thesis():
    input_path = "Final Year Project Chapter 1-3 (subomi).md"
    output_path = "Final_Year_Project_Chapters_1-5.pdf"
    
    print(f"Reading {input_path}...")
    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Normalize newlines
    content = content.replace("\r\n", "\n")
    
    # Setup document: standard 1-inch margins (left margin 1.5-inch for thesis binding)
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=1.5 * inch,
        rightMargin=1.0 * inch,
        topMargin=1.0 * inch,
        bottomMargin=1.0 * inch
    )
    
    # Styles
    styles = getSampleStyleSheet()
    
    # Custom academic styles: Times-Roman, 12pt, double-spaced (leading=24)
    body_style = ParagraphStyle(
        'AcademicBody',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=12,
        leading=24,  # Double line spacing
        spaceAfter=12,
        alignment=4  # Justified alignment
    )
    
    cover_title_style = ParagraphStyle(
        'CoverTitle',
        fontName='Times-Bold',
        fontSize=18,
        leading=26,
        alignment=1, # Centered
        spaceAfter=15
    )
    
    cover_info_style = ParagraphStyle(
        'CoverInfo',
        fontName='Times-Bold',
        fontSize=12,
        leading=18,
        alignment=1, # Centered
        spaceAfter=15
    )
    
    chapter_num_style = ParagraphStyle(
        'ChapterNum',
        fontName='Times-Bold',
        fontSize=14,
        leading=18,
        alignment=1, # Centered
        spaceAfter=10
    )
    
    chapter_title_style = ParagraphStyle(
        'ChapterTitle',
        fontName='Times-Bold',
        fontSize=16,
        leading=22,
        alignment=1, # Centered
        spaceAfter=25
    )
    
    section_style = ParagraphStyle(
        'SectionTitle',
        fontName='Times-Bold',
        fontSize=13,
        leading=18,
        spaceBefore=15,
        spaceAfter=10,
        keepWithNext=True
    )
    
    subsection_style = ParagraphStyle(
        'SubsectionTitle',
        fontName='Times-BoldItalic',
        fontSize=12,
        leading=16,
        spaceBefore=12,
        spaceAfter=8,
        keepWithNext=True
    )
    
    table_cell_style = ParagraphStyle(
        'TableCell',
        fontName='Times-Roman',
        fontSize=10,
        leading=14
    )
    
    table_header_style = ParagraphStyle(
        'TableHeader',
        fontName='Times-Bold',
        fontSize=10,
        leading=14
    )

    story = []
    
    # Simple block-based parser
    # Group content by paragraphs / tables / headings
    blocks = re.split(r'\n\n+', content.strip())
    
    # Track state
    is_cover_page = True

    for block in blocks:
        block = block.strip()
        if not block:
            continue
            
        # Parse markdown tables
        if block.startswith('|'):
            lines = block.split('\n')
            # Extract cells
            parsed_rows = []
            for line in lines:
                if re.match(r'^\|[-:| ]+\|$', line.strip()):
                    # Skip table divider row
                    continue
                cells = [c.strip() for c in line.split('|')[1:-1]]
                parsed_rows.append(cells)
            
            # Convert cells to flowable paragraphs
            row_flowables = []
            for row_idx, row in enumerate(parsed_rows):
                row_flowable = []
                for cell in row:
                    style = table_header_style if row_idx == 0 else table_cell_style
                    cleaned_cell = cell.replace('<br>', '<br/>')
                    row_flowable.append(Paragraph(cleaned_cell, style))
                row_flowables.append(row_flowable)
                
            # Build Table Flowable
            if row_flowables:
                num_cols = len(row_flowables[0])
                col_width = (6.0 * inch) / num_cols
                t = Table(row_flowables, colWidths=[col_width]*num_cols)
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,0), HexColor('#eaeaea')),
                    ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                    ('VALIGN', (0,0), (-1,-1), 'TOP'),
                    ('GRID', (0,0), (-1,-1), 0.5, HexColor('#999999')),
                    ('TOPPADDING', (0,0), (-1,-1), 6),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
                    ('LEFTPADDING', (0,0), (-1,-1), 6),
                    ('RIGHTPADDING', (0,0), (-1,-1), 6),
                ]))
                story.append(t)
                story.append(Spacer(1, 15))
            continue

        # Parse cover page headings (everything before first chapter)
        if is_cover_page:
            if block.startswith('## **Chapter 1**') or block.startswith('## **CHAPTER'):
                is_cover_page = False
                # Allow it to fall through to the chapter title parser below
            elif block.startswith('## **DESIGN') or block.startswith('**ASSESSMENT'):
                story.append(Spacer(1, 50))
                story.append(Paragraph(block.replace('**', '').replace('##', '').strip(), cover_title_style))
                continue
            else:
                story.append(Spacer(1, 15))
                story.append(Paragraph(block.replace('**', '').replace('##', '').strip(), cover_info_style))
                continue

        # Parse Chapter titles
        if block.startswith('## **CHAPTER') or block.startswith('## **Chapter'):
            story.append(PageBreak())
            cleaned_title = block.replace('##', '').replace('**', '').strip()
            story.append(Paragraph(cleaned_title, chapter_num_style))
            continue
            
        if block.startswith('## **LITERATURE') or block.startswith('## **RESEARCH') or block.startswith('## **DESIGN AND IMPLEMENTATION') or block.startswith('## **CONCLUSION AND RECOMMENDATION') or block.startswith('## **INTRODUCTION'):
            cleaned_title = block.replace('##', '').replace('**', '').strip()
            story.append(Paragraph(cleaned_title, chapter_title_style))
            continue

        # Parse Sections (e.g. ## **1.1 ...**)
        if block.startswith('## **') and not block.startswith('## **CHAPTER') and not block.startswith('## **Chapter'):
            cleaned_title = block.replace('##', '').replace('**', '').strip()
            story.append(Paragraph(cleaned_title, section_style))
            continue

        # Parse Sub-sections (e.g. ## _**1.2.1 ...**_)
        if block.startswith('## _**'):
            cleaned_title = block.replace('##', '').replace('_', '').replace('**', '').strip()
            story.append(Paragraph(cleaned_title, subsection_style))
            continue

        # Check for list markers
        if block.startswith('-') or block.startswith('*') or (len(block) > 1 and block[0].isdigit() and block[1] == '.'):
            list_items = block.split('\n')
            for item in list_items:
                item_text = re.sub(r'^[-*\d.]+\s+', '', item).strip()
                item_text = item_text.replace('**', '')
                story.append(Paragraph(f"• &nbsp; {item_text}", body_style))
            continue

        # Standard Paragraphs
        cleaned_text = block.replace('**', '').replace('_', '').strip()
        story.append(Paragraph(cleaned_text, body_style))

    # Remove duplicate leading PageBreaks
    while story and isinstance(story[0], PageBreak):
        story.pop(0)

    print(f"Generating PDF document...")
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Success! Generated {output_path}")

if __name__ == "__main__":
    compile_thesis()
