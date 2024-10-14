import json
import ollama
import sys

def translate_json(input_file, output_file, target_language):
    print(f"Iniciando traducción de {input_file} a {output_file} en {target_language}")
    
    try:
        # Cargar el JSON de entrada
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"Archivo JSON de entrada cargado correctamente: {input_file}")
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo de entrada: {input_file}")
        return
    except json.JSONDecodeError:
        print(f"Error: El archivo de entrada no es un JSON válido: {input_file}")
        return
    
    # Función para traducir un valor
    def translate_value(value):
        prompt = f"Translate the following text from English to {target_language}: {value}"
        try:
            response = ollama.generate(model='thinkverse/towerinstruct', prompt=prompt)
            translated = response['response'].strip()
            print(f"Traducido: '{value}' -> '{translated}'")
            return translated
        except Exception as e:
            print(f"Error al traducir '{value}': {str(e)}")
            return value
    
    # Traducir recursivamente los valores del JSON
    def translate_dict(d):
        new_dict = {}
        for k, v in d.items():
            if isinstance(v, dict):
                new_dict[k] = translate_dict(v)
            elif isinstance(v, str):
                new_dict[k] = translate_value(v)
            else:
                new_dict[k] = v
        return new_dict
    
    # Traducir el JSON completo
    print("Iniciando traducción del JSON...")
    translated_data = translate_dict(data)
    print("Traducción del JSON completada.")
    
    # Guardar el JSON traducido
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(translated_data, f, ensure_ascii=False, indent=2)
        print(f"Archivo JSON traducido guardado correctamente: {output_file}")
    except Exception as e:
        print(f"Error al guardar el archivo de salida {output_file}: {str(e)}")

if __name__ == "__main__":
    input_file = './inputs/en.json'
    output_file = './outputs/es.json'
    target_language = 'Spanish'  # Cambia esto al idioma deseado

    print("Iniciando script de traducción...")
    translate_json(input_file, output_file, target_language)
    print("Script de traducción finalizado.")