# Inspeção de frota com conexão instável

O checklist foi desenvolvido para ser usado na inspeção de caminhões no pátio, na doca e na garagem. O sinal oscila nesses locais, mas a inspeção precisa continuar.

## Como o registro chega ao servidor

1. O inspetor marca o item e registra a observação pelo celular.
2. Quando a rede está indisponível, os registros ficam em uma fila no próprio dispositivo.
3. Quando a conexão volta, a aplicação tenta enviar a fila para o Supabase. O fluxo pode ser verificado em um teste que simula a perda e o retorno da conexão.

| Decisão | Motivo |
| --- | --- |
| PWA com service worker | Permite instalar o aplicativo no celular e preparar a interface para uso offline. |
| Fila local | Preserva a entrada do inspetor enquanto o servidor está inacessível. |
| Regra de não conformidade | Uma pendência continua valendo nos dias seguintes até ser resolvida por um administrador. |
| Testes de lógica e de navegação | Conferem a regra da inspeção e o comportamento da aplicação quando a conexão cai. |

**Stack:** TypeScript, React, Next.js e Supabase.
