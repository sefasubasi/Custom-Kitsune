import os
import subprocess
import csv
import cupy as np
from scapy.all import *
import platform
import netStat as ns  # netStat modülünü ekliyoruz

class FE:
    def __init__(self, interface="wlan0", limit=np.inf):
        self.interface = interface
        self.limit = limit
        self.curPacketIndx = 0
        self.process = None
        self.tsvin = None
        self._start_tshark()

        # netStat nesnesini tanımlıyoruz
        self.nstat = ns.netStat(HostLimit=10000, HostSimplexLimit=1000)

    def _start_tshark(self):
        tshark_path = self._get_tshark_path()
        if not tshark_path:
            raise FileNotFoundError("tshark executable not found. Please ensure Wireshark is installed.")
        cmd = [
            tshark_path,
            "-i", self.interface,
            "-T", "fields",
            "-e", "frame.time_epoch",
            "-e", "frame.len",
            "-e", "eth.src",
            "-e", "eth.dst",
            "-e", "ip.src",
            "-e", "ip.dst",
            "-e", "tcp.srcport",
            "-e", "tcp.dstport",
            "-e", "udp.srcport",
            "-e", "udp.dstport",
            "-e", "icmp.type",
            "-e", "icmp.code",
            "-e", "arp.opcode",
            "-e", "arp.src.hw_mac",
            "-e", "arp.src.proto_ipv4",
            "-e", "arp.dst.hw_mac",
            "-e", "arp.dst.proto_ipv4",
            "-e", "ipv6.src",
            "-e", "ipv6.dst",
            "-E", "header=y",
            "-E", "occurrence=f"
        ]
        self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
        self.tsvin = csv.reader(self.process.stdout, delimiter='\t')
        next(self.tsvin, None)  # Başlık satırını atlamak için

    def _get_tshark_path(self):
        if platform.system() == 'Windows':
            possible_paths = [
                'C:\\Program Files\\Wireshark\\tshark.exe',
                'C:\\Program Files (x86)\\Wireshark\\tshark.exe'
                # Tshark'ın kurulu olduğu tam yolunuzu buraya ekleyin
            ]
            for path in possible_paths:
                if os.path.isfile(path):
                    return path
            return ''  # Eğer yukarıdaki yollardan biri bile mevcut değilse, boş string döner
        else:
            system_path = os.environ['PATH']
            for path in system_path.split(os.pathsep):
                filename = os.path.join(path, 'tshark')
                if os.path.isfile(filename):
                    return filename
        return ''

    def get_next_vector(self):
        if self.curPacketIndx == self.limit:
            self.process.terminate()
            return []

        try:
            row = next(self.tsvin)
        except StopIteration:
            return []

        if len(row) == 0:
            return []

        try:
            IPtype = np.nan
            timestamp = float(row[0])
            framelen = int(row[1])
            srcIP = ''
            dstIP = ''
            if row[4] != '':  # IPv4
                srcIP = row[4]
                dstIP = row[5]
                IPtype = 0
            elif row[17] != '':  # ipv6
                srcIP = row[17]
                dstIP = row[18]
                IPtype = 1
            srcproto = row[6] + row[8]  # UDP or TCP port
            dstproto = row[7] + row[9]  # UDP or TCP port
            srcMAC = row[2]
            dstMAC = row[3]
            if srcproto == '':  # L2/L1 level protocol
                if row[12] != '':  # ARP
                    srcproto = 'arp'
                    dstproto = 'arp'
                    srcIP = row[14]  # src IP (ARP)
                    dstIP = row[16]  # dst IP (ARP)
                    IPtype = 0
                elif row[10] != '':  # ICMP
                    srcproto = 'icmp'
                    dstproto = 'icmp'
                    IPtype = 0
                elif srcIP + srcproto + dstIP + dstproto == '':  # other protocol
                    srcIP = row[2]  # src MAC
                    dstIP = row[3]  # dst MAC
        except ValueError as ve:
            print("ValueError:", ve)
            return []

        self.curPacketIndx += 1
        return self.nstat.updateGetStats(IPtype, srcMAC, dstMAC, srcIP, srcproto, dstIP, dstproto, framelen, timestamp)

    def get_num_features(self):
        return len(self.nstat.getNetStatHeaders())
