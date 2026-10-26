import os
import json
import anthropic
from dotenv import load_dotenv

# 1. Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# 2. Inicializa o cliente do Claude lendo a API Key do ambiente
client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

# 3. Definição do Schema das Ferramentas (Tool Use)
# O Claude lê essa estrutura para saber quais funções ele pode 'chamar'
TOOLS = [
    {
        "name": "fetch_service_logs",
        "description": "Busca os últimos registros de erro de um microsserviço.",
        "input_schema": {
            "type": "object",
            "properties": {
                "service_name": {
                    "type": "string",
                    "description": "Nome do serviço com falha (ex: payment-api, auth-service)."
                },
                "lines": {
                    "type": "integer",
                    "description": "Quantidade de linhas de log a retornar.",
                    "default": 10
                }
            },
            "required": ["service_name"]
        }
    },
    {
        "name": "send_alert_summary",
        "description": "Envia o diagnóstico final consolidado para o time de SRE/DevOps.",
        "input_schema": {
            "type": "object",
            "properties": {
                "summary": {
                    "type": "string",
                    "description": "Resumo executivo do incidente e causa raiz."
                },
                "recommended_action": {
                    "type": "string",
                    "description": "Ação recomendada para correção do problema."
                }
            },
            "required": ["summary", "recommended_action"]
        }
    }
]

# 4. Funções Python Reais que executam a ação lógica solicitada pelo Claude
def execute_fetch_service_logs(service_name: str, lines: int = 10) -> str:
    """Simula a busca de logs em um serviço como AWS CloudWatch ou GCP Cloud Logging."""
    print(f"\n[SISTEMA] Consultando logs do serviço '{service_name}'...")
    # Simulação de resposta de log com erro de banco de dados
    return (
        f"[ERROR 2026-10-26 11:45:00] DatabaseConnectionError: "
        f"Timeout ao conectar com db-prod.internal:5432 após 5000ms no serviço '{service_name}'."
    )

def execute_send_alert_summary(summary: str, recommended_action: str) -> str:
    """Simula o envio de notificação formatada para o Slack ou Telegram."""
    print(f"\n[SISTEMA] Disparando alerta final no canal de Operações!")
    print(f"📌 Resumo: {summary}")
    print(f"💡 Ação Recomendada: {recommended_action}")
    return "Notificação enviada com sucesso ao canal de SRE."

# 5. Orquestrador do Agente (Loop de Execução)
def run_agent_loop(initial_prompt: str):
    print(f"🚀 Incidente recebido: {initial_prompt}\n")
    
    # Histórico de conversas enviado ao Claude
    messages = [
        {"role": "user", "content": initial_prompt}
    ]

    while True:
        # Chamada para a API do Claude
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            tools=TOOLS,
            messages=messages
        )

        # Se o Claude encerrou sem precisar chamar mais ferramentas
        if response.stop_reason == "end_turn":
            print("\n✅ Diagnóstico concluído pelo Agente OpsPulse.")
            break

        # Se o Claude solicitou o uso de uma ferramenta (Tool Use)
        if response.stop_reason == "tool_use":
            # Guarda a intenção do Claude na lista de mensagens
            messages.append({"role": "assistant", "content": response.content})

            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    tool_name = block.name
                    tool_input = block.input
                    tool_use_id = block.id

                    print(f"🤖 Claude escolheu a ferramenta: '{tool_name}' com parâmetros: {tool_input}")

                    # Roteamento da chamada de ferramenta
                    if tool_name == "fetch_service_logs":
                        result = execute_fetch_service_logs(**tool_input)
                    elif tool_name == "send_alert_summary":
                        result = execute_send_alert_summary(**tool_input)
                    else:
                        result = "Ferramenta não encontrada."

                    # Monta o bloco de resposta que é devolvido ao Claude
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": tool_use_id,
                        "content": result
                    })

            # Adiciona o resultado das ferramentas no histórico e envia de volta ao Claude
            messages.append({"role": "user", "content": tool_results})

if __name__ == "__main__":
    # Executa o teste do agente com um alerta fictício
    run_agent_loop("Alerta crítico: O serviço 'payment-api' apresentou alta taxa de erros 500.")