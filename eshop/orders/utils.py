import uuid


def generate_order_number():
    code = f"MM{uuid.uuid1()}"[0:8]
    return code.upper()
