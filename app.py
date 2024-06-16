# from flask import Flask, render_template, request
# from datetime import datetime
# import subprocess

# app = Flask(__name__)

# @app.route('/')
# def index():
#     app.logger.info('Accès à la page d\'accueil')
#     return render_template('index.html')

# @app.route('/restore', methods=['POST'])
# def restore():
#     app.logger.info('Tentative de restauration')
    
#     # Récupérer la date et l'heure actuelles
#     backup_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
#     # Écrire la date de sauvegarde dans un fichier temporaire
#     with open('backup_date.txt', 'w') as f:
#         f.write(backup_date)
#     app.logger.info(f'Date de sauvegarde écrite dans le fichier backup_date.txt : {backup_date}')
    
#     # Transférer le fichier contenant la date de sauvegarde via SCP
#     scp_command = f"scp backup_date.txt rakotondrasoa@192.168.48.131:/home/rakotondrasoa/Infra_et_SI/Backup/"
#     subprocess.run(scp_command, shell=True)
#     app.logger.info('Fichier backup_date.txt transféré via SCP')
    
#     # Commande SSH pour lire la date de sauvegarde à partir du fichier
#     ssh_command = "ssh rakotondrasoa@192.168.48.131 'cat /home/rakotondrasoa/Infra_et_SI/Backup/backup_date.txt'"
    
#     # Exécutez la commande à distance et récupérez la date de sauvegarde
#     result = subprocess.run(ssh_command, shell=True, capture_output=True, text=True)
    
#     # Vérifiez si la commande a été exécutée avec succès
#     if result.returncode == 0:
#         remote_backup_date = result.stdout.strip()
#         app.logger.info(f'Restauration démarrée avec succès. Date de sauvegarde : {remote_backup_date}')
#         return f'Restauration démarrée avec succès. Date de sauvegarde : {remote_backup_date}'
#     else:
#         error_message = f'Échec de la restauration : {result.stderr}'
#         app.logger.error(error_message)
#         return error_message

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)

from flask import Flask, render_template, request
import subprocess
import re

app = Flask(__name__)

@app.route('/')
def index():
    app.logger.info('Accès à la page d\'accueil')
    return render_template('index.html')

@app.route('/restore', methods=['POST'])
def restore():
    app.logger.info('Tentative de restauration')

    # Récupérer le motif à partir du formulaire
    pattern = request.form['pattern']
    
    # Définir le chemin du répertoire de sauvegarde distant
    remote_backup_dir = "/home/rakotondrasoa/Infra_et_SI/Backup/"

    try:
        # Exécuter une commande pour lister les fichiers dans le répertoire de sauvegarde distant
        result = subprocess.run(f"ssh rakotondrasoa@192.168.48.131 ls {remote_backup_dir}", shell=True, capture_output=True, text=True)
        app.logger.debug(f'Commande exécutée : {result.args}')
        file_list = result.stdout.split('\n')
        app.logger.debug(f'Fichiers dans le répertoire de sauvegarde : {file_list}')
        
        # Filtrer les fichiers correspondant au motif entré par l'utilisateur
        matching_files = [file for file in file_list if re.search(pattern, file)]
        app.logger.debug(f'Fichiers correspondants : {matching_files}')

        # Si aucun fichier correspondant n'est trouvé
        if not matching_files:
            app.logger.error(f'Aucun fichier trouvé correspondant au motif : {pattern}')
            return f'Aucun fichier trouvé correspondant au motif : {pattern}'

        # Récupérer le premier fichier correspondant trouvé
        filename = matching_files[0]

        # Définir les chemins de source et de destination pour la restauration
        remote_backup_file = f"rakotondrasoa@192.168.48.131:{remote_backup_dir}{filename}"
        local_restore_path = f"C:/Users/rakot/OneDrive/Bureau/Infra_et_SI/Restore/{filename}"

        # Transférer le fichier spécifié du serveur distant vers le chemin local
        scp_command = f"scp {remote_backup_file} {local_restore_path}"
        result = subprocess.run(scp_command, shell=True, capture_output=True, text=True)

        # Vérifier si le transfert a été réussi
        if result.returncode == 0:
            app.logger.info(f'Restauration du fichier {filename} réussie')
            return f'Restauration du fichier {filename} réussie'
        else:
            app.logger.error(f'Échec de la restauration du fichier {filename} : {result.stderr}')
            return f'Échec de la restauration du fichier {filename} : {result.stderr}'

    except Exception as e:
        app.logger.error(f'Erreur lors de la restauration : {e}')
        return f'Erreur lors de la restauration : {e}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

