import pandas as pd
import numpy as np
import os

def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"
    """
    
    # Crear directorio de salida si no existe
    os.makedirs("files/output", exist_ok=True)
    
    # Leer el archivo CSV con parámetros específicos para evitar problemas de inferencia
    df = pd.read_csv("files/input/solicitudes_de_credito.csv", 
                     sep=";", 
                     dtype=str,  # Leer todo como string inicialmente
                     na_values=['', 'nan', 'NaN', 'null', 'NULL', 'None'],
                     keep_default_na=True)
    
    print(f"Registros iniciales: {len(df)}")
    print(f"Columnas encontradas: {list(df.columns)}")
    
    # 1. LIMPIEZA INICIAL DE ESPACIOS Y VALORES VACÍOS
    # Limpiar espacios en blanco en todas las columnas
    for col in df.columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
            # Reemplazar 'nan' string y cadenas vacías con NaN real
            df[col] = df[col].replace(['nan', '', 'None', 'null', 'NULL'], np.nan)
    
    # 2. NORMALIZACIÓN DE CAMPOS CATEGÓRICOS
    
    # Normalizar sexo
    if 'sexo' in df.columns:
        df['sexo'] = df['sexo'].str.lower()
    
    # Normalizar tipo_de_emprendimiento  
    if 'tipo_de_emprendimiento' in df.columns:
        df['tipo_de_emprendimiento'] = df['tipo_de_emprendimiento'].str.lower()
    
    # Normalizar idea_negocio
    if 'idea_negocio' in df.columns:
        df['idea_negocio'] = df['idea_negocio'].str.lower()
    
    # Normalizar barrio
    if 'barrio' in df.columns:
        df['barrio'] = df['barrio'].str.lower()
    
    # Normalizar comuna_ciudadano
    if 'comuna_ciudadano' in df.columns:
        df['comuna_ciudadano'] = df['comuna_ciudadano'].str.lower()
    
    # Normalizar linea_credito si existe
    if 'linea_credito' in df.columns:
        df['linea_credito'] = df['linea_credito'].str.lower()
    
    # 3. CONVERSIÓN DE TIPOS DE DATOS NUMÉRICOS
    
    # Convertir monto_del_credito a numérico
    if 'monto_del_credito' in df.columns:
        # Limpiar el campo primero
        df['monto_del_credito'] = df['monto_del_credito'].str.replace(',', '', regex=False)
        df['monto_del_credito'] = df['monto_del_credito'].str.replace('$', '', regex=False)
        df['monto_del_credito'] = df['monto_del_credito'].str.replace(' ', '', regex=False)
        df['monto_del_credito'] = pd.to_numeric(df['monto_del_credito'], errors='coerce')
    
    # Convertir estrato a numérico
    if 'estrato' in df.columns:
        df['estrato'] = pd.to_numeric(df['estrato'], errors='coerce')
    
    # 4. CONVERSIÓN DE FECHAS
    if 'fecha_de_beneficio' in df.columns:
        df['fecha_de_beneficio'] = pd.to_datetime(df['fecha_de_beneficio'], 
                                                errors='coerce', 
                                                dayfirst=True,
                                                format=None)
    
    # 5. ELIMINAR FILAS COMPLETAMENTE VACÍAS
    df = df.dropna(how='all')
    print(f"Después de eliminar filas vacías: {len(df)}")
    
    # 6. ELIMINAR DUPLICADOS PRIMERO (más conservador)
    print(f"Antes de eliminar duplicados: {len(df)}")
    
    # Eliminar solo duplicados exactos (todas las columnas iguales)
    df = df.drop_duplicates()
    print(f"Después de eliminar duplicados exactos: {len(df)}")
    
    # 7. FILTROS DE VALIDACIÓN MÁS SELECTIVOS
    
    # Solo eliminar registros que definitivamente son inválidos
    
    # Eliminar solo si monto es 0, negativo o NaN
    if 'monto_del_credito' in df.columns:
        antes_monto = len(df)
        df = df[~((df['monto_del_credito'].isna()) | (df['monto_del_credito'] <= 0))]
        print(f"Registros eliminados por monto inválido: {antes_monto - len(df)}")
    
    # Eliminar solo si estrato está fuera del rango válido o es NaN
    if 'estrato' in df.columns:
        antes_estrato = len(df)
        df = df[~((df['estrato'].isna()) | (df['estrato'] < 1) | (df['estrato'] > 6))]
        print(f"Registros eliminados por estrato inválido: {antes_estrato - len(df)}")
    
    # Eliminar solo registros donde campos críticos específicos están vacíos
    # Solo sexo, tipo_de_emprendimiento, idea_negocio (los más importantes para el negocio)
    campos_muy_criticos = []
    for campo in ['sexo', 'tipo_de_emprendimiento', 'idea_negocio']:
        if campo in df.columns:
            campos_muy_criticos.append(campo)
    
    if campos_muy_criticos:
        antes_criticos = len(df)
        df = df.dropna(subset=campos_muy_criticos)
        print(f"Registros eliminados por campos muy críticos faltantes: {antes_criticos - len(df)}")
    
    # 8. ORDENAMIENTO FINAL
    if 'fecha_de_beneficio' in df.columns:
        df = df.sort_values('fecha_de_beneficio', na_position='last')
    
    # Resetear índice
    df = df.reset_index(drop=True)
    
    # 9. VERIFICACIÓN FINAL
    print(f"\n=== RESULTADO FINAL ===")
    print(f"Registros finales: {len(df)}")
    
    # Mostrar conteos para verificación con los tests
    if 'sexo' in df.columns:
        sexo_counts = df['sexo'].value_counts().to_list()
        print(f"Conteos sexo: {sexo_counts}")
        
    if 'tipo_de_emprendimiento' in df.columns:
        tipo_counts = df['tipo_de_emprendimiento'].value_counts().to_list()
        print(f"Conteos tipo_emprendimiento: {tipo_counts}")
    
    # 10. GUARDAR ARCHIVO LIMPIO
    df.to_csv("files/output/solicitudes_de_credito.csv", 
              sep=";", 
              index=False, 
              encoding='utf-8',
              na_rep='')
    
    print(f"✅ Archivo guardado exitosamente en: files/output/solicitudes_de_credito.csv")
    
    return df

# Ejecutar la función si el script se ejecuta directamente
if __name__ == "__main__":
    df_limpio = pregunta_01()