import pandas as pd
import streamlit as st
from datetime import date
from service import Service


class TotalizarAtendimentoUI:
    def main():
        st.header("Totalizar meus atendimentos")

        hoje = date.today()
        inicio_mes = hoje.replace(day=1)
        coluna_inicio, coluna_final = st.columns(2)
        with coluna_inicio:
            data_inicial = st.date_input("Data inicial", value=inicio_mes)
        with coluna_final:
            data_final = st.date_input("Data final", value=hoje)

        if data_inicial > data_final:
            st.error("A data inicial não pode ser posterior à data final.")
            return

        totais = Service.profissional_totalizar_atendimentos(
            st.session_state["usuario_id"],
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
