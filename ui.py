from pathlib import Path
import json

import streamlit as st

from app.pipeline import process_transcripts_file
from app.storage import load_claims
from app.demo_agent import answer_question
from app.models import ClaimStatus
from app.voice import text_to_speech_file

DB_PATH = Path('knowledge_base.json')
TRANSCRIPTS_PATH = Path('data/transcripts.jsonl')

st.set_page_config(
    page_title='Factory Tribal Knowledge Agent',
    page_icon='🤖',
    layout='wide'
)

def reset_knowledge_base():
    if DB_PATH.exists():
        DB_PATH.unlink()

def load_transcripts():
    if not TRANSCRIPTS_PATH.exists():
        return []
    transcripts = []
    with open(TRANSCRIPTS_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                transcripts.append(json.loads(line))
    
    return transcripts

def status_badge(status):
    status_value = str(status)

    if 'verified' in status_value:
        return '✅ Verified'
    if 'candidate' in status_value:
        return '🟡 Candidate'
    if 'conflicting' in status_value:
        return '⚠️ Conflicting'
    if 'quarantined' in status_value:
        return '🟠 Quarantined'
    if 'rejected' in status_value:
        return '❌ Rejected'
    
    return status_value   

def render_claim_card(claim):
    with st.container(border=True):
        col1, col2, col3 = st.columns([2, 2, 1])

        with col1:
            st.markdown(f'### "{claim.entity}"')
            st.write(f'**Process:** {claim.process}')
            st.write(f'**Condition:** {claim.condition}')

        with col2:
            st.write(f'**Observation:** {claim.observation}')
            st.write(f'**Recommended Action:** {claim.recommended_action}')
            st.write(f'**Source Worker:** "{claim.source_worker_id}"')

        with col3:
            st.metric('Confidence', f'{claim.confidence:.2f}')
            st.write(status_badge(claim.status))

        with st.expander('View provenance'):
            st.write(f'**Transcript ID:** {claim.source_transcript_id}')
            st.write(f'**Quote:** "{claim.source_quote}"')

            if claim.contradicts:
                st.write('**Contradicts Claims:**')
                for item in claim.contradicts:
                    st.code(item)

def run_evaluation():
    eval_path = Path("data/eval_questions.json")

    if not eval_path.exists():
        return [], 0.0

    with open(eval_path, "r", encoding="utf-8") as f:
        questions = json.load(f)

    results = []
    correct_count = 0

    for item in questions:
        question = item["question"]
        expected_keyword = item["expected_keyword"]

        answer = answer_question(question)
        is_correct = expected_keyword.lower() in answer.lower()

        if is_correct:
            correct_count += 1

        results.append(
            {
                "question": question,
                "answer": answer,
                "expected_keyword": expected_keyword,
                "correct": is_correct,
            }
        )

    accuracy = correct_count / len(questions) if questions else 0.0
    return results, accuracy


st.title('🏭 Factory Tribal Knowledge Agent')
st.caption(
    'A demo system for learning unwritten factory knowledge from worker conversations'
    'Without poisoning the agent\'s knowledge base'
)

tab1, tab2, tab3, tab4 = st.tabs(
    [
        '1. Transcripts',
        '2. Knowledge Base',
        '3. Demo Agent',
        '4. Evaluation'
    ]
)

with tab1:
    st.header('Worker Coversations Transcripts')

    st.write(
        'These transcripts are simulate worker corrections, tribal knowledge, conflicts, '
        'and unsafe/joke-line claims'
    )

    transcripts = load_transcripts()

    if not transcripts:
        st.warning('No transcripts found. Please check data/transcripts.jsonl')
    else:
        for transcript in transcripts:
            with st.container(border=True):
                st.markdown(f'### "{transcript["transcript_id"]}"')
                st.write(f"**Worker:** `{transcript['worker_id']}`")
                st.write(transcript["text"])
    
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Reset Knowledge Base", type="secondary"):
            reset_knowledge_base()
            st.success("Knowledge base reset.")

    with col2:
        if st.button("Process Transcripts", type="primary"):
            reset_knowledge_base()
            claims = process_transcripts_file()
            st.success(f"Processed {len(claims)} claims.")

with tab2:
    st.header("Structured Knowledge Base")

    claims = load_claims()

    if not claims:
        st.info("Knowledge base is empty. Go to the Transcripts tab and click Process Transcripts.")
    else:
        total = len(claims)
        verified = len([c for c in claims if c.status == ClaimStatus.VERIFIED])
        candidate = len([c for c in claims if c.status == ClaimStatus.CANDIDATE])
        conflicting = len([c for c in claims if c.status == ClaimStatus.CONFLICTING])
        quarantined = len([c for c in claims if c.status == ClaimStatus.QUARANTINED])

        col1, col2, col3, col4, col5 = st.columns(5)

        col1.metric("Total Claims", total)
        col2.metric("Verified", verified)
        col3.metric("Candidate", candidate)
        col4.metric("Conflicting", conflicting)
        col5.metric("Quarantined", quarantined)

        st.divider()

        status_filter = st.selectbox(
            "Filter by status",
            ["All", "candidate", "verified", "conflicting", "quarantined", "rejected"],
        )

        filtered_claims = claims

        if status_filter != "All":
            filtered_claims = [
                claim for claim in claims
                if str(claim.status).endswith(status_filter)
            ]

        for claim in filtered_claims:
            render_claim_card(claim)


with tab3:
    st.header("Demo Agent")

    st.write(
        "Ask questions to see whether the agent retrieves safe learned knowledge "
        "or escalates unsafe/conflicting cases."
    )

    sample_questions = [
        "What current should station 3 run at on Tuesdays after lunch?",
        "What should I do when station 3 overheats on Tuesday after lunch?",
        "How should I wash polyester from Hotel A?",
        "What temperature should dryer 2 use for towels?",
        "Should I run everything at 200°C?",
    ]

    selected_question = st.selectbox("Try a sample question", sample_questions)

    custom_question = st.text_input(
        "Or type your own question",
        value=selected_question,
    )

    if st.button("Ask Agent", type="primary"):
        answer = answer_question(custom_question)

        st.markdown("### Answer")
        st.write(answer)

        audio_path = text_to_speech_file(answer, 'agent_answer.wav')

        st.markdown("### Voice Response")
        st.audio(audio_path)

        if "human supervisor" in answer.lower():
            st.warning("The system refused to guess because the knowledge is unsafe, missing, or conflicting.")
        else:
            st.success("The system answered using safe learned knowledge.")


with tab4:
    st.header("Evaluation")

    st.write(
        "This checks whether the agent retrieves safe learned knowledge and refuses "
        "conflicting or quarantined knowledge."
    )

    if st.button("Run Evaluation", type="primary"):
        results, accuracy = run_evaluation()

        st.metric("Accuracy", f"{accuracy:.2%}")

        for result in results:
            with st.container(border=True):
                st.write(f"**Question:** {result['question']}")
                st.write(f"**Answer:** {result['answer']}")
                st.write(f"**Expected keyword:** `{result['expected_keyword']}`")

                if result["correct"]:
                    st.success("Correct")
                else:
                    st.error("Incorrect")