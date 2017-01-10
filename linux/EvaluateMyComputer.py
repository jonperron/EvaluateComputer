#!/usr/bin/env python3
# coding: utf8

"""Outil d'évaluation pour ordinateur/connexion"""

import platform, subprocess
from urllib import request,parse

__author__ = "Jonathan Perron"
__version__ = "0.5"
__maintainer__ = "Jonathan Perron"
__email__ = "contact@jonathanperron.fr"

print("Outil d'évaluation ordinateur/connexion")

# User info


class User:
    """
    Contient tous les infos de l'animatrice
    """
    def __init__(self,last_name="",first_name="",email=""):
        self.last_name = last_name
        self.first_name = first_name
        self.email = email

    def get_info(self):
        self.last_name = input('Nom : ')
        self.first_name = input('Prénom : ')
        self.email = input('Adresse e-mail : ')

    def __str__(self):
        return "Vos informations : {} - {} - {}".format(self.last_name,self.first_name,self.email)

# Computer info


class Computer:

    """
    Contient toutes les infos de l'ordinateur
    """

    def __init__(self,fab_processor="",ram="",operating_system="",operating_system_version="",\
                 computer_model="",computer_brand="",webcam=""):
        self.fab_processor = fab_processor
        self.ram = ram
        self.operating_system = operating_system
        self.operating_system_version = operating_system_version
        self.computer_model = computer_model
        self.computer_brand = computer_brand
        self.webcam = webcam

    def get_info(self):
        self.operating_system = platform.system()
        if self.operating_system == "Linux":
            self.operating_system = platform.linux_distribution()[0]
            self.operating_system_version = platform.linux_distribution()[1]
        elif self.operating_system == "Windows":
            self.operating_system_version = platform.win32_ver()[0]
        elif self.operating_system == "Darwin":
            self.operating_system_version = platform.mac_ver()[0]

        if platform.system() == "Linux":
            with open('/proc/cpuinfo') as f:
                for line in f:
                    if line.strip() and line.rstrip('\n').startswith('model name'):
                        self.fab_processor = line.rstrip('\n').split(':')[1]

            with open('/proc/meminfo') as f:
                for line in f:
                    if line.strip() and line.rstrip('\n').startswith('MemTotal'):
                        ram = line.rstrip('\n').split(':')[1]
                        self.ram = str(round(int(ram.split()[0]) / (1024*1024),0)) + " GB"

            with open('/sys/devices/virtual/dmi/id/sys_vendor') as f:
                for line in f:
                    self.computer_brand = line.split()[0]

            with open('/sys/devices/virtual/dmi/id/product_name') as f:
                for line in f:
                    self.computer_model = line.split()[0]

            output = subprocess.check_output("/sbin/udevadm info --export-db", shell=True).strip()
            output = output.decode("utf-8")
            for line in output.split('\n'):
                if 'ID_MODEL_FROM_DATABASE' in line and ('cam' in line or 'CAM' in line):
                    self.webcam = line.split('=')[1]

    def __str__(self):
        return "Votre ordinateur : \n"\
                "----- Système ----- \n"\
                "Système : {} \n"\
                "Version : {} \n"\
                "----- Ordinateur ----- \n"\
                "Modèle : {} \n"\
                "Fabricant : {} \n"\
                "Processeur : {} \n"\
                "RAM : {} \n"\
                "Webcam : {} \n".format(self.operating_system,self.operating_system_version,\
                                               self.computer_model,self.computer_brand,self.fab_processor,\
                                               self.ram,self.webcam)


# Speedtest info


class Speedtest:

    def __init__(self,server="",download_speed="",upload_speed=""):
        self.server = server
        self.download_speed = download_speed
        self.upload_speed = upload_speed

    def get_info(self):
        output = subprocess.check_output('speedtest-cli',shell=True).strip()
        output = output.decode("utf-8")
        for line in output.split('\n'):
            if 'Hosted by' in line:
                self.server = line.split('by ')[1]

            if 'Download' in line:
                self.download_speed = line.split(':')[1]

            if "Upload" in line:
                self.upload_speed = line.split(':')[1]

    def __str__(self):
        return "Votre connexion : \n"\
                "Server speedtest : {} \n"\
                "Download speed : {} \n"\
                "Upload speed : {} \n".format(self.server,self.download_speed,self.upload_speed)

# Main function


def main():

    user = Model()
    user.get_info()
    print(model)
    print()
    computer = Computer()
    computer.get_info()
    print(computer)
    print()
    connexion = Speedtest()
    connexion.get_info()
    print(connexion)
    input("Appuyez sur Entrée pour continuer...")
    data = parse.urlencode({"first_name":model.first_name,
                            "last_name": model.last_name,
                            "email": model.email,
                            "operating_system": computer.operating_system,
                            "operating_system_version": computer.operating_system_version,
                            "computer_model": computer.computer_model,
                            "computer_brand": computer.computer_brand,
                            "fab_processor": computer.fab_processor,
                            "ram": computer.ram,
                            "webcam": computer.webcam,
                            "server": connexion.server,
                            "download_speed": connexion.download_speed,
                            "upload_speed": connexion.upload_speed,
                            }).encode("utf-8")


if __name__ == '__main__':
    main()
