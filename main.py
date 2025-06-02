from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import re

app = FastAPI()

class ConsultaRequest(BaseModel):
    cpf: str
    data: str  # formato MM/AAAA

@app.post("/consultar")
def consultar_dados(dados: ConsultaRequest):
    # Validação simples do CPF
    if not re.fullmatch(r"\d{11}", dados.cpf):
        raise HTTPException(status_code=400, detail="CPF deve ter 11 dígitos.")

    # Validação da data MM/AAAA
    if not re.fullmatch(r"(0[1-9]|1[0-2])/\d{4}", dados.data):
        raise HTTPException(status_code=400, detail="Data deve estar no formato MM/AAAA.")

    # Aqui pode colocar lógica real, por enquanto só retorna dados recebidos
    return {"mensagem": "Consulta realizada com sucesso!", "cpf": dados.cpf, "mes_ano": dados.data}
