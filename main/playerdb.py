import sqlite3
import json
import datetime
def startuptable():
    connection = sqlite3.connect("Player.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS players (
            uuid TEXT PRIMARY KEY,
            name TEXT,
            town_uuid TEXT,
            nation_uuid TEXT,
            joined_town_at INTEGER,
            is_mayor INTEGER,
            is_king INTEGER,
            discord TEXT,
            town_ranks TEXT,
            nation_ranks TEXT,
            last_updated INTEGER
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS player_changes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            snapshot_id INTEGER,
            uuid TEXT,
            field TEXT,
            old_value TEXT,
            new_value TEXT,
            timestamp INTEGER
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS snapshots (
            id INTEGER PRIMARY KEY,
            timestamp INTEGER,
            type TEXT
        );
    """)
    connection.commit()
    connection.close()
    print("Created tables or checked them")

def startupinsert():
    try:
        with open("playerstemp.json", "r") as datei:
            data = json.load(datei)
            print(type(data))
            print(type(data[0]) if isinstance(data, list) else data.keys())
            print("Loaded data from file")
            print("Anzahl Listen:", len(data))
            for i, batch in enumerate(data[:10]):
                print(i, len(batch))
    except FileNotFoundError:
        print("Keine Datei gefunden")
        return
    connection = sqlite3.connect("Player.db")
    cursor = connection.cursor()
    for player in data:
        uuid = player['uuid']
        name = player['name']
        town_uuid = player["town"]["uuid"] if player["town"] else None
        nation_uuid = player['nation']['uuid'] if player["nation"] else None
        joined_town_at = player['timestamps']['joinedTownAt']
        is_mayor = player['status']['isMayor']
        is_king = player['status']['isKing']
        discord = player['discord']
        town_ranks = json.dumps(player['ranks']['townRanks'])
        nation_ranks = json.dumps(player['ranks']['nationRanks'])
        last_updated = int(datetime.datetime.now().timestamp())
        cursor.execute("""
            INSERT INTO players (
                uuid, name, town_uuid, nation_uuid, joined_town_at,
                is_mayor, is_king, discord, town_ranks, nation_ranks, last_updated
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(uuid) DO UPDATE SET
                name = excluded.name,
                town_uuid = excluded.town_uuid,
                nation_uuid = excluded.nation_uuid,
                joined_town_at = excluded.joined_town_at,
                is_mayor = excluded.is_mayor,
                is_king = excluded.is_king,
                discord = excluded.discord,
                town_ranks = excluded.town_ranks,
                nation_ranks = excluded.nation_ranks,
                last_updated = excluded.last_updated
        """, (
            uuid,
            name,
            town_uuid,
            nation_uuid,
            joined_town_at,
            is_mayor,
            is_king,
            discord,
            town_ranks,
            nation_ranks,
            last_updated
        ))
    connection.commit()
    connection.close()
    print("Finished Startup")
def add_player(uuid, name, town_uuid, nation_uuid, joined_town_at, is_mayor, is_king, discord, town_ranks, nation_ranks, last_updated):
    connection = sqlite3.connect("Player.db")
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO players (uuid, name, town_uuid, nation_uuid, joined_town_at, is_mayor, is_king, discord, town_ranks, nation_ranks, last_updated) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
        (uuid, name, town_uuid, nation_uuid, joined_town_at, is_mayor, is_king, discord, town_ranks, nation_ranks, last_updated,)
    )
    print("Neuer Player geadded")
