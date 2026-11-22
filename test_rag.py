
from rag_pipeline import ask_question


def start_chat():

    print("\n====================================")
    print("          CHAT WITH PDF")
    print("====================================")

    print("\nAsk questions about your uploaded PDF.")
    print("Type 'exit' to close the chatbot.")
    print("------------------------------------")

    while True:

        question = input("\nYou: ").strip()

        # Exit condition
        if question.lower() in ["exit", "quit", "bye"]:
            print("\nThank you for using Chat With PDF!")
            break

        # Empty question handling
        if not question:
            print("Please enter a valid question.")
            continue

        try:

            print("\nAI is thinking...")

            answer = ask_question(question)

            print("\n========== AI ANSWER ==========")
            print(answer)
            print("===============================")

        except Exception as e:

            print("\nSomething went wrong:")
            print(e)


if __name__ == "__main__":
    start_chat()
