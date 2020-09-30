# Understanding Multilingual Communities through Analysis of Code-switching Behaviors in Social Media Discussions

This is the [winning submission](https://rapid.cis.unimelb.edu.au/BigDataChallenge/Board.html) of "Understanding Multilingual Communities through Analysis of Code-switching Behaviors in Social Media Discussions", one of the BigData Cup Challenges at IEEE BigData 2019. Please see the [competition webpage](https://rapid.cis.unimelb.edu.au/BigDataChallenge/index.html) to learn more about the challenge.

## Requirements
You need the open-source implementation of Conditional Random Fields (CRFs) in CRF++ to run this model. Please follow the instructions in https://taku910.github.io/crfpp/ to install CRF++.

To install other requirements:
```shell
pip install -r requirements.txt
```
## Dataset
This competition releases three labelled datasets and two unlabeled test datasets, which are included in data/. To learn more about the format of the datasets, please see the [competition webpage](https://rapid.cis.unimelb.edu.au/BigDataChallenge/Tasks.html). 

## Model
Our model initially detects word-level language labels for multilingual social media discussions by using a CRF-based fine-tuning technique on top of the weak language labels predicted using langdetect library as depicted follows. Then, the model adopts a rule-based approach to identify code-switching behaviour in multilingual social media discussions. Please see the paper titled "Understanding Multilingual Communities through Analysis of Code-switching Behaviors in Social Media Discussions" to learn more details about the model.

## Training and Prediction
To train the model and predict the labels for testing instances:
```shell
cat [PATH TO TEST DATASET] | python program.py
```
This command reads all three labelled datasets in data/ and trains the model. Then, the labels are predicted for the provided test dataset and store the test dataset with the predicted labels under the data/Predicted_Results.json file.

## Evaluation
To evaluate the predicted results:
```shell
cat [PATH TO PREDICTED DATASET] | python score.py
```
Please note that you cannot evaluate the test datasets  (data/TestData1.json and data/TestData2.json) as they don't have the ground truth labels.

## Citation
If you have found this code beneficial to your research, please consider cite the following paper:
```
@inproceedings{harwood2019understanding,
  title={Understanding Multilingual Communities through Analysis of Code-switching Behaviors in Social Media Discussions},
  author={Harwood, Aaron and Karunasekera, Shanika and Vanni, Michelle and Falzon, Lucia and Padia, Prarthana and Silva, Amila},
  booktitle={2019 IEEE International Conference on Big Data (Big Data)},
  pages={2274--2283},
  year={2019},
  organization={IEEE}
}
```
