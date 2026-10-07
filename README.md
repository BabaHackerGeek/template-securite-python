# Template code Sécurité Python
 
## Description
 
Projet contenant les modèles de TP pour le cours de sécurité Python de 4e année de l'ESGI.
 
## Installation
 
Faire un fork puis un clone du projet :
 
```bash
git clone git@github.com:<VotreNom>/template-securite-python.git
```
 
Installer les dépendances :
 
```bash
cd template-securite-python
poetry lock
poetry install
```
 
## Utilisation
 
Lancer le projet :
 
```bash
poetry run tp1 --pcap capture.pcap --out report.json
```
 
## TP1 : IDS/IPS maison
 
Analyseur de capture réseau (PCAP) en Python avec Scapy. Il parcourt tous les
paquets, compte les protocoles, cherche 3 types d'attaques (Scan de ports, Injection SQL, ARP Spoofing) et le flag
`ESGI{...}`, puis écrit le résultat dans un fichier `report.json`.
 
Options :
 
- `--pcap` : le fichier de capture à analyser (nécessaire et obligatoire)
- `--out` : le fichier JSON où écrire le rapport (par défaut `report.json`)
### Ce que l'outil détecte
 
**Protocoles** : Ethernet, ARP, IP, TCP, UDP, ICMP, DNS et HTTP. Chaque couche
présente dans un paquet est comptée, donc un paquet TCP compte aussi pour IP
et Ethernet.
 
**Scan de ports** : on regarde les paquets TCP avec uniquement le flag SYN.
Pour chaque IP source, on garde dans un set les ports de destination
différents. À partir de 15 ports distincts, on considère que c'est un scan.
Le seuil de 15 n'a rien d'universel, je l'ai choisi pour ce TP : je le considère assez haut pour
ne pas "accuser" une machine qui utilise quelques services juste comme ca, mais assez bas pour
détecter le scan de la capture.
 
**Injection SQL** : les données des paquets sont décodées (URL decode), puis on
cherche des motifs comme `' OR 1=1`, `UNION SELECT` ou `sleep(` qui sont des classiques en injection SQL.
 
**ARP spoofing** : on regarde les réponses ARP et on note, pour chaque IP, les
adresses MAC qui la revendiquent. Normalement une IP a une seule et unique adresse MAC. Si
plusieurs MAC annoncent la même IP, c'est un indice clair de très probable spoofing. L'attaquant est la MAC
qui a envoyé le plus de réponses ARP.
 
**Flag** : la capture contient plusieurs flags dont des leurres. On les range
par IP source et on garde celui envoyé par une IP détectée en injection SQL.
 
### Format du rapport
 
```json
{
  "protocols": { "TCP": 95, "ARP": 20 },
  "attacks": [
    { "type": "port_scan", "attacker": "192.168.6.66" }
  ],
  "flag": "ESGI{...}"
}
```
 
### Limites
 
- Le seuil de 15 ports peut rater un scan lent ou très discret.
- Le choix de l'attaquant ARP (celui qui envoie le plus de réponses) est une
  règle simple, qui pourrait se tromper si l'attaquant envoyait peu de réponses.
- Le flag est choisi selon l'IP qui fait l'injection SQL : si le vrai flag
  venait d'un autre attaquant, il ne serait pas retrouvé.
- Seul le HTTP en clair est analysé.