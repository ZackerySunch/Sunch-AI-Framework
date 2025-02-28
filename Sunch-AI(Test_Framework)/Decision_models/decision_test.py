import zmq
import os
import torch
import json
import threading

class Decision_start:
    def __init__(self):
        with open("models_port.json", "r", encoding="utf-8") as file:
            port = json.load(file)  # 把 JSON 轉成 Python 字典
        #設定初始資料
        os.environ["CUDA_VISIBLE_DEVICES"] = port["Decision_models"][0]  # 讓 Expert AI 只使用 GPU 1
        print(f"Expert AI 運行在: {torch.cuda.get_device_name(0)}")

class Decision_main:
    def __init__(self):
        # 讀取設定檔
        with open("models_port.json", "r", encoding="utf-8") as file:
            self.port = json.load(file)

        # 初始化 ZeroMQ 通訊
        context = zmq.Context()
        
        # Decision AI 連接 Expert AI
        self.decision_socket = context.socket(zmq.DEALER)  # REQ = Request
        self.decision_socket.setsockopt(zmq.IDENTITY, b"Decision")  # 設定身份
        
        # Decision AI 連接 Admin AI
        self.admin_socket = context.socket(zmq.ROUTER)  # REP = Reply
        self.admin_socket.bind(f"tcp://localhost:{self.port["Decision_models"][1]}")

        print("Decision AI 準備好發送請求給 Expert AI！")
        
        # 啟動一個新執行緒來處理 Admin AI 的 PING
        threading.Thread(target=self.Admin_Report, daemon=True).start()
        
        # 呼叫主程式
        self.main()

    def Admin_Report(self):
        """ 處理 Admin AI 發送的 PING 請求 """
        while True:
            clint_id,message = self.admin_socket.recv_multipart()
            if clint_id == b"Admin" and message == b"PING":
                print("✅ 收到 Admin AI 的 PING，回應 PONG")
                self.admin_socket.send_multipart([clint_id,b"PONG"])  # 回應 Admin AI

    def main(self):
        print("\n------------已完成載入------------\n")
        self.last_port = ""
        # 送出請求
        while True:
            enter = input("Enter:")
            if enter == "Coding":
                message_port = self.port["Expert(Coding)_Test.py"][1]
            elif enter == "Education":
                message_port = self.port["Expert(Education)_Test.py"][1]
            elif enter == "Office":
                message_port = self.port["Expert(Office)_Test.py"][1]
                
            elif enter == "Close":
                print("結束程式")
                break
            else:
                print("輸入錯誤")
                continue

            try:
                self.decision_socket.disconnect(f"tcp://localhost:{self.last_port}")  # 確保不會有舊連線
            except:
                pass

            self.decision_socket.connect(f"tcp://localhost:{message_port}")  # 連接到正確的 Expert AI
            
            self.decision_socket.send_multipart([enter.encode()])
            # 接收 Expert AI 回應
            message = self.decision_socket.recv_multipart()
            print(f"Decision AI 從 {message[0].decode("utf-8")} 收到回應：")
            self.last_port = message_port
    
if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    Decision_start()
    Decision_main()