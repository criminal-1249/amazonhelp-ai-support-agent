# imports
import sys
import json
import csv
from pathlib import Path

from tqdm import tqdm
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    classification_report,
    confusion_matrix,
)

# ------------------------------------------------------------
# Fix project imports
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.agent.intent import classify_intent
from src.agent.response import generate_response
from src.agent.escalation import decide_escalation


# ------------------------------------------------------------
# Files
# ------------------------------------------------------------

EVAL_DIR = Path(__file__).resolve().parent

GOLDEN_FILE = EVAL_DIR / "golden_eval.jsonl"
RESULTS_FILE = EVAL_DIR / "golden_eval_results.jsonl"
SUMMARY_FILE = EVAL_DIR / "golden_eval_summary.json"
CONFUSION_FILE = EVAL_DIR / "golden_eval_confusion_matrix.csv"


# ------------------------------------------------------------
# Intent
# ------------------------------------------------------------

def predict_intent(query):

    result = classify_intent(query)

    if isinstance(result, str):
        return result.strip()

    if isinstance(result, dict):
        return str(
            result.get("intent")
            or result.get("predicted_intent")
            or result.get("label")
        ).strip()

    return str(result).strip()


# ------------------------------------------------------------
# Escalation
# ------------------------------------------------------------

def predict_escalation(
    query,
    intent,
    response,
    evidence
):

    result = decide_escalation(
        query,
        intent,
        response,
        evidence
    )

    if isinstance(result, dict):
        return str(
            result.get("decision", "HUMAN")
        ).upper().strip()

    text = str(result).upper()

    if "AUTO_HANDLE" in text:
        return "AUTO_HANDLE"

    return "HUMAN"


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------

def main():

    print("=" * 70)
    print("AMAZONHELP GOLDEN EVALUATION")
    print("=" * 70)

    with open(
        GOLDEN_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        golden_data = [
            json.loads(line)
            for line in f
            if line.strip()
        ][:101]

    print(
        f"\nLoaded {len(golden_data)} golden examples."
    )

    results = []

    for item in tqdm(
        golden_data,
        desc="Running evaluation"
    ):

        query = item["customer_query"]

        result = {
            "id": item.get("id"),
            "customer_query": query,
            "gold_intent": item.get("gold_intent"),
            "gold_escalation": item.get("gold_escalation"),
            "predicted_intent": None,
            "predicted_escalation": None,
            "response": None,
            "evidence": None,
            "error": None,
        }

        try:

            # 1. Intent
            intent = predict_intent(query)

            result["predicted_intent"] = intent

            # 2. RAG response
            #
            # IMPORTANT:
            # This call may need to be adjusted depending
            # on your existing generate_response() signature.
            #
            rag_result = generate_response(
                query,
                intent
            )

            # Handle dictionary output
            if isinstance(rag_result, dict):

                response = (
                    rag_result.get("response")
                    or rag_result.get("answer")
                    or ""
                )

                evidence = (
                    rag_result.get("evidence")
                    or []
                )

            else:

                response = str(rag_result)
                evidence = []

            result["response"] = response
            result["evidence"] = evidence

            # 3. Escalation
            escalation = predict_escalation(
                query,
                intent,
                response,
                evidence
            )

            result["predicted_escalation"] = escalation

        except Exception as e:

            result["error"] = repr(e)

            # Safe fallback
            result["predicted_escalation"] = "ERROR"

        results.append(result)

    # --------------------------------------------------------
    # Intent evaluation
    # --------------------------------------------------------

    intent_results = [
        x for x in results
        if x["gold_intent"]
        and x["predicted_intent"] != "ERROR"
    ]

    if intent_results:

        y_true = [
            x["gold_intent"]
            for x in intent_results
        ]

        y_pred = [
            x["predicted_intent"]
            for x in intent_results
        ]

        labels = sorted(
            set(y_true) | set(y_pred)
        )

        accuracy = accuracy_score(
            y_true,
            y_pred
        )

        precision, recall, f1, _ = (
            precision_recall_fscore_support(
                y_true,
                y_pred,
                labels=labels,
                zero_division=0
            )
        )

        print("\n" + "=" * 70)
        print("INTENT CLASSIFICATION")
        print("=" * 70)

        print(
            f"Accuracy       : {accuracy:.4f}"
        )

        print(
            f"Macro Precision: {precision.mean():.4f}"
        )

        print(
            f"Macro Recall   : {recall.mean():.4f}"
        )

        print(
            f"Macro F1       : {f1.mean():.4f}"
        )

        print(
            "\nClassification Report:"
        )

        print(
            classification_report(
                y_true,
                y_pred,
                labels=labels,
                zero_division=0
            )
        )

    else:

        print(
            "\n⚠️ No gold_intent labels found."
        )

    # --------------------------------------------------------
    # Escalation evaluation
    # --------------------------------------------------------

    escalation_results = [
        x for x in results
        if x["gold_escalation"]
        and x["predicted_escalation"] != "ERROR"
    ]

    y_true = [
        x["gold_escalation"]
        for x in escalation_results
    ]

    y_pred = [
        x["predicted_escalation"]
        for x in escalation_results
    ]

    labels = [
        "AUTO_HANDLE",
        "HUMAN"
    ]

    accuracy = accuracy_score(
        y_true,
        y_pred
    )

    precision, recall, f1, _ = (
        precision_recall_fscore_support(
            y_true,
            y_pred,
            labels=labels,
            zero_division=0
        )
    )

    print("\n" + "=" * 70)
    print("ESCALATION CLASSIFICATION")
    print("=" * 70)

    print(
        f"Accuracy       : {accuracy:.4f}"
    )

    print(
        f"Macro Precision: {precision.mean():.4f}"
    )

    print(
        f"Macro Recall   : {recall.mean():.4f}"
    )

    print(
        f"Macro F1       : {f1.mean():.4f}"
    )

    print(
        "\nClassification Report:"
    )

    print(
        classification_report(
            y_true,
            y_pred,
            labels=labels,
            zero_division=0
        )
    )

    # --------------------------------------------------------
    # Confusion matrix
    # --------------------------------------------------------

    cm = confusion_matrix(
        y_true,
        y_pred,
        labels=labels
    )

    print("\nConfusion Matrix")
    print(
        "                 Pred AUTO    Pred HUMAN"
    )

    for i, label in enumerate(labels):

        print(
            f"Actual {label:12s}"
            f"{cm[i][0]:12d}"
            f"{cm[i][1]:13d}"
        )

    # --------------------------------------------------------
    # Save results
    # --------------------------------------------------------

    with open(
        RESULTS_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        for item in results:

            f.write(
                json.dumps(
                    item,
                    ensure_ascii=False
                )
                + "\n"
            )

    # --------------------------------------------------------
    # Save summary
    # --------------------------------------------------------

    summary = {
        "num_examples": len(results),
        "intent_evaluated": bool(intent_results),
        "escalation_accuracy": accuracy,
        "escalation_macro_precision": precision.mean(),
        "escalation_macro_recall": recall.mean(),
        "escalation_macro_f1": f1.mean(),
        "errors": sum(
            1 for x in results
            if x["error"]
        )
    }

    with open(
        SUMMARY_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            summary,
            f,
            indent=2
        )

    # --------------------------------------------------------
    # Save confusion matrix
    # --------------------------------------------------------

    with open(
        CONFUSION_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.writer(f)

        writer.writerow(
            ["Actual / Predicted"] + labels
        )

        for label, row in zip(labels, cm):

            writer.writerow(
                [label] + list(row)
            )

    print("\n" + "=" * 70)
    print("EVALUATION COMPLETE")
    print("=" * 70)

    print(
        f"\nResults: {RESULTS_FILE}"
    )

    print(
        f"Summary: {SUMMARY_FILE}"
    )

    print(
        f"Confusion matrix: {CONFUSION_FILE}"
    )


if __name__ == "__main__":
    main()