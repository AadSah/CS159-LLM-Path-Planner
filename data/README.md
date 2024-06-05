## Data and Environment Generation

This folder contains the code to generate the environments, place obstacles, agent starting point, and the goals. In addition, the code for obtaining data representation in pictorial and symbolic representation is also here. We build on top of the code available [here](https://github.com/MohamedAghzal/llms-as-path-planners.git). Follow the steps below:

(1) Environment grid and obstacles:

Run the following command:

```python
python3 generate_envs.py <shape-of-the-grids> <number-of-obstacles> <number-of-environments>
```

Example:

```python
python3 generate_envs.py 6 4 25
```

This will generate the enviroment json files, and store them in the folder `./envs/grid-6/obs-4/environments4.json`

(2) Place agent and goals:

Run the following command:

```python
python3 place_agent_goals.py <directory-of-environment> <number-of-goals>
```

Example:
```python
python3 place_agent_goals.py ./envs/grid-6/obs-4/ 8
```

This will take the enviroments file generated in the previous step and place the agent starting point and the goals randomly. Multiple json files will be created inside the folder `./envs/grid-6/obs-4/8_goals/`. Note that we do not consider the splits, and consider just the `train_set` as a single corpus of data.

(3) Generate ground-truth paths:

Run the following command:

```python
python3 generate_samples.py <path-to-the-json-file>
```

Example:
```python
python3 generate_samples.py ./envs/grid-6/obs-4/8_goals/8_goals_train_set.json
```

This will generate a file `./envs/grid-6/obs-4/8_goals/8_goals_train_set_samples.json` with all the information for a task along with the groundtruth paths.


(4) Generate symbolic data:

Run the following command:

```python
python3 generate_symbolic_representations.py
```

This will read all the data generated and stored in the `./envs/` folder and create a folder `./json_with_symbols` containing data represented symbolically.

(5) Generate pictorial data:

Run the following command:

```python
python3 generate_colored_box_pictures.py
```

This will read all the data generated and stored in the `./envs/` folder and create a folder `./colored_box_pictures/` containing data represented pictorially using images.


We have included all the data generated following the above steps with the following configuration in this folder:

```
Grid Size: 6
Number of Obstacles: 4
Number of Environments: 25
Number of Goals: 8
```
