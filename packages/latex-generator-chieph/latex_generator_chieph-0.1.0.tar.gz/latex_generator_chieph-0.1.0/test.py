from task1 import gen_table_tex, gen_tex, insert_image_tex
import numpy as np
import subprocess
import os

np.random.seed(0)

A = np.random.randint(0, 10, (10, 10))

# with open("../artifacts/2.1/table.tex", "w") as f:
#     f.write(gen_table_tex(A))

with open("../artifacts/2.2/image+table.tex", "w") as f:
    f.write(gen_tex(gen_table_tex(A) + insert_image_tex("../artifacts/2.2/python.jpg")))

os.system("pdflatex ../artifacts/2.2/image+table.tex")

