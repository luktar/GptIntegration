import asyncio
import json
import websockets


class ShoppingListBackend:
    def __init__(self):
        self.items_to_buy = []
        self.port = 8765
        self.websockets = set()
        self.start_server()

    def add(self, items):
        for item in items:
            if item not in self.get_all_to_buy():
                self.items_to_buy.append({'name': item, 'bought': False})
        return True

    def delete(self, items):
        for item in items:
            for i in range(len(self.items_to_buy)):
                if self.items_to_buy[i]['name'] == item:
                    del self.items_to_buy[i]
                    break
        return True

    def bought(self, items):
        for item in items:
            for i in range(len(self.items_to_buy)):
                if self.items_to_buy[i]['name'] == item:
                    self.items_to_buy[i]['bought'] = True
                    break
        return True
    
    def unbought(self, items):
        for item in items:
            for i in range(len(self.items_to_buy)):
                if self.items_to_buy[i]['name'] == item:
                    self.items_to_buy[i]['bought'] = False
                    break
        return True
    
    def delete_all(self):
        self.items_to_buy.clear()
        return True

    # Send to all clients
    async def broadcast(self, message):
        for websocket in self.websockets:
            await websocket.send(message)

    async def handle_client(self, websocket, path):
        self.websockets.add(websocket)
        try:
            async for message in websocket:

                data = json.loads(message)
                action = data.get('action', '')
                items = data.get('items', [])
                #print(action, items)
                if action == 'get_all_to_buy':
                    await self.send_all_items_to_buy()
                elif action == 'get_all_items':
                    await self.send_all_items()
                elif action == 'add':
                    result = self.add(items)
                    await self.send_response(result, "Item already exists")
                elif action == 'delete':
                    result = self.delete(items)
                    await self.send_response(result, "Item not found")
                elif action == 'bought':
                    result=self.bought(items)
                    await self.send_response(result, "Item not found")
                elif action == 'unbought':
                    result=self.unbought(items)
                    await self.send_response(result, "Item not found")
                elif action == 'delete_all':
                    result=self.delete_all()
                    await self.send_response(result, "Items not found")
        finally:
            self.websockets.remove(websocket)

    # Response with custom text
    async def send_response(self, result, message):
        if result:
            await self.send_all_items()
        else:
            await self.broadcast(json.dumps({"message": message}))

    # Only not bought items
    async def send_all_items_to_buy(self):
        items_to_buy = json.dumps(
            {"items_to_buy": [item for item in self.items_to_buy if not item['bought']]})
        await self.broadcast(items_to_buy)

    # All items
    async def send_all_items(self):
        all_items = json.dumps({"items_to_buy": self.items_to_buy})
        await self.broadcast(all_items)

    # Only names
    def get_all_to_buy(self):
        return [item['name'] for item in self.items_to_buy]

    # This block main thread forever
    def start_server(self):
        start_server = websockets.serve(
            self.handle_client, "localhost", self.port)
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()


def main():
    shopping_list = ShoppingListBackend()


if __name__ == "__main__":
    main()
