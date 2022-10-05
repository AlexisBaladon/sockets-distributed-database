from threading import Thread
from dtServer import DtServer
from datos import client_attention_DATOS
from descubrimiento import ANNOUNCE, DISCOVER
from src.client.ClientSocket import ClientSocket

DESCUBRIMIENTO_PORT = "2022"

if __name__ == "__main__":
    server = DtServer("12","p","puerto_des")
    
    announce_udp_socket = None #UdpSocket()
    discover_udp_socket = None #UdpSocket()
    thread_announce = Thread(ANNOUNCE, announce_udp_socket, server)
    thread_discover = Thread(DISCOVER, discover_udp_socket, server)

    while True:
        datos_tcp_socket = ClientSocket()
        thread_tcp = Thread(client_attention_DATOS, server, datos_tcp_socket)