import pandas as pd
import re

class HRChatbot:
    def __init__(self, data_path="data/processed/hr_cleaned.csv"):
        self.df = pd.read_csv(data_path)
        self.df.columns = [c.strip() for c in self.df.columns]

    def _match_department(self, text):
        """Text me se department name dhoondo"""
        departments = self.df['Department'].unique()
        for dept in departments:
            if dept.lower() in text.lower():
                return dept
        return None

    def _match_gender(self, text):
        if "male" in text.lower() and "female" not in text.lower():
            return "Male"
        if "female" in text.lower():
            return "Female"
        return None

    def get_response(self, query):
        text = query.lower().strip()

        # Intent 1: Total employees / headcount
        if re.search(r"(total|how many).*(employee|headcount|staff)", text):
            dept = self._match_department(text)
            if dept:
                count = self.df[self.df['Department'] == dept].shape[0]
                return f"{dept} department me total {count} employees hain."
            count = self.df.shape[0]
            return f"Total {count} employees hain company me."

        # Intent 2: Attrition rate
        if "attrition" in text or "leaving" in text or "resign" in text:
            dept = self._match_department(text)
            if dept:
                subset = self.df[self.df['Department'] == dept]
                rate = (subset['Attrition'] == 'Yes').mean() * 100
                return f"{dept} department ka attrition rate {rate:.1f}% hai."
            rate = (self.df['Attrition'] == 'Yes').mean() * 100
            return f"Overall company attrition rate {rate:.1f}% hai."

        # Intent 3: Average salary/income
        if "salary" in text or "income" in text or "pay" in text:
            dept = self._match_department(text)
            gender = self._match_gender(text)
            subset = self.df.copy()
            label = "Overall"
            if dept:
                subset = subset[subset['Department'] == dept]
                label = dept
            if gender:
                subset = subset[subset['Gender'] == gender]
                label += f" ({gender})"
            avg_income = subset['MonthlyIncome'].mean()
            return f"{label} ka average monthly income ₹{avg_income:,.0f} hai."

        # Intent 4: Average age
        if "age" in text:
            dept = self._match_department(text)
            subset = self.df.copy()
            label = "Overall"
            if dept:
                subset = subset[subset['Department'] == dept]
                label = dept
            avg_age = subset['Age'].mean()
            return f"{label} employees ki average age {avg_age:.1f} years hai."

        # Intent 5: Overtime related
        if "overtime" in text:
            rate = (self.df['OverTime'] == 'Yes').mean() * 100
            return f"{rate:.1f}% employees overtime karte hain."

        # Intent 6: Department list
        if "department" in text and ("list" in text or "which" in text or "all" in text):
            depts = ", ".join(self.df['Department'].unique())
            return f"Company ke departments hain: {depts}"

        # Fallback: koi intent match nahi hua
        return (
            "Sorry, mujhe yeh sawal samajh nahi aaya 🤔. "
            "Aap pooch sakte hain jaise: 'What is the attrition rate in Sales?', "
            "'Average salary in R&D department?', 'How many employees in HR?'"
        )


# Quick test (yeh file directly run karne par chalega)
if __name__ == "__main__":
    bot = HRChatbot()
    test_queries = [
        "What is the attrition rate?",
        "Average salary in Sales department",
        "How many employees in Research & Development",
        "average age",
    ]
    for q in test_queries:
        print(f"Q: {q}")
        print(f"A: {bot.get_response(q)}")
        print()