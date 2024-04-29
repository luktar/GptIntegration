functions = [{
    "type": "function",
            "function": {
                "name": "add_item_to_shoppinglist",
                "description": "Add item to the shopping list",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "item": {
                            "type": "string",
                            "description": "item name",
                        },
                    },
                    "required": ["item"],
                },
            },
},
    {
    "type": "function",
            "function": {
                "name": "remove_item_from_shoppinglist",
                "description": "Remove item from the shopping list",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "item": {
                            "type": "string",
                            "description": "item name",
                        },
                    },
                    "required": ["item"],
                },
            },
},
    {
    "type": "function",
            "function": {
                "name": "mark_as_bought_in_shoppinglist",
                "description": "Interact with the shopping list by marking items as bought or purchasing items. This function will mark an item as bought when someone bought that item.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "item": {
                            "type": "string",
                            "description": "item name",
                        },
                    },
                    "required": ["item"],
                },
            },
},
    {
    "type": "function",
            "function": {
                "name": "get_all_items_from_shoppinglist",
                "description": "Get all items from the shopping list",
            },
},
    {
    "type": "function",
            "function": {
                "name": "get_items_to_buy_from_shoppinglist",
                "description": "Get only items to buy from the shopping list",
            },
}]
