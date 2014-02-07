# this is classification function
import orange, orngTree
######################
# import for svm:
from Orange.classification import svm
from Orange.evaluation import testing, scoring
######################
# For Confusion matrix:
import orngTest, orngStat
######################
import Orange
train_data = orange.ExampleTable("classification.tab") 
test_data = orange.ExampleTable("testing.tab")
bayes = orange.BayesLearner(train_data)
tree = orngTree.TreeLearner(train_data)
knnLearner = orange.kNNLearner(train_data)
knnLearner.k = 10 # k == 18 seems to be best (at least for 2-3)
    #   svm2 = svm.SVMLearner()
bayes.name = "bayes:"
tree.name = "tree:"
knnLearner.name = "knn:"
classifiers= [bayes, tree, knnLearner]

def classification():
    
    
    #classifier = orange.BayesLearner(train_data)
    c=''
    for i in range(len(test_data)):
        c0 = classifiers[0](test_data[i])
        
        c1 = classifiers[1](test_data[i])
        #print c1
        c2 = classifiers[2](test_data[i])
        #print c2
    #print c0, c1, c2
        c = c + bayes.name+str(c0)+'\t'+tree.name+str(c1)+'\t'+knnLearner.name+str(c2)+'\t'+str(i)+'\n'
    #print c        
    return c
    
classification()
    
def accuracy():
    correct = [0.0]*len(classifiers)
    for ex in test_data:
        for i in range(len(classifiers)):
            if classifiers[i](ex) == ex.getclass():
                correct[i] += 1
    for i in range(len(correct)):
        correct[i] = correct[i] / len(test_data)
    print correct
    return correct
#classCount =5
def accuracy2(test_data, classifiers, classCount):
    correct = [0.0]*len(classifiers)
    classes = []
    # now, find all classes in the set.
    counter = 0
    for ex in train_data:
        found = 'nothing'
        for j in range(counter):
            if ex.getclass() == classes[j]:
                found = 'found'
        if found == 'nothing':
            counter += 1
            classes.append(ex.getclass())
    # initialise confusion matrix
    confusionMatrix = [0]*classCount*classCount # this is a concatenation of 'classCount' arrays of size 'classCount' to represent the respective entries in the confusion matrix.
    # Problem still: I have to have all classes in order to identify which one was predicted for which.
    # The diagonal is easy, but what about the other entries?
    # Find all classes and put them in a matrix
    # other solution: provide the class count as a parameter
        # now fill confusion matrix
    for ex in test_data:
        truth = 'nothing'
        predicted = 'nothing'
        firstIndex=0
        secondIndex=0
        for j in range(counter):
            if ex.getclass() == classes[j]:
                truth = classes[j]
                firstIndex=j
            if classifiers[0](ex) == classes[j]:
                predicted = classes[j]
                secondIndex=j
        # fill the matrix
        confusionMatrix[firstIndex*classCount+secondIndex] +=1
    print confusionMatrix
    return confusionMatrix

def evaluating():
    bayes2 = orange.BayesLearner()
    tree2 = orngTree.TreeLearner()
    knnLearner2 = orange.kNNLearner()
    knnLearner2.k = 10 # k == 18 seems to be best (at least for 2-3)
    #svm2 = svm.SVMLearner()
    bayes2.name = "bayes2"
    tree2.name = "tree2"
    knnLearner2.name = "knn2"
    learners = [bayes2, tree2, knnLearner2]

    results = orngTest.crossValidation(learners, train_data, folds=10)
    print "train_data:"
    print train_data
    print "k=="
    print knnLearner2.k
    print 'Learner  CA     IS     Brier    AUC'
    c = ''
    for i in range(len(learners)):
        print "%-8s %5.3f  %5.3f  %5.3f  %5.3f" % (learners[i].name, \
            orngStat.CA(results)[i], orngStat.IS(results)[i],
            orngStat.BrierScore(results)[i], orngStat.AUC(results)[i])
        c = c+str("%-8s"%learners[i].name)+'\t'+ str("%5.3f" %orngStat.CA(results)[i])+'\t'+ str("%5.3f" %orngStat.IS(results)[i])+'\t'+str("%5.3f" %orngStat.BrierScore(results)[i])+'\t'+str("%5.3f" %orngStat.AUC(results)[i]+'\n')
    return (c)
