# Word-Predictor
Language Engineering Project

## About the project

It consists of a word prediction software, using neural networks and n-gram modeling.

<p align="right">(<a href="#top">back to top</a>)</p>

## Setup

First clone the repository

Download the data : https://d396qusza40orc.cloudfront.net/dsscapstone/dataset/Coursera-SwiftKey.zip

We used en_US.news and en_US.twitter

<p align="right">(<a href="#top">back to top</a>)</p>

## How to run

### Data Preprocessing
Inside the `data/` folder, run the following to preprocess the data (clean the data and split into train/test data): 
```
python DataPreProcess.py -f data_file -tr train_file -t test_file
```

### Neural networks

run the following to manually test the prediction of a model:
```
python RNN.py -ld -lw -news -wp
```
and you will be able to start typing words/sentences. Whenever you press enter, the program will output 3 predictions for the current word, or the next one if your input ends with a whitespace. Input exit if you wish to end the program.
The flags in parentheses are optional and mean:
`-ld`: to load existing model
`-lw`: to use lower-case model
`-news`: to use model trained on news dataset (default is blog post model)

run the following to train an lstm model:
```
python RNN.py -ld -tr -lw -f "train_file" -e number
```
where:
`-f`: path to training file
`-e`: number of epochs (default 5)
`-tr`: train

run the following to evaluate an lstm model:
```
python RNN.py -ld -lw -tf "test_file" -news -ev
```
where:
`-tf`: path to test file

### Trigram model

run the following to build a trigram model file from the raw data:
```
python TrigramTrainer.py -f path/to/data -d path/to/model
```
Optional: add the `-ls` flag to apply laplace smoothing and `-lc` to lowerise the data when processing it.

run to following to run the prediction CLI from a model file:
```
python3 TrigramTester.py -m path/to/model
```
Optional: add `-k path/to/test_data` to compute the proportion of saved keystrokes when running the predictor on test data. 

<p align="right">(<a href="#top">back to top</a>)</p>

