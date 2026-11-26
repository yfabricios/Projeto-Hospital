import pandas as pd
import streamlit as st
from datetime import date
from service import Service


class TotalizarProfissionalUI:
    def main():
        st.header("Totalizar atendimentos profissional")

        hoje = date.today()
        inicio_mes = hoje.replace(day=1)
        coluna_inicio, coluna_final = st.columns(2)
        with coluna_inicio:
            data_inicial = st.date_input(
                "Data inicial",
                value=inicio_mes,
                format="DD/MM/YYYY",
            )
        with coluna_final:
            data_final = st.date_input(
                "Data final",
                value=hoje,
                format="DD/MM/YYYY",
            )

        if data_inicial > data_final:
            st.error("A data inicial não pode ser posterior à data final.")
            return

        totais = Service.profissional_totalizar_atendimentos_periodo(
            data_inicial,
            data_final,
        )
        df = pd.DataFrame(
            [
                {
                    "Profissional": total["Profissional"],
                    "Quantidade de serviços": total["Quantidade de serviços"],
                }
                for total in totais
            ],
            columns=["Profissional", "Quantidade de serviços"],
        )
        if df.empty:
            st.info("Nenhum profissional cadastrado.")
            return

        st.dataframe(df, use_container_width=True, hide_index=True)
        st.bar_chart(
            df.set_index("Profissional"),
            x_label="Profissional",
            y_label="Serviços realizados",
        )
