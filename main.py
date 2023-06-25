from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def index():
    return {"Mensaje" : "Hola Mundo"}

@app.get("/validar/{nuemro}")
def validar_capicua(numero:str):
    respuesta = 'No es capícua'
    
    if numero == numero[::-1]:
        respuesta = 'Si es capicua'
        
    return {
        'numero': numero,
        'validación':respuesta
    }