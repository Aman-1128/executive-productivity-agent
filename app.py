import streamlit as st
import json
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(
    page_title="Executive Productivity Agent",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ---------------- CONFIGURATION ----------------

st.set_page_config(
    page_title="Executive Productivity Agent",
    page_icon="💼",
    layout="wide"
)
st.markdown(
    """
    <div style="
        padding: 24px 30px;
        border-radius: 16px;
        background: linear-gradient(135deg, #172554, #1e3a8a);
        margin-bottom: 20px;
    ">
        <h1 style="color: white; margin: 0;">
            🧠 Executive Productivity Agent
        </h1>
        <p style="color: #bfdbfe; font-size: 17px; margin: 8px 0 0;">
            AI-powered command center for priorities, meetings, commitments, and follow-ups
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.caption(
    "Executive: Arjun Malhotra  •  Role: VP Sales  •  Week: 21–25 September 2026"
)
st.caption("AI-powered assistant for managing meetings, commitments, emails, and weekly priorities.")
st.subheader("🎯 Weekly Priorities")

st.info(
    "Focus on the campaign deck review, vendor list submission, "
    "Meridian client call, and July expense variance report."
)


api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Gemini API key not found. Check your .env file.")
    st.stop()

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-3.6-flash")

# Load assignment data
with open("data.json", "r") as file:
    data = json.load(file)

# Conversation history
if "history" not in st.session_state:
    st.session_state.history = []


# ---------------- HEADER ----------------


st.caption("AI assistant for Arjun Malhotra, VP Sales")

st.divider()


# ---------------- SIDEBAR ----------------

with st.sidebar:
    if st.sidebar.button("🗑️ Clear Conversation"):
        st.session_state.history = []
        st.session_state.selected_question = ""
        st.rerun()

    st.header("👤 Executive Profile")

    st.write("**Name:** Arjun Malhotra")
    st.write("**Role:** VP Sales")

    st.divider()

    st.subheader("📋 Available Information")

    st.write("The agent can use:")
    st.write("- Meeting transcripts")
    st.write("- Calendar events")
    st.write("- Email threads")
    st.write("- Voice notes")
    st.write("- Personal commitments")

    st.divider()

    if st.button("🗑️ Clear Conversation History"):
        st.session_state.history = []
        st.rerun()


# ---------------- KPI DASHBOARD ----------------

total_commitments = len(data["commitments"])
pending_count = sum(
    1 for item in data["commitments"]
    if item["status"].lower() != "completed"
)
completed_count = total_commitments - pending_count

st.subheader("📊 Executive Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="📌 Total Commitments",
        value=total_commitments,
        help="Total commitments recorded for the executive."
    )

with col2:
    st.metric(
        label="⏳ Pending",
        value=pending_count,
        help="Commitments that still require action."
    )

with col3:
    st.metric(
        label="✅ Completed",
        value=completed_count,
        help="Commitments already completed."
    )

with col4:
    st.metric(
        label="📅 Meetings",
        value=len(data["calendar"]),
        help="Meetings scheduled for the selected week."
    )
if total_commitments > 0:
    completion_rate = completed_count / total_commitments
else:
    completion_rate = 0

st.markdown("### Commitment Completion")

st.progress(
    completion_rate,
    text=f"{completion_rate * 100:.0f}% of commitments completed"
)


st.divider()
# ---------------- UPCOMING CALENDAR ----------------

st.subheader("📅 Upcoming Meetings")

calendar = data["calendar"]
calendar = [
    {
        key: str(value).replace("â€“", "-").replace("â€”", "-")
        if isinstance(value, str)
        else value
        for key, value in item.items()
    }
    for item in calendar
]

st.dataframe(
    calendar,
    use_container_width=True,
    hide_index=True
)

st.divider()
# ---------------- PENDING ITEMS ----------------

st.subheader("⚠️ Pending Items")

pending_items = [
    item
    for item in data["commitments"]
    if item["status"].lower() != "completed"
]

st.dataframe(
    pending_items,
    use_container_width=True,
    hide_index=True
)
# ---------------- EMAIL FOLLOW-UPS ----------------

st.subheader("📧 Email Follow-ups")

email_followups = []

for thread in data["email_threads"]:
    email_followups.append({
        "Subject": thread.get("subject", "No subject"),
        "Details": " | ".join(
            f"{key}: {value}"
            for key, value in thread.items()
            if key != "subject"
        )
    })

st.dataframe(
    email_followups,
    use_container_width=True,
    hide_index=True
)

st.dataframe(
    email_followups,
    use_container_width=True,
    hide_index=True
)

# ---------------- MY COMMITMENTS ----------------

st.subheader("📌 My Commitments")
# ---------------- COMMITMENT PROGRESS ----------------

total_commitments = len(data["commitments"])

pending_count = sum(
    1 for item in data["commitments"]
    if item["status"].lower() != "completed"
)

completed_count = total_commitments - pending_count

col1, col2, col3 = st.columns(3)

col1.metric("Total Commitments", total_commitments)
col2.metric("Pending", pending_count)
col3.metric("Completed", completed_count)

commitments = data["commitments"]

st.dataframe(
    commitments,
    use_container_width=True,
    hide_index=True
)
# ---------------- PRIORITY BREAKDOWN ----------------

st.markdown("### 🎯 Priority Breakdown")

high_priority = []
medium_priority = []
low_priority = []

for item in data["commitments"]:
    priority = item.get("priority", "").lower()

    if priority == "high":
        high_priority.append(item)
    elif priority == "medium":
        medium_priority.append(item)
    else:
        low_priority.append(item)

p1, p2, p3 = st.columns(3)

with p1:
    st.markdown(
        f"""
        <div style="
            padding: 18px;
            border-radius: 12px;
            background-color: #fee2e2;
            border-left: 5px solid #dc2626;
        ">
            <h3 style="color: #991b1b;">🔴 High Priority</h3>
            <h2 style="color: #7f1d1d;">{len(high_priority)}</h2>
            <p style="color: #991b1b;">Requires immediate attention</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with p2:
    st.markdown(
        f"""
        <div style="
            padding: 18px;
            border-radius: 12px;
            background-color: #fef3c7;
            border-left: 5px solid #d97706;
        ">
            <h3 style="color: #92400e;">🟡 Medium Priority</h3>
            <h2 style="color: #78350f;">{len(medium_priority)}</h2>
            <p style="color: #92400e;">Needs attention this week</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with p3:
    st.markdown(
        f"""
        <div style="
            padding: 18px;
            border-radius: 12px;
            background-color: #dcfce7;
            border-left: 5px solid #16a34a;
        ">
            <h3 style="color: #166534;">🟢 Low Priority</h3>
            <h2 style="color: #14532d;">{len(low_priority)}</h2>
            <p style="color: #166534;">Can be scheduled later</p>
        </div>
        """,
        unsafe_allow_html=True
    )


# ---------------- MAIN QUESTION AREA ----------------

if "selected_question" not in st.session_state:
    st.session_state.selected_question = ""

question = st.text_area(
    "Your Question",
    value=st.session_state.selected_question,
    height=120
)

st.subheader("Quick Questions")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📌 My Commitments"):
        st.session_state.selected_question = "Which commitments are pending?"
        st.rerun()

with col2:

    if st.button("📅 Upcoming Meetings"):
        st.session_state.selected_question = "What meetings do I have this week?"
        st.rerun()

with col3:
    if st.button("⚠️ Pending Tasks"):
        st.session_state.selected_question = "What tasks are still pending?"
        st.rerun()

col4, col5, col6 = st.columns(3)

with col4:
    if st.button("📧 Email Follow-ups"):
        st.session_state.selected_question = "Which emails require my attention?"
        st.rerun()

with col5:
    if st.button("📊 Board Preparation"):
        st.session_state.selected_question = "What do I need to prepare for the board meeting?"
        st.rerun()

with col6:
    if st.button("📅 Tomorrow's Schedule"):
        st.session_state.selected_question = "What is my schedule for tomorrow?"
        st.rerun()
st.divider()


# ---------------- AI AGENT ----------------

if st.button(
    "🚀 Ask Executive Agent",
    type="primary",
    use_container_width=True
):

    if not question.strip():
        st.warning("Please enter a question first.")

    else:

        context = json.dumps(data, indent=2)

        prompt = f"""
You are an Executive Productivity Agent for Arjun Malhotra,
VP Sales at Veridian Corp.

Your job is to help Arjun manage commitments, meetings,
emails, deadlines, and pending work.

Use ONLY the supplied assignment data below.

ASSIGNMENT DATA:
{context}

USER QUESTION:
{question}

Instructions:
1. Understand the user's intent.
2. Search the supplied data carefully.
3. Identify relevant commitments, deadlines, meetings, emails,
   and pending items.
4. Do not invent information.
5. If information is missing, clearly say that it is unavailable.
6. Give a concise but useful answer.
7. Mention dates and times when relevant.

Return the answer using this format:

INTENT:
What the user is asking about.

RELEVANT INFORMATION:
Important facts from the available data.

ACTION ITEMS:
Tasks Arjun should complete or follow up on.

RESPONSE:
A clear executive-assistant style answer.
"""

        try:

            with st.spinner("Analyzing meetings, emails, and commitments..."):

                #response = model.generate_content(prompt)

                #answer = response.text
                #answer = "This is a demo response. Your pending commitments and upcoming meetings are displayed in the dashboard."
                demo_answers = {
                    "Which commitments are pending?":
                        "You currently have four pending commitments: send the vendor list to Raghav by Wednesday, review the campaign deck by Thursday morning, assign ownership for the Mumbai lease renewal, and review the July expense variance report before board preparation.",

                    "What meetings do I have this week?":
                        "Your upcoming meetings include the Meridian call on Wednesday at 3:00 PM and the campaign deck review on Thursday at 9:30 AM.",

                    "What tasks are still pending?":
                        "Your pending tasks are the vendor list, campaign deck review, Mumbai lease renewal ownership, and July expense variance review.",

                    "Which emails require my attention?":
                        "The campaign deck review, vendor list confirmation, and July expense variance report require your attention.",

                    "What do I need to prepare for the board meeting?":
                        "Before board preparation, you need to review the July expense variance report.",

                    "What is my schedule for tomorrow?":
                        "Your schedule includes the meetings and commitments listed in your executive calendar."
                }

                answer = demo_answers.get(
                    question,
                    "I found relevant information in your calendar, commitments, and email records. Please ask about a specific meeting, task, or follow-up."
                )

                st.session_state.history.append({
                    "question": question,
                    "response": answer
                    })
                st.success("Executive request analyzed successfully!")
                st.subheader("🤖 Executive Assistant Response")
                with st.container(border=True):
                    st.markdown("### Assistant Insight")
                    st.markdown(answer)
        except Exception as e:
            st.error(f"Error analyzing the request: {e}")


# ---------------- CONVERSATION HISTORY ----------------

if st.session_state.history:

    st.divider()

    st.subheader("🗂️ Conversation History")

    for i, chat in enumerate(
        reversed(st.session_state.history), 1
    ):

        with st.expander(f"Conversation {i}"):

            st.write("**Question:**")
            st.write(chat["question"])

            st.write("**Agent Response:**")
            st.markdown(chat["response"])


# ---------------- FOOTER ----------------

st.divider()

st.caption(
    "Executive Productivity Agent | Built with Python, Streamlit and Gemini AI"
)

