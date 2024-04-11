import os
import pandas as pd
import json
from .collect import build_data


def format_multi_index(df: pd.DataFrame, md_style: bool = False):
    '''
        used for printing multi-index dataframes to markdown
    '''
    b_multi_index_cols = isinstance(df.columns, pd.MultiIndex)
    if len(df.columns) == 0:
        return pd.DataFrame(df.index.to_list(), columns=df.index.names)
    else:
        left = pd.DataFrame(df.index.to_list(), columns=df.index.names)
        right = df.reset_index(drop=True)
        df = pd.concat([left, right], axis=1)
    if b_multi_index_cols:
        lc_char = '<br>' if md_style else '\n'
        df.columns = [(col if isinstance(col, str) else lc_char.join(col)) 
                      for col in df.columns]
    return df


def input_by_model(data):
    return (
        data.groupby(['input_name', 'model_name'])
        .agg({'run_id': 'nunique', 'name': 'nunique'})
        .reset_index()
        .rename(columns={'name': 'unique_questions'})
        .sort_values('run_id', ascending=False)
    )


def all_sheets_all_questions(data):
    tmp = (
        data.groupby(['input_name', 'name'])
        .agg({'name': 'count'})
        .drop(columns=['name'])
    )
    return tmp


def sheet_by_model_pct_correct(data):
    tmp = (
        data.groupby(['input_name', 'model_name'])
        .agg({'name': 'count', 'grade_bool': 'mean'}) 
        .rename(columns={'name': 'total_questions', 'grade_bool': 'pct_correct'})
        .sort_values(['input_name', 'pct_correct'], ascending=False)
    )
    tmp['pct_correct'] = (
        pd.to_numeric(tmp['pct_correct'], errors='coerce')
        .round(2)
    )
    return tmp

def question_by_runid_completion(data, add_index_cols = []):
    index_cols = ['name', 'run_id'] + add_index_cols
    tmp = (data
        .groupby(by=index_cols)
        .agg({
            # 'completion': lambda x: ''.join(x if x is not None else ''),        
            'completion': lambda x: x,        
        })
    )
    return tmp

def grade_discrepancy_by_runid(data, add_index_cols = [], add_values = []):
    question_names_by_models = pd.pivot(
        data, 
        index='name', 
        columns=['model_name', 'run_id'] + add_index_cols, 
        values=['grade_bool'] + add_values
    )

    grade_bool_cols = [col for col in question_names_by_models.columns if col[0] == 'grade_bool']
    grade_bool_diff_mask = question_names_by_models[grade_bool_cols].apply(
        lambda x: x.dropna().nunique() > 1, axis=1
    )

    keep_mask = grade_bool_diff_mask.copy()
    for col in question_names_by_models.columns:
        if col[0] != 'grade_bool':
            keep_mask &= grade_bool_diff_mask
    
    tmp = question_names_by_models[keep_mask]
    
    return tmp

def model_input_results(
    data,
    model_name,
    input_name,
    run_id = None, # if None, use first run_id
):

    a = (data['model_name'] == model_name)
    b = (data['input_name'] == input_name)

    run_ids = data[a & b]['run_id'].unique()
    if run_id is None:
        run_id = run_ids[0]
    c = (data['run_id'] == run_id)

    num_questions = data[a & b & c].shape[0]

    slice_wrong = data[a & b & c & (data['grade'] == 0)]
    num_wrong = slice_wrong.shape[0]
    questions_wrong_name = slice_wrong['name'].tolist()

    return {
        'num_questions': num_questions,
        'num_wrong': num_wrong,
        'questions_wrong_name': questions_wrong_name,
    }
