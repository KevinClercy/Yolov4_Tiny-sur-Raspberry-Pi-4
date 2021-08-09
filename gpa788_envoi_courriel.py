#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''Module pour envoyer un message courriel avec ou sans pièce jointe.

Note: consulter le document "Python sur le Pi (II)" pour connaître le 
      réglage du compte Gmail pour permettre à un client ordinaire
	  d'utiliser les services de Gmail.

Note: L'interface des services Gmail changent de temps à autre. Toujours
      valider auprès de Gmail pour la procédure de communication à utiliser.

T. Wong
GPA788
Jan. 2019
Aut. 2020

Utilisé dans le cadre du PFE2021 par K. Clercy, R. Lupien et M. Le Vergos
Avr. 2021
Aou. 2021
'''

# Pour communiquer avec le server mail
# voir: https://docs.python.org/3/library/smtplib.html
import smtplib
# Pour créer un message MIME multi-section
# Voir: https://docs.python.org/3/library/email.html
from email.mime.multipart import MIMEMultipart  
from email.mime.base import MIMEBase  
from email.mime.text import MIMEText  
from email.mime.image import MIMEImage
from email import encoders
# Pour faire l'extraction du nom du fichier à partir de son chemin
from os.path import basename


# ------------------------------------------------
# Définition de la classe Envoi_Courriel
# ------------------------------------------------
class Envoi_Courriel():
	""" Cette classe offre deux services publics pour l'envoie d'un courriel.

    Send_Txt_Msg: sans pièce jointe
    Send_Txt_Msg_Attachment: avec pièce jointe

    Si verbose = True alors des messages indiquant le progrès des étapes
                 seront envoyés à la sortie standard.

    Avertissement: Toujours gérer les exceptions de smtplib.
	"""

	def __init__(self, server, port, username, passwd, verbose):
		self.verbose = verbose
    
		# Contacter le serveur courriel
		if verbose: print('Contacte le serveur courriel...', end='')
		self.smtpserver = smtplib.SMTP_SSL(server, port)
		if verbose: print('Ok')
		# S'identifier
		self.smtpserver.ehlo()
		# S'authentifier auprès du serveur courriel
		if verbose: print('Authentification auprès serveur courriel...', end='')
		self.smtpserver.login(username, passwd)
		if verbose: print('Ok.')
        
	def _Init_Msg_(self, to, sender, subject):
		''' Initialiser un objet de type MIMEMultipart.

		Arguments:
		to -- adresse courriel du destinataire
		sender -- adresse courriel de l'expéditeur
		subject -- sujet du courriel

		Retour: objet MIMEMultipart dont ces champs sont initialisés.
		'''

		Message = MIMEMultipart()
		Message['Subject'] = subject
		Message['To'] = to
		Message['From'] = sender
		return Message

	def _Init_Msg_Attachment_(self, to, sender, subject, attachment):
		''' Initialiser un objet de type MIMEMultipart avec une pièce jointe.

		Arguments:
		to -- adresse courriel du destinataire
		sender -- adresse courriel de l'expéditeur
		subject -- sujet du courriel
		attachment -- document à joindre (incluant son chemin)

		Retour: objet MIMEMultipart dont ces champs sont initialisés et une pièce jointe.
		'''

		Message = self._Init_Msg_(to, sender, subject)
		part = MIMEBase('application', 'octet-stream')
		part.set_payload(open(attachment, "rb").read())
		encoders.encode_base64(part)
		part.add_header('Content-Disposition', f'attachment; filename={basename(attachment)}')
		Message.attach(part)
		if self.verbose: print('Pièce jointe encodée et jointe au courriel.')
		return Message

	def Send_Txt_Msg(self, to, sender, subject, txtmsg):
		''' Envoyer un message texte.

		Arguments:
		to -- adresse courriel du destinataire
		sender -- adresse courriel de l'expéditeur
		subject -- sujet du courriel
		txtmsg -- chaîne de caractères correspondant au message à envoyer

		Retour: none.
		'''
		if self.verbose: print('Former le message texte et joindre au courriel...', end='')
		Message = self._Init_Msg_(to, sender, subject)
		msg = MIMEText(txtmsg, 'plain')
		Message.attach(msg)
		if self.verbose: print('Ok.')
		if self.verbose: print('Transmettre le courriel au server...', end='')
		self.smtpserver.sendmail(sender, to, Message.as_string())
		if self.verbose: print('Ok.')
		self.smtpserver.close()
		if self.verbose: print('Connexion avec le serveur courriel fermé.')

	def Send_Txt_Msg_Attachment(self, to, sender, subject, txtmsg, attachment):
		''' Envoyer un message texte et une pièce jointe.

		Arguments:
		to -- adresse courriel du destinataire
		sender -- adresse courriel de l'expéditeur
		subject -- sujet du courriel
		txtmsg -- chaîne de caractères correspondant au message à envoyer
		attachment -- document à joindre (incluant son chemin)

		Retour: none.
		'''
		
		if self.verbose: print('Former le message texte et joindre au courriel...', end='')
		Message = self._Init_Msg_(to, sender, subject)
		msg = MIMEText(txtmsg, 'plain')
		Message.attach(msg)
		if self.verbose: print('Ok.')
		if self.verbose: print('Encoder la pièce jointe et la joindre au courriel...', end='')
		# part = MIMEBase('application', 'octet-stream')
		# part.set_payload(open(attachment, "rb").read())
		# encoders.encode_base64(part)
		fp = open(attachment, 'rb')
		part = MIMEImage(fp.read())
		fp.close()
		#part.add_header('Content-Disposition', f'attachment; filename={basename(attachment)}')
		Message.attach(part)
		if self.verbose: print('Ok.')
		if self.verbose: print('Transmettre le courriel au server...', end='')
		self.smtpserver.sendmail(sender, to, Message.as_string())
		if self.verbose: print('Ok.')
		self.smtpserver.close()
		if self.verbose: print('Connexion avec le serveur courriel fermé.')

	def __del__(self):
		''' Destructeur de la classe.

		Détruire l'objet smtp provoquant la fermeture de la connexion.
		'''
		del self.smtpserver
        
# Si le module est exécuté accidentellement comme un programme
if __name__ == '__main__':
	print('<{}>\nest un module et non un programme.'.format(__file__))