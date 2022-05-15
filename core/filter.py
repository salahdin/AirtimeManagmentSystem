def is_phone_valid(phone_number):

    phone = str(phone_number)

    if len(phone) < 9 or len(phone) > 13:
        return False

    elif phone[:4] != "+251" or phone[:2] != "09" or phone[:1] != "9":
        return False

    return True



print(is_phone_valid(phone))