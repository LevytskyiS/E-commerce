from eshop.celery import app
from orders.models import Order


from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer


def issue_invoice(order_id: int):
    order = Order.objects.get(id=order_id)
    order_items = [item for item in order.items.all()]
    order_code = order.code
    order_created_at = order.created_at
    shipping_address = order.shipping_address

    filename = f"invoices/{order.code}-INVOICE.pdf"

    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()
    normal_style = styles["Normal"]
    heading_style = styles["Heading2"]

    seller_info = "Imperium Inc.\n123 Paradise St.\nNYC, SL 12345"
    buyer_info = f"{order.user.first_name} {order.user.last_name},\n{order.shipping_address.address}, {order.shipping_address.city}\n{order.shipping_address.country}, {order.shipping_address.postal_code}"

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

    col_widths = [doc.width / 2, doc.width / 2]

    elements.append(Spacer(1, 20))

    ordered_items = [
        ["Product Name", "Quantity", "Price per Unit", "Total Price"],
    ]

    for item in order_items:
        ordered_items.append(
            [
                item.nomenclature.code,
                item.nomenclature.product.name,
                item.quantity,
                item.nomenclature.price,
                item.total_price(),
            ]
        )

    elements.append(Paragraph("Ordered Items", heading_style))
    elements.append(Spacer(1, 10))

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

    elements.append(Spacer(1, 20))

    total_price = order.total_price()

    total_price_data = [["Total Price:", f"{total_price:.2f} EUR"]]

    total_price_table_style = TableStyle(
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

    total_price_table = Table(
        total_price_data,
        colWidths=[col_widths[0], col_widths[1]],
        style=total_price_table_style,
        hAlign="LEFT",
    )
    elements.append(total_price_table)

    doc.build(elements)


@app.task
def send_invoice(order_id: int):
    issue_invoice(order_id)
