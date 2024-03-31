from typing import List
from random import shuffle
import spacy
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.prompts import PromptTemplate


lang_chain = ChatOpenAI(
    openai_api_key="<include your own token", model="gpt-3.5-turbo")
nlp = spacy.load("en_core_web_sm")


def extract_skills(job_description):
    doc = nlp(job_description)
    skills = [token.text for token in doc if token.pos_ in ['PROPN', 'NOUN']]
    return skills


class MCQ(BaseModel):
    question: str = Field(description="The multiple-choice question")
    options: List[str] = Field(
        description="A list of all answer options, correct and incorrect mixed")


def generate_questions_from_jd(job_id):
    job_description = fetch_job_description(job_id)
    skills = extract_skills(job_description)
    questions = []
    print(skills)
    skills_list = ", ".join(skills)
    for _ in range(1):  # Generate 5 questions
        mcq_query = f"Generate a beginner-level multiple-choice question that tests the basic understanding of any one of the {skills_list}. Include one correct answer and three plausible but incorrect options."

        parser = JsonOutputParser(pydantic_object=MCQ)
        prompt = PromptTemplate(
            template="Based on the job description, create a multiple-choice question on the skills mentioned with one correct answer and three incorrect options.\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={
                "format_instructions": parser.get_format_instructions()},
        )

        chain = prompt | lang_chain | parser
        result = chain.invoke({"query": mcq_query})

        if result['options']:
            shuffle(result['options'])
            questions.append(result)

    return questions


def fetch_job_description(job_id):
    return """Entry-Level Oracle Peoplesoft Developer requirements are:

Bachelor's degree.
Proficiency in at least one modern Object-Oriented Programming (OOP) language such as Java, C#, or similar, with a solid foundation in programming concepts, data structures, algorithms, databases, and SQL.
Familiarity with IT service management processes.
Ability to obtain a Secret Clearance.
Legally authorized to work in the U.S. under SkillStorm's W2; not a C2C position. EOE, including disability/vets.
Willingness to relocate if necessary.
Strong analytical and problem-solving skills, with a logical mindset.
Excellent verbal and written communication skills.
Entry-Level Oracle Peoplesoft Developer responsibilities include:

Leverage SQR/Application Engines and App Packages, SQL and SQL tuning, content management systems, and internet facing websites and Web services to configure, customize, and tune Peoplesoft HCM applications - payroll, compensation, benefits, etc.
Engage in the end-to-end software development lifecycle, from design and coding to testing and documentation, ensuring the delivery of robust and scalable solutions.
Collaborate with project teams to understand requirements and successfully implement new features or modifications, adhering to best practices and industry standards.
Develop and maintain automated test suites and frameworks to ensure the reliability and efficiency of software applications.
Demonstrate meticulous attention to detail, ensuring that solutions align with business objectives and are easily maintainable.
 

Where SkillStorm stands out:

Competitive salary
Enterprise-level technology training and certification
Opportunity to work for Fortune 500 companies
Health, Vision, Dental, and Life Insurance with 401K
Continuous mentorship and support"""


job_id = 'example_job_id'
questions = generate_questions_from_jd(job_id)

for question in questions:
    print(question)
