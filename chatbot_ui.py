#! /usr/bin/env python3
"""
Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro

Script chatbot_ui.py
====================
Neste script, criamos a interface do usuário para a aplicação
de entrevista de simulação com IA.

Run
---
streamlit run chatbot_ui.py --server.address localhost --server.port 8501

Executamos esse comando porque é mais seguro, já que o streamlit não permite
acesso ao microfone se não estiver em localhost.

NOTA
====
O App está funcional, mas falta alguns pequenos ajustes para melhorar
a experiência do usuário.
"""
import asyncio
import os
import tempfile

import streamlit as st
import whisper  # https://pypi.org/project/openai-whisper/
from streamlit_mic_recorder import mic_recorder

from interview_practice_system import (
    evaluate_answer,
    generate_follow_up_question,
    initialize_preparation_crew,
)

st.title("🤗 Entrevista Simulada com IA 🤗")

# Inicializa o estado da sessão:
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.interview_started = False
    st.session_state.current_question = None
    st.session_state.current_answer = None
    st.session_state.evaluation = None
    st.session_state.preparation_crew = None
    st.session_state.follow_up_question = None
    st.session_state.is_generating_follow_up = False

# Sidebar para configuração da entrevista:
with st.sidebar:
    st.header("Configuração da Entrevista")
    company_name = st.text_input("Nome da Empresa desejada", "Google")
    role = st.text_input("Cargo desejado", "Cientista de Dados Junior")
    difficulty = st.selectbox("Nível de Dificuldade", ["Fácil", "Médio", "Difícil"], index=1)

    st.divider()
    st.subheader("🎤 Configurações de Áudio")

    whisper_model = st.selectbox(
        "Modelo Whisper utilizado para reconhecimento de voz",
        ["tiny", "base", "small", "medium", "large"],
        index=1,  # "base" como padrão
        help="""
        - tiny: Mais rápido, menos preciso (~1GB de RAM)
        - base: Equilibrado (recomendado) (~1GB de RAM)
        - small: Mais preciso (~2GB de RAM)
        - medium: Muito preciso (~5GB de RAM)
        - large: Máxima precisão (~10GB de RAM)
        """,
    )

    st.info(
        f"""
        🎤 **Modelo atual:** `{whisper_model}`\n
        ✅ **Idioma:** pt-BR\n
        💰 **Custo:** GRÁTIS (roda localmente)\n
        🔑 **API Key:** Não necessária (Open Source)\n
        """
    )

    if st.button("Iniciar Entrevista Simulada"):
        st.session_state.interview_started = True
        st.session_state.messages = []
        st.session_state.current_question = None
        st.session_state.current_answer = None
        st.session_state.evaluation = None
        st.session_state.follow_up_question = None
        st.session_state.is_generating_follow_up = False

        # Inicializa a equipe de preparação:
        st.session_state.preparation_crew = initialize_preparation_crew(company_name, role, difficulty)
        st.rerun()

# Exibe as mensagens do chat:
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Inicia a entrevista se não foi iniciada:
if not st.session_state.interview_started:
    st.info(
        """👋 Bem-vindo! Por favor, configure sua entrevista simulada na barra lateral e clique
        em 'Iniciar Entrevista Simulada' para começar."""
    )
# Se não temos uma pergunta atual, inicia a entrevista:
elif st.session_state.current_question is None:
    with st.spinner("🤖 Preparando sua pergunta de entrevista..."):
        # Executa a crew de preparação para obter a pergunta e a resposta correta:
        preparation_result = st.session_state.preparation_crew.kickoff()

        # Armazena a pergunta e a resposta correta:
        st.session_state.current_question = preparation_result.pydantic.question
        st.session_state.correct_answer = preparation_result.pydantic.correct_answer

        # Adiciona a pergunta ao chat:
        st.session_state.messages.append({"role": "assistant", "content": st.session_state.current_question})
        st.rerun()

# Obtém a entrada do usuário:
st.write("Escolha seu método de entrada:")
input_method = st.radio("Método de Entrada", ["Texto", "Voz"], horizontal=True, label_visibility="collapsed")

user_input = None  # Inicializa o user_input


def convert_speech_to_text(audio_bytes, model_name="base"):
    """
    Converte áudio em texto usando Whisper.

    Args:
        audio_bytes: Bytes do áudio gravado
        model_name: Nome do modelo Whisper (tiny, base, small, medium, large)

    Returns:
        str: Texto transcrito ou None se houver erro
    """
    try:
        # Cria um arquivo temporário para armazenar o áudio:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            temp_audio.write(audio_bytes)
            temp_audio_path = temp_audio.name

        try:
            # Carrega o modelo Whisper (isso irá baixar o modelo na primeira execução)
            # Na primeira vez que usar um modelo, ele será baixado (~100MB-3GB)
            model = whisper.load_model(model_name)

            # Transcreve o áudio especificando português brasileiro
            # language='pt' força o reconhecimento em português
            # fp16=False é necessário para CPU (a maioria dos computadores)
            result = model.transcribe(
                temp_audio_path,
                language="pt",  # Português (Brasil/Portugal)
                fp16=False,  # Desabilita FP16 (necessário para CPU)
                verbose=False,  # Não mostra progresso detalhado
            )
            return result["text"]
        finally:
            # Limpa o arquivo temporário
            os.unlink(temp_audio_path)

    except FileNotFoundError as e:
        if "ffmpeg" in str(e):
            st.error(
                """
                ❌ **Erro: FFmpeg não encontrado!**
                O Whisper precisa do FFmpeg para processar áudio.
                **Solução:** Execute no terminal:
                ```bash
                sudo apt update && sudo apt install -y ffmpeg
                ```
                Depois reinicie a aplicação Streamlit.
                """
            )
        else:
            st.error(f"Arquivo não encontrado: {e!s}")
        return None
    except Exception as e:
        st.error(f"Ocorreu um erro ao processar o áudio: {e!s}")
        return None


if input_method == "Texto":
    user_input = st.chat_input("Digite sua resposta...")
else:
    # Instruções para o usuário sobre permissões do microfone
    st.info(
        """
        🎤 **Importante:** Para usar o microfone:
        1. Clique em "Iniciar gravação" abaixo
        2. Permita o acesso ao microfone quando o navegador solicitar
        3. Fale sua resposta claramente
        4. Clique em "Parar gravação" quando terminar

        ⚠️ **Nota:** Se estiver usando WSL/Linux, certifique-se de que:
        - O navegador tem permissão para acessar o microfone
        - A aplicação está rodando em HTTPS ou localhost
        """
    )

    st.write("Clique no microfone para gravar sua resposta:")

    # Adiciona uma chave única para evitar problemas de re-renderização
    audio = mic_recorder(
        start_prompt="▶︎ •၊၊||၊|။||| Iniciar gravação",
        stop_prompt="⏹️ Parar gravação",
        just_once=True,
        use_container_width=True,
        key="voice_recorder",
    )

    if audio:
        # Debug: mostra que o áudio foi capturado
        st.write(f"📊 Áudio capturado: {len(audio['bytes'])} bytes")

        with st.spinner(f"🔄 Convertendo áudio para texto usando modelo '{whisper_model}'..."):
            # Converte os bytes do áudio para texto usando o modelo selecionado
            user_input = convert_speech_to_text(audio["bytes"], model_name=whisper_model)
            if user_input:
                st.success(f"✅ Reconhecido: {user_input}")
            else:
                st.error("❌ Não foi possível reconhecer a fala. Por favor, tente novamente.")
    # Debug: indica quando o botão de gravação foi clicado mas não há áudio
    elif st.session_state.get("show_audio_warning", False):
        st.warning("⏳ Aguardando gravação... Clique em 'Iniciar gravação' e fale no microfone.")

if user_input is not None:
    # Adiciona a resposta do usuário às mensagens:
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Armazena a resposta do usuário:
    st.session_state.current_answer = user_input

    # Mostra a mensagem de pensamento:
    with st.spinner("🤖 Avaliando sua resposta..."):
        # Avalia a resposta do usuário:
        evaluation = evaluate_answer(
            question=st.session_state.current_question,
            user_answer=user_input,
            correct_answer=st.session_state.correct_answer,
        )

        # Adiciona a avaliação às mensagens:
        st.session_state.messages.append({"role": "assistant", "content": evaluation})

        # Gera uma pergunta de follow-up se não estiver gerando uma pergunta de follow-up:
        if not st.session_state.is_generating_follow_up:
            st.session_state.is_generating_follow_up = True
            try:
                # Gera uma pergunta de follow-up:
                follow_up_result = asyncio.run(
                    generate_follow_up_question(
                        question=st.session_state.current_question,
                        company_name=company_name,
                        role=role,
                        difficulty=difficulty.lower(),
                    )
                )

                # Armazena a pergunta de follow-up:
                st.session_state.follow_up_question = follow_up_result

                # Adiciona a pergunta de follow-up às mensagens:
                st.session_state.messages.append({"role": "assistant", "content": follow_up_result.question})

                # Configura para a pergunta de follow-up:
                st.session_state.current_question = follow_up_result.question
                st.session_state.correct_answer = follow_up_result.correct_answer
            except Exception as e:
                st.error(f"Ocorreu um erro ao gerar a pergunta de follow-up: {e!s}")
                st.session_state.current_question = None
                st.session_state.current_answer = None
        else:
            # Reinicia para a próxima pergunta:
            st.session_state.current_question = None
            st.session_state.current_answer = None

        st.session_state.is_generating_follow_up = False
        st.rerun()


# Auto-scroll:
scroll_placeholder = st.empty()
