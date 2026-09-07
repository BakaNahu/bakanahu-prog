import requests
import random

API_URL = "https://digi-api.com/api/v1/digimon/"

def get_random_digimons():
    digimons = []
    intentos = 0
    while len(digimons) < 3 and intentos < 20:
        intentos += 1
        d_id = random.randint(1, 1000)
        try:
            response = requests.get(f"{API_URL}{d_id}")
            if response.status_code == 200:
                data = response.json()
                
                name = data.get('name', 'Desconocido')
                img = data['images'][0]['href'] if data.get('images') else ''
                levels = data.get('levels', [{'level': '???'}])
                level = levels[0]['level'] if levels else '???'
                types = data.get('types', [{'type': '???'}])
                type_name = types[0]['type'] if types else '???'
                attributes = data.get('attributes', [{'attribute': '???'}])
                attribute = attributes[0]['attribute'] if attributes else '???'

                digimons.append({
                    "name": name,
                    "img": img,
                    "level": level,
                    "type": type_name,
                    "attribute": attribute
                })
        except Exception as e:
            pass
            
    return digimons

def generate_html(digimons):
    html = '\n<table align="center">\n  <tr>\n'
    for d in digimons:
        html += f'''    <td align="center" width="160" style="border: 2px solid #ff7b00; background-color: #fff4e6; border-radius: 10px; padding: 10px;">
      <img src="{d['img']}" width="90" alt="{d['name']}"><br>
      <h3 style="color: #cc6200; margin: 8px 0;">{d['name']}</h3>
      <sub><b>Nivel:</b> {d['level']}</sub><br>
      <sub><b>Tipo:</b> {d['type']}</sub><br>
      <sub><b>Atributo:</b> {d['attribute']}</sub>
    </td>\n'''
    html += '  </tr>\n</table>\n'
    return html

def update_readme(new_content):
    with open('README.md', 'r', encoding='utf-8') as file:
        readme = file.read()

    # Etiquetas exactas
    start_marker = ""
    end_marker = ""

    # Partición exacta a prueba de fallos
    if start_marker in readme and end_marker in readme:
        top_part = readme.split(start_marker)[0]
        bottom_part = readme.split(end_marker)[1]
        
        updated_readme = top_part + start_marker + new_content + end_marker + bottom_part
        
        with open('README.md', 'w', encoding='utf-8') as file:
            file.write(updated_readme)
        print("¡README.md actualizado con éxito!")
    else:
        print("No se encontraron las etiquetas en el README.md. No se hicieron cambios.")

if __name__ == "__main__":
    print("Buscando Digimons...")
    digi_data = get_random_digimons()
    
    if len(digi_data) == 3:
        print("¡Se encontraron 3 Digimons! Actualizando README...")
        html_table = generate_html(digi_data)
        update_readme(html_table)
    else:
        print(f"Error: La API falló y solo trajo {len(digi_data)} Digimons.")
