from .schemas import ReceiptSchema
from src.utils.logger import logger


def format_num(num: int | float):

    return "{0:.2f}".format(num)


def generate_text_receipt(width: int, user_name: str, receipt: ReceiptSchema) -> str:
    logger.info(f"GenerateTextReceipt: receipt_id={receipt.id}")

    products_text = ""
    for index, product in enumerate(receipt.products):
        products_text += f"""
{format_num(product.quantity)} x {format_num(product.price / 100)}
{product.name.rjust(0)} {str(format_num((product.price * product.quantity) / 100)).rjust(width - len(product.name) - 1)}

{"-" * width if index + 1 != len(receipt.products) else ''}
"""

    receipt_text = f"""{user_name.center(width)}
{"=" * width}

{products_text.strip()}

{"=" * width}
{'СУМА'.rjust(0)} {str(format_num(receipt.total / 100)).rjust(width - 5)}
{'РЕШТА'.rjust(0)} {str(format_num(receipt.rest / 100)).rjust(width - 6)}
{"=" * width}
{receipt.created_at.strftime('%Y.%m.%d %H:%M').center(width)}
{'Дякуємо за покупку!'.center(width)}
"""

    return receipt_text
