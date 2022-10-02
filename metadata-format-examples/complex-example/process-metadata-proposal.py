import json
from jsonspec.reference import resolve

with open("metadata-format-examples/complex-example/model-task-metadata-proposal.json", "r") as f:
  metadata = json.load(f)

resolve(metadata, '#/model_tasks/default/0/task_ids/location/required')

