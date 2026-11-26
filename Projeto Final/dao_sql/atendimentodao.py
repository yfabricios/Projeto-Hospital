from datetime import datetime

from dao_sql.dao import DAO
from dao_sql.database import Database
from models.atendimento import Atendimento

class AtendimentoDAO(DAO):
    @classmethod
    def abrir(cls):
        super().abrir()
        Database.garantir_colunas_atendimento(cls.conn)

    @staticmethod
    def _criar_objeto(row):
        (
            id,
            data,
            queixa_principal,
            historico_saude,
            avaliacao,
            prescricao,
            id_horario,
            total,
            pago,
        ) = row
        obj = Atendimento(
            id,
            datetime.strptime(data, "%d/%m/%Y %H:%M"),
            queixa_principal,
            historico_saude,
            avaliacao,
            prescricao,
        )
        obj.set_id_horario(id_horario)
        obj.set_total(total)
        obj.set_pago(bool(pago))
        return obj

    @classmethod
    def inserir(cls, obj):
        cls.abrir()
        sql = """
            INSERT INTO atendimento (
                data, queixa_principal, historico_saude, avaliacao, prescricao,
                id_horario, total, pago
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        cls.execute(
            sql,
            (
                obj.get_data().strftime("%d/%m/%Y %H:%M"),
                obj.get_queixa_principal(),
                obj.get_historico_saude(),
                obj.get_avaliacao(),
                obj.get_prescricao(),
                obj.get_id_horario(),
                obj.get_total(),
                bool(obj.get_pago()),
            ),
        )
        cls.fechar()

    @classmethod
    def listar(cls):
        cls.abrir()
        sql = """
            SELECT id, data, queixa_principal, historico_saude, avaliacao,
                   prescricao, id_horario, total, pago
            FROM atendimento
        """
        cursor = cls.execute(sql)
        objs = [cls._criar_objeto(row) for row in cursor.fetchall()]
        cls.fechar()
        return objs

    @classmethod
    def listar_id(cls, id):
        cls.abrir()
        sql = """
            SELECT id, data, queixa_principal, historico_saude, avaliacao,
                   prescricao, id_horario, total, pago
            FROM atendimento
            WHERE id = ?
        """
        cursor = cls.execute(sql, (id,))
        row = cursor.fetchone()
        obj = cls._criar_objeto(row) if row else None
        cls.fechar()
        return obj

    @classmethod
    def atualizar(cls, obj):
        cls.abrir()
        sql = """
            UPDATE atendimento
            SET data=?, queixa_principal=?, historico_saude=?, avaliacao=?,
                prescricao=?, id_horario=?, total=?, pago=?
            WHERE id=?
        """
        cls.execute(
            sql,
            (
                obj.get_data().strftime("%d/%m/%Y %H:%M"),
                obj.get_queixa_principal(),
                obj.get_historico_saude(),
                obj.get_avaliacao(),
                obj.get_prescricao(),
                obj.get_id_horario(),
                obj.get_total(),
                bool(obj.get_pago()),
                obj.get_id(),
            ),
        )
        cls.fechar()

    @classmethod
    def excluir(cls, id):
        cls.abrir()
        sql = "DELETE FROM atendimento WHERE id=?"
        cls.execute(sql, (id,))
        cls.fechar()