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

    start_marker = "<!-- DIGIMON_TEAM_START -->"
    end_marker = "<!-- DIGIMON_TEAM_END -->"

    # Buscamos la posición exacta de las etiquetas
    start_idx = readme.find(start_marker)
    end_idx = readme.find(end_marker)

    if start_idx != -1 and end_idx != -1:
        # Movemos el cursor justo después de la etiqueta de inicio
        start_idx += len(start_marker)
        
        # Cortamos y pegamos el texto usando las posiciones
        top_part = readme[:start_idx]
        bottom_part = readme[end_idx:]
        
        updated_readme = top_part + new_content + bottom_part
        
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
