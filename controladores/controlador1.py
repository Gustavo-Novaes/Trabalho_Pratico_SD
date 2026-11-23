
import sqlite3
from pathlib import Path

import Pyro5.api


# Caminho do banco de dados do controlador 1
PASTA_PROJETO = Path(__file__).resolve().parent.parent
CAMINHO_BANCO = PASTA_PROJETO / "banco_dados" / "controlador1.db"


@Pyro5.api.expose
class Controlador1:
    def __init__(self):
        self.papel = "Principal"

    def obter_papel(self):
        return self.papel

    def assumir_reserva(self):
        self.papel = "Reserva"
        return "Controlador 1 agora é Reserva."

    def assumir_principal(self):
        self.papel = "Principal"
        return "Controlador 1 agora é Principal."
    
    def obter_status(self):
        return "Controlador 1 funcionando!"

    def listar_obras(self):
        conexao = sqlite3.connect(CAMINHO_BANCO)
        conexao.row_factory = sqlite3.Row

        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM obras")

        obras = [dict(registro) for registro in cursor.fetchall()]

        conexao.close()

        return obras

    def cadastrar_obra(self, nome, localizacao, descricao, data_inicio, status):
        conexao = sqlite3.connect(CAMINHO_BANCO)
        cursor = conexao.cursor()

        try:
            # Inicia uma transação no banco
            cursor.execute("BEGIN")

            # Cadastra a obra no Controlador 1
            cursor.execute("""
                INSERT INTO obras (
                    nome, localizacao, descricao, data_inicio, status
                )
                VALUES (?, ?, ?, ?, ?)
            """, (nome, localizacao, descricao, data_inicio, status))

            id_obra = cursor.lastrowid

            # Registra a replicação como pendente
            cursor.execute("""
                INSERT INTO replicacoes_pendentes (
                    id_obra, nome, localizacao, descricao,
                    data_inicio, status, data_criacao
                )
                VALUES (?, ?, ?, ?, ?, ?, datetime('now'))
            """, (
                id_obra, nome, localizacao, descricao,
                data_inicio, status
            ))

            # Confirma as duas operações juntas
            conexao.commit()

        except Exception:
            conexao.rollback()
            conexao.close()
            raise

        conexao.close()

        # Tenta enviar a obra para o Controlador 2
        try:
            controlador2 = Pyro5.api.Proxy(
                "PYRO:controlador2@localhost:50002"
            )

            resultado = controlador2.registrar_obra_replica(
                id_obra,
                nome,
                localizacao,
                descricao,
                data_inicio,
                status
            )

            # Remove a pendência após a confirmação
            conexao = sqlite3.connect(CAMINHO_BANCO)
            conexao.execute("""
                DELETE FROM replicacoes_pendentes
                WHERE id_obra = ?
            """, (id_obra,))
            conexao.commit()
            conexao.close()

            return {
                "sucesso": True,
                "mensagem": "Obra cadastrada e replicada com sucesso!",
                "id_obra": id_obra,
                "replicacao": resultado
            }

        except Exception as erro:
            return {
                "sucesso": True,
                "mensagem": "Obra cadastrada no Controlador 1. A replicação está pendente.",
                "id_obra": id_obra,
                "erro": str(erro)
            }

    def registrar_obra_replica(self, id_obra, nome, localizacao, descricao, data_inicio, status):
        conexao = sqlite3.connect(CAMINHO_BANCO)
        conexao.execute("PRAGMA foreign_keys = ON")

        cursor = conexao.cursor()

        cursor.execute(
            "SELECT id_obra FROM obras WHERE id_obra = ?",
            (id_obra,)
        )

        obra_existente = cursor.fetchone()

        if obra_existente:
            conexao.close()
            return "Obra já estava replicada!"

        cursor.execute("""
            INSERT INTO obras (
                id_obra, nome, localizacao, descricao, data_inicio, status
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (id_obra, nome, localizacao, descricao, data_inicio, status))

        conexao.commit()
        conexao.close()

        return "Obra replicada com sucesso!"
    
    def sincronizar_pendencias(self):
        conexao = sqlite3.connect(CAMINHO_BANCO)
        conexao.row_factory = sqlite3.Row

        cursor = conexao.cursor()

        cursor.execute("""
            SELECT * FROM replicacoes_pendentes
        """)

        pendencias = cursor.fetchall()
        conexao.close()

        sincronizadas = 0
        erros = []

        for obra in pendencias:
            try:
                controlador2 = Pyro5.api.Proxy(
                    "PYRO:controlador2@localhost:50002"
                )

                controlador2.registrar_obra_replica(
                    obra["id_obra"],
                    obra["nome"],
                    obra["localizacao"],
                    obra["descricao"],
                    obra["data_inicio"],
                    obra["status"]
                )

                conexao = sqlite3.connect(CAMINHO_BANCO)

                conexao.execute("""
                    DELETE FROM replicacoes_pendentes
                    WHERE id_obra = ?
                """, (obra["id_obra"],))

                conexao.commit()
                conexao.close()

                sincronizadas += 1

            except Exception as erro:
                erros.append({
                    "id_obra": obra["id_obra"],
                    "erro": str(erro)
                })

        return {
            "total_pendentes": len(pendencias),
            "sincronizadas": sincronizadas,
            "erros": erros
        }
    
    def verificar_disponibilidade(self):
        return {
            "controlador": "Controlador 1",
            "disponivel": True
        }




if __name__ == "__main__":
    controlador = Controlador1()

    daemon = Pyro5.api.Daemon(
        host="localhost",
        port=50001
    )

    uri = daemon.register(
        controlador,
        objectId="controlador1"
    )

    print("Controlador 1 iniciado!")
    print(f"Endereço: {uri}")

    daemon.requestLoop()
