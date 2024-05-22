
from read_data import *
from llm import *


def exp_text_input(board_config):
    board_text = get_text_description(board_config)
    sys_prompt = """You are a helpful navigation assistant that reasons about the directions an agent can take
    """
    prefix = ""
    suffix = ""
    user_prompt = prefix + board_text + suffix
    response = query_gpt4v(system_prompt, user_prompt)
    return response

def exp_image_input(board_config):
    img = get_text_description(board_config)
    save_img(img, img_path)
    sys_prompt = ""
    user_prompt = ""
    response = query_gpt4v_with_single_image(image_path, system_prompt, user_prompt)
    return response

def exp_symbolic_input():
    board_symbolic = get_symbolic_description(board_config)
    sys_prompt = ""
    prefix = ""
    suffix = ""
    user_prompt = prefix + board_symbolic + suffix
    response = query_gpt4v(system_prompt, user_prompt)
    return response


def batch_exp(board_size, n_obstacles, n_rewards):
    for i in range(100):
        config = generate_config(board_size, n_obstacles, n_rewards)