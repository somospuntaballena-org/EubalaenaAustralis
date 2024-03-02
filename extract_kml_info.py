import os
import xml.etree.ElementTree as ET
import requests
from datetime import datetime
import pandas as pd
import subprocess
from tabulate import tabulate

# Create the output directory if it doesn't exist.
output_dir = 'output'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def clear_output_directory(directory='output'):
    # Check if the directory exists.
    if os.path.exists(directory):
        # List all files in the directory and remove each one.
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            # Check if it's a file before attempting to remove it.
            if os.path.isfile(file_path):
                os.remove(file_path)
        print(f"All files in {directory} have been deleted.")
    else:
        print(f"The directory {directory} does not exist.")

def fetch_and_save_kml(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        # Save the KML content to a local file.
        with open(os.path.join(output_dir, save_path), 'wb') as file:
            file.write(response.content)
        print(f"File saved successfully to {save_path}")
    else:
        print("Failed to fetch KML content")

def extract_info_from_network_link_and_save(kml_file_path):
    # Namespace for parsing.
    ns = {'kml': 'http://www.opengis.net/kml/2.2'}
    # Parse the local KML file.
    tree = ET.parse(kml_file_path)
    root = tree.getroot()

    # Find the first NetworkLink element and its href.
    network_link = root.find('.//kml:NetworkLink/kml:Link/kml:href', ns)
    if network_link is not None:
        href = network_link.text
        if href.startswith('<![CDATA[') and href.endswith(']]>'):
            href = href[9:-3]  # Strip CDATA wrapper.

        # Generate save_path with current date and time.
        current_datetime = datetime.now().strftime("%Y_%m_%d_%Hh_%Mm_%Ss")
        save_path = f"{kml_file_path.rsplit('.', 1)[0]}_{current_datetime}.kml"
        
        fetch_and_save_kml(href, save_path)
    else:
        print("No NetworkLink found")
    return save_path

# Function to perform geocoding using Nominatim (OpenStreetMap).
def geocode_coordinates(lat, lon):
    try:
        # Construct request URL
        url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        if response.status_code == 200:
            data = response.json()
            # Extract address from response.
            return data.get('display_name', 'Address not found')
        else:
            return "Error: Failed to fetch address"
    except Exception as e:
        return f"Exception: {e}"

def df_to_html_table(df, file_name):
    html_table = df.to_html(index=False)
    with open(os.path.join(output_dir, file_name), 'w') as f:
        f.write(html_table)
    print(f"HTML table saved to {os.path.join(output_dir, file_name)}")

def markdown_to_pdf(markdown_file, pdf_file, margin='2cm'):
    try:
        subprocess.run([
            'pandoc', 
            os.path.join(output_dir, markdown_file), 
            '-o', os.path.join(output_dir, pdf_file),
            '--pdf-engine=xelatex',
            '-V', f'geometry:margin={margin}'
        ], check=True)
        print(f"PDF generated: {os.path.join(output_dir, pdf_file)}")
    except subprocess.CalledProcessError as e:
        print(f"Error during PDF generation: {e}")

def df_to_markdown(df, file_name):
    markdown_content = df.to_markdown(index=False)
    with open(os.path.join(output_dir, file_name), 'w') as f:
        f.write(markdown_content)
    print(f"Markdown saved to {os.path.join(output_dir, file_name)}")

def extract_info_and_geocode(kml_file_path):
    ns = {'kml': 'http://www.opengis.net/kml/2.2'}
    tree = ET.parse(os.path.join(output_dir, kml_file_path))
    root = tree.getroot()

    data = []
    placemarks = root.findall('.//kml:Placemark', ns)
    for placemark in placemarks:
        name = placemark.find('kml:name', ns).text if placemark.find('kml:name', ns) is not None else ''
        description = placemark.find('kml:description', ns).text if placemark.find('kml:description', ns) is not None else ''
        coord_text = placemark.find('.//kml:coordinates', ns).text if placemark.find('.//kml:coordinates', ns) is not None else ''
        if coord_text:
            print(f"Found coordinates {coord_text} for placemark {placemark}")
            lon, lat, _ = map(float, coord_text.split(','))
            address = geocode_coordinates(lat, lon)
        else:
            address = "Coordinates not found"
        
        data.append({'Nombre': name, 'Dirección': address, 'Notas': description})
  
    df = pd.DataFrame(data)

    # Saving to CSV with the same base name as the KML file
    base_name = kml_file_path.rsplit('.', 1)[0]
    csv_file_path = f"{base_name}.csv"
    df.to_csv(os.path.join(output_dir, csv_file_path), index=False)
    print(f"DataFrame saved to {os.path.join(output_dir, csv_file_path)}")
    
    # Saving to HTML table.
    html_file_path = f"{base_name}.html"
    df_to_html_table(df, html_file_path)
    print(f"HTML table saved to {html_file_path}")

    # Saving to markdown.
    markdown_file_path = f"{base_name}.md"
    df_to_markdown(df, markdown_file_path)
    print(f"Markdown saved to {markdown_file_path}")

    # Saving to PDF.
    pdf_file_path = f"{base_name}.pdf"
    # df_to_pdf(df, pdf_file_path)
    markdown_to_pdf(markdown_file_path, pdf_file_path)
    print(f"PDF saved to {os.path.join(output_dir, pdf_file_path)}")

    return df

# Generate output files.
kml_network_link = 'firmas.kml'
kml_file_path = extract_info_from_network_link_and_save(kml_network_link)
df = extract_info_and_geocode(kml_file_path)
