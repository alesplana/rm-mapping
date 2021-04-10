# last edited: 04/10/2021

import pandas as pd
import os


# convert_csv function returns a pandas dataframe with reformatted tables of the map data from raman
# return values [new_csv_final, stat]
# new_csv_final - pandas dataframe
# stat - integer (0 - ok, 1 - error)


def convert_csv(old_file):
    stat = 0
    test_1 = pd.Index(['#X', 'Unnamed: 1', '#Y', 'Unnamed: 3', '#Wave', 'Unnamed: 5',
                       '#Intensity'])  # original file

    test_2 = pd.Index(['x', 'y', 'str'])  # converted file

    file_ext = os.path.splitext(old_file)[1].strip().lower()

    try:
        if file_ext == '.csv':
            test_csv = pd.read_csv(old_file)
            test1 = (test_csv.columns[0:3] == test_2).all()
        elif file_ext == '.txt':
            test_csv = pd.read_csv(old_file, sep='\t', header=0)
            test1 = (test_csv.columns == test_1).all()
            test2 = test_csv.iloc[:, 4:7].mean().isna().all()
        else:
            print('File Unsupported')
            stat = 1
            new_csv_final = []
            return new_csv_final, stat
    except ValueError:
        print('Invalid File')
        stat = 1
        new_csv_final = []
        return new_csv_final, stat

    if test1 and file_ext == '.csv':
        stat = 0
        test_csv = pd.read_csv(old_file)
        return test_csv, stat

    if test1 and test2 and file_ext == '.txt':
        stat = 0
        test_csv = pd.read_csv(old_file, sep='\t', header=0)
        test_csv.columns = ['x', 'y', 'wave', 'intensity', 'z', 'z', 'z']
        test_csv.drop(['z'], axis=1, inplace=True)

        test_csv['str'] = test_csv['x'].astype(str) + 'x' + test_csv['y'].astype(str)
        wn_int = test_csv.iloc[:, 2:5]
        pv_df = wn_int.pivot(index='str', columns='wave', values='intensity').reset_index().rename_axis(None, axis=1)

        xy = test_csv.iloc[:, :2].drop_duplicates().reset_index()
        xy.drop(['index'], axis=1, inplace=True)
        xy['str'] = xy['x'].astype(str) + 'x' + xy['y'].astype(str)

        new_csv_final = pd.merge(xy, pv_df, on=['str'])
        return new_csv_final, stat

    # if not (test_csv.columns == test_1).all() or test_csv.iloc[:, 4:7].mean().notna().all():
    #    stat = 0
    #    new_csv_final = {}
    #    return new_csv_final, stat
