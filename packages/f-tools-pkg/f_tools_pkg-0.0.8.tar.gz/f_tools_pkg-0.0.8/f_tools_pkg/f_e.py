import os
import subprocess

class yc_e:
    def __init__(self,timeout):
        for num in range(0,timeout):
            ret = os.popen("e z").readlines()
            if ret[0].find("sync 0 = 02")!=-1:
                break
        if(num >=timeout):  
            print("can't e command")
            
    def run(command, timeout_duration=None, default_value="0"):
        try:
            command = command.strip().split(" ")
            print(command)
            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=timeout_duration,
            )
            return result.stdout  # 返回正确执行时的输出
        except subprocess.TimeoutExpired:
            # 进程超时
            print("Calling '{' '.join(command)}' timed out after {timeout_duration} seconds.")
            return default_value  # 返回默认值
            
    def e_k(self):
        self.run("e k")
        
    def e_p(self):
        while True:
            ret =  self.run("e p")
            print(ret)
            if ret.find("Stopped") != -1:
                break
        return int(ret.split(" ")[3].replace(":",""),16)
    
    def e_pu(self):
        while True:
            ret = self.run("e pu")
            print(ret)
            if ret.find("Stopped") != -1:
                break
        return int(ret.split(" ")[3].replace(":",""),16)

    def e_pr(self):
        while True:
            ret = self.run("e pr")
            print(ret)
            if ret.find("Stopped") != -1:
                break
        return int(ret.split(" ")[3].replace(":",""),16)
    
    def e_tu(self):
        addr = -1
        ret = self.run("e tu")
        print(ret)
        if ret.find("CPU") != -1:
            addr = int(ret.split(" ")[3].replace(":",""),16)
        return addr
    
    def e_nu(self):
        addr = -1
        ret = self.run("e nu")
        print(ret)
        if ret.find("CPU") != -1:
            addr = int(ret.split(" ")[3].replace(":",""),16)
        return addr
    
    def e_cu(self):
        ret = self.run("e cu")
        print(ret)
        return self.e_au()
        
    def e_bu(self,addr,type=0):
        ret = self.run("e bu " + hex(addr).replace("0x","") + hex(type).replace("0x"," "))
        print(ret)
    
    def e_ru(self,reg):
        ret = self.run("e ru "+reg)
        print(ret)
        return [int(ret.split(" ")[1],10),ret.split(" ")[3].strip()]
        
    
    def e_au(self):
        isstop = 0
        pc = 0
        ret = self.run("e au")
        if ret.find("Stopped") != -1:
            isstop = 1
        else:
            isstop = 0
        pc = int(ret.split(" ")[3].replace(":",""),16)
        return [isstop,pc]
        
        
    def tohex(self,d):
        return hex(d).replace("0x","")
            
    def get_mem_data(self,addr,len):
        result = self.run("e "+self.tohex(addr)+"l"+self.tohex(len))
        odata=[]
        for line in result[1:]:
            for data in line.split(":")[1].strip().split(" "):
                odata.append(int(data,16))
        return odata
    
    def get_byte(self,addr):
        ret = self.get_mem_data(addr,1)
        return ret[0]

    def get_word(self,addr):
        ret = self.get_mem_data(addr,2)
        return ret[0] + (ret[1] << 8)

    def get_dword(self,addr):
        ret = self.get_mem_data(addr,4)
        return ret[0] + (ret[1] << 8) + (ret[2] << 16) + (ret[3] << 24)
    
    def set_data(self,addr,data):
        self.run("e "+self.tohex(addr)+" "+self.tohex(data))

    def set_byte(self,addr,data):
        self.set_data(addr,("%02x" %data))

    def set_word(self,addr,data):
        self.set_data(addr,("%04x" %data))

    def set_dword(self,addr,data):
        self.set_data(addr,("%08x" %data))