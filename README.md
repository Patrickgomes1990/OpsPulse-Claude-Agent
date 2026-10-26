# OpsPulse – Agente de Diagnóstico de Infraestrutura com Claude

O **OpsPulse** é uma solução de automação baseada em Inteligência Artificial que consome a API do Claude (Anthropic) com **Tool Use (Function Calling)** para diagnosticar falhas de infraestrutura e notificar equipes de operações autonomamente.

## 🏗️ Arquitetura da Solução

1. **Entrada:** Recebe alertas de erro de microsserviços.
2. **Raciocínio & Decisão:** O modelo `claude-3-5-sonnet` analisa o problema e decide qual ferramenta precisa consultar.
3. **Execução de Ferramentas:** Busca logs do sistema e gera diagnósticos estruturados.
4. **Saída:** Notificação formatada para resolução rápida da causa raiz.

## 🚀 Como Executar o Projeto Localmente

### Pré-requisitos
* Python 3.11+
* Chave de API da Anthropic

### Passo a Passo

1. Clone o repositório:
   \`\`\`bash
   git clone https://github.com/SEU_USUARIO/OpsPulse-Claude-Agent.git
   cd OpsPulse-Claude-Agent
   \`\`\`

2. Crie e ative o ambiente virtual:
   \`\`\`bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   \`\`\`

3. Instale as dependências:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

4. Configure as variáveis de ambiente:
   Copie o arquivo `.env.example` para `.env` e insira sua `ANTHROPIC_API_KEY`.

5. Execute o agente:
   \`\`\`bash
   python main.py
   \`\`\`