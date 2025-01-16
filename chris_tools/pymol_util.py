import pandas as pd
from pymol import (
    cmd,
    stored
)


def collect(fname, sele, variables):
    
    cmd.delete('all')
    cmd.load(fname)
    stored.t = list()
    var_sele=", ".join(map(str,variables))
    cmd.iterate_state(-1, sele, f'stored.t.append(({var_sele}))')

    return pd.DataFrame(
        data=stored.t,
        columns=variables)


def get_res_keys( fname, sele='all' ):

    df=collect(
        fname,
        sele,
        'chain resi resn'.split()
    )


    result = list()
    for i, row in df.iterrows():
        key = (row.chain, row.resi, row.resn)
        if key not in result:
            result.append(key)

    return result
