import asyncio
from pal_api import AsyncPalApiClient


async def main():
    client = AsyncPalApiClient(host="host.docker.internal", password="testtest")
    # await client.announce_message("こんにちは")
    print(await client.get_server_info())
    # print(await client.get_player_list())
    # print(await client.get_server_settings())
    # print(await client.get_server_metrics())
    # await client.kick_player("steam_76561198825398691")
    # await client.save_world()
    # await client.ban_player("steam_76561198825398691", "test")
    # await client.unban_player("steam_76561198825398691")
    # await client.shutdown_server(5, "test", True)
    await client.close()


asyncio.run(main())
