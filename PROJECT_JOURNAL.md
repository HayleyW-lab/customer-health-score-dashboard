# Project Journal — Customer Health Score Dashboard

## Entry 1 — Project Setup

**Date:** 1 October 2026

Kicked off Project 2 in the portfolio roadmap: a Customer Health Score /
Churn-Risk Dashboard. This extends the AI + sales-judgement approach from
the Lead Qualification Agent into the retention side of the customer
lifecycle, and adds a data visualization component — a gap in my current
portfolio.

**Stack decisions:**

- Python again, for consistency across portfolio projects and because
  it's well-suited to both scoring logic and data viz
- Pandas for data handling
- Plotly for charts — chosen over Matplotlib because this is an
  interactive dashboard people will click around, not a static report,
  and it integrates cleanly with Streamlit (`st.plotly_chart`)
- Streamlit again for the UI — proven to work well last project, and
  gives a live shareable link for recruiters

**Setup completed:**

- New repo, isolated from Lead Qualification Agent
- Virtual environment (venv) to keep dependencies sealed off from other
  projects
- requirements.txt locked in (pandas, plotly, streamlit) so the
  environment is reproducible
- .gitignore configured (venv/, **pycache**/, .env, etc.) — same lesson
  as before: never commit secrets or the venv itself
- Pushed to GitHub: github.com/HayleyW-lab/customer-health-score-dashboard

**Next up:** Defining what "customer health" and "churn risk" actually
mean for this project — what signals realistically predict churn, and
whether to use a synthetic dataset or a public one (e.g. Kaggle) as a
starting point. This is the step that will make the project reflect real
judgement rather than a generic tutorial.
