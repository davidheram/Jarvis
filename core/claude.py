import anthropic
from dotenv import load_dotenv
import os 
from core.rag import buscar_contexto

load_dotenv()

client = anthropic.Anthropic(api_key="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")

def enviar_mensaje(historial, callback): 
    ultima_pregunta = historial[-1]["content"]
    contexto = buscar_contexto(ultima_pregunta)

    system_prompt = f"""Eres Jarvis, un copiloto de ventas consultivas para una empresa de TI llamada TechSoluciones MX.

Tu objetivo es ayudar al ejecutivo de cuentas durante el proceso de venta consultiva.

Cuando el ejecutivo te describa la situacion de un cliente:
1. Haz preguntas para entender mejor la necesidad
2. Recomienda la solucion correcta basandote en el catalogo
3. Proporciona argumentos tecnicos y comerciales
4. Ayuda a anticipar objeciones

Usa esta informacion del catalogo para responder:
{contexto}

Si la informacion no esta en el catalogo, dilo claramente."""
    respuesta_completa = ""
    with client.messages.stream(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system= system_prompt,
        messages=historial
    ) as stream:
        for texto in stream.text_stream:
            respuesta_completa += texto 
            callback(texto) 

    return respuesta_completa