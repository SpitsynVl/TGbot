import pandas as pd
import random

data = pd.read_csv('data_model/data_for_quiz_1.csv')

def take_random_quote():
    rand_num = random.randint(0, data.shape[0])
    return [data.iloc[rand_num]['Цитата'], data.iloc[rand_num]['Автор']]