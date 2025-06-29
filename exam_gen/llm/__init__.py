from openai import OpenAI
from pydantic import BaseModel


def _read_ctx() -> str:
    with open('.cag/root.xml', 'r') as file:
        return file.read()


_sys_prompt = f'''You are a helpful AI assistant. 
You are given sample exam questions and a list of possible topics.
Use the provided topics and sample questions as a reference.
Your task is to generate the requested number of new, uncovered sub-topic questions based on the specified topics.
Return a structured response consisting of:  
    * content – The question content;  
    * possible_answers – Three realistic answer choices;  
    * correct_answer – Exactly one correct answer;  
    * description – An explanation of why the correct answer is correct and why the others are not.

{_read_ctx()}
'''


class Question(BaseModel):
    content: str
    possible_answers: list[str]
    correct_answer: str
    description: str


class Exam(BaseModel):
    questions: list[Question]


def gen_exam(
        topics: list[str],
        q_amount: int,
        client: OpenAI,
        model: str,
        **kwargs
) -> list[Question]:
    res = client.chat.completions.parse(
        model=model,
        messages=[
            {'role': 'system', 'content': _sys_prompt},
            {'role': 'user', 'content': f'Plesae generate {q_amount} questions on those topics: {topics}'}
        ],
        response_format=Exam,
        user='exam',
        **kwargs
    )

    return res.choices[0].message.parsed
