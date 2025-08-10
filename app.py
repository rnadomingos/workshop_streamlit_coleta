import os
import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Definie o título da pagina e ico
st.set_page_config(page_title="Coleta de Dados", page_icon="🎲")


# URL do Banco de Dados
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")
DATABASE_URL = f"postgresql://{DB_HOST}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

Base = declarative_base()


class SurveyData(Base):
    __tablename__ = "survey_data"
    id = Column(Integer, primary_key=True, autoincrement=True)
    estado = Column(String(50))
    bibliotecas = Column(Text)
    area_atuacao = Column(String(50))
    horas_estudo = Column(String(20))
    conforto_dados = Column(String(50))
    experiencia_python = Column(Integer)
    experiencia_sql = Column(Integer)
    experiencia_cloud = Column(Integer)


def try_connection():
    try:
        engine = create_engine(DATABASE_URL)
        return engine
    except SQLAlchemyError as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}")
        return None


# Função para criar a tabela caso não exista
def criar_tabela_se_nao_existir(engine):
    try:
        Base.metadata.create_all(engine)
    except SQLAlchemyError as e:
        st.error(f"Erro ao criar a tabela: {e}")


# Função para salvar dados no banco de dados
def salvar_dados_banco(session, dados):
    try:
        novo_dado = SurveyData(
            estado=dados["Estado"],
            bibliotecas=dados["Bibliotecas e ferramentas"],
            area_atuacao=dados["Área de Atuação"],
            horas_estudo=dados["Horas de Estudo"],
            conforto_dados=dados["Conforto com Dados"],
            experiencia_python=dados["Experiência de Python"],
            experiencia_sql=dados["Experiência de SQL"],
            experiencia_cloud=dados["Experiência de Cloud"],
        )
        session.add(novo_dado)
        session.commit()
    except SQLAlchemyError as e:
        st.error(f"Erro ao salvar os dados no banco de dados: {e}")
        session.rollback()


# Obter a instância do engine e criar a tabela se necessário
engine = try_connection()

if engine is not None:
    criar_tabela_se_nao_existir(engine)

# Configurar a sessão do SQLAlchemy
Session = sessionmaker(bind=engine)


st.title("Coleta de Dados")

# Opções de estados
estados = [
    "Acre",
    "Alagoas",
    "Amapá",
    "Amazonas",
    "Bahia",
    "Ceará",
    "Distrito Federal",
    "Espírito Santo",
    "Goiás",
    "Maranhão",
    "Mato Grosso",
    "Mato Grosso do Sul",
    "Minas Gerais",
    "Pará",
    "Paraíba",
    "Paraná",
    "Pernambuco",
    "Piauí",
    "Rio de Janeiro",
    "Rio Grande do Norte",
    "Rio Grande do Sul",
    "Rondônia",
    "Roraima",
    "Santa Catarina",
    "São Paulo",
    "Sergipe",
    "Tocantins",
]

# Opções de áreas de atuação
areas_atuacao = ["Analista de Dados", "Cientista de Dados", "Engenheiro de Dados"]

# Opções de bibliotecas
bibliotecas = [
    "Pandas",
    "Pydantic",
    "scikit-learn",
    "Git",
    "Pandera",
    "streamlit",
    "postgres",
    "databricks",
    "AWS",
    "Azure",
    "airflow",
    "dbt",
    "Pyspark",
    "Polars",
    "Kafka",
    "Duckdb",
    "PowerBI",
    "Excel",
    "Tableau",
    "storm",
]

# Opções de horas codando
horas_codando = ["Menos de 5", "5-10", "10-20", "Mais de 20"]

# Opções de conforto com dados
conforto_dados = ["Desconfortável", "Neutro", "Confortável", "Muito Confortável"]

# Criação do formulário
with st.form("dados_enquete"):
    estado = st.selectbox("Estado", estados, index=None)
    area_atuacao = st.selectbox("Área de Atuação", areas_atuacao, index=None)
    bibliotecas_selecionadas = st.multiselect(
        "Bibliotecas e ferramentas mais utilizadas", bibliotecas
    )
    horas_codando = st.selectbox(
        "Horas Codando ao longo da semana", horas_codando, index=None
    )
    conforto_dados = st.selectbox(
        "Conforto ao programar e trabalhar com dados", conforto_dados, index=None
    )
    experiencia_python = st.slider("Experiência de Python", 0, 10)
    experiencia_sql = st.slider("Experiência de SQL", 0, 10)
    experiencia_cloud = st.slider("Experiência em Cloud", 0, 10)

    # Botão para submeter o formulário
    submit_button = st.form_submit_button("Enviar")

# Se o botão foi clicado, salvar os dados no DataFrame e no CSV
if submit_button:
    novo_dado = {
        "Estado": estado,
        "Bibliotecas e ferramentas": ", ".join(bibliotecas_selecionadas),
        "Área de Atuação": area_atuacao,
        "Horas de Estudo": horas_codando,
        "Conforto com Dados": conforto_dados,
        "Experiência de Python": experiencia_python,
        "Experiência de SQL": experiencia_sql,
        "Experiência de Cloud": experiencia_cloud,
    }

    session = Session()
    salvar_dados_banco(session, novo_dado)
    st.success("Dados enviados com sucesso!")
