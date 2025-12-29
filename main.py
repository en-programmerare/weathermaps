#!/usr/bin/env python3

##################################################################################
# OBS! Detta är den automatiska versionen som är tänkt för Github actions!!!!!!! #
##################################################################################

# Version från 2025-12-29.

FILE_NAME_PREFIX = "Weather maps "

TITLE_PREFIX = "Väderkartor "


from datetime import datetime
from datetime import timedelta
from fpdf import FPDF

def main():
    now = datetime.now()
    yesterday = now - timedelta(days=1)
    
    file_name = f"maps/{FILE_NAME_PREFIX}{format_date(now)}.pdf"
    
    pdf = FPDF(orientation = "landscape", unit="mm", format="A4") 
    pdf.set_font("helvetica", size=20)
    
    # Kartor från Wetter3. 1 = 850hPa, 2 = 500 hPa, 3 = 300hPa.
    for i in range(1, 4):
        pdf.add_page()
        url = get_midnight_map_url(now, i)
        try:
            pdf.image(url, x = 51.9, y = 14.8, h = 169.7)
            print(f"Successfully added map number {i}.")
        except Exception as exc:
            print(f"Couldn't download map number {i}. Skipping it. {exc}")
        
    # Satellitbilden
    pdf.add_page()
    url = get_midnight_satellite_url(now)
    try:
        with pdf.rotation(angle=4, x = 53.7, y = 39.3):
            pdf.image(url, x = 53.7, y = 39.3, w = 158.9, h = 123.1)
            print("Successfully added satellite image.")
    except Exception as exc:
        print(f"Couldn't download the satellite image. Skipping it. {exc}")
    
    # Länk till Gervitunglamyndir
    satellite_url = get_interactive_satellite_url(yesterday)
    pdf.cell(text = satellite_url, link = satellite_url)
    
    # Metadata
    title = f"{TITLE_PREFIX}{format_date(now)}"
    pdf.set_title(title)
    pdf.set_creator("Tools for 1ME428 The Structure and Dynamics of Frontal Systems")
    pdf.set_producer("pyFPDF2")
    pdf.set_author(f"Mathias. Wetter3. Veðurstofa Íslands.")
    pdf.output(file_name)
    print(f"File saved as {file_name}.")


# URL till Wetter3-karta för angiven dag och typ.
# Typ:
#   1 - 850 hpa potentiell ekvivalent temperatur, marktryck
#   2 - 500 hpa relativ topografi
#   3 - 300 hpa vind
def get_midnight_map_url(today: datetime, type):
    # 5, 1 och 38 är de siffror som wetter3 använder för de kartor vi vill ha
    type_to_wetter_index_map = {
       1: 5,  # 850 hpa
       2: 1,  # 500 hpa
       3: 38  # 300 hpa
    }
    return f"https://www.wetter3.de/Archiv/GFS/{today.strftime('%Y%m%d00')}_{type_to_wetter_index_map[type]}.gif"

# URL till satellitbilden från midnatt för angiven dag
def get_midnight_satellite_url(today: datetime):
    year = today.strftime("%Y")
    month = today.strftime("%m")
    day = today.strftime("%d")
    return f"https://brunnur.vedur.is/myndir/seviri/{year}/{month}/{day}/seviri_eurnat_ir10-8_{year}{month}{day}_0000.jpg"

# URL till Gervitunglamyndir för angiven dag
def get_interactive_satellite_url(day: datetime):
    year = day.strftime("%Y")
    month = day.strftime("%m")
    day = day.strftime("%d")
    return f"https://brunnur.vedur.is/myndir/seviri/{year}/{month}/{day}/seviri_eurnat_ir10-8.html"

# Snygga datum
def format_date(date: datetime):
    return date.strftime('%Y-%m-%d')
    
if __name__ == "__main__":
    main()
