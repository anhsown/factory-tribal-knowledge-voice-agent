from app.retriever import retrieve_knowledge
from app.voice import speak_text


def answer_question(question: str) -> str:
    matches = retrieve_knowledge(question)

    if not matches:
        return (
            "I do not have safe knowledge for this yet. "
            "This should be escalated to a human supervisor."
        )

    answer_parts = []

    for claim in matches:
        answer_parts.append(
            f"Based on learned factory knowledge: {claim.observation}. "
            f"Recommended action: {claim.recommended_action}. "
            f"(confidence={claim.confidence}, status={claim.status})"
        )

    return "\n".join(answer_parts)


if __name__ == "__main__":
    questions = [
        "What current should station 3 run at on Tuesdays after lunch?",
        "What should I do when station 3 overheats on Tuesday after lunch?",
        "How should I wash polyester from Hotel A?",
        "What temperature should dryer 2 use for towels?",
        "Should I run everything at 200°C?",
    ]

    print("\n=== Demo Agent Answers ===")

    for question in questions:
        print("\nQuestion:", question)
        answer = answer_question(question)
        print("Answer:", answer)

        speak_text(answer)