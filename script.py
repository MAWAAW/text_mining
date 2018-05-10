#!/usr/bin/env python2.7
# coding: utf8
from __future__ import division
import os
import random
import subprocess
import re

os.environ["LIA_TAGG"]="/usr/local/lia_tagg"
os.environ["LIA_TAGG_LANG"]="french"

#path = "/info/projets/fouilles_donnees_m2/deft/"
path = "/home/moha/Bureau/text_mining/"

# En-tête au format arff pour weka
head = '''@relation corpus_tweets_t1
@attribute text string
@attribute opinion {+,-,=}
@data\n'''

# Creation de nos fichiers train et test
fichierArffApp = open("corpus_tweets_t1_app.arff","w")
fichierArffApp.write(head)
fichierArffTest = open("corpus_tweets_t1_test.arff","w")
fichierArffTest.write(head)

# Preparation pour Nettoyage / Normalisation des donnees
fstoplist = open("stoplist.txt","r")
words = fstoplist.readlines()
fstoplist.close()
stoplist = []
for word in words:
	stoplist.append(word.lower().rstrip('\n'))

# Preparation pour Selection / Enrichissement des donnees
fcsv = open('polarimots_1.csv', 'r')
opinions = fcsv.readlines()
fcsv.close()
neutre = []
pos = []
neg = []
for opinion in opinions:
	mot = ''.join(opinion.rstrip('\n').split(',')[0])
	op = ''.join(opinion.rstrip('\n').split(',')[1])
	if op=='NEUTRE':
		neutre.append(mot)
	elif op=='POS':
		pos.append(mot)
	else:
		neg.append(mot)

# Récupération des tweets
fichierRef = open(os.path.join(path,"Train_References/T1.txt"))
lignes = fichierRef.readlines()
fichierRef.close()

cpt = 0
for ligne in lignes:

	num_tweet, opinion = ligne.split("\t")

	if os.path.isfile(os.path.join(path,"Train_Data/"+num_tweet+".txt")):
		tweet = open(os.path.join(path,"Train_Data/"+num_tweet+".txt"))

		# Suppression des mots de la stoplist
		tweetlist = [x for x in tweet.read().rstrip('\n').lower().split(' ') if x not in stoplist]

		# Remplacement de mots par leurs polarites et enrichissement via leurs fréquences
		p=0
		n=0
		for i in range(len(tweetlist)):
			if tweetlist[i] in neutre:
				tweetlist[i]='NEUTRE'
			if tweetlist[i] in pos:
				tweetlist[i]='POS'
				p+=1
			if tweetlist[i] in neg:
				tweetlist[i]='NEG'
				n+=1
		if p/len(tweetlist) > n/len(tweetlist):
			res = 'POSITIVE_OPINION'
		else:
			res = 'NEGATIVE_OPINION'
		tweet_processed = ' '.join(tweetlist)

		# Pré-traitement obligatoire pour weka
		tweet_processed.replace('"','').replace(',','')

		# Représenation des urls, des pseudos et des hashtags
		tweet_processed = re.sub(r'http\S+', 'URL', tweet_processed)
		tweet_processed = re.sub(r'@\S+', 'PSEUDO', tweet_processed)
		tweet_processed = re.sub(r'#\S+', 'HASHTAG', tweet_processed)

		# Suppression de tous caractères ennuyeux et inutiles
		tweet_processed = re.sub(r'[^\sa-zA-Z]|_', '', tweet_processed)

		# LIA_TAGG
		proc = subprocess.Popen("echo {} | $LIA_TAGG/script/lia_clean | $LIA_TAGG/bin/lia_rm_ponct".format(tweet_processed), stdout=subprocess.PIPE, shell=True)
		(out, err) = proc.communicate()
		if err is None:
			tweet_processed = out.replace('\n',' ')
			# Separation en 70% train et 30% test
			r = random.random()
			if r<0.7:
				fichierArffApp.write('"'+tweet_processed+'", '+opinion)
			else:
				fichierArffTest.write('"'+tweet_processed+'", '+opinion)
		else:
			print 'Erreur avec lia_tagg: '+err
		
		'''
		if cpt>=9:
			break
		'''
		cpt+=1

# On ferme nos fichiers arff crée
fichierArffApp.close()
fichierArffTest.close()
