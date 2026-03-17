SYSTEM_PROMPT = """
You are helping build an AI-native GTM engine for a fintech company focused on cross-border payments.

Your job is to:
1. infer what a target company does from website text,
2. identify likely payment or international expansion pain points,
3. score how strong the cross-border fit is,
4. propose a relevant outreach angle,
5. write a concise, personalised cold email.

Be specific, commercially aware, and avoid generic filler.
"""


def build_analysis_prompt(company: str, website: str, website_text: str) -> str:
    return f"""
Analyze the following company based only on the website text.

Company: {company}
Website: {website}

Website text:
\"\"\"
{website_text}
\"\"\"

Return JSON with these keys:
- company_summary: short summary of what the company does
- target_customer: who they likely serve
- likely_cross_border_need: why they might care about cross-border payments
- outreach_angle: a specific angle for outreach
- personalization_points: list of 3 concrete facts/signals from the text
- fit_score: integer from 1 to 10, where 10 means very strong relevance for cross-border payments infrastructure
"""


def build_email_prompt(company: str, analysis_json: str) -> str:
    return f"""
Using the analysis below, write one short cold outbound email to {company}.

Analysis:
{analysis_json}

Constraints:
- max 120 words
- confident, sharp, natural tone
- not overly salesy
- mention one concrete personalization point
- focus on cross-border payments / global money movement value
- include:
  1. subject
  2. email_body

Return JSON with keys:
- subject
- email_body
"""