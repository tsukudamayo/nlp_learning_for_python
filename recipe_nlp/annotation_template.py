import os
import gc

import pandas as pd


_LOG_DIR = 'C:/Users/tsukuda/var/data/recipe/orangepage/combined'
_DST_DIR = 'C:/Users/tsukuda/var/data/recipe/orangepage/flow'
_ORG_COLUMNS = ['number', 'word', 'tag', 'Agent', 'Targ', 'Dest',
                'F-comp', 'T-comp', 'F-eq', 'F-part-of', 'F-set', 'T-eq',
                'T-part-of', 'V-eq', 'V-tm', 'other-mod']
# _NEW_COLUMNS = ['number', 'new_word', 'new_tag', 'Agent', 'Targ', 'Dest',
#                 'F-comp', 'T-comp', 'F-eq', 'F-part-of', 'F-set', 'T-eq',
#                 'T-part-of', 'V-eq', 'V-tm', 'other-mod',
#                 'dependency_dst', 'arclabel']
_NEW_COLUMNS = ['number', 'new_word', 'new_tag', 'Targ', 'dependency_dst', 'arclabel']

def main():
    if os.path.isdir(_DST_DIR) is False:
        os.makedirs(_DST_DIR)
    else:
        pass

    file_list = os.listdir(_LOG_DIR)
    for f in file_list:
        filepath = os.path.join(_LOG_DIR, f)
        dstpath = os.path.join(_DST_DIR, f)
        fname, ext = os.path.splitext(dstpath)
        dstfile = fname + '.csv'
        df_old = pd.read_csv(filepath, delimiter='\t', names=_ORG_COLUMNS)
        df_new = df_old[df_old['tag'] != 'O']
        df_new['word'] = df_new['word'].astype(str)
        df_new['tag'] = df_new['tag'].astype(str)
        df_new['new_word'] = df_new['word'].apply(lambda x: x.split('/')[0])
        df_new['new_tag'] = df_new['tag'].apply(lambda x: x.split('-')[0])
        del df_old
        gc.collect()
        del df_new['word']
        del df_new['tag']
        output = df_new.loc[:, _NEW_COLUMNS]
        del df_new
        gc.collect()
        print(output.head())
        output.reset_index(drop=True)
        output.to_csv(dstfile)


if __name__ == '__main__':
    main()
