import pandas as pd
import numpy as np


def convert_csv(old_file):
    old_csv = pd.read_csv(old_file, names=["x", "y", "wave", "intensity"])
    x_unq = old_csv.x.unique().astype('int')  # read unique x values
    y_unq = old_csv.y.unique().astype('int')  # read unique y values

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
        query_xy = old_csv.iloc[i].x.astype('int').astype('str') + 'x' + old_csv.iloc[i].y.astype('int').astype('str')
        rebuild_csv[i] = {'xy_id': xy_df.loc[query_xy].xy_id, 'wn_id': wn_df.loc[old_csv.iloc[i].wave].wn_id,
                          'intensity': old_csv.iloc[i].intensity}

    newdata_df = pd.DataFrame.from_dict(rebuild_csv, orient='index', columns=['xy_id', 'wn_id', 'intensity'])
    newdata_pv = newdata_df.pivot('xy_id', 'wn_id').values
    new_df = pd.DataFrame(newdata_pv)
    new_df.index.names = ['xy_id']
    new_df.columns = wn

    # merge new dataframes
    new_csv_final = pd.merge(xy_df, new_df, on=['xy_id'])
    return new_csv_final
