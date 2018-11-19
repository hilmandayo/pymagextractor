""" A module to test all the necessaries funtions/methods from `csv_handler.py`

For this purpose, a pseudo, known in advance csv files will be used. The two
csv files are within this directory known as `original.csv` and `refined.csv`.
These two csv files will be mimicking the structure and the possible problems
that the may give to the functions/methods.
"""


import csv_handler

original_path = 'test_original.csv'
refined_path = 'test_refined.csv'

dto = csv_handler.DualTrackedObjects(refined_path, original_path)
