import json

from app.demo_agent import answer_question


def run_eval():
    print("\n=== Evaluation ===")

    with open("data/eval_questions.json", "r", encoding="utf-8") as f:
        questions = json.load(f)

    correct = 0

    for item in questions:
        question = item["question"]
        expected_keyword = item["expected_keyword"]

        answer = answer_question(question)
        is_correct = expected_keyword.lower() in answer.lower()

        if is_correct:
            correct += 1

        print("\nQuestion:", question)
        print("Answer:", answer)
        print("Expected keyword:", expected_keyword)
        print("Correct:", is_correct)

    accuracy = correct / len(questions)

    print("\n=== Result ===")
    print(f"Accuracy: {accuracy:.2%}")


if __name__ == "__main__":
    run_eval()