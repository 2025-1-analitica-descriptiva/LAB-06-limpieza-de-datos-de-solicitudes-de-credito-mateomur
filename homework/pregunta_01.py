"""
Escriba el código que ejecute la acción solicitada en la pregunta.
"""

def pregunta_01():
    """
    Realiza la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    Aplica transformación y depuración de datos según lo requerido,
    y guarda el archivo limpio en "files/output/solicitudes_de_credito.csv".
    """

    import pandas as pd
    import os
    
    # Cargar los datos y eliminar filas con valores faltantes
    datos = pd.read_csv("files/input/solicitudes_de_credito.csv", sep=";").dropna()

    # Estandarización de columnas específicas
    datos["sexo"] = datos["sexo"].str.lower()
    datos["tipo_de_emprendimiento"] = datos["tipo_de_emprendimiento"].str.lower()

    datos["idea_negocio"] = (
        datos["idea_negocio"]
        .str.lower()
        .str.replace("_", " ", regex=False)
        .str.replace("-", " ", regex=False)
        .str.strip()
    )

    datos["barrio"] = (
        datos["barrio"]
        .str.lower()
        .str.replace("_", " ", regex=False)
        .str.replace("-", " ", regex=False)
    )

    # Normalización de fechas: convierte YYYY/MM/DD → DD/MM/YYYY
    def formatear_fecha(fecha):
        return f"{fecha[8:10]}/{fecha[5:7]}/{fecha[0:4]}" if fecha[0:4].isdigit() else fecha


    datos["fecha_de_beneficio"] = datos["fecha_de_beneficio"].apply(formatear_fecha)

    # Limpieza y conversión del monto del crédito
    datos["monto_del_credito"] = (
        datos["monto_del_credito"]
        .str.replace(" ", "", regex=False)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .astype(float)
    )

    # Estandarización de línea de crédito
    datos["línea_credito"] = (
        datos["línea_credito"]
        .str.lower()
        .str.replace("_", " ", regex=False)
        .str.replace("-", " ", regex=False)
    )

    # Eliminación de duplicados basados en columnas clave
    datos_limpios = datos.drop_duplicates(subset=[
        "sexo",
        "tipo_de_emprendimiento",
        "idea_negocio",
        "barrio",
        "estrato",
        "comuna_ciudadano",
        "fecha_de_beneficio",
        "monto_del_credito",
        "línea_credito",
    ])

    os.makedirs(os.path.dirname("files/output/solicitudes_de_credito.csv"), exist_ok=True)
    datos_limpios.to_csv("files/output/solicitudes_de_credito.csv", sep=";", index=False)

if __name__ == "__main__":
    pregunta_01()