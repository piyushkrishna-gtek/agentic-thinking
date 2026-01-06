"""
Analyzer Sub-Agent - Evaluates question quality and provides feedback.
"""

import json
import google.generativeai as genai
from typing import Optional

from prompts.analyzer_prompts import (
    get_analyzer_prompt,
    get_session_summary_prompt,
    FRAMEWORK_COVERAGE_AREAS,
    COVERAGE_DESCRIPTIONS
)


class AnalyzerAgent:
    """Sub-agent that analyzes question quality and tracks coverage."""

    def __init__(self, api_key: str):
        """Initialize the analyzer agent with Google API key."""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.0-flash")
        self.system_prompt = get_analyzer_prompt()
        self.coverage_tracker = {area: 0 for area in FRAMEWORK_COVERAGE_AREAS}
        self.question_scores = []
        self.feedbacks = []

    def analyze_question(
        self,
        question: str,
        stakeholder_response: str,
        conversation_context: list
    ) -> dict:
        """
        Analyze a question and provide feedback.

        Args:
            question: The question asked by the practitioner
            stakeholder_response: The stakeholder's answer
            conversation_context: Previous conversation for context

        Returns:
            Dictionary with score, coverage areas, and feedback
        """
        # Build context from conversation history
        context_str = ""
        if conversation_context:
            recent = conversation_context[-6:]  # Last 3 exchanges
            for entry in recent:
                role = entry.get("role", "unknown")
                content = entry.get("content", "")
                context_str += f"\n{role.upper()}: {content}\n"

        prompt = f"""{self.system_prompt}

## Current Conversation Context
{context_str}

## Question to Analyze
"{question}"

## Stakeholder's Response
"{stakeholder_response}"

Analyze this question and provide your evaluation in JSON format.
Consider the conversation context - reward questions that build on previous answers.
"""

        response = self.model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json"
            )
        )

        try:
            analysis = json.loads(response.text)
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            analysis = {
                "score": 3,
                "coverage_areas": ["process_mapping"],
                "strengths": "Question received",
                "improvement": "Try to be more specific",
                "follow_up_suggestion": "Can you tell me more about the specific steps involved?",
                "tip": "Ask follow-up questions to dig deeper"
            }

        # Update coverage tracker
        for area in analysis.get("coverage_areas", []):
            if area in self.coverage_tracker:
                self.coverage_tracker[area] += 1

        # Track scores
        score = analysis.get("score", 3)
        self.question_scores.append(score)
        self.feedbacks.append({
            "question": question,
            "analysis": analysis
        })

        return analysis

    def get_coverage_status(self) -> dict:
        """
        Get current coverage status across all framework areas.

        Returns:
            Dictionary mapping areas to coverage levels
        """
        status = {}
        for area, count in self.coverage_tracker.items():
            if count == 0:
                level = "not_covered"
            elif count < 2:
                level = "lightly_covered"
            elif count < 4:
                level = "partially_covered"
            else:
                level = "well_covered"

            status[area] = {
                "count": count,
                "level": level,
                "description": COVERAGE_DESCRIPTIONS.get(area, "")
            }

        return status

    def get_coverage_summary_text(self) -> str:
        """Get a text summary of coverage for display."""
        status = self.get_coverage_status()

        lines = ["## Framework Coverage\n"]

        # Group by coverage level
        well_covered = []
        partial = []
        light = []
        not_covered = []

        for area, info in status.items():
            display_name = area.replace("_", " ").title()
            if info["level"] == "well_covered":
                well_covered.append(f"- {display_name} ({info['count']} questions)")
            elif info["level"] == "partially_covered":
                partial.append(f"- {display_name} ({info['count']} questions)")
            elif info["level"] == "lightly_covered":
                light.append(f"- {display_name} ({info['count']} questions)")
            else:
                not_covered.append(f"- {display_name}")

        if well_covered:
            lines.append("**Well Covered:**")
            lines.extend(well_covered)
            lines.append("")

        if partial:
            lines.append("**Partially Covered:**")
            lines.extend(partial)
            lines.append("")

        if light:
            lines.append("**Needs More Depth:**")
            lines.extend(light)
            lines.append("")

        if not_covered:
            lines.append("**Not Yet Explored:**")
            lines.extend(not_covered)

        return "\n".join(lines)

    def get_average_score(self) -> float:
        """Get the average question score for the session."""
        if not self.question_scores:
            return 0.0
        return sum(self.question_scores) / len(self.question_scores)

    def get_session_summary(self, conversation_history: list) -> str:
        """
        Generate a comprehensive session summary.

        Args:
            conversation_history: Full conversation from the session

        Returns:
            Markdown formatted summary
        """
        # Build conversation transcript
        transcript = ""
        for entry in conversation_history:
            role = entry.get("role", "unknown")
            content = entry.get("content", "")
            transcript += f"\n**{role.upper()}**: {content}\n"

        # Build summary of all feedback
        feedback_summary = ""
        for i, fb in enumerate(self.feedbacks, 1):
            analysis = fb["analysis"]
            feedback_summary += f"""
Question {i}: "{fb['question'][:50]}..."
- Score: {analysis.get('score', 'N/A')}/5
- Areas: {', '.join(analysis.get('coverage_areas', []))}
"""

        prompt = f"""{get_session_summary_prompt()}

## Session Transcript
{transcript}

## Question-by-Question Analysis
{feedback_summary}

## Coverage Statistics
{self.get_coverage_summary_text()}

## Overall Statistics
- Total Questions: {len(self.question_scores)}
- Average Score: {self.get_average_score():.1f}/5
- Highest Score: {max(self.question_scores) if self.question_scores else 0}
- Lowest Score: {min(self.question_scores) if self.question_scores else 0}

Generate a comprehensive, encouraging but honest summary of this session.
"""

        response = self.model.generate_content(prompt)
        return response.text

    def reset(self):
        """Reset the analyzer for a new session."""
        self.coverage_tracker = {area: 0 for area in FRAMEWORK_COVERAGE_AREAS}
        self.question_scores = []
        self.feedbacks = []

    def format_feedback_for_display(self, analysis: dict) -> str:
        """Format analysis results for Gradio display."""
        score = analysis.get("score", 0)
        stars = "★" * score + "☆" * (5 - score)

        areas = analysis.get("coverage_areas", [])
        areas_display = ", ".join(a.replace("_", " ").title() for a in areas)

        return f"""### Question Quality: {stars} ({score}/5)

**Areas Covered:** {areas_display}

**Strengths:** {analysis.get('strengths', 'N/A')}

**How to Improve:** {analysis.get('improvement', 'N/A')}

**Suggested Follow-up:**
> {analysis.get('follow_up_suggestion', 'N/A')}

**Tip:** {analysis.get('tip', 'N/A')}
"""
