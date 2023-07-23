import numpy as np
import pandas as pd


class CutterOptimizer:
    def __init__(self, _originals, _inherited):
        self.originals = sorted(_originals, reverse=True)  # TODO check if the reverse is correct
        self.inherited = sorted(_inherited, reverse=True)  # TODO check if the reverse is correct
        self.possibilities_table = []

        # starting the possibilities table
        self.create_table()
        self.sum_criteria_calculations = []

        # checking the initial sum criteria
        self.sum_criteria_calculations = []

    # initialization of the possibilities table
    def create_table(self):
        for length in self.originals:
            df = pd.DataFrame(0, index=[length] * len(self.inherited), columns=self.inherited)
            df = df.where(np.tril(np.ones(df.shape), k=-1).astype(bool))

            # reshaping pd df
            df = df.fillna('-')
            df = df.replace(0, np.nan)
            df = df.replace('-', float(0))

            # saving to the main level
            self.possibilities_table.append(pd.DataFrame(df))

    # sum criteria for the
    def row_sum_criteria(self):
        # resetting the output variable
        self.sum_criteria_calculations = []

        # interacting the possibilities tables
        for table_index in range(len(self.possibilities_table)):
            current_table = self.possibilities_table[table_index]

            # appending a nev array for the current calculation
            self.sum_criteria_calculations.append([])

            # interacting table
            for row_index in range(len(current_table)):
                row_header = originals_sheets[table_index]
                current_line = current_table.iloc[row_index]

                # calculation of the multiplication of the between row and table headers
                results = []
                for index in range(len(current_line)):
                    x = float(current_line.iloc[index])
                    y = float(self.inherited[index])
                    result = x * y if not pd.isna(x) else 0
                    results.append(result)

                # saving calculations
                res = row_header - sum(results)
                self.sum_criteria_calculations[-1].append(res)
                if res < 0:  # conditions of the production
                    return False

        # if all conditions are okay, return true
        return True

    # optimization function
    def optimizer(self):
        for table_index in range(len(self.possibilities_table)):
            current_table = self.possibilities_table[table_index]
            for row_index in range(len(current_table)):
                current_line = current_table.iloc[row_index]
                for line_index in range(len(current_line)):
                    value = current_line.iloc[line_index]

                    # skipping NaN values
                    if np.isnan(value):
                        continue

                    # increment all indexes by one,
                    while self.row_sum_criteria():
                        self.possibilities_table[table_index].iloc[row_index, line_index] += 1

                    # if it doesn't match, revert one
                    else:
                        self.possibilities_table[table_index].iloc[row_index, line_index] -= 1

        # calculation of the final criteria
        self.row_sum_criteria()


# -------------------------------------------------------------
# users' input ------------------------------------------------
originals_sheets = [1000, 900, 790]  # mother
inherited_sheets = [780, 727, 575, 520, 467, 314, 150]  # child
# -------------------------------------------------------------

if __name__ == "__main__":

    # optimizer object definition
    opt = CutterOptimizer(originals_sheets, inherited_sheets)

    # running optimization
    opt.optimizer()

    # printin results by original sheets
    for item in range(len(opt.possibilities_table)):
        print('\n*** ----')
        print(f'*** Original Coil Stock Length: {originals_sheets[item]} [mm]\n')
        print(opt.possibilities_table[item])
        print(f'\n**  Loss Results:\n    {str(opt.sum_criteria_calculations[item])[1:-1]} [mm]')
