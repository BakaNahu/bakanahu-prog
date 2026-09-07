import requests
import random
import re

API_URL = "https://digi-api.com/api/v1/digimon/"

def get_random_digimons():
    digimons = []
    # Buscamos 3 IDs al azar
    ids = random.sample(range(1, 1000), 3)
    
    for d_id in ids:
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
            print(f"Error buscando el ID {d_id}: {e}")
            
    return digimons

def generate_html(digimons):
    # Armamos la tabla horizontal con cajas de colores para cada Digimon
    html = '<table align="center">\n  <tr>\n'
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

    # Patrón actualizado con los comentarios exactos de tu README
    pattern = r'(\n).*?(\n)'
    # Usamos re.sub para reemplazar lo que haya en el medio
    updated_readme = re.sub(pattern, r'\g<1>' + new_content + r'\g<2>', readme, flags=re.DOTALL)

    with open('README.md', 'w', encoding='utf-8') as file:
        file.write(updated_readme)

if __name__ == "__main__":
    digi_data = get_random_digimons()
    if len(digi_data) == 3:
        html_table = generate_html(digi_data)
        update_readme(html_table)
        print("¡README.md actualizado con éxito con los Digimons!")
    else:
        print("Hubo un problema trayendo la información de la API.")
