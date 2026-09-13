import requests
import time
import json
baseurl = "https://api.earthmc.net/v4/"
def playerssave():
  url = f"{baseurl}players"

  try:
    response = requests.get(url)
    if response.status_code != 200:
      print(f"Fehler beim Laden: {response.status_code}")
      return

    data = response.json()  
    all_names = []
    for player in data:
      if player.get("status", {}).get("isNPC", False):
        continue
      else:
        all_names.append(player["name"])

    tempdata = []
    chunk_size = 100
    counter2 = 0
    for i in range(0, len(all_names), chunk_size):
        chunk = all_names[i : i + chunk_size]
        body = {
          "query": chunk,
          "template": {
              "name": True,
              "uuid": True,
              "town": True,
              "nation": True,
              "timestamps": True,
              "status": True,
              "stats": True,
              "ranks": True,
              "friends": True,
              "discord": True,
          },
        }
        while True:
            finaldata = requests.post(url, json=body)

            if finaldata.status_code == 200:
                detailed_data = finaldata.json()
                tempdata.extend(detailed_data)
                counter2 += 1
                print(f"Chunk {counter2} wurde erfolgreich geladen.")
                time.sleep(0.4)
                break
            elif finaldata.status_code == 429:
                retry_after = finaldata.headers.get("Retry-After")

                if retry_after:
                    wait_time = float(retry_after)
                else:
                    wait_time = 5

                print(f"429! Warte {wait_time} Sekunden...")
                time.sleep(wait_time)
            else:
                print(f"Fehler beim POST-Request: {finaldata.status_code}")
                break
    print(f"Fetched around {counter2 * chunk_size}")
    with open("playerstemp.json", "w", encoding="utf-8") as datei:
      json.dump(tempdata, datei, indent=4)
    print("Erfolgreich in playerstemp.json gespeichert!")

  except Exception as e:
    print(f"Ein Fehler ist aufgetreten: {e}")
