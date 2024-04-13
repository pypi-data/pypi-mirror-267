# irt_test
Package for calc difficult of test tasks and ability of test subjects by Rasch model (IRT 0).

## Installation
You can install irt_test using pip:

```bash
pip install irt-test
```

### Example Usage
Input DataFrame example:
|         |   Task 1 |   Task 2 |   Task 3 |   Task 4 |   Task 5 |   Task 6 |   Task 7 |   Task 8 |   Task 9 |   Task 10 |   Task 11 |
|:--------|---------:|---------:|---------:|---------:|---------:|---------:|---------:|---------:|---------:|----------:|----------:|
| Julia   |        1 |        1 |        1 |        1 |        1 |        1 |        1 |        1 |        0 |         1 |         1 |
| Ivan    |        1 |        1 |        1 |        1 |        1 |        1 |        1 |        0 |        1 |         0 |         1 |
| Anna    |        1 |        1 |        1 |        1 |        1 |        1 |        0 |        1 |        0 |         0 |         1 |
| Peter   |        1 |        1 |        1 |        1 |        1 |        1 |        0 |        1 |        0 |         0 |         1 |
| Helen   |        1 |        1 |        1 |        1 |        1 |        1 |        0 |        1 |        0 |         0 |         1 |
| Bill    |        1 |        1 |        1 |        1 |        1 |        0 |        1 |        0 |        0 |         0 |         1 |
| Tony    |        1 |        1 |        1 |        1 |        0 |        1 |        0 |        0 |        0 |         0 |         1 |
| Dmitry  |        1 |        0 |        1 |        0 |        1 |        0 |        0 |        0 |        0 |         0 |         1 |
| Natasha |        0 |        1 |        0 |        1 |        0 |        0 |        0 |        0 |        0 |         0 |         1 |
| Jimmy   |        0 |        0 |        0 |        0 |        0 |        0 |        0 |        0 |        0 |         0 |         1 |


For get logits of tasks and subjects use 'irt' function:

```python
from irt_test.irt import irt

# Get logits and additional info from IRT0 model
irt_result = irt(df)
```

```python
# Abilites of test subjects
irt_result.abilities
```
|         |         0 |
|:--------|----------:|
| Julia   |  4.72094  |
| Ivan    |  3.29019  |
| Anna    |  1.97836  |
| Peter   |  1.97836  |
| Helen   |  1.97836  |
| Bill    |  0.711974 |
| Tony    | -0.451242 |
| Dmitry  | -2.2367   |
| Natasha | -3.0347   |
```python
# Difficult of test tasks
irt_result.difficult
```
|         |         0 |
|:--------|----------:|
| Task 1  | -2.84779  |
| Task 2  | -2.84779  |
| Task 3  | -2.84779  |
| Task 4  | -2.84779  |
| Task 5  | -1.4046   |
| Task 6  | -0.212051 |
| Task 7  |  2.3964   |
| Task 8  |  1.59305  |
| Task 9  |  4.50918  |
| Task 10 |  4.50918  |
```python
# "IRT model error
irt_result.err
```
0.0196
```python
# Can't get logits for these subjects
irt_result.rejected_subjects
```
['Jimmy']
```python
# Can't get logits for these tasks
irt_result.rejected_tasks
```
['Task 11']


