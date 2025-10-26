#! /usr/bin/env python3
"""
Senior Data Scientist: Dr. Eddy Giusepe Chirinos Isidro

Script interview_practice_system.py
===================================
Este script é responsável por preparar a prática de entrevista mock
para um cargo específico em uma empresa específica.
Este estudo foi baseado no tutorial de Miguel Otero Pedrido e Alessandro Romano.

Run
---
uv run interview_practice_system.py
"""

import asyncio

from crewai import Agent, Crew, Process, Task
from crewai_tools import SerperDevTool
from pydantic import BaseModel, Field


class QuestionAnswerPair(BaseModel):
    """Schema para a pergunta e sua resposta correta."""

    question: str = Field(..., description="A pergunta técnica a ser feita")
    correct_answer: str = Field(..., description="A resposta correta para a pergunta")


# Inicializa a ferramenta de busca:
search_tool = SerperDevTool()

# Primeira Crew: Preparação da Pergunta
# Cria o agente de pesquisa da empresa
company_researcher = Agent(
    role="Especialista em Pesquisa de Empresa",
    goal="Coletar informações sobre a empresa e criar perguntas de entrevista com respostas",
    backstory="""Você é um especialista em pesquisar empresas e criar perguntas de entrevista técnicas.
    Você tem conhecimento profundo das práticas de contratação da indústria de tecnologia e pode criar
    perguntas relevantes que testam tanto conhecimento teórico quanto habilidades práticas.""",
    tools=[search_tool],
    verbose=True,
)


question_preparer = Agent(
    role="Preparador de Perguntas e Respostas",
    goal="Preparar perguntas e respostas completas com respostas modeladas",
    backstory="""Você é um entrevistador técnico experiente que sabe como criar
    perguntas desafiadoras, mas justas, e fornecer respostas detalhadas modeladas.
    Você entende como avaliar diferentes níveis de habilidade e criar perguntas que
    testam tanto conhecimento teórico quanto habilidades de resolução de problemas práticas.""",
    verbose=True,
)


# Segunda Crew: Avaliação da Resposta
# Cria o agente de avaliação da resposta:
answer_evaluator = Agent(
    role="Avaliador de Respostas",
    goal="Avaliar se a resposta dada é correta para a pergunta",
    backstory="""Você é um entrevistador técnico experiente que avalia respostas
    contra a solução esperada. Você sabe como identificar se uma resposta é
    técnicamente correta e completa.""",
    verbose=True,
)


# Cria o agente de pergunta de follow-up:
follow_up_questioner = Agent(
    role="Especialista em Perguntas de Follow-up",
    goal="Criar perguntas de follow-up relevantes com base no contexto",
    backstory="""Você é um entrevistador técnico experiente que sabe como criar
    perguntas de follow-up significativas que exploram mais profundamente o conhecimento
    e compreensão do candidato. Você pode criar perguntas que sejam baseadas em respostas
    anteriores e testem diferentes aspectos da expertise técnica do candidato.""",
    verbose=True,
)


# Cria as tarefas para a primeira crew:
def create_company_research_task(company_name: str, role: str, difficulty: str) -> Task:
    return Task(
        description=f"""Pesquise {company_name} e colete informações sobre:
        1. Seu processo de entrevista técnica
        2. Perguntas de entrevista comuns para cargos de {role} no nível de dificuldade {difficulty}
        3. Pilha técnica e requisitos
        Forneça um resumo de suas descobertas.""",
        expected_output="""Um resumo das descobertas sobre os requisitos técnicos da empresa e seu
                           processo de entrevista técnica""",
        agent=company_researcher,
    )


def create_question_preparation_task(difficulty: str) -> Task:
    return Task(
        description=f"""Baseado na pesquisa da empresa, crie:
        1. Uma pergunta técnica no nível de dificuldade {difficulty} que testa tanto teoria quanto prática
        2. Uma resposta modelada que cubra todos os pontos chave
        3. Pontos chave para serem buscados nas respostas do candidato
        A pergunta deve ser apropriada para o nível de dificuldade {difficulty} - desafiadora, mas justa,
        e a resposta deve ser detalhada.""",
        expected_output="""Uma pergunta e sua resposta correta""",
        output_pydantic=QuestionAnswerPair,
        agent=question_preparer,
    )


# Cria a tarefa para a segunda crew:
def create_evaluation_task(question: str, user_answer: str, correct_answer: str) -> Task:
    return Task(
        description=f"""Avalie se a resposta dada é correta para a pergunta:
        Pergunta: {question}
        Resposta: {user_answer}
        Resposta Correta: {correct_answer}
        Forneça:
        1. Se a resposta é correta (Sim/Não)
        2. Pontos chave que foram corretos ou faltantes
        3. Uma explicação breve de por que a resposta é correta ou incorreta""",
        expected_output="""Uma avaliação de se a resposta é correta para a pergunta com feedback""",
        agent=answer_evaluator,
    )


def create_follow_up_question_task(question: str, company_name: str, role: str, difficulty: str) -> Task:
    return Task(
        description=f"""Baseado no seguinte contexto, crie uma pergunta de follow-up relevante:
        Pergunta Original: {question}
        Empresa: {company_name}
        Cargo: {role}
        Nível de Dificuldade: {difficulty}
        Crie uma pergunta de follow-up que:
        1. Seja baseada na pergunta original
        2. Teste uma compreensão mais profunda do tópico
        3. Seja apropriada para o nível de dificuldade especificado
        4. Seja relevante para a empresa e cargo
        A pergunta de follow-up deve ser desafiadora, mas justa, e deve ajudar a avaliar a profundidade
        técnica e as habilidades de resolução de problemas do candidato.""",
        expected_output="""Uma pergunta de follow-up que seja baseada na pergunta original""",
        output_pydantic=QuestionAnswerPair,
        agent=follow_up_questioner,
    )


def create_follow_up_crew(question: str, company_name: str, role: str, difficulty: str) -> Crew:
    """Inicializa a crew responsável por criar perguntas de follow-up."""
    crew = Crew(
        agents=[follow_up_questioner],
        tasks=[
            create_follow_up_question_task(question, company_name, role, difficulty),
        ],
        process=Process.sequential,
        verbose=True,
    )
    return crew


async def generate_follow_up_question(
    question: str, company_name: str, role: str, difficulty: str
) -> QuestionAnswerPair:
    """Gera uma pergunta de follow-up assincronamente."""
    result = await create_follow_up_crew(question, company_name, role, difficulty).kickoff_async()
    return result.pydantic


# Função para iniciar a prática de entrevista:
async def start_interview_practice(company_name: str, role: str, difficulty: str = "easy"):
    # Primeira Crew: Preparar a pergunta e a resposta
    preparation_crew = Crew(
        agents=[company_researcher, question_preparer],
        tasks=[
            create_company_research_task(company_name, role, difficulty),
            create_question_preparation_task(difficulty),
        ],
        process=Process.sequential,
        verbose=True,
    )

    # Executa a primeira crew para obter a pergunta e a resposta modelada
    preparation_result = preparation_crew.kickoff()

    # Gera uma pergunta de follow-up logo após a preparação (assincronamente)

    follow_up_question_task = asyncio.create_task(
        generate_follow_up_question(
            question=preparation_result.pydantic.question,
            company_name=company_name,
            role=role,
            difficulty=difficulty,
        )
    )

    # Imprime a pergunta principal e obtém a resposta do usuário:
    print("\nPergunta:")
    print(preparation_result.pydantic.question)
    user_answer = input("\nSua resposta: ")

    # Segunda Crew: Avaliar a resposta
    evaluation_crew = Crew(
        agents=[answer_evaluator],
        tasks=[
            create_evaluation_task(
                question=preparation_result.pydantic.question,
                user_answer=user_answer,
                correct_answer=preparation_result.pydantic.correct_answer,
            )
        ],
        process=Process.sequential,
        verbose=True,
    )

    # Executa a segunda crew e obtém a avaliação:
    evaluation_result = evaluation_crew.kickoff()
    print("\nAvaliação:")
    print(evaluation_result)

    input("\nPressione Enter para continuar para a pergunta de follow-up...")

    # Obtém a pergunta de follow-up (deve estar pronta agora):
    follow_up_question_result = await follow_up_question_task

    # Mostra a pergunta de follow-up pré-gerada:
    print("\nPergunta de Follow-up:")
    print(follow_up_question_result.question)
    follow_up_answer = input("\nSua resposta para a pergunta de follow-up: ")

    # Avalia a resposta de follow-up:
    follow_up_evaluation_crew = Crew(
        agents=[answer_evaluator],
        tasks=[
            create_evaluation_task(
                question=follow_up_question_result.question,
                user_answer=follow_up_answer,
                correct_answer=follow_up_question_result.correct_answer,
            )
        ],
        process=Process.sequential,
        verbose=True,
    )

    # Executa a avaliação de follow-up:
    follow_up_evaluation = follow_up_evaluation_crew.kickoff()
    print("\nAvaliação de Follow-up:")
    print(follow_up_evaluation)


if __name__ == "__main__":
    company = "Google"
    role = "Cientista de Dados Junior"
    print(f"Iniciando prática de entrevista mock para o cargo de {role} na empresa {company}...")
    asyncio.run(start_interview_practice(company, role))


# -------------------------------------------------------------------------------------
# Para o aplicativo Streamlit
# -------------------------------------------------------------------------------------
def initialize_preparation_crew(company_name: str, role: str, difficulty: str) -> Crew:
    """Initialize the crew responsible for preparing interview questions."""
    return Crew(
        agents=[company_researcher, question_preparer],
        tasks=[
            create_company_research_task(company_name, role, difficulty),
            create_question_preparation_task(difficulty),
        ],
        process=Process.sequential,
        verbose=True,
    )


def evaluate_answer(question: str, user_answer: str, correct_answer: str) -> str:
    """Create and execute the evaluation crew to assess the user's answer."""
    evaluation_crew = Crew(
        agents=[answer_evaluator],
        tasks=[
            create_evaluation_task(
                question=question,
                user_answer=user_answer,
                correct_answer=correct_answer,
            )
        ],
        process=Process.sequential,
        verbose=True,
    )
    return evaluation_crew.kickoff()
