"""
chatbot.py
Career AI Assistant

Version 1
"""

import os
import random
import pandas as pd

############################################################
# LOAD DATASETS
############################################################

class CareerChatbot:

    def __init__(self):

        self.career_df = pd.DataFrame()
        self.university_df = pd.DataFrame()

        self.conversation = []

        self.greetings = [

            "Hello! 👋",
            "Hi there!",
            "Welcome!",
            "Nice to meet you!",
            "Hey! Ready to explore careers?"

        ]

        self.default_responses = [

            "Could you tell me a little more?",

            "Interesting! Tell me more about what you enjoy.",

            "I'm here to help you discover your perfect career.",

            "Let's figure out what career suits you best!"

        ]

    ########################################################

    def load_data(

            self,

            career_file,

            university_file=None

    ):

        self.career_df = pd.read_excel(career_file)

        if university_file:

            self.university_df = pd.read_excel(university_file)

    ########################################################

    def remember(self, speaker, message):

        self.conversation.append({

            "speaker": speaker,

            "message": message

        })

        if len(self.conversation) > 20:

            self.conversation.pop(0)

    ########################################################

    def latest_messages(self):

        return self.conversation

    ########################################################

    def greeting(self):

        return random.choice(self.greetings)

    ########################################################

    def search_career(self, keyword):

        if self.career_df.empty:

            return None

        keyword = keyword.lower()

        for _, row in self.career_df.iterrows():

            text = " ".join(

                [str(v).lower() for v in row.values]

            )

            if keyword in text:

                return row

        return None

    ########################################################

    def search_university(self, keyword):

        if self.university_df.empty:

            return None

        keyword = keyword.lower()

        for _, row in self.university_df.iterrows():

            text = " ".join(

                [str(v).lower() for v in row.values]

            )

            if keyword in text:

                return row

        return None

    ########################################################

    def answer(self, message):

        self.remember("user", message)

        text = message.lower()

        ####################################################

        if "hello" in text or "hi" in text:

            response = self.greeting()

            self.remember("assistant", response)

            return response

        ####################################################

        if "career" in text:

            response = (

                "There are hundreds of careers available. "

                "Tell me what subjects or hobbies you enjoy "

                "and I'll help you find careers that match."

            )

            self.remember("assistant", response)

            return response

        ####################################################

        if "university" in text:

            response = (

                "I can recommend universities based on "

                "your dream career."

            )

            self.remember("assistant", response)

            return response

        ####################################################

        if "salary" in text:

            response = (

                "Salary depends on the country, experience, "

                "education and industry."

            )

            self.remember("assistant", response)

            return response

        ####################################################

        result = self.search_career(text)

        if result is not None:

            response = ""

            for column in self.career_df.columns[:8]:

                response += f"{column}: {result[column]}\n"

            self.remember("assistant", response)

            return response

        ####################################################

        response = random.choice(self.default_responses)

        self.remember("assistant", response)

        return response


############################################################

if __name__ == "__main__":

    bot = CareerChatbot()

    bot.load_data(

        "datasets/comprehensive_career_dataset_mongolia_2026.xlsx",

        "datasets/university_and_career_300plus.xlsx"

    )

    while True:

        question = input("You: ")

        if question.lower() == "quit":

            break

        print("Bot:", bot.answer(question))
            ########################################################
    # PERSONALITY-BASED RECOMMENDATIONS
    ########################################################

    def recommend_from_personality(self, personality):

        personality = personality.lower()

        recommendations = {

            "creative": [
                "Graphic Designer",
                "Animator",
                "Game Designer",
                "Architect",
                "UI/UX Designer"
            ],

            "analytical": [
                "Software Engineer",
                "Data Scientist",
                "Cybersecurity Analyst",
                "AI Engineer",
                "Research Scientist"
            ],

            "social": [
                "Teacher",
                "Psychologist",
                "Doctor",
                "Nurse",
                "Social Worker"
            ],

            "leader": [
                "CEO",
                "Business Manager",
                "Marketing Director",
                "Entrepreneur",
                "Project Manager"
            ],

            "practical": [
                "Mechanical Engineer",
                "Electrician",
                "Pilot",
                "Civil Engineer",
                "Construction Manager"
            ]

        }

        for key in recommendations:

            if key in personality:

                return recommendations[key]

        return [

            "Software Engineer",

            "Business Analyst",

            "Doctor",

            "Teacher",

            "Accountant"

        ]

    ########################################################
    # SUBJECT RECOMMENDATION
    ########################################################

    def recommend_from_subjects(self, subjects):

        careers = []

        for subject in subjects:

            s = subject.lower()

            if "math" in s:

                careers.extend([

                    "Engineer",

                    "Data Scientist",

                    "Actuary",

                    "Economist"

                ])

            elif "biology" in s:

                careers.extend([

                    "Doctor",

                    "Dentist",

                    "Veterinarian",

                    "Pharmacist"

                ])

            elif "chemistry" in s:

                careers.extend([

                    "Chemical Engineer",

                    "Pharmacist",

                    "Scientist"

                ])

            elif "physics" in s:

                careers.extend([

                    "Engineer",

                    "Astronomer",

                    "Pilot"

                ])

            elif "art" in s:

                careers.extend([

                    "Animator",

                    "Graphic Designer",

                    "Fashion Designer",

                    "Illustrator"

                ])

            elif "english" in s:

                careers.extend([

                    "Journalist",

                    "Lawyer",

                    "Teacher",

                    "Author"

                ])

            elif "computer" in s:

                careers.extend([

                    "Software Engineer",

                    "AI Engineer",

                    "Cybersecurity Specialist",

                    "Web Developer"

                ])

        return list(set(careers))

    ########################################################
    # TOP UNIVERSITY SEARCH
    ########################################################

    def university_recommendation(self, career):

        if self.university_df.empty:

            return []

        results = []

        career = career.lower()

        for _, row in self.university_df.iterrows():

            text = " ".join(

                [str(v).lower() for v in row.values]

            )

            if career in text:

                results.append(

                    row.iloc[0]

                )

        return results[:5]

    ########################################################
    # SALARY ESTIMATION
    ########################################################

    def salary_estimate(self, career):

        estimates = {

            "software engineer":"$70,000 - $180,000",

            "doctor":"$80,000 - $350,000",

            "teacher":"$35,000 - $90,000",

            "pilot":"$90,000 - $250,000",

            "lawyer":"$70,000 - $250,000",

            "architect":"$60,000 - $150,000",

            "ai engineer":"$120,000 - $250,000",

            "data scientist":"$100,000 - $220,000"

        }

        career = career.lower()

        for key in estimates:

            if key in career:

                return estimates[key]

        return "Salary varies depending on country and experience."

    ########################################################
    # FUTURE DEMAND SCORE
    ########################################################

    def future_demand(self, career):

        career = career.lower()

        high = [

            "software",

            "ai",

            "cyber",

            "robot",

            "data",

            "doctor",

            "renewable"

        ]

        medium = [

            "teacher",

            "lawyer",

            "engineer",

            "architect"

        ]

        for item in high:

            if item in career:

                return "★★★★★ Excellent Future Demand"

        for item in medium:

            if item in career:

                return "★★★★☆ High Future Demand"

        return "★★★☆☆ Stable Demand"