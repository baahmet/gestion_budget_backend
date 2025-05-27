from io import BytesIO
from django.core.files.base import ContentFile
from django.utils.timezone import now
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie

def generate_rapport_file(budget, recettes, depenses, commandes, periode, user):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # ========== TITRE ==========
    title = Paragraph(f"<b>RAPPORT FINANCIER - {budget.exercice}</b>", styles["Title"])
    elements.append(title)
    elements.append(Spacer(1, 12))

    # ========== INFOS ==========
    infos = [
        ["Période :", periode],
        ["Montant Total :", f"{budget.montant_total:,.0f} FCFA"],
        ["Montant Disponible :", f"{budget.montant_disponible:,.0f} FCFA"]
    ]
    table_infos = Table(infos, hAlign='LEFT')
    table_infos.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(table_infos)
    elements.append(Spacer(1, 12))

    # ========== TABLE RECETTES ==========
    if recettes:
        elements.append(Paragraph("<b>Recettes :</b>", styles["Heading3"]))
        data = [["Source", "Type", "Montant (FCFA)"]]
        for r in recettes:
            data.append([r.source, r.type, f"{r.montant:,.0f}"])
        table = Table(data, hAlign='LEFT')
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4F81BD")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 12))

    # ========== TABLE DÉPENSES ==========
    if depenses:
        elements.append(Paragraph("<b>Dépenses validées :</b>", styles["Heading3"]))
        data = [["Type", "Catégorie", "Montant (FCFA)"]]
        for d in depenses:
            data.append([d.type_depense, d.categorie, f"{d.montant:,.0f}"])
        table = Table(data, hAlign='LEFT')
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4F81BD")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 12))

    # ========== TABLE COMMANDES ==========
    if commandes:
        elements.append(Paragraph("<b>Commandes :</b>", styles["Heading3"]))
        data = [["Désignation", "Quantité", "Total (FCFA)"]]
        for c in commandes:
            data.append([c.designation, c.quantite, f"{c.total:,.0f}"])
        table = Table(data, hAlign='LEFT')
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4F81BD")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 12))

    # ========== PIE CHART (Camembert) ==========
    pie_data = [budget.montant_disponible, budget.montant_total_depenses_validees]
    pie_labels = ["Montant Disponible", "Dépenses Validées"]

    drawing = Drawing(200, 150)
    pie = Pie()
    pie.x = 50
    pie.y = 0
    pie.data = pie_data
    pie.labels = pie_labels
    pie.width = 100
    pie.height = 100
    pie.slices[0].fillColor = colors.green
    pie.slices[1].fillColor = colors.red
    drawing.add(pie)
    elements.append(Paragraph("<b>Répartition du Budget</b>", styles["Heading3"]))
    elements.append(drawing)
    elements.append(Spacer(1, 12))

    # ========== FOOTER ==========
    elements.append(Paragraph(
        f"<i>Généré par : {user.nom} ({user.role}) - {now().strftime('%d/%m/%Y %H:%M')}</i>",
        styles["Normal"]
    ))

    doc.build(elements)
    buffer.seek(0)

    fichier_nom = f"rapport_{budget.exercice}_{periode}.pdf".replace(" ", "_")
    return ContentFile(buffer.read(), name=fichier_nom), fichier_nom
