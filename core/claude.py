import anthropic

client = anthropic.Anthropic(api_key="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")

def enviar_mensaje(historial): 
    respuesta = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=historial

    )

    return respuesta.content[0].text