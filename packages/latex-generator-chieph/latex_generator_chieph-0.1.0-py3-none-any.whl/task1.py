from typing import List


def gen_tex(document: str):
    return f"""
    \\documentclass{{article}}
    \\usepackage{{graphicx}}
    \\begin{{document}}
    {document}
    \\end{{document}}
    """


def gen_table_tex(a: List[List]):
    n, m = len(a), len(a[0])
    content = ' \\\\\n\t'.join([' & '.join(map(str, row)) for row in a])
    res = f"""
    \\begin{{tabular}}{{{' c' * m}}}
    {content}
    \\end{{tabular}}
    """
    return res


def insert_image_tex(path: str):
    return f"""\\includegraphics[width=\\linewidth]{{{path}}}"""
