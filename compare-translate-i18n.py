import json
import ollama
import sys

def update_and_translate_json(input_file, existing_output_file, new_output_file, target_language):
    print(f"Iniciando actualización y traducción de {input_file} usando {existing_output_file}")
    
    try:
        # Cargar el JSON de entrada
        with open(input_file, 'r', encoding='utf-8') as f:
            input_data = json.load(f)
        print(f"Archivo JSON de entrada cargado correctamente: {input_file}")
        
        # Cargar el JSON de salida existente
        with open(existing_output_file, 'r', encoding='utf-8') as f:
            existing_output_data = json.load(f)
        print(f"Archivo JSON de salida existente cargado correctamente: {existing_output_file}")
    except FileNotFoundError as e:
        print(f"Error: No se pudo encontrar el archivo: {str(e)}")
        return
    except json.JSONDecodeError as e:
        print(f"Error: Uno de los archivos no es un JSON válido: {str(e)}")
        return
    
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
    
    def update_and_translate_dict(input_dict, existing_dict):
        updated_dict = {}
        for key, value in input_dict.items():
            if isinstance(value, dict):
                if key in existing_dict and isinstance(existing_dict[key], dict):
                    updated_dict[key] = update_and_translate_dict(value, existing_dict[key])
                else:
                    updated_dict[key] = update_and_translate_dict(value, {})
            else:
                if key in existing_dict:
                    updated_dict[key] = existing_dict[key]
                    print(f"Manteniendo valor existente para '{key}': '{existing_dict[key]}'")
                else:
                    updated_dict[key] = translate_value(value)
        return updated_dict
    
    print("Iniciando actualización y traducción del JSON...")
    updated_data = update_and_translate_dict(input_data, existing_output_data)
    print("Actualización y traducción del JSON completada.")
    
    # Guardar el JSON actualizado y traducido
    try:
        with open(new_output_file, 'w', encoding='utf-8') as f:
            json.dump(updated_data, f, ensure_ascii=False, indent=2)
        print(f"Archivo JSON actualizado y traducido guardado correctamente: {new_output_file}")
    except Exception as e:
        print(f"Error al guardar el archivo de salida {new_output_file}: {str(e)}")

if __name__ == "__main__":
    input_file = './inputs/en.json'
    existing_output_file = './preOutput/nl.json'
    new_output_file = './outputs/nl.json'
    target_language = 'Dutch'  # Cambia esto al idioma deseado

    print("Iniciando script de actualización y traducción...")
    update_and_translate_json(input_file, existing_output_file, new_output_file, target_language)
    print("Script de actualización y traducción finalizado.")