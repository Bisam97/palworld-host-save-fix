import sys
import json
import os
import subprocess
from fix_host_save import sav_to_json


def find_guid_info(level_json, guid):
    guid_formatted = '{}-{}-{}-{}-{}'.format(guid[:8], guid[8:12], guid[12:16], guid[16:20], guid[20:]).lower()
    
    character_save_parameter_map = level_json['properties']['worldSaveData']['value']['CharacterSaveParameterMap']['value']
    player_info = {}
    
    for i in range(len(character_save_parameter_map)):
        candidate_guid_formatted = character_save_parameter_map[i]['key']['PlayerUId']['value']
        save_parameter = character_save_parameter_map[i]['value']['RawData']['value']['object']['SaveParameter']['value']
        
        if 'IsPlayer' in save_parameter and save_parameter['IsPlayer']['value']:
            nickname = save_parameter['NickName']['value']
            level = save_parameter['Level']['value'] if 'Level' in save_parameter else 0
            is_player = True
            player_info[nickname] = {
                'GUID': str(candidate_guid_formatted).replace("-", ""),  
                'NickName': nickname,
                'Level': level,
                'IsPlayer': is_player
            }
    
    return player_info


if len(sys.argv) < 3:
        print('getUUIDs.py <save_path> <temp_path>')
        exit(1)
    
save_path = sys.argv[1]
temp_path = sys.argv[2]    
    
# Verzeichnispfad, in dem sich die GUID-Dateien befinden
directory_path = save_path+"/Players/"

# Laden der Level.sav-Datei
data = sav_to_json(save_path+'/Level.sav')

# Liste von Dateinamen ohne Endung
guids = [os.path.splitext(file)[0] for file in os.listdir(directory_path)]

# Iteriere über jede GUID und erhalte die Spielerinformationen
for guid in guids:
    player_info = find_guid_info(data, guid)
    for nickname, info in player_info.items():
        print(f"Found Player {nickname}")
        # Verwende eine eindeutige Dateinamenkonvention, um Konflikte zu vermeiden
        file_name = f"{temp_path}/{nickname}.json"
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(info, f)