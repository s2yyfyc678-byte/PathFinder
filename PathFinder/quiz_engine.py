import random
from collections import defaultdict

class QuizEngine:

    def __init__(self):

        ###########################################################
        # RIASEC MODEL
        ###########################################################

        self.categories = {
            "R": "Realistic",
            "I": "Investigative",
            "A": "Artistic",
            "S": "Social",
            "E": "Enterprising",
            "C": "Conventional"
        }

        ###########################################################
        # QUESTIONS
        ###########################################################

        self.questions = [

            {
                "id":1,
                "question":"I enjoy solving difficult problems.",
                "type":"I"
            },

            {
                "id":2,
                "question":"I like drawing or designing things.",
                "type":"A"
            },

            {
                "id":3,
                "question":"I enjoy helping people.",
                "type":"S"
            },

            {
                "id":4,
                "question":"I enjoy fixing machines.",
                "type":"R"
            },

            {
                "id":5,
                "question":"I like leading groups.",
                "type":"E"
            },

            {
                "id":6,
                "question":"I enjoy organizing information.",
                "type":"C"
            },

            {
                "id":7,
                "question":"Technology excites me.",
                "type":"I"
            },

            {
                "id":8,
                "question":"I enjoy making videos or music.",
                "type":"A"
            },

            {
                "id":9,
                "question":"I enjoy teaching others.",
                "type":"S"
            },

            {
                "id":10,
                "question":"I like building things.",
                "type":"R"
            },

            {
                "id":11,
                "question":"I like starting new projects.",
                "type":"E"
            },

            {
                "id":12,
                "question":"I enjoy spreadsheets and numbers.",
                "type":"C"
            }

        ]

    #############################################################

    def get_questions(self):

        return self.questions

    #############################################################

    def calculate_scores(self, answers):

        """
        answers format

        {
            1:5,
            2:3,
            3:4
        }

        """

        scores = defaultdict(int)

        for question in self.questions:

            qid = question["id"]

            qtype = question["type"]

            if qid in answers:

                scores[qtype] += answers[qid]

        return scores

    #############################################################

    def personality_type(self, scores):

        ordered = sorted(

            scores.items(),

            key=lambda x:x[1],

            reverse=True

        )

        return ordered

    #############################################################

    def strongest_traits(self, scores):

        ordered = self.personality_type(scores)

        traits = []

        for code, value in ordered[:3]:

            traits.append(self.categories[code])

        return traits

    #############################################################

    def interests(self, scores):

        traits = self.strongest_traits(scores)

        interests = []

        if "Investigative" in traits:

            interests.extend([
                "technology",
                "science",
                "engineering",
                "research",
                "robotics"
            ])

        if "Artistic" in traits:

            interests.extend([
                "design",
                "music",
                "animation",
                "film",
                "photography"
            ])

        if "Social" in traits:

            interests.extend([
                "teaching",
                "psychology",
                "medicine",
                "communication"
            ])

        if "Enterprising" in traits:

            interests.extend([
                "business",
                "marketing",
                "finance",
                "leadership"
            ])

        if "Realistic" in traits:

            interests.extend([
                "construction",
                "mechanics",
                "aviation",
                "electronics"
            ])

        if "Conventional" in traits:

            interests.extend([
                "accounting",
                "office",
                "administration",
                "banking"
            ])

        return list(set(interests))

    #############################################################

    def skills(self, scores):

        skills = []

        ordered = self.strongest_traits(scores)

        for trait in ordered:

            if trait == "Investigative":

                skills.extend([
                    "critical thinking",
                    "problem solving",
                    "coding",
                    "analysis"
                ])

            elif trait == "Artistic":

                skills.extend([
                    "creativity",
                    "design",
                    "storytelling",
                    "innovation"
                ])

            elif trait == "Social":

                skills.extend([
                    "communication",
                    "teamwork",
                    "leadership",
                    "empathy"
                ])

            elif trait == "Enterprising":

                skills.extend([
                    "negotiation",
                    "business",
                    "management",
                    "sales"
                ])

            elif trait == "Realistic":

                skills.extend([
                    "technical",
                    "engineering",
                    "mechanical",
                    "repair"
                ])

            elif trait == "Conventional":

                skills.extend([
                    "organization",
                    "planning",
                    "documentation",
                    "accuracy"
                ])

        return list(set(skills))

    #############################################################

    def generate_profile(self, answers):

        scores = self.calculate_scores(answers)

        profile = {

            "scores": dict(scores),

            "top_traits": self.strongest_traits(scores),

            "interests": self.interests(scores),

            "skills": self.skills(scores)

        }

        return profile

###############################################################

if __name__ == "__main__":

    engine = QuizEngine()

    demo_answers = {

        1:5,
        2:4,
        3:2,
        4:3,
        5:4,
        6:2,
        7:5,
        8:5,
        9:2,
        10:3,
        11:4,
        12:1

    }

    profile = engine.generate_profile(demo_answers)

    print(profile)