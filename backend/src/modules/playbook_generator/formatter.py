import re
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class PlaybookFormatter:
    """Format and parse playbook output"""

    def parse_playbook(self, playbook_text: str) -> Dict:
        """Parse playbook text into structured format"""
        try:
            # Extract title
            title = self._extract_title(playbook_text)

            # Extract summary
            summary = self._extract_summary(playbook_text)

            # Extract steps
            steps = self._extract_steps(playbook_text)

            # Extract metadata
            estimated_time = self._extract_estimated_time(playbook_text)
            risk_level = self._extract_risk_level(playbook_text)

            return {
                "title": title,
                "summary": summary,
                "steps": steps,
                "estimated_time": estimated_time,
                "risk_level": risk_level
            }
        except Exception as e:
            logger.error(f"Error parsing playbook: {str(e)}")
            return self._default_playbook()

    def _extract_title(self, text: str) -> str:
        """Extract title from playbook"""
        match = re.search(r'^#\s+(.+)', text, re.MULTILINE)
        if match:
            return match.group(1).strip()
        return "Incident Remediation Playbook"

    def _extract_summary(self, text: str) -> str:
        """Extract summary from playbook"""
        summary_match = re.search(
            r'##\s+Summary\s*\n(.+?)(?=\n##|\Z)', text, re.DOTALL | re.IGNORECASE)
        if summary_match:
            return summary_match.group(1).strip()
        return "No summary available"

    def _extract_steps(self, text: str) -> List[Dict]:
        """Extract steps from playbook"""
        steps = []

        # Find all step sections
        step_pattern = r'###\s+Step\s+(\d+):?\s+(.+?)\n(.+?)(?=###\s+Step|\n##|\Z)'
        matches = re.finditer(step_pattern, text, re.DOTALL | re.IGNORECASE)

        for match in matches:
            step_num = int(match.group(1))
            step_title = match.group(2).strip()
            step_content = match.group(3).strip()

            # Extract details from step content
            action = step_title
            command = self._extract_field(step_content, "Command")
            expected_outcome = self._extract_field(step_content, "Expected Outcome")
            verification = self._extract_field(step_content, "Verification")

            steps.append({
                "step_number": step_num,
                "action": action,
                "command": command,
                "expected_outcome": expected_outcome or "Step completed successfully",
                "verification": verification
            })

        return steps if steps else self._default_steps()

    def _extract_field(self, text: str, field_name: str) -> str:
        """Extract a specific field from text"""
        pattern = rf'\*\*{field_name}\*\*:?\s*(.+?)(?=\n\*\*|\Z)'
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            value = match.group(1).strip()
            # Clean up markdown code blocks
            value = re.sub(r'`([^`]+)`', r'\1', value)
            return value
        return None

    def _extract_estimated_time(self, text: str) -> str:
        """Extract estimated time"""
        match = re.search(
            r'##\s+Estimated Time\s*\n(.+?)(?=\n##|\Z)', text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return "30-60 minutes"

    def _extract_risk_level(self, text: str) -> str:
        """Extract risk level"""
        match = re.search(
            r'##\s+Risk Level\s*\n(.+?)(?=\n##|\Z)', text, re.IGNORECASE)
        if match:
            risk = match.group(1).strip().lower()
            if 'critical' in risk:
                return "Critical"
            elif 'high' in risk:
                return "High"
            elif 'low' in risk:
                return "Low"
            return "Medium"
        return "Medium"

    def _default_playbook(self) -> Dict:
        """Return default playbook structure"""
        return {
            "title": "Incident Remediation Playbook",
            "summary": "Unable to generate playbook. Please check the incident description and try again.",
            "steps": self._default_steps(),
            "estimated_time": "Unknown",
            "risk_level": "Medium"
        }

    def _default_steps(self) -> List[Dict]:
        """Return default steps"""
        return [
            {
                "step_number": 1,
                "action": "Assess the situation",
                "command": None,
                "expected_outcome": "Clear understanding of the incident",
                "verification": "Document findings"
            }
        ]
