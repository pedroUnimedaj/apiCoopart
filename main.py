from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, root_validator
import re

app = FastAPI()

class Entrada(BaseModel):
    cpf: str | None = None
    carteirinha: str | None = None
    competencia: str

    @root_validator
    def validar_campos(cls, values):
        cpf = values.get('cpf')
        carteirinha = values.get('carteirinha')
        competencia = values.get('competencia')

        if not cpf and not carteirinha:
            raise ValueError("É obrigatório informar CPF ou carteirinha.")

        if cpf and not re.fullmatch(r"\d{11}", cpf):
            raise ValueError("CPF deve ter exatamente 11 dígitos numéricos.")

        if carteirinha and len(carteirinha) != 17:
            raise ValueError("Carteirinha deve ter exatamente 17 caracteres.")

        if not re.fullmatch(r"(0[1-9]|1[0-2])/20\d{2}", competencia):
            raise ValueError("Competência deve estar no formato MM/AAAA.")

        return values

@app.post("/receber")
def receber_dados(dados: Entrada):
    return {"mensagem": "Dados recebidos com sucesso", "dados": dados}
