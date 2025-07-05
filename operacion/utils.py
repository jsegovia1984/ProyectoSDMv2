def numero_a_letras(numero):
    """
    Convierte un número flotante (decimal) en su representación en letras en español.
    Soporta números hasta billones y maneja centavos (decimales).
    """
    if numero is None:
        return ""
    
    # Manejo de números negativos (opcional, si los necesitas)
    if numero < 0:
        return "MENOS " + numero_a_letras(abs(numero))

    # Definir las palabras para los números
    unidades = ['', 'UN', 'DOS', 'TRES', 'CUATRO', 'CINCO', 'SEIS', 'SIETE', 'OCHO', 'NUEVE']
    dieces = ['', 'DIEZ', 'VEINTE', 'TREINTA', 'CUARENTA', 'CINCUENTA', 'SESENTA', 'SETENTA', 'OCHENTA', 'NOVENTA']
    diez_a_diecinueve = ['DIEZ', 'ONCE', 'DOCE', 'TRECE', 'CATORCE', 'QUINCE', 'DIECISEIS', 'DIECISIETE', 'DIECIOCHO', 'DIECINUEVE']
    centenas = ['', 'CIEN', 'DOSCIENTOS', 'TRESCIENTOS', 'CUATROCIENTOS', 'QUINIENTOS', 'SEISCIENTOS', 'SETECIENTOS', 'OCHOCIENTOS', 'NOVECIENTOS']

    def _convertir_bloque_cien(n):
        if n == 0:
            return ""
        if n < 10:
            return unidades[n]
        elif n < 20:
            return diez_a_diecinueve[n - 10]
        elif n < 30:
            return "VEINTI" + unidades[n % 10] if n % 10 != 0 else "VEINTE"
        else:
            decena = dieces[n // 10]
            unidad = unidades[n % 10]
            if unidad == "":
                return decena
            return decena + (" Y " if n // 10 < 10 else "") + unidad

    def _convertir_bloque_mil(n, sufijo_singular, sufijo_plural):
        if n == 0:
            return ""
        
        texto = ""
        # Cientos
        c = n // 100
        if c == 1:
            if n % 100 != 0:
                texto += "CIENTO "
            else:
                texto += "CIEN "
        elif c > 1:
            texto += centenas[c] + " "
        
        # Decenas y Unidades
        d_u = n % 100
        texto += _convertir_bloque_cien(d_u)
        
        return texto.strip() + " " + (sufijo_singular if n == 1 else sufijo_plural)

    
    # Separar la parte entera de la parte decimal
    try:
        entero, decimal = str(f"{numero:.2f}").split('.') # Aseguramos 2 decimales para precisión
    except ValueError: # If number is an integer, it won't have a decimal part in split.
        entero = str(int(numero))
        decimal = "00"

    entero_val = int(entero)
    decimal_val = int(decimal)

    if entero_val == 0 and decimal_val == 0:
        return "CERO PESOS CON CERO CENTAVOS"
    
    partes = []

    # Billones
    billones = entero_val // 1_000_000_000_000
    if billones > 0:
        if billones == 1:
            partes.append("UN BILLON")
        else:
            partes.append(_convertir_bloque_mil(billones, "BILLON", "BILLONES")) # Adaptar para billones


    # Millones
    millones = (entero_val % 1_000_000_000_000) // 1_000_000
    if millones > 0:
        if millones == 1:
            partes.append("UN MILLON")
        else:
            partes.append(_convertir_bloque_mil(millones, "MILLON", "MILLONES"))

    # Miles
    miles = (entero_val % 1_000_000) // 1000
    if miles > 0:
        if miles == 1: # "MIL" no "UN MIL"
            partes.append("MIL")
        else:
            partes.append(_convertir_bloque_mil(miles, "MIL", "MIL")) # Adapta el sufijo

    # Cientos (resto)
    resto_cientos = entero_val % 1000
    if resto_cientos > 0:
        texto_resto = ""
        c = resto_cientos // 100
        if c == 1:
            if resto_cientos % 100 != 0:
                texto_resto += "CIENTO "
            else:
                texto_resto += "CIEN "
        elif c > 1:
            texto_resto += centenas[c] + " "
        
        d_u = resto_cientos % 100
        texto_resto += _convertir_bloque_cien(d_u)
        
        partes.append(texto_resto.strip())

    # Unir las partes enteras
    letras_entero = " ".join(filter(None, partes)).strip() # Elimina strings vacíos

    # Si la parte entera es 0 pero los decimales no, ajusta
    if entero_val == 0 and decimal_val > 0:
        letras_entero = "CERO"
    elif entero_val == 1 and len(partes) == 1 and partes[0] == "UN": # Para "UN PESO"
        letras_entero = "UN" # Se convierte a "UN PESO"
    
    # Manejar el final con PESOS/PESO
    if entero_val == 1:
        letras_entero += " PESO"
    elif entero_val > 1:
        letras_entero += " PESOS"
    
    # Manejar los centavos
    letras_decimal = ""
    if decimal_val > 0:
        letras_decimal = f"{decimal_val:02d}" 
    else:
        letras_decimal = "00"
    
    # Combinar todo
    resultado = f"{letras_entero} CON {letras_decimal} CENTAVOS."
    
    # Limpiar espacios extra y capitalizar
    return resultado.replace("  ", " ").strip().upper()

# --- Cómo usarlo en tu modelo de Django ---

# 1. En tu modelo (por ejemplo, en models.py):
#    Podrías añadir un método a tu modelo Contrato para obtener el precio en letras.

# from django.db import models

# class Contrato(models.Model):
#     # ... tus otros campos
#     precio_arrendamiento_inicial = models.FloatField()
#     # ... otros campos

#     def get_precio_arrendamiento_inicial_letras(self):
#         return numero_a_letras(self.precio_arrendamiento_inicial)

# 2. En tu template HTML (`contrato/contrato.html`):
#    Podrías llamarlo directamente así:

# <p>El precio del arrendamiento... en la suma de $ **{{ contrato.precio_arrendamiento_inicial|floatformat:2 }}** (Pesos **{{ contrato.get_precio_arrendamiento_inicial_letras }}**) más iva mensual...</p>