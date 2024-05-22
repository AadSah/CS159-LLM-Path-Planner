#!/bin/bash

# Define the observations and goals arrays
observations=("obs-2" "obs-4" "obs-8" "obs-16")
goals=("1_goals" "2_goals" "4_goals" "8_goals" "16_goals")

# Loop over each observation
for obs in "${observations[@]}"; do
  # Loop over each goal
  for goal in "${goals[@]}"; do
    # Print progress statement
    echo "Processing observation: ${obs}, goal: ${goal}"
    
    # Generate samples for each dataset type
    python3 generate_samples.py ./envs/${obs}/${goal}/${goal}_train_set.json
    echo "Completed: ${obs}, ${goal}, train set"
    
    python3 generate_samples.py ./envs/${obs}/${goal}/${goal}_test_set_seen.json
    echo "Completed: ${obs}, ${goal}, test set seen"
    
    python3 generate_samples.py ./envs/${obs}/${goal}/${goal}_dev_set.json
    echo "Completed: ${obs}, ${goal}, dev set"
    
    python3 generate_samples.py ./envs/${obs}/${goal}/${goal}_unseen.json
    echo "Completed: ${obs}, ${goal}, unseen set"
  done
done
