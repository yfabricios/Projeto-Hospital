import streamlit as st
import pandas as pd
import time
from service import Service

class ManterServicoUI:
    def main():
        st.header("Cadastro de Serviços")
        tab1, tab2, tab3, tab4 = st.tabs(["Listar", "Inserir", "Atualizar", "Excluir"])
        with tab1: ManterServicoUI.listar()
        with tab2: ManterServicoUI.inserir()
        with tab3: ManterServicoUI.atualizar()
        with tab4: ManterServicoUI.excluir()

    def listar():
        servicos = Service.servico_listar()
        if len(servicos) == 0: st.write("Nenhum serviço cadastrado")
        else:
            list_dic = []
            for obj in servicos:
                profissional = Service.profissional_listar_id(
                    obj.get_id_profissional()
                )
                list_dic.append(
                    {
                        "id": obj.get_id(),
                        "descricao": obj.get_descricao(),
                        "valor": obj.get_valor(),
                        "profissional": (
                            profissional.get_nome()
                            if profissional
                            else "Sem profissional vinculado"
                        ),
                    }
                )
            df = pd.DataFrame(list_dic)
            st.dataframe(df)

    def inserir():
        profissionais = Service.profissional_listar()
        descr = st.text_input("Informe a descrição")
        valor = st.text_input("Informe o valor")
        profissional = st.selectbox(
            "Informe o profissional",
            profissionais,
            index=None,
            key="servico_profissional_inserir",
        )
        if st.button("Inserir"):
            try:
                if profissional is None:
                    raise ValueError("Selecione um profissional para o serviço")
                Service.servico_inserir(
                    descr, float(valor), profissional.get_id()
                )
                st.success("Serviço inserido com sucesso")
                time.sleep(2)
                st.rerun()
            except ValueError as erro:
                st.error(erro)

    def atualizar():
        servicos = Service.servico_listar()
        if len(servicos) == 0: st.write("Nenhum serviço cadastrado")
        else:
            profissionais = Service.profissional_listar()
            op = st.selectbox("Atualização de Serviços", servicos)
            descr = st.text_input("Informe a nova descrição", op.get_descricao())
            valor = st.text_input("Informe o novo valor", str(op.get_valor()))
            index_profissional = next(
                (
                    i
                    for i, profissional in enumerate(profissionais)
                    if profissional.get_id() == op.get_id_profissional()
                ),
                None,
            )
            profissional = st.selectbox(
                "Informe o profissional",
                profissionais,
                index=index_profissional,
                key="servico_profissional_atualizar",
            )
            if st.button("Atualizar"):
                try:
                    if profissional is None:
                        raise ValueError("Selecione um profissional para o serviço")
                    id = op.get_id()
                    Service.servico_atualizar(
                        id, descr, float(valor), profissional.get_id()
                    )
                    st.success("Serviço atualizado com sucesso")
                    time.sleep(2)
                    st.rerun()
                except ValueError as erro:
                    st.error(erro)
                

    def excluir():
        servicos = Service.servico_listar()
        if len(servicos) == 0: st.write("Nenhum serviço cadastrado")
        else:
            op = st.selectbox("Exclusão de Serviços", servicos)
            if st.button("Excluir"):
                try:
                    id = op.get_id()
                    Service.servico_excluir(id)
                    st.success("Serviço excluído com sucesso")
                    time.sleep(2)
                    st.rerun()
                except ValueError as erro:
                    st.error(erro)

