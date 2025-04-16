import os
import json
import time
import torch
import subprocess 

class Default_startup:
    def __init__(self):
        print("確認版本中......")
        if not torch.cuda.is_available():
            print("❌ CUDA 不可用，請確保已安裝 NVIDIA 驅動")
        
        print("Cuda版本:",torch.version.cuda)          # PyTorch 目前的 CUDA 版本
        print("可用GPU數量:",torch.cuda.device_count())   # CUDA 可用的 GPU 數量 
        
        print("\n抓取模組中......")
        global dicision_models, Expert_models
        try:
            dicision_models = [f for f in os.listdir("Decision_models") if f.endswith((".py"))]
            Expert_models = [f for f in os.listdir("Expert_models") if f.endswith((".py"))]
        except:
            pass
        print("\n抓取模組完成......\n")

class admin:
    print("error : 目前尚未開放 admin AI 模式")
    
class Manual:
    def __init__(self):
        global file_launch_dict,models_port
        file_launch_dict = {}
        models_port = {}
        self.Decision_setting()
        self.Expert_setting()
        
    def Decision_setting(self):
        print("----------設定 Decision_models----------")
        print("Dicision_models:\n")
        Index = 0
        for models in dicision_models:
            print(f"{Index} : {models}")
            Index += 1
            
        model = int(input("\n請輸入 Decision_models 模型(int):"))
        print(f"已選擇 {dicision_models[model]}\n")
        file_launch_dict["Decision_models"] = [dicision_models[model]]
        
        print("----------設定 Decision AI 運行GPU----------")
        num_gpus = torch.cuda.device_count()
        print(f"🎮 你的電腦上有 {num_gpus} 張 NVIDIA 顯示卡！\n")
        for i in range(num_gpus):
            print(f"GPU {i}: {torch.cuda.get_device_name(i)}")
        decision_gpu = input("\n請輸入 Decision_models 的 GPU:")
        
        decision_port = input("請輸入 Decision_models 的 TCP Port:")
        models_port["Decision_models"] = decision_gpu, decision_port
        print("\n")

    def Expert_setting(self):
        print("----------設定 Expert_models----------")
        expert_models = []
        for models in Expert_models:
            print(f"\n=>設定{models}")
            if input(f"是否啟動此模組 : {models} (y/n)") == "y":
                expert_models.append(models)
                
                num_gpus = torch.cuda.device_count()
                print(f"🎮 你的電腦上有 {num_gpus} 張 NVIDIA 顯示卡！\n")
                for i in range(num_gpus):
                    print(f"GPU {i}: {torch.cuda.get_device_name(i)}")
                    
                Expert_gpu = input("\n請輸入 Decision_models 的 GPU:")
                Expert_port = input("請輸入 Decision_models 的 TCP Port:")
                models_port[models] = Expert_gpu, Expert_port
                
        file_launch_dict["Expert_models"] = expert_models
        print("\n")
        
class ProgramStarter:
    def __init__(self):
        print("----------啟動程式----------")
        # 將字典寫入 JSON 檔案
        self.create_json()
        self.open_models()
    
    def create_json(self):
        # 將字典寫入 JSON 檔案
        with open("Decision_models\\models_port.json", "w", encoding="utf-8") as file:
            json.dump(models_port, file, indent=4)
        
        with open("Expert_models\\models_port.json", "w", encoding="utf-8") as file:
            json.dump(models_port, file, indent=4)

    def open_models(self):
        for models in file_launch_dict:
            print(f"正在開啟 : {models}")
            for file in file_launch_dict[models]:
                print(file)
                if file.endswith(".py"):
                    subprocess.Popen(["python", f"{models}/{file}"])
                elif file.endswith(".pt"):
                    print("error : 目前尚未開放 .pt 模型")
                elif file.endswith(".onnx"):
                    print("error : 目前尚未開放 .onnx 模型")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    Default_startup()
    while True:
        global mode
        print("-----------選擇模式-------------")
        mode = input("請輸入模式 (手動:0/admin AI:1):")
        if mode == "0":
            print("以選擇手動模式......(0)")
            break
        elif mode == "1":
            print("以選擇 admin AI 模式......(1)")
            print("error : 目前尚未開放 admin AI 模式")
        else:
            print("輸入錯誤")

    print("\n")

    if mode == "0":
        Manual()
    elif mode == "1":
        admin()
    
    ProgramStarter()