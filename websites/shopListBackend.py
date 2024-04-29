import asyncio
import json
import websockets


class ShoppingListBackend:
    def __init__(self):
        self.items_to_buy = []
        self.port = 8765
        self.websockets = set()
        self.start_server()

    def add(self, item: str):
        if item not in self.get_all_to_buy():
            self.items_to_buy.append({'name': item, 'bought': False})
            return True
        return False

    def delete(self, item):
        for i in range(len(self.items_to_buy)):
            if self.items_to_buy[i]['name'] == item:
                del self.items_to_buy[i]
                return True
        return False

    def bought(self, item):
        for i in range(len(self.items_to_buy)):
            if self.items_to_buy[i]['name'] == item:
                self.items_to_buy[i]['bought'] = True
                return True
        return False
    
    def unbought(self, item):
        for i in range(len(self.items_to_buy)):
            if self.items_to_buy[i]['name'] == item:
                self.items_to_buy[i]['bought'] = False
                return True
        return False

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
                item = data.get('item', '')
                print(action, item)
                if action == 'add':
                    result = self.add(item)
                    await self.send_response(result, "Item already exists")
                elif action == 'delete':
                    result = self.delete(item)
                    await self.send_response(result, "Item not found")
                elif action == 'bought':
                    result=self.bought(item)
                    await self.send_response(result, "Item not found")
                elif action == 'unbought':
                    result=self.unbought(item)
                    await self.send_response(result, "Item not found")
                elif action == 'get_all_to_buy':
                    await self.send_all_items_to_buy()
                elif action == 'get_all_items':
                    await self.send_all_items()
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
