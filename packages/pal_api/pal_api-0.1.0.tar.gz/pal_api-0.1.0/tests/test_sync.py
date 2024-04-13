from pal_api import PalApiClient


def test_request():
    # client = PalApiClient(host="host.docker.internal", password="testtest")
    # client.announce_message("こんにちは")
    # print(client.get_server_info())
    # print(client.get_player_list())
    # print(client.get_server_settings())
    # print(client.get_server_metrics())
    # client.kick_player("steam_76561198825398691")
    # client.save_world()
    # client.ban_player("steam_76561198825398691", "test")
    # client.unban_player("steam_76561198825398691")
    # client.shutdown_server(10, "test", True)
    with PalApiClient(host="host.docker.internal", password="testtest") as client:
        print(client.get_player_list())


test_request()
