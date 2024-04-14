# irt_test
Package for calc difficult of test tasks and ability of test subjects by Rasch model (IRT 0).

## Installation
You can install irt_test using pip:

```bash
pip install irt-test
```

## Example Usage

### ℹ️ Important

**🔥 Note:** The Rasch model works only with binary data, also no column or row should contain a single value, for example, a row of zeros or ones will be excluded from the analysis.

### Input DataFrame example:
|       |   Task 1 |   Task 2 |   Task 3 |   Task 4 |   Task 5 |
|:------|---------:|---------:|---------:|---------:|---------:|
| Julia |        1 |        0 |        1 |        1 |        1 |
| Ivan  |        1 |        1 |        1 |        0 |        1 |
| Anna  |        1 |        0 |        0 |        0 |        1 |
| Peter |        0 |        0 |        0 |        1 |        1 |

### For get logits of tasks and subjects use 'irt' function.

This function calculates scores for the subjects' abilities and tasks' difficulty in the form of logits using the IRT model.

**Parameters:**
- `df` (DataFrame): A matrix with only zeros and ones values.
- `steps` (int): Number of learning steps (if 0, the model will run until the error > accept).
- `accept` (float): Acceptable error value (ignored when steps > 0).

**Returns:**
- `result` (IrtResult): An object containing logit vectors, rejected subjects and tasks, and model error.

```python
from irt_test.irt import irt

# Get logits and additional info from IRT0 model
irt_result = irt(df)
```
irt_result object contains logits of tasks and subjects from the IRT0 model, along with error and rejected units.

**Attributes:**
- `abilities` (pandas.Series): Logits of subjects' abilities (subjects are the index of the Series).
- `difficult` (pandas.Series): Logits of task difficulty (tasks are the index of the Series).
- `err` (float): Metric of the difference between real test results and estimated results by logits.
- `rejected_tasks` (list): Names of tasks that cannot be used to calculate difficulty logits.
- `rejected_subjects` (list): Names of subjects that cannot be used to calculate ability logits.

