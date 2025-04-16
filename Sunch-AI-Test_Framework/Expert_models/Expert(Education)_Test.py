import zmq
import torch
import os
import json

class Expert:
    def __init__(self):
        with open("models_port.json", "r", encoding="utf-8") as file:
            port = json.load(file) 

        os.environ["CUDA_VISIBLE_DEVICES"] = port["Expert(Education)_Test.py"][0]  
        print(f"Expert AI(Education) 運行在: {torch.cuda.get_device_name(int(port["Expert(Education)_Test.py"][0]))}")

        context = zmq.Context()
        self.socket = context.socket(zmq.ROUTER) 
        self.socket.bind(f"tcp://*:{port["Expert(Education)_Test.py"][1]}")  
        print(f"Expert AI(Education) TCP/IP Port : {port["Expert(Education)_Test.py"][1]}")
        print("Expert(Education) AI 啟動，等待 Decision AI 請求...")

        self.main()

    def main(self):
        while True:
            # 接收 Decision AI 的請求
            client_id,message = self.socket.recv_multipart()
            print(f"Expert(Education) AI 從 {client_id} 收到請求：{message}")

            if client_id == b"Admin" and message == b"PING":
                print("接收到Admin AI PING，回應PONG")
                self.socket.send_multipart([client_id,b"PONG"])
            else:
                response =f"🚀 發送回應：client_id={client_id}， 此訊息來自Expert(Education)".encode("utf-8")
                self.socket.send_multipart([client_id, response])
                
if __name__ == "__main__": 
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    Expert()