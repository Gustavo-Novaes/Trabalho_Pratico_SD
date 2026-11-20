
import sqlite3
from pathlib import Path

# Local onde os bancos de dados serão armazenados
PASTA = Path(__file__).resolve().parent

# Estrutura das tabelas
TABELAS = [
    """
    CREATE TABLE IF NOT EXISTS obras (
        id_obra INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        localizacao TEXT NOT NULL,
        descricao TEXT,
        data_inicio TEXT,
        status TEXT NOT NULL
    )
    """,

    """
    CREATE TABLE IF NOT EXISTS usuarios (
        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        login TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL,
        especialidade TEXT NOT NULL
            CHECK (especialidade IN ('Gestor', 'Funcionário'))
    )
    """,

    """
    CREATE TABLE IF NOT EXISTS tipos_atividade (
        id_tipo INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        descricao TEXT
    )
    """,

    """
    CREATE TABLE IF NOT EXISTS agendamentos (
        id_agendamento INTEGER PRIMARY KEY AUTOINCREMENT,
        id_obra INTEGER NOT NULL,
        id_tipo INTEGER NOT NULL,
        data_inicio TEXT NOT NULL,
        data_fim TEXT NOT NULL,
        status TEXT NOT NULL,
        FOREIGN KEY (id_obra) REFERENCES obras(id_obra),
        FOREIGN KEY (id_tipo) REFERENCES tipos_atividade(id_tipo)
    )
    """,

    """
    CREATE TABLE IF NOT EXISTS agendamento_funcionarios (
        id_agendamento INTEGER NOT NULL,
        id_usuario INTEGER NOT NULL,
        PRIMARY KEY (id_agendamento, id_usuario),
        FOREIGN KEY (id_agendamento)
            REFERENCES agendamentos(id_agendamento),
        FOREIGN KEY (id_usuario)
            REFERENCES usuarios(id_usuario)
    )
    """,

    """
    CREATE TABLE IF NOT EXISTS execucoes (
        id_execucao INTEGER PRIMARY KEY AUTOINCREMENT,
        id_agendamento INTEGER NOT NULL,
        id_funcionario INTEGER NOT NULL,
        data_execucao TEXT NOT NULL,
        descricao TEXT,
        observacao TEXT,
        FOREIGN KEY (id_agendamento)
            REFERENCES agendamentos(id_agendamento),
        FOREIGN KEY (id_funcionario)
            REFERENCES usuarios(id_usuario)
    )
    """,

    """
    CREATE TABLE IF NOT EXISTS presencas (
        id_presenca INTEGER PRIMARY KEY AUTOINCREMENT,
        id_funcionario INTEGER NOT NULL,
        data TEXT NOT NULL,
        status TEXT NOT NULL,
        observacao TEXT,
        UNIQUE (id_funcionario, data),
        FOREIGN KEY (id_funcionario)
            REFERENCES usuarios(id_usuario)
    )
    """,
    
    """
    CREATE TABLE IF NOT EXISTS replicacoes_pendentes (
        id_obra INTEGER PRIMARY KEY,
        nome TEXT NOT NULL,
        localizacao TEXT NOT NULL,
        descricao TEXT,
        data_inicio TEXT,
        status TEXT NOT NULL,
        data_criacao TEXT NOT NULL
    )
    """
]


def criar_banco(nome_arquivo):
    caminho = PASTA / nome_arquivo

    conexao = sqlite3.connect(caminho)

    # Ativa a verificação das chaves estrangeiras
    conexao.execute("PRAGMA foreign_keys = ON")

    cursor = conexao.cursor()

    for tabela in TABELAS:
        cursor.execute(tabela)

    conexao.commit()
    conexao.close()

    print(f"Banco {nome_arquivo} criado com sucesso!")


def inicializar_bancos():
    criar_banco("controlador1.db")
    criar_banco("controlador2.db")


if __name__ == "__main__":
    inicializar_bancos()
