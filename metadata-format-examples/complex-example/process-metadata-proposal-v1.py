import json
from jsonspec.reference import resolve

with open("metadata-format-examples/complex-example/model-task-metadata-proposal-v1.json", "r") as f:
  metadata = json.load(f)

resolve(metadata, '#/model_tasks/default/0/task_ids/location/required')

