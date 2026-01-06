"""
Stakeholder Agent - Roleplays as Agent Owner or Business Owner.
"""

import json
import random
import google.generativeai as genai
from typing import Optional

from prompts.stakeholder_prompts import get_stakeholder_prompt, get_use_case_generation_prompt
from data.use_cases import SAMPLE_USE_CASES


class StakeholderAgent:
    """Agent that roleplays as a stakeholder in discovery workshops."""

    def __init__(self, api_key: str):
        """Initialize the stakeholder agent with Google API key."""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.0-flash")
        self.chat = None
        self.role = None
        self.use_case = None
        self.conversation_history = []

    def start_session(
        self,
        role: str,
        use_case: Optional[dict] = None,
        generate_new: bool = False
    ) -> str:
        """
        Start a new practice session.

        Args:
            role: "agent_owner" or "business_owner"
            use_case: Optional pre-defined use case dict
            generate_new: If True, generate a new use case

        Returns:
            Opening message from the stakeholder
        """
        self.role = role
        self.conversation_history = []

        if generate_new:
            self.use_case = self._generate_use_case()
        elif use_case:
            self.use_case = use_case
        else:
            # Pick a random sample use case
            self.use_case = random.choice(SAMPLE_USE_CASES)

        # Create system prompt and start chat
        system_prompt = get_stakeholder_prompt(role, self.use_case)

        self.chat = self.model.start_chat(history=[])

        # Send system prompt as first message to establish context
        self.chat.send_message(
            f"""[SYSTEM CONTEXT - You are now in character]

{system_prompt}

Start the session by briefly introducing yourself and the initiative you're working on.
Don't reveal too much detail - just set the stage for the discovery conversation.
Keep your introduction to 2-3 sentences."""
        )

        # Get the introduction
        intro = self.chat.last.text

        self.conversation_history.append({
            "role": "stakeholder",
            "content": intro
        })

        return intro

    def respond(self, question: str) -> str:
        """
        Respond to a question from the practitioner.

        Args:
            question: The question being asked

        Returns:
            Response from the stakeholder character
        """
        if not self.chat:
            return "Please start a session first."

        self.conversation_history.append({
            "role": "practitioner",
            "content": question
        })

        # Send the question and get response
        response = self.chat.send_message(
            f"""[The practitioner asks]: {question}

Remember:
- Stay in character as the {self.role.replace('_', ' ').title()}
- Match the depth of your answer to the depth of the question
- Don't volunteer information they haven't asked about
- Be realistic and authentic"""
        )

        answer = response.text

        self.conversation_history.append({
            "role": "stakeholder",
            "content": answer
        })

        return answer

    def _generate_use_case(self, role: str = None) -> dict:
        """Generate a new use case dynamically."""
        effective_role = role or self.role or "agent_owner"
        prompt = get_use_case_generation_prompt(effective_role)

        response = self.model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json"
            )
        )

        try:
            use_case = json.loads(response.text)
            # Handle if LLM returns a list instead of dict
            if isinstance(use_case, list) and len(use_case) > 0:
                use_case = use_case[0] if isinstance(use_case[0], dict) else {}
            if not isinstance(use_case, dict):
                use_case = {}
            # Ensure it has required fields
            if "name" not in use_case:
                use_case["name"] = "Generated Use Case"
            if "brief_description" not in use_case:
                use_case["brief_description"] = "A dynamically generated use case"
            if "hidden_details" not in use_case:
                use_case["hidden_details"] = {}
            return use_case
        except (json.JSONDecodeError, TypeError, KeyError):
            # Fallback to a sample use case if generation fails
            return random.choice(SAMPLE_USE_CASES)

    def get_use_case_brief(self) -> str:
        """Get the visible use case information (name and description)."""
        if not self.use_case:
            return "No use case selected"

        return f"""**{self.use_case.get('name', 'Unknown')}**

{self.use_case.get('brief_description', 'No description available')}"""

    def get_conversation_history(self) -> list:
        """Get the full conversation history."""
        return self.conversation_history

    def get_role_display(self) -> str:
        """Get a display-friendly role name."""
        if self.role == "agent_owner":
            return "Agent Owner"
        elif self.role == "business_owner":
            return "Business Owner"
        return "Stakeholder"
