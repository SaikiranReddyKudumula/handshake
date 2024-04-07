from typing import List
from random import shuffle
import os
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.prompts import PromptTemplate
from langchain_mistralai.chat_models import ChatMistralAI


class SKILLS(BaseModel):
    options: List[str] = Field(
        description="A list of all technical skills extracted from the job description.")


class MCQ(BaseModel):
    question: str = Field(description="The multiple-choice question")
    options: List[str] = Field(
        description="A list of all answer options, correct and incorrect mixed")


class JobDescriptionProcessor:
    def __init__(self, openai_api_key: str, mistral_api_key: str):
        self.lang_chain_openai = ChatOpenAI(
            openai_api_key=openai_api_key, model="gpt-4")
        self.lang_chain_mistral = ChatMistralAI(
            model="mistral-large-latest", temperature=0, mistral_api_key=mistral_api_key)

    def get_job_description_from_file(self, file_path: str) -> str:
        """Reads a job description from a specified text file."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        with open(file_path, 'r', encoding='utf-8') as file:
            job_description = file.read()
        return job_description

    def extract_skills(self, job_description: str) -> List[str]:
        template = """
        system:You are an assistant knowledgeable in identifying technical skills from job descriptions. Your task is to analyze the provided job description and list only the core technical skills mentioned. Focus on programming languages, engineering practices, and any tools or technologies specified that can be generalized or observed in resumes. Avoid including general skills or attributes that are not technical in nature.
        job description: {query}\n{format_instructions}\n
        """
        parser = JsonOutputParser(pydantic_object=SKILLS)
        prompt = PromptTemplate(
            template=template,
            input_variables=["query"],
            partial_variables={
                "format_instructions": parser.get_format_instructions()},
        )
        # can use either openai or mistral
        # runnable = prompt | self.lang_chain_mistral | parser
        runnable = prompt | self.lang_chain_openai | parser
        result = runnable.invoke({"query": job_description})
        if result['options']:
            shuffle(result['options'])
        return result['options']

    def generate_questions_from_jd(self, job_description: str) -> List[dict]:
        skills = self.extract_skills(job_description)
        questions = []
        for skill in skills[:5]:  # Generate questions for the first 5 skills
            mcq_query = f"Generate a beginner-level multiple-choice question that tests the basic understanding of {skill}. Include one correct answer and three plausible but incorrect options."
            parser = JsonOutputParser(pydantic_object=MCQ)
            prompt = PromptTemplate(
                template="Based on the skills list, create a multiple-choice question on the skills mentioned with one correct answer and three incorrect options.\n{format_instructions}\n{query}\n",
                input_variables=["query"],
                partial_variables={
                    "format_instructions": parser.get_format_instructions()},
            )
            chain = prompt | self.lang_chain_openai | parser
            result = chain.invoke({"query": mcq_query})

            if result['options']:
                shuffle(result['options'])
                questions.append(result)
        return questions


if __name__ == "__main__":
    # Specify the path to your job description file
    file_path = "job_description.txt"
    processor = JobDescriptionProcessor(
        openai_api_key="<insert your own key>", mistral_api_key="<insert your own key>")

    try:
        job_description = processor.get_job_description_from_file(file_path)
        print("Job Description:", job_description)
        questions = processor.generate_questions_from_jd(job_description)
        for question in questions:
            print(question)
    except FileNotFoundError as e:
        print(e)
