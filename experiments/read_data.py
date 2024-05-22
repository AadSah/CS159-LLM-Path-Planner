import json

# this fetches the full json object of one game configuration
# mode is train/dev/test/unseen
def get_json(num_goals, mode, idx):
    path = f"data/json_with_symbols/obs-2/{num_goals}_goals/{num_goals}_goals_{mode}_set_samples_with_symbols.json"
    with open(path) as file:
        worlds = json.load(file)
    return worlds[idx]

def get_image_path(num_goals, mode, idx):
    path = f"data/colored_box_pictures/obs-2/{num_goals}_goals/{num_goals}_goals_{mode}_set_samples/{num_goals}_goals_{mode}_set_samples_{idx}.png"
    return worlds[i]

def get_symbolic_description(world):
    return world["symbolic_representation"]

def get_text_description(world):
    return world["nl_description"]