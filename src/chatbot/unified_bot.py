import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.chatbot.rule_based_bot import HRChatbot
from src.chatbot.rag_bot import HRPolicyRAGBot
from src.chatbot.rule_based_bot import HRChatbot
from src.chatbot.rag_bot import HRPolicyRAGBot

# Keywords jo policy-related sawal identify karte hain
POLICY_KEYWORDS = [
    "leave", "policy", "notice period", "resign", "resignation",
    "work from home", "wfh", "overtime policy", "benefit", "insurance",
    "performance review", "code of conduct", "training", "exit process",
    "settlement", "working hours",
]

# Keywords jo data-related sawal identify karte hain
DATA_KEYWORDS = [
    "attrition rate", "average salary", "average income", "average age",
    "how many employee", "total employee", "headcount", "department list",
    "overtime rate",
]

class UnifiedHRChatbot:
    def __init__(self):
        print("Unified chatbot load ho raha hai (dono bots initialize ho rahe hain)...")
        self.rule_bot = HRChatbot()
        self.rag_bot = HRPolicyRAGBot()
        print("Unified chatbot ready hai!")

    def _is_policy_question(self, text):
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in POLICY_KEYWORDS)

    def _is_data_question(self, text):
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in DATA_KEYWORDS)

    def get_response(self, query):
        # Pehle check karo yeh policy sawal hai ya data sawal
        if self._is_policy_question(query) and not self._is_data_question(query):
            answer = self.rag_bot.ask(query)
            return f"📄 {answer}"

        # Default: data/stats related sawal → rule-based bot try karo
        response = self.rule_bot.get_response(query)

        # Agar rule-based bot ko intent match nahi mila, RAG bot try karo (fallback)
        if "Sorry, mujhe yeh sawal samajh nahi aaya" in response:
            rag_answer = self.rag_bot.ask(query)
            return f"📄 {rag_answer}"

        return f"📊 {response}"


# Quick test
if __name__ == "__main__":
    bot = UnifiedHRChatbot()

    test_questions = [
        "What is the attrition rate?",
        "What is the leave policy?",
        "Average salary in Sales department?",
        "What is the notice period?",
    ]

    for q in test_questions:
        print(f"\nQ: {q}")
        print(f"A: {bot.get_response(q)}")