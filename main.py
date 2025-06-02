from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, model_validator
import re

app = FastAPI()

class ConsultaRequest(BaseModel):
    cpf: str | None = None
    carteirinha: str | None = None
    data: str  # formato MM/AAAA

    @model_validator(mode="after")
    def validar_campos(self):
        if not self.cpf and not self.carteirinha:
            raise ValueError("É obrigatório informar CPF ou carteirinha.")

        if self.cpf and not re.fullmatch(r"\d{11}", self.cpf):
            raise ValueError("CPF deve ter exatamente 11 dígitos numéricos.")

        if self.carteirinha and not re.fullmatch(r"[A-Za-z0-9]{17}", self.carteirinha):
            raise ValueError("Carteirinha deve ter exatamente 17 caracteres alfanuméricos.")

        if not re.fullmatch(r"(0[1-9]|1[0-2])/\d{4}", self.data):
            raise ValueError("Data deve estar no formato MM/AAAA.")

        return self

@app.post("/consultar")
def consultar_dados(dados: ConsultaRequest):
    return {
        "mensagem": "Consulta realizada com sucesso!",
        "cpf": dados.cpf,
        "carteirinha": dados.carteirinha,
        "mes_ano": dados.data
    }
