import zmq
import torch
import os
import json

class Expert:
    def __init__(self):
        with open("models_port.json", "r", encoding="utf-8") as file:
            port = json.load(file)  # 把 JSON 轉成 Python 字典

        os.environ["CUDA_VISIBLE_DEVICES"] = port["Expert(Coding)_Test.py"][0]  # 讓 Expert AI 只使用 GPU 1
        print(f"Expert AI(Coding) 運行在: {torch.cuda.get_device_name(int(port["Expert(Coding)_Test.py"][0]))}")


        # 初始化 ZeroMQ 通訊
        context = zmq.Context()
        self.socket = context.socket(zmq.ROUTER)  # REP = Response
        self.socket.bind(f"tcp://*:{port["Expert(Coding)_Test.py"][1]}")  # 監聽端口，等待 Decision AI 連接
        print(f"Expert AI(Coding) TCP/IP Port : {port["Expert(Coding)_Test.py"][1]}")
        print("Expert(Coding) AI 啟動，等待 Decision AI 請求...")

        self.main()
        
    def main(self):
        while True:
            # 接收 Decision AI 的請求
            client_id,message = self.socket.recv_multipart()
            print(f"Expert(Coding) AI 從 {client_id} 收到請求：{message}")
            if client_id == b"Admin" and message == b"PING":
                print("接收到Admin AI PING，回應PONG")
                self.socket.send_multipart([client_id,b"PONG"])
            else:
                response =f"🚀 發送回應：client_id={client_id}， 此訊息來自Expert(Coding)".encode("utf-8")
                self.socket.send_multipart([client_id, response])
if __name__ == "__main__": 
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    Expert()