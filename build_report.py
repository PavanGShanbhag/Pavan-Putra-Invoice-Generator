import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def create_project_report(filename="Pavanputra_AI_Invoicing_Report.pdf"):
    # 1. Initialize Document Canvas
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=54, leftMargin=54, topMargin=54, bottomMargin=54
    )
    story = []
    
    # 2. Setup Typography Styles
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Title'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#0284c7'),
        alignment=0,
        spaceAfter=6
    )
    
    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#1e293b'),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=15,
        textColor=colors.HexColor('#334155'),
        spaceAfter=8
    )
    
    bullet_style = ParagraphStyle(
        'BulletCustom',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    # 3. Document Content Data Array
    story.append(Paragraph("PROJECT REPORT: Pavanputra AI Invoicing", title_style))
    
    # Metadata Table Block
    meta_data = [
        [Paragraph("<b>Track:</b> Agents for Business", body_style), Paragraph("<b>Author:</b> Pavan G Shanbhag", body_style)],
        [Paragraph("<b>Date:</b> June 20, 2026", body_style), Paragraph("<b>Deployment:</b> Localized Agentic Harness", body_style)]
    ]
    meta_table = Table(meta_data, colWidths=[250, 250])
    meta_table.setStyle(TableStyle([
        ('LINEBELOW', (0,1), (-1,1), 1, colors.HexColor('#cbd5e1')),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 15))

    # Section 1
    story.append(Paragraph("1. Executive Summary", h1_style))
    story.append(Paragraph(
        "<b>Pavanputra AI Invoicing</b> is a next-generation enterprise billing and international trade automation system "
        "designed to eliminate manual input friction in export workflows. Moving away from fragile, cloud-dependent agent "
        "architectures, this project builds a robust local 'Harness' that safely sandwiches a Large Language Model between "
        "deterministic validation scripts and a print-ready user interface. The system interprets unstructured human natural "
        "language intent, dynamically routes transaction metadata through external APIs, and auto-populates complex logistics "
        "arrays to output compliant Proforma Invoices instantly.", body_style
    ))

    # Section 2
    story.append(Paragraph("2. Problem Statement & The 'Black-Box' Bottleneck", h1_style))
    story.append(Paragraph(
        "During initial development with fully automated workspace agents in cloud sandboxes, minor environment snags—such "
        "as path mismatches under Windows filesystems or dependency download hiccups—routinely caused silent failures. Because "
        "these platform-native sidebar agents operate like a 'black box,' debugging them provides zero visibility to the operator, "
        "leading to rapid token quota exhaustion.", body_style
    ))
    story.append(Paragraph("Furthermore, traditional international trade billing requires merchants to manually:", body_style))
    story.append(Paragraph("• Compute item discounts and compounding profit margins row-by-row.", bullet_style))
    story.append(Paragraph("• Look up fluctuating foreign exchange (Forex) conversion ratios.", bullet_style))
    story.append(Paragraph("• Adjust logistics surcharges dynamically based on diverse Incoterms (Ex-Works, FOB, C&F).", bullet_style))
    story.append(Paragraph(
        "Pavanputra AI Invoicing solves this twin challenge by extracting the developer out of the fragile autonomous sandbox "
        "into a direct, localized API 'Orchestrator' loop.", body_style
    ))

    # Section 3
    story.append(Paragraph("3. System Architecture & The 'Harness' Philosophy", h1_style))
    story.append(Paragraph(
        "Following the structured principles of the factory model, the developer's output is shifted from writing raw syntax "
        "to engineering the system that produces the output. The architecture is explicitly decoupled into two fundamental layers:", body_style
    ))
    story.append(Paragraph("<b>The Engine:</b> Powered by gemini-2.0-flash. It acts as the core cognitive processor, identifying user intent, extracting parameter values from conversational prompts, and invoking functional tools.", bullet_style))
    story.append(Paragraph("<b>The Harness:</b> A lightweight FastAPI local implementation executing on the D: drive. It isolates system logic from global interpreter path conflicts using a dedicated Python virtual environment (venv). The frontend canvas layout utilizes Tailwind CSS configured with explicit @media print directives to ensure that dynamically rendered invoices automatically compile into perfectly formatted, print-ready sheets with absolute visual consistency.", bullet_style))

    # Section 4
    story.append(Paragraph("4. Multi-Tool Orchestration & Financial Logic", h1_style))
    story.append(Paragraph(
        "<b>A. Dynamic API Data Pipeline:</b> The agent is armed with a native execution tool: fetch_live_exchange_rates. "
        "When a user provides unstructured inputs containing overseas quotes (e.g., USD, EUR) or inputs an exchange override, "
        "the model calls the pipeline to parse live global financial indices.", body_style
    ))
    story.append(Paragraph(
        "<b>B. Deterministic Mathematical Harness:</b> To protect the system against LLM math inaccuracies (hallucinations), "
        "all primary calculations are executed strictly by deterministic JavaScript code bound directly to the form variables. "
        "The mathematical core formulas calculate the Gross Values by applying discounts and profit margins sequentially before dividing "
        "by the current conversion factor index to output accurate Target values. The financial summary blocks handle progressive incoterm totals automatically:", body_style
    ))
    story.append(Paragraph("• <b>Ex-Works Total:</b> Cargo Subtotal + Documentation + Packing + Transit Surcharges.", bullet_style))
    story.append(Paragraph("• <b>FOB Total:</b> Ex-Works Total + Customs Port Clearing Charges.", bullet_style))
    story.append(Paragraph("• <b>C&F Total:</b> FOB Total + Freight Transit Surcharge Matrix.", bullet_style))

    # Section 5
    story.append(Paragraph("5. Interaction Workflows & Operational Modes", h1_style))
    story.append(Paragraph("The system enables a hybrid workspace supporting two operational states:", body_style))
    story.append(Paragraph("<b>Conductor Mode (Manual Ingestion):</b> The merchant utilizes the data grid, inputs numbers manually, or hooks an external spreadsheet using the integrated Excel/CSV file upload listener to mount massive item arrays natively.", bullet_style))
    story.append(Paragraph("<b>Orchestrator Mode (AI-Driven Ingestion):</b> The merchant drops casual text strings into the AI Copilot console. The agent parses the parameters, systematically populates the data canvas variables on the fly, and generates a structured confirmation layout automatically.", bullet_style))

    # Section 6
    story.append(Paragraph("6. Conclusion", h1_style))
    story.append(Paragraph(
        "By wrapping the flexible cognitive intelligence of Gemini inside a highly controlled, locally compiled programmatic harness, "
        "<b>Pavanputra AI Invoicing</b> provides an enterprise billing system where speed never compromises accuracy. Generation "
        "is effectively automated, leaving validation, strategic routing, and corporate judgment entirely in the hands of the human architect.", body_style
    ))

    # Build PDF
    doc.build(story)
    print(f"✨ Success! '{filename}' has been generated perfectly in this directory.")

if __name__ == "__main__":
    create_project_report()