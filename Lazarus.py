import wmi 

class wmi_class:
    def __init__ (self):
        pass

    def handshake(self):
        c=wmi.WMI()
        
        drivers=c.Win32_DiskDrive()
        driver_list={}
        n=0
        for drive in (drivers):
            n+=1
            if drive.InterfaceType=="USB":
                size_raw=int(drive.Size)
                size=round(size_raw/1024/1024/1024,2)
                print(f"[{n}]  {drive.Caption} => {size}GB")

                driver_list[n]={"id":drive.DeviceID,"size":size,"caption":drive.Caption}

            else:
                n=n-1    


        return driver_list             

class read:
    def __init__ (self):
        pass

    def read(self,id):
        found=False
        with open(id,"rb") as d:
            with open(f"Lazarus.jpg","wb") as f:
                while True:
                    data=d.read(512)
                    if len(data) == 0:
                        break

                    else:
                        
                          if found==False:  
                            if b'\xff\xd8\xff' in data:
                                found=True
                                start_in=data.find(b'\xff\xd8\xff')
                                clean_data=data[start_in:]

                                f.write(clean_data)
                                continue

                          if found:
                             if b'\xff\xd9' in data:
                                f.write(data)
                                print("Recovery Complete")
                                break

                             else:
                                f.write(data)
                                continue
                             

                          


class main:
    def __init__(self):
        self.scan=wmi_class()
        self.read=read()

    def run(self):
        driver_list=self.scan.handshake()

        sel=input("Select Drive: ")

        id=driver_list[int(sel)]["id"]  
        driver=driver_list[int(sel)]["caption"]  
        print(f"\n======'{driver}' is selected======\n")

        self.read.read(id)

if __name__ == "__main__":
    main().run()


