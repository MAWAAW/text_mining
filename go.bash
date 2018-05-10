#!/bin/sh

#export CLASSPATH=/Applications/weka/3.8.0/weka-3-8-0/weka.jar
export CLASSPATH=/usr/share/java/weka.jar

echo 'entree python'
python script.py
echo 'sortie python'
# mahmat
#java weka.filters.unsupervised.attribute.StringToWordVector -R first-last -W 1000 -C -c 2 -b -i corpus_tweets_t1_app.arff -o corpus_tweets_t1_app_wordVector.arff -r corpus_tweets_t1_test.arff -s corpus_tweets_t1_test_wordVector.arff

# Prétraitement
echo 'pretraitement...'
java weka.filters.unsupervised.attribute.StringToWordVector -b -i corpus_tweets_t1_app.arff -o corpus_tweets_t1_app_wordVector.arff -r corpus_tweets_t1_test.arff -s corpus_tweets_t1_test_wordVector.arff
#java weka.filters.unsupervised.attribute.StringToWordVector -b -R first-last -W 1000 -prune-rate -1.0 -N 0 -stemmer weka.core.stemmers.NullStemmer -tokenizer weka.core.tokenizers.WordTokenizer -C -c 2 -i corpus_tweets_t1_app.arff -o corpus_tweets_t1_app_wordVector.arff -r corpus_tweets_t1_test.arff -s corpus_tweets_t1_test_wordVector.arff

# Apprentissage NaiveBayes
echo 'app NaiveBayes'
java weka.classifiers.bayes.NaiveBayes -t corpus_tweets_t1_app_wordVector.arff -c first -no-cv -d model_corpus_tweets_t1_appNB >  m2078.T1.run1.txt

# Test NaiveBayes
echo 'test NaiveBayes'
java weka.classifiers.bayes.NaiveBayes -T corpus_tweets_t1_test_wordVector.arff -c first -no-cv -l model_corpus_tweets_t1_appNB > m2078.T1.run1.stat
#java weka.classifiers.bayes.NaiveBayes -T corpus_tweets_t1_test_wordVector.arff -c first -no-cv -l model_corpus_tweets_t1_appNB -p 0 > m2078.T1.run1.res

# Apprentissage J48
echo 'app J48'
java weka.classifiers.trees.J48 -t corpus_tweets_t1_app_wordVector.arff -c first -no-cv -d model_corpus_tweets_t1_appJ48 >  m2078.T1.run2.txt

# Test J48
echo 'test J48'
java weka.classifiers.trees.J48 -T corpus_tweets_t1_test_wordVector.arff -c first -no-cv -l model_corpus_tweets_t1_appJ48 > m2078.T1.run2.stat
#java weka.classifiers.trees.J48 -T corpus_tweets_t1_test_wordVector.arff -c first -no-cv -l model_corpus_tweets_t1_appJ48 -p 0 > m2078.T1.run2.res

# Apprentissage OneR
echo 'app OneR'
java weka.classifiers.rules.OneR -t corpus_tweets_t1_app_wordVector.arff -c first -no-cv -d model_corpus_tweets_t1_app1R >  m2078.T1.run3.txt

# Test OneR
echo 'test OneR'
java weka.classifiers.rules.OneR -T corpus_tweets_t1_test_wordVector.arff -c first -no-cv -l model_corpus_tweets_t1_app1R > m2078.T1.run3.stat
#java weka.classifiers.rules.OneR -T corpus_tweets_t1_test_wordVector.arff -c first -no-cv -l model_corpus_tweets_t1_app1R -p 0 > m2078.T1.run3.res


