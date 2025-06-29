from pydantic import BaseModel
from typing import List

from ..llm import Exam


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
            display: block;
            margin: 4px 0;
            padding: 5px;
            border: 1px solid #ccc;
            border-radius: 5px;
            cursor: pointer;
            width: fit-content;
        }
        .spoiler {
            background-color: black;
            color: black;
            cursor: pointer;
            display: inline-block;
            padding: 3px 6px;
            border-radius: 5px;
        }
        .spoiler.revealed {
            color: white;
        }
        .correct { background-color: #c8e6c9; }  /* green */
        .wrong { background-color: #ffcdd2; }    /* red */
        #showAnswersBtn {
            margin-bottom: 20px;
            padding: 8px 12px;
            font-size: 16px;
            cursor: pointer;
        }
    </style>
</head>
<body>

<h1>Exam</h1>
<button id="showAnswersBtn">Show Answers</button>
<div id="exam">
"""
    for i, question in enumerate(exam.questions):
        qid = f"q{i}"
        html += f"""
<div class="question" id="{qid}">
    <p><strong>Q{i + 1}:</strong> {question.content}</p>
    <div class="answers">
"""
        for ans in question.possible_answers:
            correct_class = "correct" if ans == question.correct_answer else "wrong"
            html += f'<span data-correct="{correct_class}">{ans}</span>\n'

        # Description spoiler
        html += f"""
    </div>
    <p>Description: <span class="spoiler" onclick="this.classList.toggle('revealed')">{question.description}</span></p>
</div>
"""
    html += """
</div>
<script>
    document.getElementById("showAnswersBtn").onclick = function() {
        const answers = document.querySelectorAll(".answers span");
        answers.forEach(el => {
            el.classList.add(el.dataset.correct);
        });
    };
</script>
</body>
</html>
"""
    return html
