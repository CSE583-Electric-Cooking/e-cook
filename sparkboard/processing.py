"""
This script is used in the event only raw data is avaliable
or in the event modifications to how the data is processed is selected
this script will generate/overwrite old data
"""
from .process_kosko import Kosko
from .process_a2ei import A2EI
from .process_survey import process_data_survey

if __name__ == "__main__":
    A2EI(write_csv = True)
    Kosko(write_csv = True)
    process_data_survey(write_csv=True)
