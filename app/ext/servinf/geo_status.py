# -*- coding: utf-8 -*-


def status_geo(code):
    type_status = {
        'A': 'Aproximado con geo al 100%',
        'B': 'Normalizado y Georreferenciado Exacto',
        'C': 'Intraducible',
        'D': 'Normalizado y georreferenciado aproximado',
        'E': 'Normalizado y no georreferenciado',
        'F': 'Normalizado por cruce y georreferenciado exacto',
        'G': 'Normalizado por cruce y no georreferenciado',
        'H': 'Atípicas',
        'I': 'Normalizado por barrio georreferenciado',
        'J': 'Normalizado por barrio no georreferenciado',
        'K': 'Georreferenciado a centroide de barrio',
        'L': 'Normalizado por sitio y georreferenciado',
        'M': 'Normalizado y georreferenciado por predio',
        'N': 'Normalizado y georreferenciado por predio MZ',
        'O': 'Georreferenciado a centroide de localidad / comuna',
        'R': 'Direcciones Rurales',
        'W': 'Apartados aereos',
        'X': 'Ciudad disponible no adquirida',
        'Y': 'Georreferenciado por predio aproximado',
        'Z': 'Ubicado por centroide del centro poblado'
    }

    if code is not None:
        if code in type_status:
            return type_status[code]
    return None
