import json
import sqlite3
import time
import datetime
def record_changes():
    spalten = ["name", "town_uuid", "nation_uuid", "joined_town_at", "is_mayor", "is_king", "discord", "town_ranks", "nation_ranks"]
    try:
        with open("playerstemp.json", "r") as datei:
            data = json.load(datei)
            print(type(data))
            print(type(data[0]) if isinstance(data, list) else data.keys())
            print("Loaded data from file")
    except FileNotFoundError:
        print("Error while loading file")
    try: 
        connection = sqlite3.connect("Player.db")
        cursor = connection.cursor()
        for player in data:
            uuid = player.get('uuid')
            cursor.execute("SELECT * FROM players WHERE uuid == ?;", (uuid,))
            results = cursor.fetchall()
            if not results:
                cursor.execute("""
                    INSERT INTO players (
                        uuid, name, town_uuid, nation_uuid, joined_town_at,
                        is_mayor, is_king, discord, town_ranks, nation_ranks, last_updated
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    player["uuid"],
                    player["name"],
                    player["town"]["uuid"] if player["town"] else None,
                    player["nation"]["uuid"] if player["nation"] else None,
                    player["timestamps"]["joinedTownAt"],
                    player["status"]["isMayor"],
                    player["status"]["isKing"],
                    player["discord"],
                    json.dumps(player["ranks"]["townRanks"]),
                    json.dumps(player["ranks"]["nationRanks"]),
                    int(datetime.datetime.now().timestamp())
                ))

                print("Neuer Player geadded")
                continue
            row = results[0]
            alte_werte = (
                row[1],
                row[2],
                row[3],
                row[4],
                row[5],
                row[6],
                row[7],  
                json.loads(row[8]) if row[8] else [],
                json.loads(row[9]) if row[9] else [],
            )
            neue_werte = (
                player.get("name"),
                player.get("town", {}).get("uuid"),
                player.get("nation", {}).get("uuid"),
                player.get("timestamps", {}).get("joinedTownAt"),
                player.get("status", {}).get("isMayor"),
                player.get("status", {}).get("isKing"),
                player.get("discord"),
                player.get("ranks", {}).get("townRanks", []),
                player.get("ranks", {}).get("nationRanks", []),
                )
            for spalte, alt, neu in zip(spalten, alte_werte, neue_werte):
                if alt != neu:
                    print(f"Änderung in '{spalte}': Alt = {alt} | Neu = {neu}")
                    if spalte in ("town_ranks", "nation_ranks"):
                        old_value = json.dumps(alt)
                        new_value = json.dumps(neu)
                    else:
                        old_value = alt
                        new_value = neu
                    try:
                        snapshot_id = 1 #snapshot system muss noch gemacht werden
                        uuid = row[0]
                        field = f"{spalte}"
                        timestamp = int(datetime.datetime.now().timestamp())
                        cursor.execute(
                            "INSERT INTO player_changes (snapshot_id, uuid, field, old_value, new_value, timestamp) VALUES (?, ?, ?, ?, ?, ?);",
                            (snapshot_id, uuid, field, old_value, new_value, timestamp),
                        )
                        print("Eingefügt in changes")
                        cursor.execute(
                            f"UPDATE players SET {spalte} = ?, last_updated = ? WHERE uuid = ?;",
                            (new_value, timestamp, uuid),
                        )
                    except Exception as e:
                        print(f"Error {e}")
        connection.commit()
        connection.close()
    except ValueError:
        print("Error")