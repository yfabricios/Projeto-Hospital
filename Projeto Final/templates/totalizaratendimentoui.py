import pandas as pd
import streamlit as st
from datetime import date
from service import Service


class TotalizarAtendimentoUI:
    def main():
        if st.session_state.get("usuario_nome") == "admin":
            profissionais = Service.profissional_listar()
            profissional = st.sidebar.selectbox(
                "Profissional",
                profissionais,
                index=None,
                key="totalizar_atendimentos_profissional",
            )
            if profissional is None:
                st.header("Totalizar atendimentos")
                st.info("Selecione um profissional na barra lateral.")
                return
            id_profissional = profissional.get_id()
            nome_profissional = profissional.get_nome()
        else:
            id_profissional = st.session_state["usuario_id"]
            nome_profissional = st.session_state["usuario_nome"]

        st.header(f"Atendimentos de {nome_profissional}")

        hoje = date.today()
        inicio_mes = hoje.replace(day=1)
        coluna_inicio, coluna_final = st.columns(2)
        with coluna_inicio:
            data_inicial = st.date_input(
                "Data inicial", value=inicio_mes, format="DD/MM/YYYY"
            )
        with coluna_final:
            data_final = st.date_input(
                "Data final", value=hoje, format="DD/MM/YYYY"
            )

        if data_inicial > data_final:
            st.error("A data inicial não pode ser posterior à data final.")
            return

        totais = Service.profissional_totalizar_atendimentos(
            id_profissional,
            data_inicial,
            data_final,
        )
        df = pd.DataFrame(
            totais,
            columns=["Serviço", "Quantidade de atendimentos"],
        )
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.bar_chart(
            df.set_index("Serviço"),
            x_label="Serviço",
            y_label="Atendimentos",
        )

        atendimentos = Service.profissional_listar_atendimentos(
            id_profissional,
            data_inicial,
            data_final,
        )
        if not atendimentos:
            st.info("Nenhum atendimento encontrado nesse período.")
            return

        atendimentos_df = pd.DataFrame(
            [
                {
                    "Data": atendimento["data"].strftime("%d/%m/%Y %H:%M"),
                    "Cliente": atendimento["cliente"],
                    "Serviço": atendimento["servico"],
                    "Valor (R$)": atendimento["valor"],
                    "Pago": atendimento["pago"],
                }
                for atendimento in atendimentos
            ]
        )
        st.subheader("Atendimentos no período")
        st.dataframe(atendimentos_df, use_container_width=True, hide_index=True)
