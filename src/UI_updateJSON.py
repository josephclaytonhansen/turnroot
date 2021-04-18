import json
def updateJSON():
    with open("src/tmp/preferences.json", "r") as read_file:
        read_file.seek(0)
        data = json.load(read_file)
        font_size = data["font_size"]
        icon_size = data["icon_size"]
        rfont_size = data["rfont_size"]
        active_theme = data["active_theme"]
        active_layout = data["active_layout"]
        ah_rte = ["ah_rte"]
        ah_tasks = data["ah_tasks"]
        ah_taskss = data["ah_taskss"]
        ah_overlays = data["ah_overlays"]

        read_file.close()
        return data

def dumpJSON(data):
        with open("src/tmp/preferences.json", "w") as write_file:
            json.dump(data, write_file)
            write_file.close()