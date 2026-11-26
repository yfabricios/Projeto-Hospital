from dao_sql.dao import DAO
from dao_sql.database import Database
from models.servico import Servico

class ServicoDAO(DAO):
    @classmethod
    def abrir(cls):
        super().abrir()
        Database.garantir_vinculo_servico_profissional(cls.conn)

    @classmethod
    def inserir(cls, obj):
        cls.abrir()
        sql = """
            INSERT INTO servico (descricao, valor, id_profissional)
            VALUES (?, ?, ?)
        """
        cls.execute(
            sql,
            (
                obj.get_descricao(),
                obj.get_valor(),
                obj.get_id_profissional(),
            ),
        )
        cls.fechar()

    @classmethod
    def listar(cls):
        cls.abrir()
        sql = "SELECT id, descricao, valor, id_profissional FROM servico"
        cursor = cls.execute(sql)

        rows = cursor.fetchall()
        objs = [
            Servico(id, descricao, valor, id_profissional)
            for (id, descricao, valor, id_profissional) in rows
        ]
        cls.fechar()
        return objs

    @classmethod
    def listar_id(cls, id):
        cls.abrir()
        sql = "SELECT id, descricao, valor, id_profissional FROM servico WHERE id = ?"
        cursor = cls.execute(sql, (id,))
        row = cursor.fetchone()
        obj = Servico(*row) if row else None
        cls.fechar()
        return obj

    @classmethod
    def atualizar(cls, obj):
        cls.abrir()
        sql = """
            UPDATE servico SET descricao=?, valor=?, id_profissional=?
            WHERE id=?
        """
        cls.execute(
            sql,
            (
                obj.get_descricao(),
                obj.get_valor(),
                obj.get_id_profissional(),
                obj.get_id(),
            ),
        )
        cls.fechar()

    @classmethod
    def excluir(cls, id):
        cls.abrir()
        sql = "DELETE FROM servico WHERE id=?"
        cls.execute(sql, (id,))
        cls.fechar()