from openai import OpenAI
from pydantic import BaseModel


def _read_ctx() -> str:
    with open('.cag/root.xml', 'r') as file:
        return file.read()


_sys_prompt = f'''You are a helpful AI assistant.  
You are provided with sample exam questions and a list of potential topics.  
Use these as references to generate new, previously uncovered sub-topic questions based on the specified topics.  

Your response should include the following structured elements:  
    * content – The question itself  
    * possible_answers – Three realistic but incorrect answer choices. They should be plausible yet clearly wrong, without being too obvious  
    * correct_answer – One clearly correct answer  
    * description – A brief explanation of why the correct answer is right, and why the other choices are not  

There must be exactly four answer choices in total: one correct and three incorrect.  
Make the question challenging by ensuring the correct answer is not easily recognizable — only someone with a solid understanding should be able to identify it.

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
