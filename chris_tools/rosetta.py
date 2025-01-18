import os
from .file_system import (
    write_lines,
    get_lines,
    file_exists,
    safe_rm,
    safe_mkdir,
    abs_path
)

from .pymol_util import (
    collect,
    get_res_keys
)

def make_ddg_mapper( fname ):
    lines = get_lines(fname)
    temp_mapper = dict()
    for ll in lines:
        if not ll.startswith('residue_ddg'):
            continue
        l, r = ll.split()
        temp_mapper[int(l.rsplit('_')[-1])] = float(r)


    res_keys=get_res_keys(fname)

    result = dict()
    cov = list()
    it = 1
    for key in res_keys:
        if key not in cov:
            cov.append( key )
            (chain, resi, resn)=key
            result[resi+chain] = temp_mapper[it]
            it += 1

    return result


def ddg_sele(fname, extra_res_fa=None, ddg_cutoff:float=0.1,jump:str=1, work_dir:str='./prddg/'):
    
    safe_mkdir(work_dir)
    protocol = write_lines(f'./{work_dir}/prddg.xml', 
        ['<ROSETTASCRIPTS>',
            '	<SCOREFXNS>',
            '        <ScoreFunction name="ligand" weights="ligand" />',
            '	</SCOREFXNS>',
            '	<MOVERS>',
            '        <ddG name="ddg" ',
            '            scorefxn="ligand"',
           f'            jump="{jump}"',
            '            per_residue_ddg="true" />',
            '	</MOVERS>',
            '	<PROTOCOLS>',
            '        <Add mover_name="ddg" />',
            '	</PROTOCOLS>',
            '</ROSETTASCRIPTS>',
        ])
    cmd=[
        'rosetta_scripts',
        "-mistakes:restore_pre_talaris_2013_behavior",
        f"-parser:protocol {abs_path(protocol)}",
        f"-in:file:s {abs_path(fname)}",
        f"-out:prefix prddg_",
        f"-out:path:all {abs_path(work_dir)}",
        "-overwrite"
    ]
    
    if extra_res_fa is not None:
        cmd.append("-extra_res_fa")
        cmd.extend([
            f"'{abs_path(erf)}'" for erf in extra_res_fa
        ])
    cmd = " ".join(cmd)
    print(cmd)
    result = os.system(f"{cmd} > log.txt ")
    outfile = f"./{work_dir}/prddg_production_0001.pdb"
    assert file_exists(outfile) 
    ddg_mapper = make_ddg_mapper( outfile )
    tks = list()
    for k,v in ddg_mapper.items():
        if abs(v) >= ddg_cutoff:
            tks.append( k )

    safe_rm(outfile)
    safe_rm(protocol)
    return ','.join(tks)

