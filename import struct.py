import struct
import numpy as np
import csv  # Importamos el módulo csv

# https://github.com/flybywiresim/fdr-analysis


def decode_arinc717(file_path, output_csv_path):  # Añadimos output_csv_path para la ruta del CSV
    with open(file_path, 'rb') as f:
        data = f.read()
    
    words = []
    sync_word = 0x3F2  # Palabra de sincronización típica
    
    # Leer palabras de 12 bits
    for i in range(0, len(data), 2):  # 2 bytes = 16 bits (12 útiles)
        chunk = data[i:i+2]
        if not chunk:
            break
        
        # Convertir a entero (little-endian o big-endian según el FDR)
        value = struct.unpack('<H', chunk)[0]  # '<H' = unsigned short (16 bits)
        word = value & 0x0FFF  # Máscara para 12 bits
        
        if word == sync_word:
            print(f"¡Sync encontrado en posición {i}!")
        
        words.append(word)
    
    # Guardar los datos en un archivo CSV
    with open(output_csv_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Palabra ARINC 717"])  # Escribimos los encabezados de las columnas
        for word in words:
            writer.writerow([word])  # Escribimos cada palabra en una nueva fila
    
    print(f"Datos guardados en {output_csv_path}")
    return words

# Ejemplo de uso
file_path = "C:/Users/SAID/Desktop/ARIN 717/1.DLU"  # Ruta al archivo de entrada
output_csv_path = "C:/Users/SAID/Desktop/ARIN 717/decoded_words.csv"  # Ruta al archivo de salida CSV
decoded_words = decode_arinc717(file_path, output_csv_path)
print(f"Se decodificaron {len(decoded_words)} palabras ARINC 717.")
