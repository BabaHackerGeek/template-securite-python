import json

from scapy.all import ARP, IP, TCP, Ether, Raw, wrpcap

from src.tp1.main import analyser, main


def test_port_scan(tmp_path):
    paquets = []
    for port in range(1, 21):
        paquets.append(Ether() / IP(src="10.0.0.5", dst="10.0.0.1") / TCP(dport=port, flags="S"))
    fichier = str(tmp_path / "test.pcap")
    wrpcap(fichier, paquets)

    rapport = analyser(fichier)

    assert {"type": "port_scan", "attacker": "10.0.0.5"} in rapport["attacks"]


def test_flag_et_injection_sql(tmp_path):
    vrai = Ether() / IP(src="10.0.0.7", dst="10.0.0.1") / TCP() / Raw(
        b"GET /?id=1' OR 1=1 token=ESGI{vrai} HTTP/1.1\r\n\r\n"
    )
    leurre = Ether() / IP(src="10.0.0.9", dst="10.0.0.1") / TCP() / Raw(
        b"GET /?t=ESGI{leurre} HTTP/1.1\r\n\r\n"
    )
    fichier = str(tmp_path / "test.pcap")
    wrpcap(fichier, [leurre, vrai])

    rapport = analyser(fichier)

    assert {"type": "sql_injection", "attacker": "10.0.0.7"} in rapport["attacks"]
    assert rapport["flag"] == "ESGI{vrai}"


def test_arp_spoofing(tmp_path):
    attaquant = "aa:aa:aa:aa:aa:aa"
    routeur = "bb:bb:bb:bb:bb:bb"
    paquets = [Ether() / ARP(op=2, psrc="10.0.0.1", hwsrc=routeur, pdst="10.0.0.2")]
    for _ in range(3):
        paquets.append(Ether() / ARP(op=2, psrc="10.0.0.1", hwsrc=attaquant, pdst="10.0.0.2"))
    fichier = str(tmp_path / "test.pcap")
    wrpcap(fichier, paquets)

    rapport = analyser(fichier)

    assert {"type": "arp_spoofing", "attacker": attaquant} in rapport["attacks"]


def test_main(tmp_path, monkeypatch):
    pcap = str(tmp_path / "test.pcap")
    sortie = tmp_path / "rapport.json"
    wrpcap(pcap, [Ether() / IP(src="10.0.0.5", dst="10.0.0.1") / TCP()])
    monkeypatch.setattr("sys.argv", ["tp1", "--pcap", pcap, "--out", str(sortie)])

    main()

    contenu = json.loads(sortie.read_text())
    assert "protocols" in contenu