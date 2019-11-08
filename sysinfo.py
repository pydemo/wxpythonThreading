import psutil

def getCPU():
    return psutil.cpu_percent(interval=1)

def getRAM():
    a,b,c,d,e = psutil.virtual_memory()
    data = {'total':'%.4f'%(a/(1024*1024*1024)), 'available':'%.4f'%(b/(1024*1024*1024)), 'percent':c, 'used':'%.4f'%(d/(1024*1024*1024)), 'free':'%.4f'%(e/(1024*1024*1024))}
    return data

# if __name__ == '__main__':
#     print(psutil.virtual_memory())