from rdkit.Chem import Draw
from base64 import b64encode
MOL_SIZE = (200, 200)


def mol2html(mol, legend=""):
    data = Draw._moltoimg(mol, MOL_SIZE, [], legend=legend, returnPNG=True, kekulize=True)
    b64image = b64encode(data).decode('ascii')
    return (f'<div style="width: {MOL_SIZE[0]}px; height: {MOL_SIZE[1]}px" data-content="rdkit/molecule">'
            f'<img src="data:image/png;base64,{b64image}" alt="Mol"/></div>')
