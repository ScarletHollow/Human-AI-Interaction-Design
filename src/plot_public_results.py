"""Generate portfolio figures from the public aggregate datasets."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
FIGURE_DIR = ROOT / "figures" / "generated"


def plot_assistant_sentiment() -> None:
    aggregate = pd.read_csv(DATA_DIR / "aggregate_emotion_metrics.csv")
    assistants = (
        aggregate.groupby(["assistant"], as_index=False)[["mean_positive", "mean_negative", "mean_trust", "mean_fear"]]
        .mean()
        .sort_values("assistant")
    )

    ax = assistants.set_index("assistant").plot(kind="bar", figsize=(9, 5), width=0.78)
    ax.set_title("Mean Conversation Emotion Scores By Assistant")
    ax.set_ylabel("Mean score")
    ax.set_xlabel("")
    ax.legend(title="Metric", loc="upper right")
    ax.tick_params(axis="x", rotation=20)
    plt.tight_layout()
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    plt.savefig(FIGURE_DIR / "assistant_emotion_summary.png", dpi=180)
    plt.close()


def plot_questionnaire_summary() -> None:
    questionnaire = pd.read_csv(DATA_DIR / "questionnaire_summary.csv")
    pivot = questionnaire.pivot_table(index="assistant", columns="dimension", values="score", aggfunc="mean")
    ax = pivot.plot(kind="bar", figsize=(9, 5), width=0.78)
    ax.set_title("Mean Questionnaire Scores By Assistant")
    ax.set_ylabel("Score")
    ax.set_ylim(0, 5)
    ax.set_xlabel("")
    ax.legend(title="Dimension", loc="lower right")
    ax.tick_params(axis="x", rotation=20)
    plt.tight_layout()
    FIGURE_DIR.mkdir(parents=True, exist_ok=True)
    plt.savefig(FIGURE_DIR / "assistant_questionnaire_summary.png", dpi=180)
    plt.close()


def main() -> None:
    plot_assistant_sentiment()
    plot_questionnaire_summary()


if __name__ == "__main__":
    main()
