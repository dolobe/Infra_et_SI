# import os
# from datetime import datetime
# import paramiko

# # Chemin du fichier de log
# LOG_FILE = "task_scheduler_log.txt"

# # Fonction pour enregistrer les messages de log
# def log_message(message):
#     with open(LOG_FILE, "a") as log_file:
#         log_file.write(f"{datetime.now()} - {message}\n")

# # Fonction pour exécuter la commande sur la VM
# def execute_command_on_vm(command, password):
#     try:
#         # Établir une connexion SSH
#         ssh_client = paramiko.SSHClient()
#         ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#         ssh_client.connect(hostname='ip_address_of_vm', username='your_username', password=password)

#         # Exécuter la commande
#         stdin, stdout, stderr = ssh_client.exec_command(command)
#         output = stdout.read().decode()
#         error = stderr.read().decode()

#         # Afficher la sortie et les erreurs
#         if output:
#             log_message(f"Output: {output.strip()}")
#         if error:
#             log_message(f"Error: {error.strip()}")

#         # Fermer la connexion SSH
#         ssh_client.close()
#     except Exception as e:
#         log_message(f"Error: {str(e)}")

# # Demander le mot de passe à l'utilisateur
# vm_password = input("Enter the password for VM: ")

# # Définir la commande à exécuter
# commande = "python3 Backup.py"

# # Exécuter la commande sur la VM
# execute_command_on_vm(commande, vm_password)

# # Automatiser la tâche pour s'exécuter tous les jours à 20h40 et répéter toutes les heures
# try:
#     os.system("(crontab -l ; echo '40 20-23 * * * python3 /path/to/script.py') | crontab -")
#     log_message("Tâche ajoutée à crontab avec succès !")
# except Exception as e:
#     log_message(f"Erreur lors de l'ajout de la tâche à crontab : {str(e)}")

import os
import subprocess
from datetime import datetime

# Définir les chemins et paramètres
SOURCE_DIR = "test.txt"
DEST_DIR = "rakotondrasoa@192.168.48.131:/home/rakotondrasoa/Infra_et_SI/Backup/"
LOG_FILE = "file.log"

# Générer le nom de fichier de destination avec la date et l'heure actuelles
now = datetime.now()
timestamp = now.strftime("%d-%m-%Y_%H%M%S")
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
