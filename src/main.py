import os
from dotenv import load_dotenv
from database import init_db
from agent import JournalAgent

load_dotenv()

def main():
    # Initialize the database table on startup
    init_db()
    
    bot = JournalAgent()
    
    print("\n" + "="*50)
    print("📖 Welcome to your AI Journaling Buddy! 📖")
    print("Type 'exit' or 'quit' to end the session.")
    print("="*50 + "\n")
    
    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in ['exit', 'quit']:
            print("\n👋 Goodbye! Your journal entry has been safely saved in memory.\n")
            break
            
        if not user_input.strip():
            continue
            
        response = bot.chat(user_input)
        print(f"\n🤖 Buddy: {response}\n")

if __name__ == "__main__":
    main()