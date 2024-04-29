import json
from typing import Dict, List
import websockets
import asyncio


class ShoppingListConnector:
    def __init__(self, websocket_url='ws://localhost:8765') -> None:
        self.websocket_url = websocket_url

    async def send_message(self, message):
        async with websockets.connect(self.websocket_url) as websocket:
            await websocket.send(json.dumps(message))
            response = await websocket.recv()  # Receive the response from the server
            return json.loads(response)

    def add_items_to_shoppinglist(self, items: str):
        items=self.convert_to_list(items)
        response=asyncio.run(self.send_message({"action": "add", "items": items}))
        if 'message' in response:
            return response['message']
        else:
            return f"Items added successfully"

    def remove_item_from_shoppinglist(self, items: str):
        items=self.convert_to_list(items)
        response=asyncio.run(self.send_message({"action": "delete", "items": items}))
        if 'message' in response:
            return response['message']
        else:
            return f"Items removed successfully"

    def mark_as_bought_in_shoppinglist(self, items: str):
        items=self.convert_to_list(items)
        response=asyncio.run(self.send_message({"action": "bought", "items": items}))
        if 'message' in response:
            return response['message']
        else:
            return f"Items marked as bought"
    
    def delete_all_from_shoppinglist(self):
        response=asyncio.run(self.send_message({"action": "delete_all"}))
        if 'message' in response:
            return response['message']
        else:
            return f"Delete all items successfully"

    def get_all_items_from_shoppinglist(self):
        items = asyncio.run(self.send_message({"action": "get_all_items"}))
        return self.format_shopping_list_all_items(items)

    def get_items_to_buy_from_shoppinglist(self):
        items = asyncio.run(self.send_message({"action": "get_all_to_buy"}))
        return self.format_shopping_list(items)

    def format_shopping_list(self, items):
        if not items or 'items_to_buy' not in items:
            return "Shopping list: (empty)"

        item_list = [item['name'] for item in items['items_to_buy']]
        formatted_list = ', '.join(set(item_list))
        return f"Shopping list: {formatted_list}"
    
    def format_shopping_list_all_items(self, items):
        if not items or 'items_to_buy' not in items:
            return "Shopping list: (empty)"

        formatted_list = []
        for item in items['items_to_buy']:
            item_name = item['name']
            bought_status = "bought" if item['bought'] else "not bought"
            formatted_list.append(f"{item_name} - {bought_status}")

        return "Shopping list: " + ", ".join(formatted_list)

    def convert_to_list(self, items):
        item_names = [item.strip() for item in items.split(",")]
        return item_names