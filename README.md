# Factory Tribal Knowledge Voice Agent

A prototype voice-enabled factory knowledge agent that learns operational tips from worker transcripts, extracts useful tribal knowledge, detects unsafe or conflicting claims, and answers worker questions without blindly trusting unverified information.

This project was built for the Minder AI SWE/AI Engineer technical challenge.

---

## 1. Problem

Factory workers often know practical operational details that are never formally documented, for example:

- "Station 3 overheats after lunch on Tuesdays."
- "Polyester from Hotel A shrinks unless we separate it and use a cooler cycle."
- "Dryer 2 should run at 80°C."
- "Actually, dryer 2 should run at 72°C."

The challenge is not only to capture this knowledge, but to integrate it safely.

A naive assistant would immediately store and use every claim. That can poison the knowledge base with:

- unsafe instructions,
- low-confidence claims,
- duplicate claims,
- contradictory claims,
- vague claims,
- unverified worker knowledge.

This prototype focuses on building a safety-aware knowledge ingestion pipeline.

---

## 2. What This Prototype Does

The system can:

1. Read worker transcript examples.
2. Extract structured knowledge claims.
3. Assign each claim a confidence score.
4. Mark claims as:
   - `candidate`
   - `verified`
   - `conflicting`
   - `quarantined`
5. Store accepted claims in a JSON knowledge base.
6. Answer worker questions using only safe knowledge.
7. Escalate risky or conflicting cases to a human supervisor.
8. Run a small evaluation suite.
9. Provide a Streamlit demo UI.
10. Support a simple voice-style demo flow.

---

## 3. Core Design Principle

The main design goal is:

> Learn from workers, but do not blindly trust everything workers say.

The agent only answers from knowledge that is considered usable. If a claim is unsafe, low-confidence, unknown, or conflicting, the agent refuses to give an operational recommendation and escalates to a human supervisor.

Example:

```text```
Question:
Should I run everything at 200°C?

Answer:
I do not have safe knowledge for this yet. This should be escalated to a human supervisor.

## 4. Architecture

Worker Transcript
        |
        v
Claim Extractor
        |
        v
KnowledgeClaim object
        |
        v
Conflict / Safety Resolver
        |
        v
Knowledge Base JSON
        |
        v
Demo Agent / Voice UI
        |
        v
Safe Answer or Human Escalation

### Main Components
app/
  main.py                 Runs the transcript processing pipeline
  pipeline.py             Orchestrates extraction, validation, conflict detection, and storage
  extractor.py            Converts transcript text into structured claims
  conflict_resolver.py    Detects unsafe or conflicting knowledge
  storage.py              Loads and saves the JSON knowledge base
  demo_agent.py           Answers user questions from safe stored knowledge

eval/
  run_eval.py             Runs a small evaluation suite

ui.py                     Streamlit demo interface
requirements.txt          Python dependencies
knowledge_base.json       Generated local knowledge base

## 5. Knowledge Claim Schema

Each extracted claim is represented as a structured object.

Example:

{
  "claim_id": "example-id",
  "topic": "station_3",
  "condition": "Station 3 overheats after lunch on Tuesdays",
  "recommendation": "drop current by 5%",
  "confidence": 0.7,
  "status": "candidate",
  "source_transcript_id": "transcript_001",
  "created_at": "2026-05-13T10:00:00"
}

Important fields:

| Field                  | Meaning                                              |
| ---------------------- | ---------------------------------------------------- |
| `topic`                | The machine, process, or material the claim is about |
| `condition`            | When or why the knowledge applies                    |
| `recommendation`       | The action suggested by the worker                   |
| `confidence`           | Estimated trust level                                |
| `status`               | Safety state of the claim                            |
| `source_transcript_id` | Where the claim came from                            |

## 6. Safety and Conflict Handling

The prototype use simple but clear rules.

**Candidate**

A claim is marked as candidate when it appears useful but is not fully verified.

Example:

station_3 | candidate | drop current by 5%

**Verified**

A claim can become verified when repeated or reinforced by another compatible source.

Example:

hotel_a_polyester | verified | separate it and use a cooler cycle

**Conflicting**

A claim is marked as conflicting when multiple different recommendations exist for the same topic.

Example:

dryer_2_towels | conflicting | run dryer 2 at 80°C
dryer_2_towels | conflicting | run dryer 2 at 72°C

In this case, the agent does not choose one. It escalates.

**Quarantined**

A claim is marked as quarantined when it is unsafe, vague, or too risky.

Example:

unknown | quarantined | run everything at 200°C

## 7. How to run locally

**Step 1: Clone the repo**

git clone <[repo-url](https://github.com/anhsown/factory-tribal-knowledge-voice-agent)>
cd factory-tribal-knowledge-agent

**Step 2: Create a virtual environment**

Windows PowerShell:

python -m venv .venv
.venv\Scripts\activate

macOS / Linux:

python -m venv .venv
source .venv/bin/activate

**Step 3: Install dependencies**

pip install -r requirements.txt

**Step 4: Reset the local knowledge base**

Windows PowerShell:

Remove-Item knowledge_base.json -ErrorAction SilentlyContinue

macOS / Linux:

rm -f knowledge_base.json

**Step 5: Run the ingestion pipeline**

python -m app.main

*Expected output*:

Processed Claims:
- station_3 | candidate | drop current by 5%
- hotel_a_polyester | candidate | separate it and use a cooler cycle
- dryer_2_towels | candidate | run dryer 2 at 80°C
- dryer_2_towels | conflicting | run dryer 2 at 72°C
- unknown | quarantined | run everything at 200°C

**Step 6: Run the demo agent**

python -m app.demo_agent

*Expected behavior:*

Question: What should I do when station 3 overheats on Tuesday after lunch?
Answer: Based on learned factory knowledge: Station 3 overheats. Recommended action: drop current by 5%.

Question: What temperature should dryer 2 use for towels?
Answer: I do not have safe knowledge for this yet. This should be escalated to a human supervisor.

**Step 7: Run evalation**

python -m eval.run_eval

*Expected result:*

=== Result ===
Accuracy: 100.00%

**8. Run the Streamlit Demo UI**

Start the UI with:

streamlit run ui.py

The UI allows you to:

* process the transcript examples,
* inspect the generated knowledge base,
* ask the demo agent questions,
* run evaluation,
* test the voice-style interaction flow.

Recommended demo questions:

What should I do when station 3 overheats on Tuesday after lunch?
How should I wash polyester from Hotel A?
What temperature should dryer 2 use for towels?
Should I run everything at 200°C?

**9. Voice Demo**

The challenge asks for a voice agent. This prototype supports a simple voice-oriented demo flow around the same safety-aware reasoning pipeline.

The intended interaction is:

Worker speaks a question
        |
        v
Speech-to-text / text input
        |
        v
Demo agent retrieves safe knowledge
        |
        v
Answer generated
        |
        v
Text-to-speech response

For reliability, the core demo can also run in text mode. The important part is that the same reasoning and safety rules are used for both text and voice.

**10. Evaluation**

The evaluation checks whether the assistant gives the correct behavior for known cases.

Example evaluation cases:

| Question                | Expected Behavior                 |
| ----------------------- | --------------------------------- |
| Station 3 overheats     | Recommend dropping current by 5%  |
| Hotel A polyester       | Recommend separate + cooler cycle |
| Dryer 2 towels          | Escalate because of conflict      |
| Run everything at 200°C | Escalate because unsafe           |

Current local result:

Accuracy: 100.00%

**11. Design Tradeoffs**

This is a prototype, not a finished production system.

*What I prioritized*
* Clear reasoning pipeline
* Structured claim extraction
* Human escalation for risky cases
* Conflict detection
* Demoability
* Simple local storage
* Easy-to-read code and README

*What I intentionally kept simple*
* Rule-based extraction instead of a full LLM extraction service
* JSON file storage instead of a database
* Small handcrafted evaluation set
* Simple confidence scoring
* Local Streamlit demo instead of production deployment

**12. Future Improvements**

*With more time, I would improve the system by adding:*

* Real-time microphone streaming.
* Production-grade speech-to-text.
* Better LLM-based claim extraction.
* Human review dashboard.
* Audit trails for every accepted or rejected claim.
* Role-based approval for dangerous operational changes.
* Vector search over historical knowledge.
* Database storage instead of JSON.
* More robust conflict clustering.
* Continuous evaluation with real factory transcripts

**13. Why This Is More Than a Wrapper**

A simple wrapper would just send worker text to an LLM and return an answer.

This prototype adds a safety layer:

* it extracts structured claims,
* tracks source transcripts,
* assigns confidence,
* detects conflicts,
* quarantines unsafe claims,
* refuses uncertain recommendations,
* escalates to humans when needed.

That is the beginning of a moat: the system learns operational knowledge while preserving trust and safety.

**14. Tech Stack**

* Python
* Pydantic
* Streamlit
* JSON local storage
* Simple rule-based evaluation
* Optional voice input / output layer

**15. Submission Notes**

This repository includes:

* working backend pipeline,
* local knowledge base generation,
* demo agent,
* evaluation script,
* Streamlit UI,
* README with setup instructions,
* architecture explanation for interview discussion.
