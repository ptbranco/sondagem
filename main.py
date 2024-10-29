import streamlit as st
import sqlite3
from datetime import datetime, timedelta
import socket

# Função para obter o IP do usuário
def get_user_ip():
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)

# Configuração do banco de dados SQLite
conn = sqlite3.connect('respostas.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS respostas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ip TEXT NOT NULL,
                    data_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    respostas TEXT NOT NULL)''')
conn.commit()

# Função para verificar e atualizar respostas anteriores do mesmo IP nas últimas 2 horas
def resposta_duplicada_ou_atualizar(ip, novas_respostas):
    duas_horas_atras = datetime.now() - timedelta(hours=2)
    cursor.execute("SELECT id FROM respostas WHERE ip = ? AND data_envio > ?", (ip, duas_horas_atras))
    resultado = cursor.fetchone()
    if resultado:
        # Alerta ao usuário sobre a substituição
        st.warning("Já existe uma resposta sua na nossa base de dados. A nova resposta irá substituir a anterior.")
        # Atualiza a resposta existente
        cursor.execute("UPDATE respostas SET respostas = ?, data_envio = CURRENT_TIMESTAMP WHERE id = ?", 
                       (str(novas_respostas), resultado[0]))
    else:
        # Insere uma nova resposta
        cursor.execute("INSERT INTO respostas (ip, respostas) VALUES (?, ?)", (ip, str(novas_respostas)))
    conn.commit()

# Adicionando estilo CSS para melhorar o layout
st.markdown(
    '''
    <style>
    .stRadio > div { gap: 10px; } /* Reduz espaçamento entre as opções de rádio */
    .stTextArea, .stTextInput { margin-bottom: 5px; } /* Compacta espaçamento para textarea e input */
    hr { border: 1px solid #ddd; } /* Linha divisória entre perguntas */
    .pergunta { font-weight: bold; font-size: 1.1em; margin-bottom: 2px; } /* Estiliza perguntas */
    </style>
    ''', unsafe_allow_html=True
)

# Interface do questionário
st.title("Questionário OSAE")

# Obtém IP do usuário
ip_usuario = get_user_ip()

# Perguntas do questionário
with st.form("questionario_form"):
    st.markdown('<div class="pergunta">Há quanto tempo está inscrito na OSAE?</div>', unsafe_allow_html=True)
    questao1 = st.radio("", ["Menos de 5 anos", "5 a 10 anos", "11 a 20 anos", "Mais de 20 anos"])
    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown('<div class="pergunta">Conselho Regional a que pertence?</div>', unsafe_allow_html=True)
    questao2 = st.radio("", ["Porto", "Coimbra", "Lisboa"])
    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown('<div class="pergunta">A que Colégio(s) de especialidade a que pertence?</div>', unsafe_allow_html=True)
    questao3 = st.multiselect("", ["Solicitadores", "Agentes de Execução"])
    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown('<div class="pergunta">Como avalia a atuação da atual direção da OSAE?</div>', unsafe_allow_html=True)
    questao4 = st.radio("", ["Muito boa", "Boa", "Regular", "Má", "Muito Má"])
    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown('<div class="pergunta">Que aspectos da atual direção considera que precisam de mudar?</div>', unsafe_allow_html=True)
    questao5 = st.text_area("Resposta livre:", key="questao5")
    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown('<div class="pergunta">Qual destas áreas considera mais importante para o futuro da OSAE?</div>', unsafe_allow_html=True)
    questao6_opcoes = ["Transparência e gestão financeira", "Modernização tecnológica", 
                       "Defesa dos direitos dos solicitadores e agentes de execução",
                       "Especialização em Cadastro", "Formação contínua de qualidade", "Outra"]
    questao6 = st.radio("", questao6_opcoes)
    questao6_outra = ""
    if questao6 == "Outra":
        questao6_outra = st.text_input("Por favor, especifique:", key="questao6_outra")
    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown('<div class="pergunta">Qual destas propostas do Caminho Certo considera mais relevante?</div>', unsafe_allow_html=True)
    questao7 = st.radio("", [
        "Os dirigentes são eleitos para dirigir...",
        "As Assembleias Gerais vão realizar-se por seções...",
        "Instituir um Conselho Técnico do Cadastro...",
        "Acabar com o GeoBlocking",
        "Abrir estágio para agentes de execução...",
        "Realizar a AG extraordinária...",
        "Fazer um estudo económico para conhecer..."
    ])
    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown('<div class="pergunta">Se as eleições fossem hoje, em que candidato a bastonário votaria?</div>', unsafe_allow_html=True)
    questao8 = st.radio("", ["Rui Simão", "Anabela Veloso", "Delfim Costa", "Paulo Teixeira", 
                             "Ainda não decidi", "Não vou votar"])
    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown('<div class="pergunta">Que qualidades considera mais importantes para o próximo bastonário?</div>', unsafe_allow_html=True)
    questao9 = st.multiselect("", ["Liderança forte", "Capacidade de inovação", 
                                   "Experiência negocial e de gestão", "Habilidade de comunicação", "Outra"])
    questao9_outra = ""
    if "Outra" in questao9:
        questao9_outra = st.text_input("Por favor, especifique:", key="questao9_outra")
    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown('<div class="pergunta">Tem acompanhado a campanha das candidaturas do Caminho Certo?</div>', unsafe_allow_html=True)
    questao10 = st.radio("", ["Sim, ativamente", "Apenas ocasionalmente", "Não"])
    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown('<div class="pergunta">Por onde prefere informar-se sobre as eleições da OSAE?</div>', unsafe_allow_html=True)
    questao11 = st.multiselect("", ["Redes sociais", "E-mails e sites das candidaturas", 
                                    "Indicações de colegas", "Outros"])
    questao11_outra = ""
    if "Outros" in questao11:
        questao11_outra = st.text_input("Por favor, especifique:", key="questao11_outra")
    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown('<div class="pergunta">Gostaria de ver os Conselhos Regionais a promover debates entre os candidatos?</div>', unsafe_allow_html=True)
    questao12 = st.radio("", ["Sim", "Não", "É irrelevante"])
    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown('<div class="pergunta">O que gostaria de partilhar connosco?</div>', unsafe_allow_html=True)
    questao13 = st.text_area("Resposta livre:", key="questao13")
    st.markdown("<hr>", unsafe_allow_html=True)

    # Submissão do questionário
    submit_button = st.form_submit_button(label="Enviar")

# Processamento do questionário
if submit_button:
    respostas = {
        "questao1": questao1,
        "questao2": questao2,
        "questao3": questao3,
        "questao4": questao4,
        "questao5": questao5,
        "questao6": questao6 if questao6 != "Outra" else questao6_outra,
        "questao7": questao7,
        "questao8": questao8,
        "questao9": questao9 if "Outra" not in questao9 else questao9 + [questao9_outra],
        "questao10": questao10,
        "questao11": questao11 if "Outros" not in questao11 else questao11 + [questao11_outra],
        "questao12": questao12,
        "questao13": questao13
    }
    resposta_duplicada_ou_atualizar(ip_usuario, respostas)
    st.success("Obrigado por responder ao questionário!")
