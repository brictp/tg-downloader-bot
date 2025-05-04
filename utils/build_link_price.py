async def build_link_price(item_data):
    """Construir el enlace de precios para Albion Online"""
    # Extraer el comando y los argumentos del mensaje

    item_name, tier, enchantment = item_data.values()
    # Determinar si el objeto es de refinar o refinado
    refining_items = [
        "hide",
        "ore",
        "metalbar",
        "leather",
        "wood",
        "rock",
        "planks",
        "cloth",
        "fiber",
        "stone",
    ]

    if any(refining_item in item_name for refining_item in refining_items):
        item = f"T{tier}_{item_name.upper()}_LEVEL{enchantment}@{enchantment}"
    else:
        item = f"T{tier}_{item_name}@{enchantment}"

    # Construir el enlace
    host = "https://west.albion-online-data.com"
    next = f"/api/v2/stats/charts/{item}.json?time-scale=1"
    LINK = f"{host}{next}"

    return LINK
