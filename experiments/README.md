## Experimenting different input modalities
The exp_input_modality.py contains code for comparing various modalities. To perform experiment please run

```python
python3 exp_input_modality.py
```

This generates outputs in txt format the LLM output for various modalities, as well as (optionally) the evaluation metrics in json format in the outputs/exp_input_modality folder.

## Evaluation
Evaluation of metrics including ``Valid" ---the percentage of paths that do not run into obstacles; ``Reaches Goal" --- the percentage of paths that successfully reach the goal; ``Distance"--- the distance of the end position of the LLM-generated path to the actual goal; ``Is Optimal" --- the percentage of paths that are optimal. The metrics are consistent with https://arxiv.org/abs/2403.18778.

To include evaluation, uncomment the batch_eval(<modality_name>) in the exp_input_modality.py script before running.