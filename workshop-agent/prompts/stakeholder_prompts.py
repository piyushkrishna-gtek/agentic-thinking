"""
System prompts for the stakeholder agent that roleplays as Agent Owner or Business Owner.
"""


def get_stakeholder_prompt(role: str, use_case: dict) -> str:
    """
    Generate the system prompt for a stakeholder based on role and use case.

    Args:
        role: Either "agent_owner" or "business_owner"
        use_case: Dictionary containing use case details including hidden_details
    """

    hidden = use_case.get("hidden_details", {})

    role_context = {
        "agent_owner": {
            "title": "Agent Owner",
            "perspective": """You are the Agent Owner for this initiative. Your focus is on:
- Day-to-day operations and user experience
- Making sure users actually adopt and use the agent
- Collecting feedback and iterating on the agent
- Understanding user pain points deeply
- Balancing feature requests vs. core value

You know the operational details intimately but may not have full visibility into
budget constraints or strategic priorities at the executive level.""",
            "knowledge_focus": [
                "User workflows and pain points",
                "Adoption challenges and barriers",
                "Feedback from users",
                "Operational metrics",
                "Day-to-day process details"
            ]
        },
        "business_owner": {
            "title": "Business Owner",
            "perspective": """You are the Business Owner for this initiative. Your focus is on:
- ROI and business case justification
- Strategic alignment with company goals
- Resource allocation and prioritization
- Risk management and compliance
- Making scale/fix/kill decisions for the agent portfolio

You understand the business context and executive expectations but may not know
every operational detail of how users interact with systems day-to-day.""",
            "knowledge_focus": [
                "Budget and resource constraints",
                "Strategic priorities",
                "Executive expectations",
                "Competitive pressures",
                "Risk tolerance"
            ]
        }
    }

    role_info = role_context.get(role, role_context["agent_owner"])

    prompt = f"""You are roleplaying as the {role_info['title']} in a Discovery Workshop for an AI agent initiative.

## Your Role
{role_info['perspective']}

## The Use Case
**Name:** {use_case.get('name', 'Unknown')}
**Description:** {use_case.get('brief_description', 'No description')}

## Your Hidden Knowledge (reveal only when asked good questions)

### Current Process
{_format_dict(hidden.get('current_process', {}))}

### Data Landscape
{_format_dict(hidden.get('data_landscape', {}))}

### Your Specific Concerns
{_format_concerns(hidden.get('stakeholder_concerns', {}), role)}

### Guardrails You Know About
{_format_list(hidden.get('guardrails_needed', []))}

### Success Metrics You're Tracking
{_format_metrics(hidden.get('success_metrics', {}))}

### Adoption Challenges You're Aware Of
{_format_list(hidden.get('adoption_challenges', []))}

## How to Respond

1. **Be authentic to your role** - Answer from your perspective with appropriate knowledge gaps
2. **Don't volunteer information** - Wait for the questioner to ask. If they ask a vague question, give a vague answer
3. **Reward good questions** - When asked specific, insightful questions, provide rich detail
4. **Show realistic behavior**:
   - If asked about something outside your expertise, say so
   - Express genuine concerns and hopes
   - Sometimes be uncertain or say "I'd need to check on that"
5. **Stay in character** - You're a real stakeholder, not an AI assistant

## Response Style
- Speak naturally as a business professional
- Use realistic hedging ("I think...", "From what I've seen...", "The team tells me...")
- Show appropriate emotion (frustration with pain points, excitement about potential)
- Keep responses conversational, not like a data dump
- If a question is too broad, answer broadly and let them follow up

Remember: The goal is to help the questioner practice asking detailed, specific questions.
Reward depth with depth. Punish vagueness with vagueness (politely).
"""

    return prompt


def get_use_case_generation_prompt(role: str) -> str:
    """
    Generate prompt for creating a new use case with hidden details.
    """
    import random
    import time

    # Random FMCG context for variety
    fmcg_functions = ["Sales", "Supply Chain", "Trade Marketing", "Distribution", "Field Force", "Finance", "Quality", "Customer Service"]
    fmcg_challenges = ["manual data entry", "delayed decisions", "inconsistent execution", "lack of visibility", "coordination gaps", "compliance issues", "slow response time", "data silos"]

    selected_function = random.choice(fmcg_functions)
    selected_challenge = random.choice(fmcg_challenges)

    # Add timestamp for uniqueness
    seed = int(time.time() * 1000) % 10000

    return f"""Generate a unique AGENTIC AI use case for FMCG Discovery Workshop.

IMPORTANT: This must be an AGENTIC AI use case, not just analytics or insights.

Agentic AI means the agent:
- Takes ACTIONS autonomously (not just provides recommendations)
- Orchestrates multi-step workflows
- Integrates with multiple systems (ERP, DMS, CRM, etc.)
- Makes decisions within defined guardrails
- Escalates to humans when needed
- Executes tasks end-to-end

Random seed: {seed}
FMCG Function: {selected_function}
Key Challenge: {selected_challenge}

Generate a COMPLETELY NEW and UNIQUE agentic use case. Examples of agentic behaviors:
- Auto-creates purchase orders when stock falls below threshold
- Sends WhatsApp reminders to retailers and updates CRM
- Processes claims, validates documents, and triggers payments
- Monitors shelf photos, flags issues, and assigns tasks to reps
- Handles customer complaints end-to-end including refund processing

Create a use case with:
1. A clear, professional name (e.g., "Distributor Claims Processing Agent")
2. A 1-2 sentence description highlighting the AGENTIC nature (actions it takes)
3. Hidden details for the {role}:
   - Current manual process and pain points
   - Volume and scale (SKUs, outlets, distributors)
   - Systems it would integrate with
   - Actions it would take autonomously
   - Guardrails and approval workflows
   - Success metrics
   - Adoption challenges

Focus on ACTIONS the agent takes, not just insights it provides.

Output as a JSON object with this structure:
{{
    "name": "Use Case Name",
    "brief_description": "One sentence description",
    "hidden_details": {{
        "current_process": {{
            "steps": [...],
            "pain_points": [...],
            "volume": "..."
        }},
        "data_landscape": {{
            "sources": [...],
            "quality_issues": [...]
        }},
        "stakeholder_concerns": {{
            "agent_owner": {{"worries": "...", "hopes": "..."}},
            "business_owner": {{"worries": "...", "hopes": "..."}}
        }},
        "guardrails_needed": [...],
        "success_metrics": {{
            "baseline": {{...}},
            "targets": {{...}}
        }},
        "adoption_challenges": [...]
    }}
}}
"""


def _format_dict(d: dict) -> str:
    """Format a dictionary for prompt inclusion."""
    if not d:
        return "No information available"

    lines = []
    for key, value in d.items():
        if isinstance(value, list):
            lines.append(f"**{key.replace('_', ' ').title()}:**")
            for item in value:
                lines.append(f"  - {item}")
        else:
            lines.append(f"**{key.replace('_', ' ').title()}:** {value}")
    return "\n".join(lines)


def _format_list(items: list) -> str:
    """Format a list for prompt inclusion."""
    if not items:
        return "No items"
    return "\n".join(f"- {item}" for item in items)


def _format_concerns(concerns: dict, role: str) -> str:
    """Format stakeholder concerns for the specific role."""
    if not concerns:
        return "No specific concerns documented"

    role_concerns = concerns.get(role, {})
    if not role_concerns:
        return "No specific concerns for this role"

    return f"""**Your Worries:** {role_concerns.get('worries', 'None specified')}
**Your Hopes:** {role_concerns.get('hopes', 'None specified')}"""


def _format_metrics(metrics: dict) -> str:
    """Format success metrics."""
    if not metrics:
        return "No metrics defined"

    baseline = metrics.get('baseline', {})
    targets = metrics.get('targets', {})

    lines = ["**Current Baseline:**"]
    for k, v in baseline.items():
        lines.append(f"  - {k.replace('_', ' ').title()}: {v}")

    lines.append("\n**Targets:**")
    for k, v in targets.items():
        lines.append(f"  - {k.replace('_', ' ').title()}: {v}")

    return "\n".join(lines)
