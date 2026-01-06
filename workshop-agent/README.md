# Agentic Thinking Workshop Practice Agent

A web-based practice tool for learning to ask effective discovery questions using the Agentic Transformation Framework.

## Overview

This tool helps you practice the art of discovery questioning by:
- **Roleplaying stakeholders**: An AI agent acts as either an Agent Owner or Business Owner, answering your questions in character
- **Real-time feedback**: Each question is analyzed for depth, relevance, and coverage
- **Coverage tracking**: Visual tracking of which framework areas you've explored
- **Session summaries**: Comprehensive feedback on your questioning skills

## Quick Start

1. **Install dependencies:**
   ```bash
   cd workshop-agent
   pip install -r requirements.txt
   ```

2. **Set your API key** (optional - a default is included):
   ```bash
   export GOOGLE_API_KEY=your_key_here
   ```

3. **Run the app:**
   ```bash
   python app.py
   ```

4. **Open in browser:** Navigate to `http://localhost:7860`

## How to Use

### 1. Setup Your Session
- **Select a Role**: Choose who you want to interview
  - **Agent Owner**: Knows day-to-day operations, user pain points, adoption challenges
  - **Business Owner**: Knows strategic priorities, ROI expectations, resource constraints

- **Select a Use Case**: Choose from pre-built scenarios or generate a new one

### 2. Ask Questions
- Start with broad questions to understand the context
- Follow up with specific, detailed questions
- Try to cover all framework areas

### 3. Review Feedback
After each question, you'll see:
- **Score (1-5 stars)**: How effective was your question?
- **Coverage Areas**: Which framework topics did you address?
- **Strengths**: What you did well
- **Improvement**: How to make it better
- **Suggested Follow-up**: A better question to ask next

### 4. Track Coverage
The coverage panel shows which areas you've explored:
- **Process Mapping**: Current/future state, workflows
- **User Value**: Why users will adopt
- **Capabilities**: What the agent should do
- **Guardrails**: Safety, escalation, constraints
- **Data**: Sources, quality, accessibility
- **ROI/Metrics**: Success measures, baselines, targets
- **Adoption**: Barriers, champions, training
- **Deployment**: Rollout strategy, first users

## Tips for Better Questions

1. **Start broad, then narrow**: "Walk me through the current process" → "What happens when a ticket is misrouted?"

2. **Ask "why" and "how"**: Not just "what data do you use?" but "how does data quality affect accuracy?"

3. **Quantify**: "How many tickets per day? What percentage get misrouted?"

4. **Build on answers**: Reference what the stakeholder just said

5. **Explore edge cases**: "What happens when...?" "What if...?"

6. **Challenge assumptions**: "Why is that the target? What drove that decision?"

## Sample Use Cases Included

1. **Customer Support Ticket Triage** - Auto-categorization and routing
2. **Contract Review Assistant** - Legal document analysis
3. **Sales Proposal Generator** - Automated proposal creation
4. **Employee Onboarding Assistant** - New hire guidance
5. **IT Incident Response Coordinator** - Outage management

## Project Structure

```
workshop-agent/
├── app.py                    # Main Gradio application
├── agents/
│   ├── stakeholder.py        # Roleplay agent
│   └── analyzer.py           # Question evaluation agent
├── prompts/
│   ├── stakeholder_prompts.py
│   └── analyzer_prompts.py
├── data/
│   └── use_cases.py          # Framework knowledge & samples
├── requirements.txt
└── README.md
```

## Framework Areas Explained

| Area | What to Discover |
|------|------------------|
| Process Mapping | Current workflow, pain points, reimagined future state |
| User Value | Who benefits, why they'll use it, the "aha moment" |
| Capabilities | Must-haves vs nice-to-haves, MVP scope |
| Guardrails | What NOT to do, escalation triggers, compliance |
| Data | Sources, quality, gaps, accessibility |
| ROI/Metrics | Baselines, targets, how to measure success |
| Adoption | Barriers, champions, resistance, training needs |
| Deployment | First users, rollout strategy, feedback loops |

## Technology

- **Google Gemini 2.5 Flash Pro** - Powers both the stakeholder and analyzer agents
- **Gradio** - Web UI framework
- **Python 3.9+** - Runtime

## License

MIT - Use freely for learning and practice.
