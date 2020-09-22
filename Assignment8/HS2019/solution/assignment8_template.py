# -*- coding: utf-8 -*-
"""4af1df28fedc5707576d0dd50c98728f.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17na1r0CWYL3EQE2ophlZVMm2jOsJQ_1o
"""

grading = False

from copy import deepcopy

import pandas as pd
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC, LinearSVC
from sklearn.model_selection import GridSearchCV, train_test_split

def load_questions():
    """
    Task 1a)

    Load the questions and their classes.

    Complete the following steps:
      - load the file "train_5500.label.txt" with "ISO-8859-1" encoding
      - read the lines of the file
      - consider only the lines that start with "LOC:city" or "HUM:ind"
      - create a list in the following format:
        [ (text, class), ... ]
      - "text" is the content of the line AFTER the label
         LOC:city What is the name of the city that Maurizio Pellegrin lives in ?
        For this line the content would be: "What is the name of the city that Maurizio Pellegrin lives in ?"
      - class is based on the label: "CITY" for "LOC:city" and "HUMAN" for "HUM:ind"
        For the example above this would be "CITY"
      - keep only the first 128 lines with class "HUMAN" (labelled as "HUM:ind")
      - keep all samples for "CITY"
      - return the list in the format described above
    
    INPUT:
      - no input
    OUTPUT:
      - texts: a list of tuples
        Each tuple should represent ONE (1) line from the text file "train_5500.label.txt"
        The first element in the tuple is the the question part of the line.
        That means everything after the label.
        Example:
          Consider this line from the text file:
            HUM:ind Name the scar-faced bounty hunter of The Old West .
          To your output list you have to add this tuple:
            ("Name the scar-faced bounty hunter of The Old West .", "HUM:ind")
                          ^ the text of the question                    ^ class
    """
    texts = []

    f = open("train_5500.label.txt", mode="r", encoding="ISO-8859-1")
    lines = f.readlines()

    hum_count = 0

    for line in lines:
      line = line.split(" ")
      if "LOC:city" == line[0]:
        text = " ".join(line[1:])
        tpl = (text, "CITY")
        texts.append(tpl)
      elif "HUM:ind" == line[0] and hum_count < 128:
        text = " ".join(line[1:])
        tpl = (str(text), "HUMAN")
        hum_count += 1
        texts.append(tpl)
      
    f.close()

    ### YOUR CODE HERE ###
    return texts

if not grading:
    # you need to import this before you can use it
    from collections import Counter
    # this is the function you must implement in task 1a)
    texts = load_questions()
    # this counts how often the second element (accessed with x[1]) appears
    # this means it counts how often each class appears in your dataset
    count = Counter(x[1] for x in texts)
    # the "CITY" class should appear 129 times, the "HUMAN" class should appear 128 times
    print(count)
    # Counter({'CITY': 129, 'HUMAN': 128})

def build_dataframe_q(texts):
    """
    Task 1b)

    Process the texts and create a DataFrame you can use for training a classifier.

    Complete the following steps:
      - load the spacy model "en_core_web_sm"
      - for each text, create a spacy doc object
      - for each token in this doc object, do:
        - if the token begins an entity, keep the entity type
        - elif the token is outside an entity, and not a stopword, keep token.text
        - if the token is a stopword, continue
        - keep token.text
          (if the token is outside an entity then this means you keep token.text twice)
        - you can find everything you need here: https://spacy.io/api/token
        - create a dictionary for the current document in this format:
          {
            "text": list of the tokens joined with whitespace (use " ".join(tokens)),
            "class": the class of the text,
          }
        - store this dictionary, for each document, in a list
        - create a new dataframe where each row is represented by one of the
         document dictionaries
        - return this dataframe

    vvvvvvvvvvvvvvvvvvvv
    To check whether or not a token is inside an entity, you can use this code.
    You need to put in a for-loop. This for-loop must iterate over each
    token in a text.

      t = []
      if token.ent_iob == 3:
          t.append(token.ent_type_)
      elif token.ent_iob == 2 and not token.is_stop:
          t.append(token.text)
      # if token is not a stopword, then use "continue" here
      # if the token is NOT a stopword, add it to your list "t"

    "token" comes from a spaCy Document object. Refer to the spaCy documentation
    or the lecture slides to see how to process the tokens in a text with
    spaCy.
    You also need to check if a token is a stopword. If it is a stopword, use
    the "continue" keyword to go to the next token in your for-loop.
    After you have processed all tokens for the current text, combine them 
    together from a list of strings (your "t" list) to a string.
    vvvvvvvvvvvvvvvvvvvv

    INPUT:
      - texts: The list of texts that you get from your task 1a) function.
        You need to pre-process the texts. In this case, that means that you have to
        remove stopwords.
    OUTPUT:
      - df: A DataFrame, where each row represents one text / question from the "texts"
        list that you get as a function argument.
    PSEUDOCODE:
      This is not actual code but it describes what your function will have to do.
      If you translate this "fake" code into Python then your function is correct.
    ```
    rows = []
    nlp = load spacy model
    for text, class in texts:
        doc = make spaCy document object out of "text"
        t = []
        for token in doc:
            if token.ent_iob == 3:
                t.append(token.ent_type_)
            elif token.ent_iob == 2 and not token.is_stop:
                t.append(token.text)
            if token is a stopword:
                continue
            append "token.text" to the list "t"
        t = " ".join(t)
        text_information = dictionary that has the keys "text" and "class" that maps to the joined together string (t) and the class of the text (from the for loop)
        append "text_information" to the list "rows"
    df = a DataFrame that contains the content of the "rows" list as actual DataFrame rows
    return df
    ```
    """
    rows = []

  

    nlp = spacy.load("en_core_web_sm")
    for text in texts:
      #Why text[0] (what is text???)
      doc = nlp(text[0])
      tokens = []
      dct = {}

      #Recheck if all if conditions are right according to what they write in comments!è!!!!!!
      for token in doc:
        if token.ent_iob == 3:
          tokens.append(token.ent_type_)
        elif token.ent_iob == 2 and not token.is_stop:
          tokens.append(token.text)
        elif token.is_stop:
          continue
        tokens.append(token.text)

      dct["text"] = " ".join(tokens)
      dct["class"] = text[1]
      rows.append(dct)



  
    ### YOUR CODE HERE ###
    df = pd.DataFrame(rows)
    return df

if not grading:
    texts = load_questions()
    df = build_dataframe_q(texts)
    print(df.iloc[10])
    # text        city city oldest oldest relationship relations...
    # class                                                    CITY
    # Name: 10, dtype: object
    print("----")
    print(df.iloc[100])
    # text        FAC McCarren Airport located located city city...
    # class                                                    CITY
    # Name: 100, dtype: object
    print("----")
    print(df.iloc[123])
    # text        graced graced airwaves airwaves pearls pearls ...
    # class                                                   HUMAN
    # Name: 123, dtype: object

def create_train_test_set(df, train_size, test_size, random_state=42):
    """
    Task 1c)

    Split a DataFrame into training and test set.
    Use a method from scikit-learn to accomplish this.

    !!! You need to import this scikit-learn method! !!!

    vvvvvvvvvvvvvvvvvvvv
    You can find the correct function in lecture slides or with Google!
    vvvvvvvvvvvvvvvvvvvv


    Specify the train_size, test_size and random_state of this scikit-learn method
    to use the values passed into this function.

    INPUT:
      - df: The DataFrame that was created by your "build_dataframe_q" function.
      - train_size: The size of your training set, between 0 and 1. 0.6 for example
        means that you use 60% of your data for the training set.
      - test_size: The size of your test set, between 0 and 1. 0.4 for example
        means that you use 60% of your data for the test set.
      - random_state: This is an optional parameter that you need to use in the 
        scikit-learn method that helps you split your data into training and test set.
    OUTPUT:
      - X_train: The texts that are going to be used for training.
      - X_test: The texts that are going to be used for validation.
      - y_train: The correct labels/classes of the texts in X_train.
      - y_test: The correct labels/classes of the texts in X_test.
    PSEUDOCODE:
      Find and import the correct method from scikit-learn. The required method
      lets you split your data into training and test set. You can find it in the
      official scikit-learn documentation or in the lecture slides.
    ```
    from sklearn.model_selection import name_of_the_function
    X = the "text" column of "df" (the first function argument)
    y = the "class" column of "df"
    X_train, X_test, y_train, y_test = name_of_the_function(X, y, 
        train_size=train_size, 
        test_size=test_size, 
        random_state=random_state)
    return X_train, X_test, y_train, y_test
    ```
    """

    X_train, X_test, y_train, y_test = train_test_split(df['text'], df['class'], train_size=train_size, test_size=test_size, random_state=random_state)

    ### YOUR CODE HERE ###
    return X_train, X_test, y_train, y_test

if not grading:
    # your "create_train_test_set" function is called here
    texts = load_questions()
    df = build_dataframe_q(texts)
    X_train, X_test, y_train, y_test = create_train_test_set(df, 0.6, 0.4)
    print(len(X_train))
    print(len(X_test))
    print(len(y_train))
    print(len(y_test))
    # 154
    # 103
    # 154
    # 103

def gridsearch(clf, parameters, X, y):
    """
    Task 1d)

    Perform a gridsearch for a given classifier, data and parameters.
    Print the best parameters and also return them.

    The parameters of this function are the same ones you can pass directly into
    the scikit-learn GridSearchCV: 
    https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html

    INPUT:
      - clf: A classifier object. For example, this could be "PassiveAggressiveClassifier()"
      - parameters: A dictionary containing the paramaters that you use in the gridsearch.
        You have to read the documentation of the classifier to find what parameters exist for it!
        EXAMPLE:
          parameters = {
            "C": [x/10 for x in range(0, 11)],
            "fit_intercept": [True, False],
            "max_iter": [x*1000 for x in range(1, 4)],
            "shuffle": [False],
            "random_state": [42],
            "tol": [0.0001, 0.001, 0.01, 0.1],
          }
      - X: The training data
      - y: The correct labels/classes of the training data
    OUTPUT:
      - clf.best_params_: The best parameters, as found by the gridsearch, as a dictionary.
    PSEUDOCODE:
    ```
    clf = GridSearchCV(clf, parameters)
    train "clf" by giving it training_data (function argument "X") and training data labels (function argument "Y") Training GridSearchCV works exactly like training a classifier!
    print(clf.best_params_)   <-- these are the parameters that you have to use in task 2!
    return clf.best_params_
    ```
    """

    clf.fit(X,y)
    grid_search = GridSearchCV(estimator=clf, param_grid=parameters, cv=10)
    grid_search = grid_search.fit(X, y)

    best_param = dict(grid_search.best_params_)
    print(best_param)
    
    return best_param

def evaluate_classifier(true_labels, predictions):
    """
    Task 1e)

    true_labels = The class labels of your test set.
    predictions = The predicted labels, predictions made by your classifier.

    Evaluate how good the predictions of a classifier are.
    "true_labels" are the correct class labels, "predictions" is what the
    classifier predicted.

    You have to call this method in your "train_classifier" method (task 1f)!

    INPUT:
      - true_labels: The correct classes/labels of your test set
      - predictions: The predictions that your classifier has made
    OUTPUT:
      - accuracy: The accuracy classification score
      - precision: The precision (weighted)
      - recall: The recall (weighted)
      - f1: The F1-measure (weighted)
    PSEUDOCODE:
    ```
    accuracy = calculate accuracy using the correct method
    precision = calculate precision using the correct method
    recall = calculate recall using the correct method
    f1 = calculate f1 using the correct method
    return accuracy, precision, recall, f1
    ```
    EXTRA HINT:
      The functions you need are already imported - look near the top of
      this notebook file to find their names!
    
      --> Use "weighted" for the "average" argument in the evaluation methods! <--
      If you don't know what this means, refer to the lecture slides or read the
      documentation of the functions!
    """
    accuracy = accuracy_score(y_true=true_labels, y_pred=predictions)
  
    precision = precision_score(y_true=true_labels, y_pred=predictions, average='weighted')
  
    recall = recall_score(y_true=true_labels, y_pred=predictions, average='weighted')
    f1 = f1_score(y_true=true_labels, y_pred=predictions, average='weighted')


    return accuracy, precision, recall, f1

def train_classifier(df, clf, do_gridsearch=False, parameters=None):
    """
    Task 1f)

    Train and evaluate a classifier.

    - Split the data (df) into training and test set, using your
      "create_train_test_set" method.
      Use a 60:40 training:test split.
    - create a vectorizer object. You can find vectorizers here:
      https://scikit-learn.org/stable/modules/classes.html#module-sklearn.feature_extraction.text
      Pick one that you think is suitable. If you are unsure, pick any one of 
      them and evaluate your classifier. Then replace the vectorizer (change
      your code to use a different vectorizer and run the cell again) 
      and see how the results change.
      The task should be solvable with any of the vectorizers, but some of them
      are better suited for this task than others.
    - transform your training data using the .fit_transform() method of
      the vectorizer (read the scikit-learn documentation of your vectorizer
      to see how to call this method)
    - use the .fit method of the classifier to train your classifier
      Example here:
      https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.PassiveAggressiveClassifier.html#sklearn.linear_model.PassiveAggressiveClassifier.fit
    - get the predictions for your test data using clf.predict()
      HINT: There is something you need to do with your test data beforehand.
            You had to do the same thing with your training data before you could
            use the .fit method..
    - calculate accuracy, precision, recall and f1-measure of your classifier
      based on the predictions of your test set and the vectorizer
      Use your "evaluate_classifier" method for this.
      Return these values in the format (accuracy, precision, recall, f1, vectorizer)

    INPUT:
      - df: The DataFrame as it was created by your "build_dataframe_q" function
      - clf: A classifier object. See for example task 2a) what it looks like
      - do_gridsearch: An optional parameter that is set to "False" by default.
        If it is set to "True" then you need to call your "gridsearch" method
        and perform a gridsearch for the current classifier.
      - parameters: An optional parameter. If "do_gridsearch" is set to "True"
        then you need to pass this into your "gridsearch" function.
    OUTPUT:
      - accuracy: The accuracy of the classifier's performance
      - precision: The precision of the classifier's performance
      - recall: The recall of the classifier's performance
      - f1: The F1-measure of your classifier's performance
      - vectorizer: The vectorizer used
    PSEUDOCODE:
    ```
    # create_train_test_set is the function you implemented for 1c)
    X_train, X_test, y_train, y_test = create_train_test_set(df, 0.6, 0.4)
    # remove the index, the following two lines ensure you have only text data
    X_train = X_train["text"]
    X_test = X_test["text]
    vectorizer = create a vectorizer. Pick any vectorizer that you like. Refer to the lecture slides to find which vectorizers exist. Experiment with different vectorizers by changing your code to use a different one.
    X_train = vectorize "X_train" using "vectorizer". Refer to the lecture slides if you are unsure how to do this.
    if do_gridsearch:
        gridsearch(clf, parameters, X_train, y_train)
    train your classifier with "X_train" and "y_train" If you are unsure how to do this, refer to the lecture slides.
    X_test = vectorize "X_test" using "vectorizer". !! Ensure to use the correct method for transforming test data. !!
    predictions = clf.predict(X_test)
    # this uses your "evaluate_classifier" function that you did for the previous task
    accuracy, precision, recall, f1 = evaluate_classifier(y_test, predictions)
    return accuracy, precision, recall, f1, vectorizer
    ```
    """

    X_train, X_test, y_train, y_test = create_train_test_set(df, 0.6, 0.4)



    #X_train = X_train["text"]
    #X_test = X_test["text"]
    X_train = X_train.to_list()
    X_test = X_test.to_list()
  
    vectorizer = TfidfVectorizer()
    X_train = vectorizer.fit_transform(X_train)
    if do_gridsearch==True:
      best_param = gridsearch(clf, parameters, X_train, y_train)

      #We could even set the best parameters here if we wanted to!
      #clf.set_params(**best_param)
  
    clf.fit(X_train, y_train)
  
    y_test_predicted = clf.predict(vectorizer.transform(X_test))
    accuracy, precision, recall, f1 = evaluate_classifier(y_test, y_test_predicted)

    return accuracy, precision, recall, f1, vectorizer

"""# For task 2 all you have to do is find optimized parameters for the classifiers.
For example in task 2a):


```
  clf = PassiveAggressiveClassifier(random_state=42)
```


You need to CHANGE THIS LINE. You have to provide optional parameters! For example:

```
  clf = PassiveAggressiveClassifier(random_state=42, C=3)
```
We know that "PassiveAggressiveClassifier" has this parameter "C" because of the documentation:

https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.PassiveAggressiveClassifier.html

You can find examples of how to use GridSearchCV in the lecture or here:

https://scikit-learn.org/stable/auto_examples/model_selection/plot_grid_search_digits.html
"""

def build_pa(df):
    """
    Task 2a)

    https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.PassiveAggressiveClassifier.html
    Train a PassiveAggressiveClassifier on the provided data.
    Accuracy, precision, recall and f1-measure should all be above 96%.

    Optimize the classifier parameters so the result of your "train_classifier" fucntion are all above 96%.

    HINT: Perform a gridsearch to find optimized parameters to improve your classifier.
    
    :return: accuracy, precision, recall, f1, vectorizer
    """
    #clf = PassiveAggressiveClassifier(random_state=42)
    #Optimized classifier

    # Instead of setting the parameters here we could also set them after the gridsearch directly.
    clf = PassiveAggressiveClassifier(C=0.3 , fit_intercept=True , max_iter=1000 , shuffle=True , random_state=10 , tol=0.0001)


    #Parameters for grid search
    params = {"C": [x/10 for x in range(0, 11)],
            "fit_intercept": [True, False],
            "max_iter": [x*1000 for x in range(1, 4)],
            "shuffle": [True, False],
            "random_state": [42, 10],
            "tol": [0.0001, 0.001, 0.01, 0.1]}

    accuracy, precision, recall, f1, v = train_classifier(df, clf, do_gridsearch=False, parameters=params)
    print(accuracy, precision, recall, f1)
    pred = clf.predict(v.transform(["Who is Ghandi?"]))
    print(pred)
    return accuracy, precision, recall, f1, v

if not grading:
    q = load_questions()
    df = build_dataframe_q(q)
    accuracy, precision, recall, f1, v = build_pa(df)
    print(accuracy, precision, recall, f1)

def build_mnb(df):
    """
    Task 2b)

    https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.MultinomialNB.html 
    Train an MultinomialNB classifier on the provided data.
    Accuracy, precision, recall and f1-measure should all be above 79%.

    Optimize the classifier parameters so the result of your "train_classifier" fucntion are all above 79%.

    HINT: Perform a gridsearch to find optimized parameters to improve your classifier.

    :return: accuracy, precision, recall, f1, vectorizer
    """
    #clf = MultinomialNB()

    #Optimized classifier
    clf = MultinomialNB(alpha=0.1, class_prior= [0.1, 0.9], fit_prior=False)

    params = {'alpha': [0.1,1], 'fit_prior': [False, True], 'class_prior':[[0.1,0.9],[0.6,0.4],[0.9,0.1]]}
    accuracy, precision, recall, f1, v = train_classifier(df, clf, do_gridsearch=False, parameters=params)
    print(accuracy, precision, recall, f1)
    pred = clf.predict(v.transform(["Who is Ghandi?"]))
    print(pred)
    return accuracy, precision, recall, f1, v

if not grading:
    q = load_questions()
    df = build_dataframe_q(q)
    accuracy, precision, recall, f1, v = build_mnb(df)
    print(accuracy, precision, recall, f1)

def build_svc(df):
    """
    Task 2c)

    https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html  Train an SVC on the provided data.
    Accuracy, precision, recall and f1-measure should all be above 96%.

    Optimize the classifier parameters so the result of your "train_classifier" fucntion are all above 96%.

    HINT: Perform a gridsearch to find optimized parameters to improve your classifier.

    :return: accuracy, precision, recall, f1, vectorizer
    """
    #clf = SVC()

    #Optimized Classifier
    clf = SVC(C=1, kernel='linear')

    params = [{'C': [1,100, 1000], 'kernel':['linear']},{'C': [1,100, 1000], 'kernel':['rbf'], 'gamma': [0.1,0.2,0.3,0.4,0.5,0.6,0.7]}]
  

    accuracy, precision, recall, f1, v = train_classifier(df, clf, do_gridsearch=False, parameters= params)
    print(accuracy, precision, recall, f1)
    pred = clf.predict(v.transform(["Who is Ghandi?"]))
    print(pred)
    return accuracy, precision, recall, f1, v

if not grading:
    q = load_questions()
    df = build_dataframe_q(q)
    accuracy, precision, recall, f1, v = build_svc(df)
    print(accuracy, precision, recall, f1)