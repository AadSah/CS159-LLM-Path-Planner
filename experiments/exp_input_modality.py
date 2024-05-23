from read_data import *
from llm import *
import time

text_fewshot_prompt = """
Provide a sequence of actions to navigate a world to reach a goal similarly to the examples below. (0,0) is located in the upper-left corner and (M, N) lies in the M row and N column.
###
Task: You are in a 6 by 6 world. There are obstacles that you have to avoid at: (3,3) and (3,0). Go from (2,0) to (1,5)
Actions: up right right right right right
###
Task: You are in a 6 by 6 world. There are obstacles that you have to avoid at: (3,3) and (3,0). Go from (2,1) to (3,5)
Actions: right right right right down 
###
Task: You are in a 6 by 6 world. There are obstacles that you have to avoid at: (3,3) and (3,0). Go from (4,3) to (5,3)
Actions: down 
###
Task: You are in a 6 by 6 world. There are obstacles that you have to avoid at: (3,3) and (3,0). Go from (2,4) to (1,0)
Actions: up left left left left
###
Task: You are in a 6 by 6 world. There are obstacles that you have to avoid at: (3,3) and (3,0). Go from (3,1) to (2,2)
Actions: up right
###
Task:
"""

symbolic_fewshot_prompt = """
Provide a sequence of actions to navigate a world to reach a goal similarly to the examples below. X means obstacles, $ is the goal,
ans # is the starting location.
###
Task: |   |   |   |   |   |   |\n|   |   |   |   |   | $ |\n| # |   |   |   |   |   |\n| X |   |   | X |   |   |\n|   |   |   |   |   |   |\n|   |   |   |   |   |   |
Actions: up right right right right right
###
Task: |   |   |   |   |   |   |\n|   |   |   |   |   |   |\n|   | # |   |   |   |   |\n| X |   |   | X |   | $ |\n|   |   |   |   |   |   |\n|   |   |   |   |   |   |
Actions: right right right right down 
###
Task: |   |   |   |   |   |   |\n|   |   |   |   |   |   |\n|   |   |   |   |   |   |\n| X |   |   | X |   |   |\n|   |   |   | # |   |   |\n|   |   |   | $ |   |   |
Actions: down 
###
Task: |   |   |   |   |   |   |\n| $ |   |   |   |   |   |\n|   |   |   |   | # |   |\n| X |   |   | X |   |   |\n|   |   |   |   |   |   |\n|   |   |   |   |   |   |
Actions: up left left left left
###
Task: |   |   |   |   |   |   |\n|   |   |   |   |   |   |\n|   |   | $ |   |   |   |\n| X | # |   | X |   |   |\n|   |   |   |   |   |   |\n|   |   |   |   |   |   |
Actions: up right
###
Task:
"""

image_fewshot_prompt_texts = [
    """
    Provide a sequence of actions to navigate a world to reach a goal similarly to the examples below. The red squares are goals, grey squares
    are the obstacles, and blue square is the starting point.
    ###
    Task:
    """,
    """
    Actions: up right right right right right
    ###
    Task:
    """,
    """
    Actions: right right right right down 
    ###
    Task:
    """,
    """
    Actions: down 
    ###
    Task:
    """,
    """
    Actions: up left left left left
    ###
    Task:
    """,
    """
    Actions: up right
    ###
    Task:
    """,
    """
    Reminder please only output the actions. Actions:
    """
]

image_fewshot_paths = [
    "../data/colored_box_pictures/obs-2/1_goals/1_goals_train_set_samples/1_goals_train_set_samples_1.png",
    "../data/colored_box_pictures/obs-2/1_goals/1_goals_train_set_samples/1_goals_train_set_samples_2.png",
    "../data/colored_box_pictures/obs-2/1_goals/1_goals_train_set_samples/1_goals_train_set_samples_3.png",
    "../data/colored_box_pictures/obs-2/1_goals/1_goals_train_set_samples/1_goals_train_set_samples_4.png",
    "../data/colored_box_pictures/obs-2/1_goals/1_goals_train_set_samples/1_goals_train_set_samples_5.png"
]

def exp_text_input(board_config):
    board_text = get_text_description(board_config)
    sys_prompt = """You are a helpful navigation assistant that reasons about the directions an agent can take
    to collect rewards and avoid obstacles based on the text description of the board.
    """
    prefix = text_fewshot_prompt
    suffix = "\n Actions:"
    user_prompt = prefix + board_text + suffix
    response = query_gpt(sys_prompt, user_prompt)
    return response

def exp_image_input(num_goals, mode, idx):
    img_path = get_image_path(num_goals, mode, idx)
    sys_prompt = """You are a helpful navigation assistant that reasons about the directions an agent can take
    to collect rewards and avoid obstacles based on the image of the board.
    """
    text_prompts = image_fewshot_prompt_texts
    image_prompt_paths = image_fewshot_paths + [img_path]
    response = query_gpt4v_with_images_and_texts(sys_prompt, text_prompts, image_prompt_paths)
    return response

def exp_symbolic_input(board_config):
    board_symbolic = get_symbolic_description(board_config)
    sys_prompt = """You are a helpful navigation assistant that reasons about the directions an agent can take
    to collect rewards and avoid obstacles based on the symbolic description of the board.
    """
    prefix = symbolic_fewshot_prompt
    suffix = "Reminder please only output the actions. Actions:"
    user_prompt = prefix + board_symbolic + suffix
    response = query_gpt(sys_prompt, user_prompt)
    return response


def batch_exp(num_goals = 1, mode = "dev"):
    text_outs = []
    img_outs = []
    symbolic_outs = []

    for i in range(25):
        print(f"experiment world {i}")
        board_config = get_world_config(num_goals, mode, i)
        text_out = exp_text_input(board_config)
        img_out = exp_image_input(num_goals, mode, i)
        symbolic_out = exp_symbolic_input(board_config)
        time.sleep(20)

        text_outs.append(text_out)
        img_outs.append(img_out)
        symbolic_outs.append(symbolic_out)
    
    # save
    with open('outputs/exp_input_modality/text_outputs.txt', 'w') as f_text:
        f_text.write("\n".join(text_outs))

    with open('outputs/exp_input_modality/image_outputs.txt', 'w') as f_text:
        f_text.write("\n".join(img_outs))

    with open('outputs/exp_input_modality/symbolic_outputs.txt', 'w') as f_text:
        f_text.write("\n".join(symbolic_outs))
    return


def batch_eval(modality, num_goals = 1, mode = "dev"):
    world_list = []
    gt_list = []
    for i in range(30):
        board_config = get_world_config(num_goals, mode, i)
        world_list.append(board_config["world"])
        gt_list.append(board_config["agent_as_a_point"])
    
    with open(f'outputs/exp_input_modality/{modality}_outputs.txt', 'r') as f:
        predicted_list = f.readlines(f)
    metrics, path_lengths = get_metrics(world_list, predicted_list, gt_list)
    
    for metric in metrics:
        print(metric, metrics[metric])
    metrics["path_lengths"] = path_lengths

    # write
    with open(f'outputs/exp_input_modality/{modality}_metrics.json', 'w') as f:
        json.dump(metrics, f)

    


batch_exp()
#batch_eval("text")
#batch_eval("image")
#batch_eval("symbolic")
    
