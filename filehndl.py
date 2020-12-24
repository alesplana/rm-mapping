import pandas as pd
import numpy as np

'''
convert_csv function returns a pandas dataframe with reformatted tables of the map data from raman
return values [new_csv_final, stat]
new_csv_final - pandas dataframe
stat - integer (0 - ok, 1 - error)
'''


def convert_csv(old_file):
    stat = 0
    test_1 = pd.Index(['#X', 'Unnamed: 1', '#Y', 'Unnamed: 3', '#Wave', 'Unnamed: 5',
                       '#Intensity'])  # original file

    test_csv = pd.read_csv(old_file, sep='\t', header=0)
    test_col = test_csv.columns

    try:
        test1 = (test_col == test_1).all()
        test2 = test_csv.iloc[:, 4:7].mean().isna().all()
    except ValueError:
        print('Invalid File')
        stat = 1
        new_csv_final = []
        return new_csv_final, stat

    if test1 and test2:
        stat = 0
        test_csv.columns = ['x', 'y', 'wave', 'intensity', 'z', 'z', 'z']
        old_csv = test_csv.drop(['z'], axis=1)
        # old_csv = pd.read_csv(old_file, names=["x", "y", "wave", "intensity"])
        x_unq = old_csv.x.unique().astype('float')  # read unique x values
        y_unq = old_csv.y.unique().astype('float')  # read unique y values

        # convert x and y coordinates to dict
        xy = {}
        i = 0

        for a in range(len(x_unq)):
            for b in range(len(y_unq)):
                xy[i] = {'x': x_unq[a], 'y': y_unq[b], 'str': x_unq[a].astype('str') + 'x' + y_unq[b].astype('str'),
                         'xy_id': i}
                i = i + 1

        i = 0  # reinitialize i for future use

        # create x y dataframe with spectra identifier
        xy_df = pd.DataFrame.from_dict(xy, orient='index', columns=['x', 'y', 'str', 'xy_id'])
        xy_df.set_index('str', inplace=True)

        # create wavenumber dataframe
        wn = old_csv.wave.unique().tolist()
        wn.sort()  # sort to increasing

        wn_df = pd.DataFrame(wn, columns=['wavenumber'])
        wn_df['wn_id'] = wn_df.index
        wn_df.set_index('wavenumber', inplace=True)

        # rebuild dataframe
        rebuild_csv = {}

        for i in range(len(old_csv)):
            query_xy = old_csv.iloc[i].x.astype('float').astype('str') + 'x' + old_csv.iloc[i].y.astype('float').astype(
                'str')
            rebuild_csv[i] = {'xy_id': xy_df.loc[query_xy].xy_id.astype('int'),
                              'wn_id': wn_df.loc[old_csv.iloc[i].wave].wn_id,
                              'intensity': old_csv.iloc[i].intensity}

        newdata_df = pd.DataFrame.from_dict(rebuild_csv, orient='index', columns=['xy_id', 'wn_id', 'intensity'])
        newdata_pv = newdata_df.pivot('xy_id', 'wn_id').values
        new_df = pd.DataFrame(newdata_pv)
        new_df.index.names = ['xy_id']
        new_df.columns = wn

        # merge new dataframes
        new_csv_final = pd.merge(xy_df, new_df, on=['xy_id'])
        return new_csv_final, stat
    elif not (test_col == test_1).all() or test_csv.iloc[:, 4:7].mean().notna().all():
        stat = 0
        new_csv_final = {}
        return new_csv_final, stat
