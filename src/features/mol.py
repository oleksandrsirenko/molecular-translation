from tqdm import tqdm
from rdkit import Chem
from rdkit import RDLogger
RDLogger.DisableLog('rdApp.*')
from pathlib import Path

def normalize_inchi(inchi):
    try:
        mol = Chem.MolFromInchi(inchi)
        return inchi if (mol is None) else Chem.MolToInchi(mol)
    except: return inchi


# Segfault in rdkit taken care of, run it with:
# while [ 1 ]; do python normalize_inchis.py && break; done
if __name__=='__main__':
    # Input & Output
    orig_path = Path('submission_LB_322.csv')
    norm_path = orig_path.with_name(orig_path.stem+'_norm.csv')
    
    # Do the job
    N = norm_path.read_text().count('\n') if norm_path.exists() else 0
    print(N, 'number of predictions already normalized')

    r = open(str(orig_path), 'r')
    w = open(str(norm_path), 'a', buffering=1)

    for _ in range(N):
        r.readline()
    line = r.readline()  # this line is the header or is where it segfaulted last time
    w.write(line)

    for line in tqdm(r):
        splits = line[:-1].split(',')
        image_id = splits[0]
        inchi = ','.join(splits[1:]).replace('"','')
        inchi_norm = normalize_inchi(inchi)
        w.write(f'{image_id},"{inchi_norm}"\n')

    r.close()
    w.close()