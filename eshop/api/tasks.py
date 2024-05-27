from eshop.celery import app
from orders.models import Order


from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer


def issue_invoice(order_id: int):
    order = Order.objects.get(id=order_id)

    filename = f"invoices/{order.code}-INVOICE.pdf"

    # Создание PDF-документа
    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = []

    # Стиль текста
    styles = getSampleStyleSheet()
    normal_style = styles["Normal"]
    heading_style = styles["Heading2"]

    # Данные для таблицы
    seller_info = "Seller Company\n123 Seller St.\nSeller City, SL 12345"
    buyer_info = "Buyer Company\n456 Buyer St.\nBuyer City, BY 67890"

    # Таблица с информацией о компаниях
    company_data = [
        [Paragraph(seller_info, normal_style), Paragraph(buyer_info, normal_style)]
    ]

    company_table_style = TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]
    )

    company_table = Table(company_data, style=company_table_style, hAlign="LEFT")
    elements.append(company_table)

    # Добавление отступа между таблицами
    elements.append(Spacer(1, 20))

    # Данные для списка заказанных товаров
    ordered_items = [
        ["Product Name", "Quantity", "Price per Unit", "Total Price"],
        ["Product 1", "2", "$10.00", "$20.00"],
        ["Product 2", "1", "$15.00", "$15.00"],
        ["Product 3", "5", "$7.00", "$35.00"],
    ]

    # Заголовок для списка товаров
    elements.append(Paragraph("Ordered Items", heading_style))
    elements.append(Spacer(1, 10))

    # Таблица со списком заказанных товаров
    items_table_style = TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]
    )

    items_table = Table(ordered_items, style=items_table_style, hAlign="LEFT")
    elements.append(items_table)

    # Сохранение PDF
    doc.build(elements)


@app.task
def send_invoice(order_id: int):
    issue_invoice(order_id)
