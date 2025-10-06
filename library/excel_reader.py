
import os
import openpyxl

def read_excel(ruta_relativa_excel, nombre_hoja):
    """
    Lee un archivo Excel y devuelve una lista de diccionarios,
    donde cada diccionario representa una fila, usando la primera fila como header.
    """
    mydata = []

    try:
        # Ajusta la ruta según tu proyecto
        ruta = os.path.join(os.getcwd(), "resources", ruta_relativa_excel)
        if not os.path.exists(ruta):
            raise Exception(f"El archivo {ruta_relativa_excel} no existe!")

        workbook = openpyxl.load_workbook(ruta)
        sheet = workbook[nombre_hoja]

        header_row = sheet[1]  # primera fila como headers

        # Iterar todas las filas a partir de la 2
        for row in sheet.iter_rows(min_row=2, values_only=True):
            current_hash = {}
            for idx, cell in enumerate(row):
                header_cell_value = header_row[idx].value if header_row[idx].value else ""
                cell_value = str(cell) if cell else ""
                current_hash[header_cell_value.strip()] = cell_value.strip()
            mydata.append(current_hash)

    except Exception as e:
        print(f"[ERROR] No se pudo leer el archivo excel: {e}")
        raise e

    return mydata
