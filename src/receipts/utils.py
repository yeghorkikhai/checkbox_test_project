from .schemas import ReceiptSchema


def generate_text_receipt(width: int, user_name: str, receipt: ReceiptSchema) -> str:
    products_text = ""

    for index, product in enumerate(receipt.products):
        products_text += f"""
{product.quantity} x {product.price}
{product.name.rjust(0)} {str(float((product.price * product.quantity) / 100)).rjust(width - len(product.name) - 2)}

{"-" * width if index + 1 != len(receipt.products) else ''}
"""

    receipt_text = f"""{user_name.center(width)}
{"=" * width}

{products_text.strip()}

{"=" * width}
{'СУМА'.rjust(0)} {str(receipt.total / 100).rjust(width - 5)}
{'РЕШТА'.rjust(0)} {str(receipt.rest / 100).rjust(width - 6)}
{"=" * width}
{receipt.created_at.strftime('%Y.%m.%d %H:%M').center(width)}
{'Дякуємо за покупку!'.center(width)}
"""

    return receipt_text
