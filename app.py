import json
import pandas as pd
from tqdm import tqdm

from scraper import scrape_multiple_pages
from prompts import SYSTEM_PROMPT, build_analysis_prompt, build_email_prompt
from llm import call_llm_json
from utils import safe_join_lines


def process_company(company: str, website: str) -> dict:
    website_text = scrape_multiple_pages(website)

    if website_text.startswith("SCRAPE_ERROR:"):
        return {
            "company": company,
            "website": website,
            "scrape_status": "failed",
            "company_summary": "",
            "target_customer": "",
            "likely_cross_border_need": "",
            "outreach_angle": "",
            "personalization_points": "",
            "subject": "",
            "email_body": "",
            "error": website_text,
        }

    analysis_prompt = build_analysis_prompt(company, website, website_text)
    analysis = call_llm_json(SYSTEM_PROMPT, analysis_prompt)

    email_prompt = build_email_prompt(company, json.dumps(analysis, ensure_ascii=False))
    email = call_llm_json(SYSTEM_PROMPT, email_prompt)

    return {
        "company": company,
        "website": website,
        "scrape_status": "success",
        "company_summary": safe_join_lines(analysis.get("company_summary", "")),
        "target_customer": safe_join_lines(analysis.get("target_customer", "")),
        "likely_cross_border_need": safe_join_lines(analysis.get("likely_cross_border_need", "")),
        "outreach_angle": safe_join_lines(analysis.get("outreach_angle", "")),
        "personalization_points": " | ".join(analysis.get("personalization_points", [])),
        "subject": email.get("subject", ""),
        "email_body": email.get("email_body", ""),
        "error": "",
    }


def main() -> None:
    df = pd.read_csv("input_companies.csv")
    results = []

    for _, row in tqdm(df.iterrows(), total=len(df), desc="Processing companies"):
        result = process_company(row["company"], row["website"])
        results.append(result)

    out_df = pd.DataFrame(results)
    out_df.to_csv("output_emails.csv", index=False)

    print("\nDone. Results saved to output_emails.csv\n")
    print(out_df[["company", "subject", "email_body", "scrape_status", "error"]])


if __name__ == "__main__":
    main()