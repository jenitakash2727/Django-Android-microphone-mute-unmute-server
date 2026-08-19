from scapy.all import ARP, Ether, srp

target_ip = "192.168.0.1"

packet = (
    Ether(dst="ff:ff:ff:ff:ff:ff")
    / ARP(pdst=target_ip)
)

print("Scanning:", target_ip)

result = srp(
    packet,
    timeout=5,
    verbose=1
)[0]

print("Responses:", len(result))

for sent, received in result:
    print("IP :", received.psrc)
    print("MAC:", received.hwsrc)