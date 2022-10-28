# Modified `hubmeta` examples

The folder contains modified examples of files in [`hub-infrastructure-experiments/json-schema/hubmeta-examples`](https://github.com/reichlab/hub-infrastructure-experiments/tree/main/json-schema/hubmeta-examples) to allow for json schema validation.

The main difference relates to encoding round specific configuration as arrays of round objects contained in a `rounds` element. Each round object contains a `round_id` key, the value of which contains the `round_id`. This way, each round can be validated against a generic round metadata schema. In the previous metadata structure, round metadata were contained as values to `round_id` keys making generic validation difficult.

- **`simple-hubmeta-mod.json`** is modified from [`hub-infrastructure-experiements/json-schema/hubmeta-examples/simple-hubmeta.json`](https://github.com/reichlab/hub-infrastructure-experiments/blob/main/json-schema/hubmeta-examples/simple-hubmeta.json)
- **`complex-hubmeta-mod.json`** is modified from [`hub-infrastructure-experiements/json-schema/hubmeta-examples/complex-hubmeta.json`](https://github.com/reichlab/hub-infrastructure-experiments/blob/main/json-schema/hubmeta-examples/complex-hubmeta.json)
