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

app = Flask(__name__)

@app.route('/')
def index():
    app.logger.info('Accès à la page d\'accueil')
    return render_template('index.html')

@app.route('/restore', methods=['POST'])
def restore():
    app.logger.info('Tentative de restauration')

    # Récupérer le nom du fichier à restaurer à partir du formulaire
    filename = request.form['filename']
    
    # Définir les chemins de source et de destination pour la restauration
    remote_backup_file = f"rakotondrasoa@192.168.48.131:/home/rakotondrasoa/Infra_et_SI/Backup/{filename}"
    local_restore_path = f"./restored_{filename}"

    # Transférer le fichier spécifié du serveur distant vers le chemin local
    scp_command = f"scp {remote_backup_file} {local_restore_path}"
    result = subprocess.run(scp_command, shell=True, capture_output=True, text=True)

    # Vérifiez si le transfert a été réussi
    if result.returncode == 0:
        app.logger.info(f'Restauration du fichier {filename} réussie')
        return f'Restauration du fichier {filename} réussie'
    else:
        app.logger.error(f'Échec de la restauration du fichier {filename} : {result.stderr}')
        return f'Échec de la restauration du fichier {filename} : {result.stderr}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
