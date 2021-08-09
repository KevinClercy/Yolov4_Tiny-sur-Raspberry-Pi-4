'''
Auteur T. Wong
GPA788
Jan. 2019
Aut. 2020

Révisé par Kévin Clercy 
PFE2021
Avr. 2021
Aou. 2021
'''
# ------------------------------------------------
# Paramètres du serveur Gmail, l'adresse courriel
# de l'envoi et du destinataire, le mot de passe,
# le sujet, le texte, le chemin et le nom du
# fichier image à joindre au courriel.
# ------------------------------------------------
server = 'smtp.gmail.com'
port = 465
sender = 'xxxxxxxxx@gmail.com'  # 'ton.nomg@gmail.com'
password = 'mdpApplication'     # 'ton mot de passe' voir https://support.google.com/accounts/answer/185833 pour obtenir un mot de passe d’application
to = "destinataire@xxx.com"     # "Adresse couriel du destinataire"  
to_sms = "514000000@xxxxx.com"  # "NumCellulaire@SMSGateway.com" Voir https://en.wikipedia.org/wiki/SMS_gateway pour optenir le gateway de votre opérateur télephonique
subject = 'Alerte : Couteau'    # Sujet du courriel
msg = "Attention : Il y a un couteau dans la pièce" # Message dans le courriel
msg_sms = "Attention : Il y a un couteau dans la pièce. Voir l\'emplacement sur votre couriel a l\'adresse : " + to # Message dans le sms avec redirection vers le courriel pour la pièe jointe
path = '/home/pi/...'           # Chemin du dossier contenet le programme
attachment = path + 'knife_pos.png' # Définition de la pièce jointe

    