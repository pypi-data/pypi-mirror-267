import numpy as np
import pandas as pd



class IrtResult:
    """Contain logits of tasks and subjects from IRT0 model.
       Also contain error and rejected units. 
       Rejected units (subjects or tasks) - units wich cannot be used to 
       calculate logits.
       
    Attributes:
            abilities (pandas.Series): Logits of subjects abilities (subjects is index of Series).
            difficult (pandas.Series): Logits of task difficult (tasks is index of Series).
            err (float): Metric of difference between real test results and estimated results by logits.
            rejected_tasks (list): Name of tasks wich cannot be used to calculate difficult logits.
            rejected_subjects (list): Name of subjects wich cannot be used to calculate ability logits.
    """

    def __init__(self, abilities:         pd.Series, 
                       difficult:         pd.Series, 
                       err:               float, 
                       rejected_tasks:    list, 
                       rejected_subjects: list):
        
        self.abilities = abilities
        self.difficult = difficult
        self.err = err
        self.rejected_tasks = rejected_tasks
        self.rejected_subjects = rejected_subjects



def prepare(df: pd.DataFrame) -> (pd.DataFrame, list, list):
    '''
    Iterative remove consisting only of zeros or only ones columns and rows.

        Parameters:
                df (DataFrame): A matrix with zeros and ones values only.

        Returns:
                df (DataFrame): Filtered matrix.
                rejected_subjects (list): List of subjects, who only have zero or only one results.
                rejected_tasks (list): List of tasks, who got only zero  or only one results.
    '''

    def _check_row_zeros(row_index: int) -> bool:
        '''
        Returns True if DataFrame row contains only zeros.
        '''
        return df.loc[row_index].sum() == 0
    
    def _check_row_ones(row_index: int) -> bool:
        '''
        Returns True if DataFrame row contains only ones.
        '''
        return df.loc[row_index].sum() >= len(df.loc[row_index])
    
    def check_subject(subject_index: int) -> bool:
        '''
        Returns True if DataFrame row contains only 0 or 1 valuses.
        '''
        return _check_row_zeros(subject_index) or _check_row_ones(subject_index)

    def _check_col_zeros(column_index: int) -> bool:
        '''
        Returns True if DataFrame column contains only zeros.        
        '''
        return df[column_index].sum() == 0

    def _check_col_ones(column_index: int) -> bool:
        '''
        Returns True if DataFrame column contains only ones.
        '''
        return df[column_index].sum() >= len(df[column_index])
    
    def check_task(task_index: int) -> bool:
        '''
        Returns True if DataFrame column contains only same valuses 0 or 1.        
        '''
        return _check_col_zeros(task_index) or _check_col_ones(task_index)

    rejected_subjects = []
    rejected_tasks = []

    # cycle while found rejected.
    while True:
        subjects = df.index
        tasks = df.columns

        # check for bad test units.
        rej_subjects = list(filter(check_subject, subjects))
        rej_tasks = list(filter(check_task, tasks))

        # stop if bad units not found.
        if len(rej_subjects) == 0 and len(rej_tasks) == 0:
            break
        
        # must return info about all bad units.
        rejected_subjects += rej_subjects
        rejected_tasks += rej_tasks

        # remove bad units from DataFrame.
        df = df.drop(index=rej_subjects)
        df = df.loc[:, ~df.columns.isin(rej_tasks)]

        rej_subjects = []
        rej_tasks = []

    return df, rejected_subjects, rejected_tasks    


def irt(df: pd.DataFrame, steps: int = 0, accept: float = 0.02) -> IrtResult:
    '''
    Calculatie scores for the subjects ability and tasks difficult 
    in the form of logits via IRT model.

        Parameters:
                df (DataFrame): A matrix with zeros and ones values only.
                steps (int): number of learning steps (if 0 -> model will run until error > accept).
                accept (float): acceptable error value (ignored when steps > 0)

        
        Returns:
                result (IrtResult): object with logit vectors, 
                                    rejected subjects and tasks, 
                                    model error.
    '''

    if not _df_consist_only_of(df, set([0, 1])):
        raise ValueError("Input data can contain only ones and zeros.")
    
    # Remove zeros and ones Series from input data.
    df, rejected_subjects, rejected_tasks = prepare(df)
    tasks = df.columns
    subjects = df.index

    matrix = df.to_numpy()

    ability, difficult = predict(matrix)

    # Shift vector of difficults to zero mean.
    bias_difficult = difficult - difficult.mean()

    if steps:
        for _ in range(steps):
            ability, bias_difficult, err = learn_step(matrix, 
                                                      ability, 
                                                      bias_difficult)
    else:
        while True:
            ability, bias_difficult, err = learn_step(matrix, 
                                                      ability, 
                                                      bias_difficult)
            if err <= accept:
                break
    
    # Concatenate logits and units.
    ability = pd.Series(ability, subjects)
    bias_difficult = pd.Series(bias_difficult, tasks)

    irt_result = IrtResult(
        abilities=ability, 
        difficult=bias_difficult, 
        err=err, 
        rejected_tasks=rejected_tasks, 
        rejected_subjects=rejected_subjects
    )

    return irt_result


def predict(matrix: np.array) -> (np.array, np.array):
    '''
    Calculate subjects ability and task difficult in test as logits. 
    Accepts test results in binary form as input.

        Parameters:
                matrix (2d np.array): A matrix with zeros and ones values only.

        Returns:
                ability (1d np.array): Binary array of subjects ability.
                difficult (1d np.array): Binary array of tasks difficult.
    '''
    subjects_mean = np.mean(matrix, axis=1)
    ability = np.log(subjects_mean / (1 - subjects_mean))
    
    tasks_mean = np.mean(matrix, axis=0)
    difficult = np.log((1 - tasks_mean) / tasks_mean)

    return ability, difficult


def learn_step(matrix, ability, bias_difficult):
    '''
    Calculate subjects ability and task difficult in test as logits. 
    Accepts test results in binary form as input.

        Parameters:
                matrix (2d np.array): Original test matrix.
                ability (1d np.array): Binary array of subjects ability from previous step.
                difficult (1d np.array): Binary array of tasks difficult from previous step.

        Returns:
                ability (1d np.array): Binary array of subjects ability.
                difficult (1d np.array): Binary array of tasks difficult. 
                err (float): difference metric between estimated values and original matrix.
    '''

    ev = estimated_values(ability, bias_difficult)

    ability_err, diff_err = error(ev)
    ability_diff, diff_diff = logits_difference(matrix, ev)

    err = np.sum(ability_diff * ability_diff)

    # get new logits.
    ability = ability - (ability_diff / ability_err)
    difficult = bias_difficult - (diff_diff / diff_err)

    # Set logits of difficult average to zero.
    bias_difficult = difficult - difficult.mean()

    return ability, bias_difficult, err


def estimated_values(ability: np.array, bias_difficult: np.array) -> np.array: 
    '''
    Calculate matrix of estimated values, step of Rasch model learning.
        
        Parameters:
                ability (1d np.array): Vector of predicted subjects ability.
                bias_difficult (1d np.array): Vector of predicted task difficult.
                                              The average of this vector must be almost zero.

        Returns: 
                ev_matrix (2d np.array): Matrix of estimated values.
            
    '''   
    ev_matrix = np.array([ability])

    for dif_value in bias_difficult:
        diff_exp = np.exp(ability - dif_value)
        ev_vec = diff_exp / (1 + diff_exp)
        ev_matrix = np.concatenate((ev_matrix, [ev_vec]), axis=0)

    return ev_matrix[1::].T


def error(ev: np.array) -> (float, float):
    '''
    Calculate errors for abilities and difficult based on estimated values dispersion, step of Rasch model learning.
        
        Parameters:
                ev (2d np.array): Estimated values.

        Returns: 
                ability error (float): Error value for subject abilities predict.
                difficult error (float): Error value for task difficult predict.
            
    '''   
    ev_dispersion = ev * (1-ev)
    ability_err = -1 * np.sum(ev_dispersion, axis=1)
    diff_err = -1 * np.sum(ev_dispersion, axis=0)

    return ability_err, diff_err


def logits_difference(prev_matrix: np.array, ev: np.array) -> (float, float):
    '''
    How changes logits in current step of Rasch model learning.

    Parameters:
        prev_matrix (2d np.array): Matrix of logits from previous learning step.
        ev (2d np.array): Estimated values.

    Returns: 
        ability difference (float): Difference between previous step calculated ability logits and current abilities.
        difficult difference (float): Difference between previous step calculated difficult logits and current difficult.
    '''
    difference = prev_matrix - ev
    ability_diff = np.sum(difference, axis=1)
    diff_diff = -1 * np.sum(difference, axis=0)

    return ability_diff, diff_diff


def _df_consist_only_of(df: pd.DataFrame, values: set) -> bool:
    df_values = df.stack().tolist()
    diff = set(df_values).difference(values)
    return len(diff) == 0
