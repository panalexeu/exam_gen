import random
from typing import List

from ..llm import Exam


def _unique(seq: List[str]) -> List[str]:
    """Return seq with duplicates removed, preserving original order."""
    seen = set()
    return [x for x in seq if not (x in seen or seen.add(x))]


def exam_to_html(exam: Exam) -> str:
    html = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Exam</title>
<style>
    body { font-family: sans-serif; padding: 20px; }
    .question { margin-bottom: 30px; }
    .answers span {
        display: block; margin: 4px 0; padding: 5px;
        border: 1px solid #ccc; border-radius: 5px;
        cursor: pointer; width: fit-content;
    }
    .spoiler {
        background-color: black; color: black; cursor: pointer;
        display: inline-block; padding: 3px 6px; border-radius: 5px;
    }
    .spoiler.revealed { color: white; }
    .correct { background-color: #c8e6c9; }
    .wrong   { background-color: #ffcdd2; }
    .disabled { pointer-events: none; opacity: 0.6; }
</style>
</head>
<body>

<h1>Exam</h1>
<div id="exam">
"""

    for idx, q in enumerate(exam.questions):
        answers = _unique(q.possible_answers)  # de-dupe wrong answers
        if q.correct_answer not in answers:
            answers.append(q.correct_answer)
        answers = _unique(answers)  # sanity re-de-dupe
        random.shuffle(answers)

        html += f"""
<div class="question" id="q{idx}">
    <p><strong>Q{idx + 1}:</strong> {q.content}</p>
    <div class="answers">
"""
        for ans in answers:
            html += f'<span data-correct="{str(ans == q.correct_answer).lower()}">{ans}</span>\n'
        html += f"""
    </div>
    <p>Description: <span class="spoiler">{q.description}</span></p>
</div>
"""

    html += """
</div>

<script>
document.addEventListener("DOMContentLoaded", () => {

    // Spoiler toggle
    document.querySelectorAll(".spoiler").forEach(el =>
        el.addEventListener("click", () => el.classList.toggle("revealed"))
    );

    // Answer selection logic
    document.querySelectorAll(".answers").forEach(group => {
        group.querySelectorAll("span").forEach(option => {
            option.addEventListener("click", () => {
                if (group.classList.contains("disabled")) return;

                const isCorrect = option.dataset.correct === "true";
                option.classList.add(isCorrect ? "correct" : "wrong");

                group.querySelectorAll("span").forEach(span => {
                    span.classList.add("disabled");
                    if (span.dataset.correct === "true") span.classList.add("correct");
                });
                group.classList.add("disabled");
            });
        });
    });

});
</script>

</body>
</html>
"""
    return html
