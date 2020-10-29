import pandas as pd
import numpy as np
import os


class InitialCases:
    def __init__(self, area_codes, not_home_probs, data_dir="microsim/opencl/data/"):
        """
        Seeds initial infections by assigning initial cases based on the GAM assigned cases data.
        The cases for the first num_seed_days days are all seeded at once, eg. they are in the snapshot before the
        simulation is run.
        Initial cases are assigned to people from higher risk area codes who spend more time outside of their home.
        """

        # load initial case data
        self.initial_cases = pd.read_csv(os.path.join(data_dir, "devon_initial_cases.csv"))

        msoa_risks_df = pd.read_csv(os.path.join(data_dir, "msoas.csv"), usecols=[1, 2])

        # combine into a single dataframe to allow easy filtering based on high risk area codes and
        # not home probabilities
        people_df = pd.DataFrame({"area_code": area_codes,
                                  "not_home_prob": not_home_probs})
        people_df = people_df.merge(msoa_risks_df, on="area_code")

        # get people_ids for people in high risk MSOAs and high not home probability
        self.high_risk_ids = np.where((people_df["risk"] == "High") & (people_df["not_home_prob"] > 0.3))[0]

    def get_seed_people_ids_for_day(self, day):
        # randomly choose a given number of cases from the high risk people ids.
        num_cases = self.initial_cases.loc[day, "num_cases"]
        selected_ids = np.random.choice(self.high_risk_ids, num_cases, replace=False)

        # remove people from high_risk_ids so they are not chosen again
        self.high_risk_ids = np.setdiff1d(self.high_risk_ids, selected_ids)

        return selected_ids
