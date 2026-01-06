"""
Agentic Thinking Workshop Practice Agent

A Gradio-based web UI for practicing discovery questions
with AI-powered stakeholder roleplay and feedback.
"""

import os
import gradio as gr
from dotenv import load_dotenv

from agents.stakeholder import StakeholderAgent
from agents.analyzer import AnalyzerAgent
# Load environment variables
load_dotenv()

# Get API key from environment (required)
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable is required. Set it in a .env file or environment.")

# Initialize agents
stakeholder_agent = StakeholderAgent(API_KEY)
analyzer_agent = AnalyzerAgent(API_KEY)

# Store current generated use case
current_use_case = {"use_case": None}

# Light Theme Colors
COLORS = {
    "primary": "#0066CC",
    "primary_light": "#E6F2FF",
    "accent": "#FF6B00",
    "success": "#059669",
    "warning": "#D97706",
    "error": "#DC2626",
    "purple": "#7C3AED",
    "bg_white": "#FFFFFF",
    "bg_light": "#F8FAFC",
    "bg_gray": "#F1F5F9",
    "text_dark": "#1E293B",
    "text_medium": "#475569",
    "text_light": "#64748B",
    "border": "#E2E8F0",
    "border_dark": "#CBD5E1",
}


def generate_new_use_case(role: str):
    """Generate a new use case and display it."""
    # Use the stakeholder agent to generate a use case
    use_case = stakeholder_agent._generate_use_case(role=role)
    current_use_case["use_case"] = use_case

    name = use_case.get("name", "Generated Use Case")
    brief = use_case.get("brief_description", "A dynamically generated scenario for practice.")

    use_case_html = f'''
<div style="font-family: system-ui, sans-serif; padding: 20px; background: {COLORS["bg_white"]}; border-radius: 12px; border: 2px solid {COLORS["primary"]};">
    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px;">
        <span style="font-size: 1.5em;">🎲</span>
        <span style="font-size: 1.2em; font-weight: 700; color: {COLORS["primary"]};">{name}</span>
    </div>
    <div style="color: {COLORS["text_dark"]}; line-height: 1.6; font-size: 0.95em;">{brief}</div>
    <div style="margin-top: 16px; padding: 12px; background: {COLORS["primary_light"]}; border-radius: 8px; border-left: 4px solid {COLORS["primary"]};">
        <div style="color: {COLORS["primary"]}; font-size: 0.85em; font-weight: 500;">✓ Ready to start! Click "Start Session" to begin the interview.</div>
    </div>
</div>
'''
    # Show start button (visible and interactive)
    return use_case_html, gr.update(interactive=True, visible=True)


def get_score_html(score: int) -> str:
    """Generate HTML for score display with color coding."""
    colors = {
        1: COLORS["error"],
        2: COLORS["accent"],
        3: COLORS["warning"],
        4: COLORS["success"],
        5: COLORS["primary"],
    }
    color = colors.get(score, COLORS["text_light"])
    filled = "★" * score
    empty = "☆" * (5 - score)
    return f'<span style="color: {color}; font-size: 1.6em;">{filled}{empty}</span> <span style="color: {color}; font-weight: bold; font-size: 1.1em;">({score}/5)</span>'


def get_coverage_html(coverage_status: dict) -> str:
    """Generate HTML for coverage display with progress bars."""
    html_parts = [f'<div style="font-family: system-ui, sans-serif; color: {COLORS["text_dark"]};">']

    well_covered = []
    partial = []
    light = []
    not_covered = []

    for area, info in coverage_status.items():
        display_name = area.replace("_", " ").title()
        count = info["count"]
        level = info["level"]

        if level == "well_covered":
            well_covered.append((display_name, count))
        elif level == "partially_covered":
            partial.append((display_name, count))
        elif level == "lightly_covered":
            light.append((display_name, count))
        else:
            not_covered.append((display_name, count))

    def make_progress_bar(name, count, color, max_count=4):
        pct = min(100, (count / max_count) * 100)
        return f'''
        <div style="margin-bottom: 12px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                <span style="font-size: 0.9em; color: {COLORS["text_dark"]}; font-weight: 500;">{name}</span>
                <span style="font-size: 0.85em; color: {COLORS["text_light"]};">{count} questions</span>
            </div>
            <div style="background: {COLORS["bg_gray"]}; border-radius: 6px; height: 10px; overflow: hidden;">
                <div style="background: {color}; width: {pct}%; height: 100%; border-radius: 6px; transition: width 0.3s;"></div>
            </div>
        </div>'''

    if well_covered:
        html_parts.append(f'<div style="margin-bottom: 20px;"><h4 style="color: {COLORS["primary"]}; margin: 0 0 12px 0; font-size: 0.95em; font-weight: 600;">✓ Well Covered</h4>')
        for name, count in well_covered:
            html_parts.append(make_progress_bar(name, count, COLORS["primary"]))
        html_parts.append('</div>')

    if partial:
        html_parts.append(f'<div style="margin-bottom: 20px;"><h4 style="color: {COLORS["success"]}; margin: 0 0 12px 0; font-size: 0.95em; font-weight: 600;">◐ Partially Covered</h4>')
        for name, count in partial:
            html_parts.append(make_progress_bar(name, count, COLORS["success"]))
        html_parts.append('</div>')

    if light:
        html_parts.append(f'<div style="margin-bottom: 20px;"><h4 style="color: {COLORS["warning"]}; margin: 0 0 12px 0; font-size: 0.95em; font-weight: 600;">○ Needs More Depth</h4>')
        for name, count in light:
            html_parts.append(make_progress_bar(name, count, COLORS["warning"]))
        html_parts.append('</div>')

    if not_covered:
        html_parts.append(f'<div style="margin-bottom: 20px;"><h4 style="color: {COLORS["text_light"]}; margin: 0 0 12px 0; font-size: 0.95em; font-weight: 600;">○ Not Yet Explored</h4>')
        for name, count in not_covered:
            html_parts.append(make_progress_bar(name, count, COLORS["border_dark"]))
        html_parts.append('</div>')

    html_parts.append('</div>')
    return ''.join(html_parts)


def format_feedback_html(analysis: dict) -> str:
    """Format analysis as styled HTML."""
    score = analysis.get("score", 0)
    areas = analysis.get("coverage_areas", [])
    areas_display = ", ".join(a.replace("_", " ").title() for a in areas)

    score_html = get_score_html(score)

    return f'''
<div style="font-family: system-ui, sans-serif; color: {COLORS["text_dark"]};">
    <div style="text-align: center; padding: 20px; background: {COLORS["primary_light"]}; border-radius: 12px; margin-bottom: 16px; border: 1px solid {COLORS["border"]};">
        <div style="font-size: 0.9em; color: {COLORS["text_medium"]}; margin-bottom: 8px; font-weight: 500;">Question Quality</div>
        {score_html}
    </div>

    <div style="background: {COLORS["bg_white"]}; border-radius: 10px; padding: 16px; margin-bottom: 14px; border: 1px solid {COLORS["border"]};">
        <div style="color: {COLORS["primary"]}; font-weight: 600; font-size: 0.9em; margin-bottom: 8px;">📍 Areas Covered</div>
        <div style="color: {COLORS["text_dark"]}; font-size: 0.95em;">{areas_display or "None identified"}</div>
    </div>

    <div style="background: {COLORS["bg_white"]}; border-radius: 10px; padding: 16px; margin-bottom: 14px; border: 1px solid {COLORS["border"]};">
        <div style="color: {COLORS["success"]}; font-weight: 600; font-size: 0.9em; margin-bottom: 8px;">✓ Strengths</div>
        <div style="color: {COLORS["text_dark"]}; font-size: 0.95em;">{analysis.get('strengths', 'N/A')}</div>
    </div>

    <div style="background: {COLORS["bg_white"]}; border-radius: 10px; padding: 16px; margin-bottom: 14px; border: 1px solid {COLORS["border"]};">
        <div style="color: {COLORS["accent"]}; font-weight: 600; font-size: 0.9em; margin-bottom: 8px;">↑ How to Improve</div>
        <div style="color: {COLORS["text_dark"]}; font-size: 0.95em;">{analysis.get('improvement', 'N/A')}</div>
    </div>

    <div style="background: {COLORS["primary_light"]}; border-radius: 10px; padding: 16px; margin-bottom: 14px; border-left: 4px solid {COLORS["primary"]};">
        <div style="color: {COLORS["primary"]}; font-weight: 600; font-size: 0.9em; margin-bottom: 8px;">💡 Suggested Follow-up</div>
        <div style="color: {COLORS["text_dark"]}; font-size: 0.95em; font-style: italic;">"{analysis.get('follow_up_suggestion', 'N/A')}"</div>
    </div>

    <div style="background: {COLORS["bg_white"]}; border-radius: 10px; padding: 16px; border: 1px solid {COLORS["border"]};">
        <div style="color: {COLORS["purple"]}; font-weight: 600; font-size: 0.9em; margin-bottom: 8px;">📝 Tip</div>
        <div style="color: {COLORS["text_dark"]}; font-size: 0.95em;">{analysis.get('tip', 'N/A')}</div>
    </div>
</div>
'''


def start_session(role: str):
    """Start a new practice session."""
    analyzer_agent.reset()

    # Check if we have a generated use case
    if current_use_case["use_case"] is None:
        return (
            [],
            f'''
<div style="text-align: center; padding: 40px; color: {COLORS["error"]}; font-family: system-ui, sans-serif;">
    <div style="font-size: 2em; margin-bottom: 16px;">⚠️</div>
    <div style="font-size: 1.1em; font-weight: 600;">Please generate a use case first!</div>
    <div style="color: {COLORS["text_medium"]}; margin-top: 8px;">Click "🎲 Generate Use Case" to create a scenario.</div>
</div>
''',
            f'''<div style="text-align: center; padding: 30px; color: {COLORS["text_light"]};">No session active</div>''',
            "",
            # Keep sections hidden
            gr.update(visible=False),  # conversation_section
            gr.update(visible=False),  # feedback_column
            gr.update(visible=False),  # summary_section
            gr.update(visible=False),  # tips_section
        )

    # Start session with the generated use case
    intro = stakeholder_agent.start_session(role, use_case=current_use_case["use_case"])

    role_display = stakeholder_agent.get_role_display()
    use_case_brief = stakeholder_agent.get_use_case_brief()

    chat_history = [{"role": "assistant", "content": f"**[{role_display}]**: {intro}"}]

    initial_feedback = f'''
<div style="font-family: system-ui, sans-serif; color: {COLORS["text_dark"]};">
    <div style="text-align: center; padding: 24px; background: linear-gradient(135deg, {COLORS["primary_light"]} 0%, {COLORS["bg_white"]} 100%); border-radius: 12px; margin-bottom: 16px; border: 1px solid {COLORS["border"]};">
        <div style="color: {COLORS["primary"]}; font-size: 1.4em; font-weight: 700; margin-bottom: 8px;">🎯 Session Started!</div>
        <div style="color: {COLORS["text_medium"]}; font-size: 1em;">Role: <span style="color: {COLORS["text_dark"]}; font-weight: 600;">{role_display}</span></div>
    </div>

    <div style="background: {COLORS["bg_white"]}; border-radius: 10px; padding: 16px; margin-bottom: 16px; border: 1px solid {COLORS["border"]};">
        <div style="color: {COLORS["primary"]}; font-weight: 600; margin-bottom: 10px;">📋 Use Case</div>
        <div style="color: {COLORS["text_dark"]};">{use_case_brief}</div>
    </div>

    <div style="background: {COLORS["bg_light"]}; border-radius: 10px; padding: 16px; border-left: 4px solid {COLORS["purple"]};">
        <div style="color: {COLORS["purple"]}; font-weight: 600; margin-bottom: 6px;">💡 Tip</div>
        <div style="color: {COLORS["text_dark"]}; font-size: 0.95em;">Start by understanding the current process before diving into specifics.</div>
    </div>
</div>
'''

    coverage_status = analyzer_agent.get_coverage_status()
    coverage_html = get_coverage_html(coverage_status)

    return (
        chat_history,
        initial_feedback,
        coverage_html,
        "",
        # Show all sections progressively
        gr.update(visible=True),   # conversation_section
        gr.update(visible=True),   # feedback_column
        gr.update(visible=True),   # summary_section
        gr.update(visible=True),   # tips_section
    )


def submit_question(question: str, chat_history: list):
    """Process a question and get response + feedback."""
    if not question.strip():
        coverage_status = analyzer_agent.get_coverage_status()
        return chat_history, "Please enter a question.", get_coverage_html(coverage_status), get_stats_html()

    response = stakeholder_agent.respond(question)

    analysis = analyzer_agent.analyze_question(
        question,
        response,
        stakeholder_agent.get_conversation_history()
    )

    role_display = stakeholder_agent.get_role_display()
    chat_history.append({"role": "user", "content": question})
    chat_history.append({"role": "assistant", "content": f"**[{role_display}]**: {response}"})

    feedback_html = format_feedback_html(analysis)
    coverage_status = analyzer_agent.get_coverage_status()
    coverage_html = get_coverage_html(coverage_status)
    stats_html = get_stats_html()

    return chat_history, feedback_html, coverage_html, stats_html


def get_stats_html() -> str:
    """Generate stats HTML."""
    avg_score = analyzer_agent.get_average_score()
    num_questions = len(analyzer_agent.question_scores)

    if num_questions == 0:
        return ""

    if avg_score >= 4:
        color = COLORS["primary"]
    elif avg_score >= 3:
        color = COLORS["success"]
    elif avg_score >= 2:
        color = COLORS["warning"]
    else:
        color = COLORS["accent"]

    return f'''
<div style="display: flex; justify-content: center; gap: 40px; padding: 16px; background: {COLORS["bg_light"]}; border-radius: 10px; border: 1px solid {COLORS["border"]};">
    <div style="text-align: center;">
        <div style="color: {COLORS["text_light"]}; font-size: 0.85em; margin-bottom: 4px; font-weight: 500;">Questions</div>
        <div style="color: {COLORS["text_dark"]}; font-size: 1.5em; font-weight: 700;">{num_questions}</div>
    </div>
    <div style="text-align: center;">
        <div style="color: {COLORS["text_light"]}; font-size: 0.85em; margin-bottom: 4px; font-weight: 500;">Avg Score</div>
        <div style="color: {color}; font-size: 1.5em; font-weight: 700;">{avg_score:.1f}/5</div>
    </div>
</div>
'''


def get_summary():
    """Generate session summary."""
    if not stakeholder_agent.conversation_history:
        return "No session to summarize. Start a session first."

    summary = analyzer_agent.get_session_summary(
        stakeholder_agent.get_conversation_history()
    )
    return summary


# Build the Gradio interface with Light Theme
with gr.Blocks(
    title="Agentic Thinking Workshop",
    theme=gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="slate",
    )
) as app:

    gr.Markdown("""
    # 🎯 Agentic Thinking Workshop

    Practice discovery questioning by interviewing AI stakeholders. Get real-time feedback and track your coverage.
    """)

    with gr.Row():
        with gr.Column(scale=3):
            # Phase 1: Setup (always visible)
            with gr.Group():
                gr.Markdown("### Setup Your Session")
                with gr.Row():
                    role_dropdown = gr.Dropdown(
                        choices=[
                            ("Agent Owner", "agent_owner"),
                            ("Business Owner", "business_owner")
                        ],
                        value="agent_owner",
                        label="Stakeholder Role",
                        info="Who do you want to interview?",
                        scale=2
                    )
                    generate_btn = gr.Button("🎲 Generate Use Case", variant="secondary", scale=1)

                use_case_display = gr.HTML(
                    value=f'''
<div style="text-align: center; padding: 30px; color: {COLORS["text_light"]}; font-family: system-ui, sans-serif; background: {COLORS["bg_gray"]}; border-radius: 12px; border: 2px dashed {COLORS["border_dark"]};">
    <div style="font-size: 2em; margin-bottom: 12px;">🎲</div>
    <div style="font-size: 1em;">Click <strong>"Generate Use Case"</strong> to create a practice scenario</div>
</div>
''',
                    label="Generated Use Case"
                )

                start_btn = gr.Button("🚀 Start Session", variant="primary", size="lg", interactive=False, visible=False)

            # Phase 2: Conversation (hidden until session starts)
            conversation_section = gr.Column(visible=False)
            with conversation_section:
                chatbot = gr.Chatbot(
                    label="Discovery Conversation",
                    height=450,
                    show_copy_button=True,
                    type="messages"
                )

                with gr.Row():
                    question_input = gr.Textbox(
                        placeholder="Ask a discovery question... (Press Enter to submit)",
                        label="Your Question",
                        scale=5,
                        interactive=True,
                        lines=1
                    )
                    submit_btn = gr.Button("Ask", variant="primary", scale=1, interactive=True)

        # Phase 2: Right sidebar (hidden until session starts)
        feedback_column = gr.Column(scale=2, visible=False)
        with feedback_column:
            stats_output = gr.HTML(value="")

            gr.Markdown("### 📊 Question Feedback")
            feedback_output = gr.HTML(
                value=f'''
<div style="text-align: center; padding: 50px 20px; color: {COLORS["text_light"]}; font-family: system-ui, sans-serif;">
    <div style="font-size: 3em; margin-bottom: 16px;">🎯</div>
    <div style="font-size: 1.1em;">Ask your first question to get feedback!</div>
</div>
'''
            )

            gr.Markdown("### 📈 Framework Coverage")
            coverage_output = gr.HTML(
                value=f'''
<div style="text-align: center; padding: 30px; color: {COLORS["text_light"]}; font-family: system-ui, sans-serif;">
    No session active
</div>
'''
            )

            summary_btn = gr.Button("📋 Get Session Summary", variant="secondary", interactive=True)

    # Phase 3: Summary section (hidden until session starts)
    summary_section = gr.Accordion("📝 Session Summary", open=False, visible=False)
    with summary_section:
        summary_output = gr.Markdown(
            value="Complete a session and click 'Get Session Summary' to see your results."
        )

    # Tips section (hidden until session starts)
    tips_section = gr.Markdown(visible=False, value="""
    ---
    ### 💡 Tips for Better Questions

    | Strategy | Example |
    |----------|---------|
    | **Start broad, then narrow** | "Walk me through the process" → "What happens when X fails?" |
    | **Ask "why" and "how"** | "Why is it done this way?" "How do you handle exceptions?" |
    | **Quantify everything** | "How many per day?" "What percentage fail?" |
    | **Build on answers** | Reference what they just said in your follow-up |
    | **Explore edge cases** | "What's the worst case scenario?" |

    *Built with Google Gemini 2.0 Flash and Gradio*
    """)

    generate_btn.click(
        fn=generate_new_use_case,
        inputs=[role_dropdown],
        outputs=[use_case_display, start_btn]
    )

    start_btn.click(
        fn=start_session,
        inputs=[role_dropdown],
        outputs=[
            chatbot,
            feedback_output,
            coverage_output,
            stats_output,
            conversation_section,
            feedback_column,
            summary_section,
            tips_section
        ]
    )

    submit_btn.click(
        fn=submit_question,
        inputs=[question_input, chatbot],
        outputs=[chatbot, feedback_output, coverage_output, stats_output]
    ).then(
        fn=lambda: "",
        outputs=[question_input]
    )

    question_input.submit(
        fn=submit_question,
        inputs=[question_input, chatbot],
        outputs=[chatbot, feedback_output, coverage_output, stats_output]
    ).then(
        fn=lambda: "",
        outputs=[question_input]
    )

    summary_btn.click(
        fn=get_summary,
        outputs=[summary_output]
    )


if __name__ == "__main__":
    app.launch(share=False)
