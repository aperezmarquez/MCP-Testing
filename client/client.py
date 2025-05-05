import asyncio
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env

class MCPClient:
    def __init__(self):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.anthropic = Anthropic()

    async def connect_to_server(self, server_script_path: str):
        """Connect to an MCP server

        Args:
            server_script_path: Path to the server script (.py)
        """
        is_python = server_script_path.endswith('.py')
        if not is_python:
            raise ValueError("Server script must be a .py file")

        server_params = StdioServerParameters(
            command="python",
            args=[server_script_path],
            env=None
        )

        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        await self.session.initialize()

        # List available tools
        response = await self.session.list_tools()
        tools = response.tools
        print("\nConnected to server with tools:", [tool.name for tool in tools])

    async def process_query(self, query: str, messages: list) -> str:
        """Process a query using Claude and available tools"""
        system = ('Eres un asistente virtual de "Pizza Deliciosa", especializado en atender pedidos online. Tu objetivo es guiar al cliente en el proceso de pedido de manera amigable y eficiente.'
'INSTRUCCIONES TÉCNICAS:'
'- Inicia mostrando un saludo cordial y pregunta al cliente qué desea ordenar.'
'- Usa la función "get_restaurant_menu()" para obtener el menú actualizado.'
'- Presenta el menú de forma clara, separando por categorías: pizzas (con tamaños disponibles), bebidas (latas/botellas) y extras.'
'- Cuando el cliente seleccione productos, utiliza estas funciones en secuencia:'
  '1. Para pizzas: "add_pizza_order(pizza_order=None, pizza_name, pizza_size, pizza_price)"'
  '2. Para bebidas: "add_drink_order(drink_order=None, drink_name, drink_type, drink_price)"'
  '3. Para extras: "add_extra_order(extra_order=None, extra_name, extra_price)"'
  '4. Para finalizar: "create_order(pizza_order, drink_order, extra_order)"'
'IMPORTANTE:'
'- La primera vez que llames a cada función de añadir, NO incluyas el parámetro de orden (pizza_order, drink_order, extra_order).'
'- En llamadas posteriores a la misma función, SÍ debes incluir el valor devuelto anteriormente.'
'- Verifica siempre que los productos solicitados existan en el menú antes de añadirlos.'
'- Si el usuario pide algo que no está en el menú, indícaselo amablemente y sugiere alternativas.'
'- Confirma siempre los productos añadidos y pregunta si desea algo más antes de finalizar.'
'- Al completar el pedido, muestra un resumen detallado con todos los productos y el precio total.'
'- Maneja posibles errores de conexión o base de datos de forma amigable, sin mostrar detalles técnicos. '
'Haz que la experiencia sea conversacional y natural, como si el cliente estuviera hablando con un empleado amable de la pizzería.')

        messages.append(
            {
                "role": "user",
                "content": query
            }
        )

        response = await self.session.list_tools()
        available_tools = [{
            "name": tool.name,
            "description": tool.description,
            "input_schema": tool.inputSchema
        } for tool in response.tools]

        # Initial Claude API call
        response = self.anthropic.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            system=system,
            messages=messages,
            tools=available_tools
        )

        # Process response and handle tool calls
        final_text = []

        assistant_message_content = []

        print(response.content)

        for content in response.content:
            if content.type == 'text':
                final_text.append(content.text)
                assistant_message_content.append(content)
            elif content.type == 'tool_use':
                tool_name = content.name
                tool_args = content.input

                # Execute tool call
                result = await self.session.call_tool(tool_name, tool_args)
                final_text.append(f"[Calling tool {tool_name} with args {tool_args}]")

                assistant_message_content.append(content)
                messages.append({
                    "role": "assistant",
                    "content": assistant_message_content
                })
                messages.append({
                    "role": "user",
                    "content": [
                        {
                            "type": "tool_result",
                            "tool_use_id": content.id,
                            "content": result.content
                        }
                    ]
                })

                # Get next response from Claude
                response = self.anthropic.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=1000,
                    system=system,
                    messages=messages,
                    tools=available_tools
                )

                final_text.append(response.content[0].text)

        return messages, "\n".join(final_text)

    async def chat_loop(self):
        """Run an interactive chat loop"""
        print("\nMCP Client Started!")
        print("Type your queries or 'quit' to exit.")

        messages = []

        while True:
            try:
                query = input("\nQuery: ").strip()

                if query.lower() == 'quit':
                    break

                messages, respuesta = await self.process_query(query, messages)
                print("\n" + respuesta)

            except Exception as e:
                print(f"\nError: {str(e)}")

    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()

async def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py <path_to_server_script>")
        sys.exit(1)

    client = MCPClient()
    try:
        await client.connect_to_server(sys.argv[1])
        await client.chat_loop()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    import sys
    asyncio.run(main())
