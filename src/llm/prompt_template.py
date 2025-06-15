import textwrap


def user_query_llm_prompt(query: str) -> str:
    return f"""
You are a JSON-only generator.

Your task:
- Extract multiple CVE IDs (e.g., "CVE-2023-1234") if mentioned.
- Detect user intent: either "remediation", "summary", or "general".

Only respond in the following strict JSON format:
{{
  "cve_id": ["CVE-XXXX-YYYY" or null, "CVE-XXXX-YYYY" or null]
  "intent": "remediation" | "summary" | "general"
}}

No preamble, no explanation — just the JSON.

User query: "{query}"
"""


def get_prompts(cve_id, description) -> list:
    cve_id = cve_id.strip() if cve_id else "UNKNOWN_CVE"
    description = description.strip() if description else "No description provided."

    prompts = [
        {
            "intent": "full_summary",
            "prompt": textwrap.dedent(
                f"""
            You are a cybersecurity analyst.

            Based on the CVE below, provide:
            1. A 2–3 sentence summary.
            2. List of affected systems and components.
            3. Likely method of exploitation.
            4. Suggested remediations (patch, config, upgrade).
            5. Future hardening strategies.

            CVE ID: {cve_id}
            Description: {description}
        """
            ),
        },
        {
            "intent": "root_cause_and_fix",
            "prompt": textwrap.dedent(
                f"""
            Explain the root cause of the following vulnerability in simple terms, and then provide:
            - Potential risk if exploited
            - Known exploitation method (if any)
            - Recommended fix or mitigation

            CVE: {cve_id}
            Description: {description}
        """
            ),
        },
        {
            "intent": "risk_assessment",
            "prompt": textwrap.dedent(
                f"""
            You are conducting a risk assessment. Summarize the following CVE with:
            - A short abstract
            - Severity level (low, medium, high, critical)
            - Exploitable conditions
            - Systems at risk
            - Remediation recommendation

            CVE: {cve_id}
            {description}
        """
            ),
        },
        {
            "intent": "remediation_strategy",
            "prompt": textwrap.dedent(
                f"""
            Analyze the following vulnerability and propose an effective remediation plan.

            Include:
            - Immediate remediation steps
            - Alternative temporary mitigations
            - Long-term hardening guidance

            CVE: {cve_id}
            {description}
        """
            ),
        },
        {
            "intent": "engineering_ticket",
            "prompt": textwrap.dedent(
                f"""
            Write a security engineering ticket based on the following CVE. The ticket should include:
            - Title
            - Summary of the issue
            - Impacted systems
            - Required remediation steps
            - Priority (Low/Medium/High/Critical)

            CVE: {cve_id}
            {description}
        """
            ),
        },
        {
            "intent": "educational_summary",
            "prompt": textwrap.dedent(
                f"""
            Explain the vulnerability below as if you're teaching a junior developer.

            Include:
            - What caused the vulnerability?
            - Why is it dangerous?
            - How to prevent it in future code

            CVE: {cve_id}
            {description}
        """
            ),
        },
    ]

    return prompts
