
import sqlite3
from pathlib import Path

import Pyro5.api


# Caminho do banco de dados do controlador 2
PASTA_PROJETO = Path(__file__).resolve().parent.parent
CAMINHO_BANCO = PASTA_PROJETO / "banco_dados" / "controlador2.db"


@Pyro5.api.expose
class Controlador2:

    def obter_status(self):
        return "Controlador 2 funcionando!"

    def listar_obras(self):
        conexao = sqlite3.connect(CAMINHO_BANCO)
        conexao.row_factory = sqlite3.Row

        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM obras")

        obras = [dict(registro) for registro in cursor.fetchall()]

        conexao.close()

        return obras
    
    
    def registrar_obra_replica(self, id_obra, nome, localizacao, descricao, data_inicio, status):
        conexao = sqlite3.connect(CAMINHO_BANCO)
        conexao.execute("PRAGMA foreign_keys = ON")

        cursor = conexao.cursor()

        # Verifica se a obra já existe
        cursor.execute(
            "SELECT id_obra FROM obras WHERE id_obra = ?",
            (id_obra,)
        )

        obra_existente = cursor.fetchone()

        if obra_existente:
            conexao.close()
            return "Obra já estava replicada!"

        # Insere a obra caso ainda não exista
        cursor.execute("""
            INSERT INTO obras (
                id_obra, nome, localizacao, descricao, data_inicio, status
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (id_obra, nome, localizacao, descricao, data_inicio, status))

        conexao.commit()
        conexao.close()

        return "Obra replicada com sucesso!"
    
    def verificar_disponibilidade(self):
        return {
            "controlador": "Controlador 2",
            "disponivel": True
        }





if __name__ == "__main__":
    controlador = Controlador2()

    daemon = Pyro5.api.Daemon(
        host="localhost",
        port=50002
    )

    uri = daemon.register(
        controlador,
        objectId="controlador2"
    )

    print("Controlador 2 iniciado!")
    print(f"Endereço: {uri}")

    daemon.requestLoop()
