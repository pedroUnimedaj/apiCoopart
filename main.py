from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, root_validator
import re

app = FastAPI()

class ConsultaRequest(BaseModel):
    cpf: str = None
    carteirinha: str = None
    data: str  # formato MM/AAAA

    @root_validator
    def validar_campos(cls, valores):
        cpf = valores.get('cpf')
        carteirinha = valores.get('carteirinha')
        data = valores.get('data')

        if not cpf and not carteirinha:
            raise ValueError("É obrigatório informar CPF ou carteirinha.")

        if cpf and not re.fullmatch(r"\d{11}", cpf):
            raise ValueError("CPF deve ter exatamente 11 dígitos numéricos.")

        if carteirinha and not re.fullmatch(r"[A-Za-z0-9]{17}", carteirinha):
            raise ValueError("Carteirinha deve ter exatamente 17 caracteres alfanuméricos.")

        if not re.fullmatch(r"(0[1-9]|1[0-2])/\d{4}", data):
            raise ValueError("Data deve estar no formato MM/AAAA.")

        return valores

@app.post("/consultar")
def consultar_dados(dados: ConsultaRequest):
    return {
        "mensagem": "Consulta realizada com sucesso!",
        "cpf": dados.cpf,
        "carteirinha": dados.carteirinha,
        "mes_ano": dados.data
    }
