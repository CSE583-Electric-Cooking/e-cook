from process_kosko import Kosko
from process_a2ei import A2EI
from process_survey import *

if __name__ == "__main__":
    A2EI(write_csv = True)
    Kosko(write_csv = True)
    process_data_survey(write_csv=True)