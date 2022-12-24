def generate_registration_code(name, lastRegCode):
    return f"{name[:3].upper()}-{lastRegCode+3155}"
