import os
import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def process_json_file(json_file_path, output_base_dir):
    # Load the JSON file
    with open(json_file_path) as f:
        data = json.load(f)
    
    worlds = []
    for inst in data:
        worlds.append(inst['world'])
    
    for idx, world in enumerate(worlds):
        size = len(world)

        # Create a figure and axis with equal aspect ratio
        fig, ax = plt.subplots()
        ax.set_aspect('equal')

        # Set the size of the grid
        ax.set_xlim(0, size)
        ax.set_ylim(0, size)

        # Draw the grid
        for i in range(size):
            for j in range(size):
                if world[i][j] == 0:
                    # Empty cell
                    rect = patches.Rectangle((j, size-i-1), 1, 1, linewidth=1, edgecolor='black', facecolor='white')
                elif world[i][j] == 1:
                    # Obstacle
                    rect = patches.Rectangle((j, size-i-1), 1, 1, linewidth=1, edgecolor='black', facecolor='gray')
                elif world[i][j] == 2:
                    # Robot
                    rect = patches.Rectangle((j, size-i-1), 1, 1, linewidth=1, edgecolor='black', facecolor='blue')
                elif world[i][j] == 3:
                    # Target
                    rect = patches.Rectangle((j, size-i-1), 1, 1, linewidth=1, edgecolor='black', facecolor='red')
                ax.add_patch(rect)

        # Set grid lines
        ax.set_xticks([x for x in range(size+1)])
        ax.set_yticks([y for y in range(size+1)])
        ax.grid(which='both', color='black', linestyle='-', linewidth=1)

        # Hide the axes
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.tick_params(left=False, bottom=False, labelleft=False, labelbottom=False)

        # Create the output directory structure
        relative_path = os.path.relpath(json_file_path, start=base_dir)
        output_dir = os.path.join(output_base_dir, os.path.dirname(relative_path), f"{os.path.splitext(os.path.basename(json_file_path))[0]}")
        os.makedirs(output_dir, exist_ok=True)

        # Save the figure with indexing
        output_file_path = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(json_file_path))[0]}_{idx+1}.png")
        print(f"Saving {output_file_path}")
        plt.savefig(output_file_path, bbox_inches='tight', pad_inches=0)
        plt.close(fig)

def process_directory(base_dir, output_base_dir):
    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith('_samples.json'):
                # print(f"Processing {os.path.join(root, file)}")
                json_file_path = os.path.join(root, file)
                process_json_file(json_file_path, output_base_dir)

# Define the base directory containing JSON files and the output directory
base_dir = './envs/'
output_base_dir = './colored_box_pictures/'

# Process the directory
process_directory(base_dir, output_base_dir)
