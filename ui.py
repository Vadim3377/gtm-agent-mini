import json
import streamlit as st

from scraper import scrape_multiple_pages
from prompts import SYSTEM_PROMPT, build_analysis_prompt, build_email_prompt
from llm import call_llm_json


st.set_page_config(page_title="GTM Agent Mini", layout="wide")

st.title("GTM Agent Mini")
st.caption("AI-native prospect research and personalised outreach for fintech GTM.")

with st.sidebar:
    st.header("Inputs")
    company = st.text_input("Company name", placeholder="e.g. Deel")
    website = st.text_input("Website", placeholder="https://www.deel.com")
    run_button = st.button("Generate outreach", use_container_width=True)

if run_button:
    if not company or not website:
        st.error("Please enter both a company name and a website.")
    else:
        with st.spinner("Scraping company pages..."):
            website_text = scrape_multiple_pages(website)

        if website_text.startswith("SCRAPE_ERROR:"):
            st.error(website_text)
        else:
            with st.spinner("Running GTM analysis..."):
                analysis_prompt = build_analysis_prompt(company, website, website_text)
                analysis = call_llm_json(SYSTEM_PROMPT, analysis_prompt)

            with st.spinner("Generating personalised email..."):
                email_prompt = build_email_prompt(
                    company,
                    json.dumps(analysis, ensure_ascii=False)
                )
                email = call_llm_json(SYSTEM_PROMPT, email_prompt)

            left, right = st.columns([1, 1])

            with left:
                st.subheader("Company analysis")
                st.write("**Summary**")
                st.write(analysis.get("company_summary", ""))

                st.write("**Target customer**")
                st.write(analysis.get("target_customer", ""))

                st.write("**Likely cross-border need**")
                st.write(analysis.get("likely_cross_border_need", ""))

                st.write("**Outreach angle**")
                st.write(analysis.get("outreach_angle", ""))

                points = analysis.get("personalization_points", [])
                if points:
                    st.write("**Personalization points**")
                    for p in points:
                        st.write(f"- {p}")

                fit_score = analysis.get("fit_score")
                if fit_score is not None:
                    st.metric("Fit score", fit_score)

            with right:
                st.subheader("Generated outreach")
                st.write("**Subject**")
                st.code(email.get("subject", ""), language=None)

                st.write("**Email body**")
                st.text_area(
                    "Email preview",
                    value=email.get("email_body", ""),
                    height=220,
                    label_visibility="collapsed",
                )

            with st.expander("Scraped text preview"):
                st.write(website_text[:6000])