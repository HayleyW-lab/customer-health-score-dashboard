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

## Entry 2 — Data Schema Design

**Date:** [today's date]

Designed the data schema for the synthetic dataset, working through each
churn-risk signal one at a time and deciding on raw fields rather than
pre-calculated metrics, so the scoring logic (next step) reflects my own
judgement rather than being baked into the data itself.

**Schema so far:**

- **Usage:** logins_last_30_days, logins_31_to_60_days_ago,
  logins_61_to_90_days_ago (3 periods for a trend, not just before/after)
- **Support tickets:** support_tickets_last_90_days,
  high_severity_tickets_last_90_days, open_tickets_count,
  avg_days_open_for_unresolved, resolved_tickets_count,
  avg_resolution_time_days
- **Renewal/engagement:** days_until_renewal, contract_length_months,
  cs_touchpoints_last_90_days, days_since_last_contact
- **Satisfaction:** latest_nps_score, latest_csat_score,
  days_since_last_survey_response
- **Champion turnover:** champion_changed_last_90_days,
  days_since_champion_change, champion_tenure_at_company_months

**Key insight to carry into scoring logic (not a data field):**
Champion-change data is only as reliable as how recently we've actually
checked in. If `days_since_last_contact` is high (e.g. 90+ days) and
`champion_changed_last_90_days` says "No," that shouldn't be read as
"stable" — it likely means we simply don't know. The scoring logic
should treat long-uncontacted accounts as _unverified_, not safe. This
is the kind of real-world CS judgement a naive model would miss.

**Still to design:** onboarding completion, new staff/turnover, training
on core + newly released features, add-on/module whitespace.

## Entry 3 — Full Churn-Risk Signal Schema

**Date:** [today's date]

Completed the full data schema for the synthetic dataset, working through
all 9 churn-risk signal categories one at a time. Every field is grounded
in real patterns from my own CS/implementation experience (Wise.NET,
Spotlight Reporting, ASG Education) rather than a generic churn-prediction
tutorial — including a real 32-step implementation process, SugarCRM's
call/email/document activity logging, and a defined retention cadence
(first call → 1-month check-in → quarterly check-ins).

**Final schema by signal:**

1. **Usage:** logins_last_30_days, logins_31_to_60_days_ago,
   logins_61_to_90_days_ago
2. **Support tickets:** support_tickets_last_90_days,
   high_severity_tickets_last_90_days, open_tickets_count,
   avg_days_open_for_unresolved, resolved_tickets_count,
   avg_resolution_time_days
3. **Renewal/engagement:** days_until_renewal, contract_length_months,
   cs_touchpoints_last_90_days, days_since_last_contact,
   first_retention_call_completed, one_month_checkin_completed,
   quarterly_checkins_scheduled, quarterly_checkins_completed
4. **Satisfaction:** latest_nps_score, latest_csat_score,
   days_since_last_survey_response
5. **Champion turnover:** champion_changed_last_90_days,
   days_since_champion_change, champion_tenure_at_company_months
6. **Onboarding:** onboarding_steps_total, onboarding_steps_completed,
   onboarding_completed_flag, addons_purchased_count,
   free_training_hours_used, extra_paid_training_hours_purchased,
   onsite_training_delivered
7. **Staff/training:** new_staff_last_90_days, new_staff_trained_count,
   staff_trained_on_system_pct
8. **Feature training:** core_features_trained_pct,
   release_email_open_rate, feature_confusion_tickets_last_90_days,
   days_since_last_feature_training
9. **Whitespace/upsell:** core_features_available_count,
   core_features_actively_used_count, addons_available_count,
   upsell_opportunity_flagged_last_90_days, upsell_demo_delivered,
   upsell_converted

**Key judgement calls baked into the design (not the data generation):**

- Champion-change data should be treated as _unverified_, not _stable_,
  when days_since_last_contact is high
- Whitespace only gets closed through action (retention call → demo →
  quote → implementation) — a real example from my own experience: grew
  one Essentials client from $1,000/year to a $60,000 account this way
- Feature-release training was passive (email only) — support tickets
  consistently spiked after releases, which is why confusion tickets are
  tracked as the real signal instead of a fake "trained on release" flag

**Next up:** Write the Python script to generate the synthetic dataset —
need to decide on customer count and how to keep generated data internally
consistent (e.g. a high-risk customer shouldn't randomly also have a
perfect NPS score).
