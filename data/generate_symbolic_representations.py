import os
import json

def process_json_file(json_file_path, output_base_dir):
    # Load the JSON file
    with open(json_file_path) as f:
        data = json.load(f)
    
    for inst in data:
        world = inst['world']
        size = len(world)

        # Create a string representation of the grid
        symbolic_representation = ""
        for i in range(size):
            symbolic_representation += "| "  # Leftmost separator
            for j in range(size):
                if world[i][j] == 0:
                    # Empty cell
                    symbolic_representation += " "
                elif world[i][j] == 1:
                    # Obstacle
                    symbolic_representation += "X"
                elif world[i][j] == 2:
                    # Robot
                    symbolic_representation += "#"
                elif world[i][j] == 3:
                    # Target
                    symbolic_representation += "$"
                # Add separator between columns
                if j < size - 1:
                    symbolic_representation += " | "
            symbolic_representation += " |"  # Rightmost separator
            # Add newline between rows
            if i < size - 1:
                symbolic_representation += "\n"
        
        # Add the symbolic representation to the JSON entry
        inst['symbolic_representation'] = symbolic_representation

    # Create the output directory structure
    relative_path = os.path.relpath(json_file_path, start=base_dir)
    output_dir = os.path.join(output_base_dir, os.path.dirname(relative_path))
    os.makedirs(output_dir, exist_ok=True)

    # Save the modified JSON to a new file
    output_file_path = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(json_file_path))[0]}_with_symbols.json")
    print(f"Saving {output_file_path}")
    with open(output_file_path, 'w') as f:
        json.dump(data, f, indent=4)

def process_directory(base_dir, output_base_dir):
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith('_samples.json'):
                json_file_path = os.path.join(root, file)
                process_json_file(json_file_path, output_base_dir)

# Define the base directory containing JSON files and the output directory
base_dir = './envs/'
output_base_dir = './json_with_symbols/'

# Process the directory
process_directory(base_dir, output_base_dir)
