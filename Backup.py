# import os
# import subprocess
# from datetime import datetime

# # Définir les chemins et paramètres
# SOURCE_DIR = "test.txt"
# DEST_DIR = "rakotondrasoa@192.168.48.131:/home/rakotondrasoa/Infra_et_SI/Backup/"
# LOG_FILE = "file.log"

# # Test de l'existence du fichier source
# if os.path.isfile(SOURCE_DIR):
#     # Commande scp pour transférer le fichier
#     try:
#         subprocess.run(["scp", SOURCE_DIR, DEST_DIR], check=True)
#         with open(LOG_FILE, "a") as log_file:
#             log_file.write(f"{datetime.now()} - Transfert terminé avec succès.\n")
#     except subprocess.CalledProcessError:
#         with open(LOG_FILE, "a") as log_file:
#             log_file.write(f"{datetime.now()} - Erreur lors du transfert.\n")
#             exit(1)
# else:
#     with open(LOG_FILE, "a") as log_file:
#         log_file.write(f"{datetime.now()} - Le fichier source {SOURCE_DIR} n'existe pas.\n")
#         exit(1)

import os
import subprocess
from datetime import datetime

# Définir les chemins et paramètres
SOURCE_DIR = "test.txt"
DEST_DIR = "rakotondrasoa@192.168.48.131:/home/rakotondrasoa/Infra_et_SI/Backup/"
LOG_FILE = "file.log"

# Générer le nom de fichier de destination avec la date et l'heure actuelles
now = datetime.now()
timestamp = now.strftime("%d-%m-%Y_%H:%M:%S")
dest_filename = f"test_{timestamp}.txt"
dest_path = os.path.join(DEST_DIR, dest_filename)

# Test de l'existence du fichier source
if os.path.isfile(SOURCE_DIR):
    # Commande scp pour transférer le fichier
    try:
        subprocess.run(["scp", SOURCE_DIR, dest_path], check=True)
        with open(LOG_FILE, "a") as log_file:
            log_file.write(f"{datetime.now()} - Transfert terminé avec succès. Fichier transféré: {dest_filename}\n")
    except subprocess.CalledProcessError:
        with open(LOG_FILE, "a") as log_file:
            log_file.write(f"{datetime.now()} - Erreur lors du transfert.\n")
            exit(1)
else:
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"{datetime.now()} - Le fichier source {SOURCE_DIR} n'existe pas.\n")
        exit(1)
