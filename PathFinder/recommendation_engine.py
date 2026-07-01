import pandas as pd
import numpy as np
import os

class CareerRecommendationEngine:

    def __init__(self):

        self.career_data = pd.DataFrame()
        self.university_data = pd.DataFrame()

    ##########################################################
    # LOAD DATASETS
    ##########################################################

    def load_data(
            self,
            career_file,
            university_file=None
    ):

        self.career_data = pd.read_excel(career_file)

        if university_file:

            self.university_data = pd.read_excel(university_file)

    ##########################################################
    # SAFE TEXT
    ##########################################################

    def clean(self, value):

        if pd.isna(value):

            return ""

        return str(value).lower()

    ##########################################################
    # SCORE MATCH
    ##########################################################

    def keyword_score(self, user_answers, career_text):

        score = 0

        career_text = self.clean(career_text)

        for answer in user_answers:

            if answer.lower() in career_text:

                score += 10

        return score

    ##########################################################
    # MAIN AI
    ##########################################################

    def recommend(

            self,

            interests,

            personality,

            skills,

            values

    ):

        recommendations = []

        if self.career_data.empty:

            return []

        for _, row in self.career_data.iterrows():

            score = 0

            row_text = " ".join([

                self.clean(v)

                for v in row.values

            ])

            ######################################

            score += self.keyword_score(

                interests,

                row_text

            )

            ######################################

            score += self.keyword_score(

                skills,

                row_text

            )

            ######################################

            score += self.keyword_score(

                values,

                row_text

            )

            ######################################

            if personality.lower() in row_text:

                score += 30

            ######################################

            salary_bonus = 0

            future_bonus = 0

            try:

                salary_bonus = int(score * 0.15)

            except:

                salary_bonus = 0

            try:

                future_bonus = int(score * 0.10)

            except:

                future_bonus = 0

            score += salary_bonus

            score += future_bonus

            ######################################

            recommendations.append({

                "career":

                row.iloc[0],

                "score":

                score

            })

        recommendations = sorted(

            recommendations,

            key=lambda x: x["score"],

            reverse=True

        )

        top3 = recommendations[:3]

        highest = top3[0]["score"]

        final = []

        for career in top3:

            compatibility = round(

                (career["score"] / highest) * 100,

                1

            )

            final.append({

                "career":

                career["career"],

                "compatibility":

                compatibility

            })

        return final

###############################################################
# EXAMPLE
###############################################################

if __name__ == "__main__":

    engine = CareerRecommendationEngine()

    engine.load_data(

        "datasets/comprehensive_career_dataset_mongolia_2026.xlsx"

    )

    result = engine.recommend(

        interests=[

            "technology",

            "gaming",

            "robotics"

        ],

        personality="creative",

        skills=[

            "coding",

            "problem solving"

        ],

        values=[

            "money",

            "innovation"

        ]

    )

    print(result)