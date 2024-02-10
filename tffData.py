import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.tff.org/default.aspx?pageID=198"

response = requests.get(url)
data = {"DateTime": [], "Home Team": [], "Score": [], "Away Team": []}
if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")

    # Çekmek istediğiniz tablonun id'sini belirleyin.
    hedef_tablo_id = "ctl00_MPane_m_198_12491_ctnr_m_198_12491_dtlHaftaninMaclari"

    # Hedef tabloyu bulmak için id kullanın.
    hedef_tablo = soup.find("table", {"id": hedef_tablo_id})

    if hedef_tablo:
        print(f"\nTable found - ID: {hedef_tablo_id}\n")

        # Tablonun içeriğini bulalım.
        rows = hedef_tablo.find_all("tr")

        for row in rows:
            cells = row.find_all(["th", "td"])
            row_data = [cell.text.strip() for cell in cells]
            
            # Gereksiz boş liste elemanlarını temizleyelim.
            row_data = [item for item in row_data if item]

            if len(row_data) == 5:  # Eğer detaylar mevcutsa
                print("\nDate:", row_data[0])
            
                print("Home Team:", row_data[1])
           
                score_parts = row_data[2].strip().replace('\r', '').replace('\n', '').split("-")  # Score'yu "-" karakterine göre ayıralım
                score = "-".join(part.strip() for part in score_parts) 
                print("Score:", score)
                print("Away Team:", row_data[3])
                data["DateTime"].append(row_data[0])
                data["Home Team"].append(row_data[1])
                data["Score"].append(score)
                data["Away Team"].append(row_data[3])
       
   

    else:
        print(f"{hedef_tablo_id} bulunamadı.")
else:
    print(f"Hata: {response.status_code}")


# DataFrame oluşturalım
df = pd.DataFrame(data)

# Excel dosyasına yazalım
df.to_excel("output.xlsx", index=False)