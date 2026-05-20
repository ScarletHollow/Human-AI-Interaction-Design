# Human-AI Interaction Design: Chatbot Evaluation

Public portfolio version of a Human-AI Interaction Design project evaluating
assistant behaviour across healthcare, education, and travel scenarios. The
project compares chatbot responses using turn-level emotion analysis and
questionnaire-style evaluation dimensions such as trust, empathy, effectiveness,
user experience, and safety.

Coursework mark: 76.6/100.

## What This Project Shows

- Conversation-level evaluation design for multiple assistant types.
- Turn-level emotion scoring with NRC-style emotion categories.
- Sentiment and subjectivity analysis using TextBlob.
- Aggregation by assistant, task, domain, and speaker role.
- Questionnaire visualisation across trust, empathy, effectiveness, UX, and
  safety.
- Privacy-aware public release that excludes raw transcripts and screenshots.

## Repository Structure

```text
.
├── src/
│   ├── analyse_conversations.py    # Pipeline for private raw transcript CSVs
│   └── plot_public_results.py      # Rebuilds figures from public aggregate data
├── data/
│   ├── aggregate_emotion_metrics.csv
│   ├── turn_metrics_no_text.csv
│   └── questionnaire_summary.csv
├── figures/
│   ├── conversation-emotion/        # Generated conversation emotion plots
│   └── questionnaire/               # Questionnaire summary charts
├── requirements.txt
└── README.md
```

## Data Privacy

The original work used chatbot transcripts and interaction screenshots. Those
raw materials are not included in this public version because they contain
conversation text, user prompts, and evaluation context. The public data keeps
only derived numerical metrics and aggregate figures.

`turn_metrics_no_text.csv` deliberately omits the original `text` column while
preserving turn order, speaker role, timing, and emotion scores.

## Quick Start

Install dependencies:

```powershell
pip install -r requirements.txt
```

Regenerate portfolio summary figures from public aggregate data:

```powershell
python src/plot_public_results.py
```

The generated figures will be written to:

```text
figures/generated/
```

## Running The Private-Data Pipeline

If you have a private transcript CSV with `speaker` and `text` columns:

```powershell
python src/analyse_conversations.py private_transcript.csv `
  --output-dir outputs `
  --scenario-id healthcare_sleep_chatgpt `
  --domain Healthcare `
  --task "Sleep schedule support" `
  --assistant ChatGPT
```

The script writes anonymised metrics and aggregate summaries without exporting
raw conversation text.

## Evaluation Scope

The project includes scenarios across:

- Healthcare: sleep schedule support.
- Education: presentation anxiety support.
- Travel and tourism: itinerary planning and hotel delay/refund support.

The assistants evaluated include general-purpose LLM assistants and
domain-specific chatbot experiences.

## Notes

This repository is a cleaned public version for portfolio use. Raw transcripts,
screenshots, assignment files, assessment records, zip submissions, and private
course materials are not included.
