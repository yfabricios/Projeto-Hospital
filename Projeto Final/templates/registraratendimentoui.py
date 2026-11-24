import streamlit as st
from service import Service
import time
from datetime import datetime

class RegistrarAtendimentoUI:
    def main():
        st.header("Registrar Atendimento")
        horarios = Service.profissional_visualizar_agenda(st.session_state["usuario_id"])
        horarios_usados = {
            atendimento.get_id_horario()
            for atendimento in Service.atendimento_listar()
        }
        horarios = [
            horario
            for horario in horarios
            if horario.get_confirmado() and horario.get_id() not in horarios_usados
        ]

        if len(horarios) == 0:
            st.write("Nenhum atendimento disponível")
        else:
            horario = st.selectbox("Informe o horário", horarios)
            servico = Service.servico_listar_id(horario.get_id_servico())
            if servico is None:
                st.error("O horário selecionado não possui um serviço cadastrado.")
                return

            st.write(f"Serviço realizado: {servico.get_descricao()}")
            st.write(f"Valor: R$ {servico.get_valor():.2f}")
            data = st.text_input("Informe a data e horário do atendimento", datetime.now().strftime("%d/%m/%Y %H:%M"))
            queixa_principal = st.text_input("Informe a queixa principal")
            historico_saude = st.text_input("Informe o histórico de saúde")
            avaliacao = st.text_input("Informe a avaliação")
            prescricao = st.text_input("Informe a prescrição")

            if st.button("Registrar"):
                Service.atendimento_inserir(
                    datetime.strptime(data, "%d/%m/%Y %H:%M"),
                    queixa_principal,
                    historico_saude,
                    avaliacao,
                    prescricao,
                    horario.get_id(),
                    servico.get_valor(),
                    False,
                )
                st.success("Atendimento registrado")
                time.sleep(2)
                st.rerun()