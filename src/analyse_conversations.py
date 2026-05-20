"""Conversation emotion-analysis pipeline.

This script expects a private CSV with at least these columns:

- speaker
- text
- optional t_min

It outputs:

- turn_metrics_no_text.csv: turn-level emotion metrics with raw text removed
- aggregate_emotion_metrics.csv: speaker-level aggregate metrics

Raw conversation text is intentionally not written to the public outputs.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from nrclex import NRCLex
from textblob import TextBlob


EMOTION_COLUMNS = [
    "joy",
    "trust",
    "fear",
    "anger",
    "sadness",
    "disgust",
    "surprise",
    "anticipation",
    "positive",
    "negative",
]


def score_text(text: str) -> dict[str, float]:
    """Return NRC emotion proportions plus TextBlob polarity/subjectivity."""
    safe_text = "" if pd.isna(text) else str(text)
    nrc = NRCLex(safe_text)
    raw_scores = {emotion: float(nrc.raw_emotion_scores.get(emotion, 0.0)) for emotion in EMOTION_COLUMNS}
    total = sum(raw_scores.values()) or 1.0
    normalized = {emotion: raw_scores[emotion] / total for emotion in EMOTION_COLUMNS}

    blob = TextBlob(safe_text)
    normalized["polarity"] = float(blob.sentiment.polarity)
    normalized["subjectivity"] = float(blob.sentiment.subjectivity)
    return normalized


def analyse(input_csv: Path, output_dir: Path, scenario_id: str, domain: str, task: str, assistant: str) -> None:
    df = pd.read_csv(input_csv)
    required = {"speaker", "text"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Input CSV missing required columns: {', '.join(sorted(missing))}")

    if "turn_index" not in df.columns:
        df["turn_index"] = range(1, len(df) + 1)
    if "t_min" not in df.columns:
        df["t_min"] = 0.0

    scores = pd.DataFrame([score_text(text) for text in df["text"]])
    scored = pd.concat([df[["speaker", "turn_index", "t_min"]], scores], axis=1)
    scored.insert(0, "assistant", assistant)
    scored.insert(0, "task", task)
    scored.insert(0, "domain", domain)
    scored.insert(0, "scenario_id", scenario_id)

    aggregate = (
        scored.groupby(["scenario_id", "domain", "task", "assistant", "speaker"], as_index=False)
        .agg(
            turns=("turn_index", "count"),
            mean_t_min=("t_min", "mean"),
            **{f"mean_{col}": (col, "mean") for col in [*EMOTION_COLUMNS, "polarity", "subjectivity"]},
        )
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    scored.to_csv(output_dir / "turn_metrics_no_text.csv", index=False)
    aggregate.to_csv(output_dir / "aggregate_emotion_metrics.csv", index=False)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyse chatbot conversation emotion metrics.")
    parser.add_argument("input_csv", type=Path)
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    parser.add_argument("--scenario-id", default="scenario")
    parser.add_argument("--domain", default="domain")
    parser.add_argument("--task", default="task")
    parser.add_argument("--assistant", default="assistant")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    analyse(
        input_csv=args.input_csv,
        output_dir=args.output_dir,
        scenario_id=args.scenario_id,
        domain=args.domain,
        task=args.task,
        assistant=args.assistant,
    )


if __name__ == "__main__":
    main()
