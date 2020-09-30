from langdetect import detect
import preprocessor as p
from copy import deepcopy
import emoji
import string
import re

punct = string.punctuation
pattern1 = '^[!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~\s\b\n\t“”«»🏻🇫🇷🇨🇭🇪🇸.‍‘]+$'
pattern2 = '^[A-Z0-9a-z]+/[A-Z0-9a-z]+$'
tweet_sc = ['$URL$', '$MENTION$', '$HASHTAG$', '$RESERVED$',
            '$EMOJI$', '$SMILEY$', '$NUMBER$']
LANG_TYPE = ['und', 'en', 'fr', 'it', 'es', 'oth']


class Prediction_Engine:
    def __init__(self):
        return None

    def predict(self, dataset):

        for discussion in dataset:
            if 'predicted_ground_truth' in discussion:
                idx = [item['post_id'] for item
                       in discussion['predicted_ground_truth']]
            else:
                idx = [item['post_id'] for item in discussion['ground_truth']]

            predictions = []
            for id, i in enumerate(idx):
                temp_pred = {'post_id': i, 'consensus': {}}

                temp_pred['consensus']['tokens'] =\
                    self.calculate_tokens(discussion, i, id)

                temp_pred['consensus']['postFullSentence'] =\
                    self.calculate_full_sentence(discussion, i)

                temp_pred['consensus']['postOpposes'] =\
                    self.calculate_opposes(discussion, i)

                temp_pred['consensus']['postProvidesAdditionalInfo'] =\
                    self.calculate_additional_info(discussion, i)

                temp_pred['consensus']['postQuestions'] =\
                    self.calculate_questions(discussion, i)

                temp_pred['consensus']['postSupports'] =\
                    self.calculate_post_support(discussion, i)

                temp_pred['consensus']['relevance'] =\
                    self.calculate_relevance(discussion, i)

                predictions.append(temp_pred)

            discussion['predicted_ground_truth'] = predictions

        return dataset

    def calculate_full_sentence(self, discussion, i):
        # majority Baseline
        return True

    def calculate_relevance(self, discussion, i):
        # majority Baseline
        return 5

    def calculate_opposes(self, discussion, i):
        # majority Baseline
        return False

    def calculate_additional_info(self, discussion, i):
        # majority Baseline
        return True

    def calculate_questions(self, discussion, i):
        # majority Baseline
        if '?' in discussion['discussion']['discussion'][i-1]['text']:
            return True
        return False

    def calculate_post_support(self, discussion, i):
        # majority Baseline
        return False

    # partial language detection
    def calculate_tokens(self, discussion, i, id=None):
        text = deepcopy(discussion['discussion']['discussion'][i-1]['text'])
        text = text.strip()

        text_splits = text.split(' ')
        tokenized_text = p.tokenize(text)
        tok_text_splits = tokenized_text.split(' ')
        size = len(text_splits)

        assert len(tok_text_splits) == len(text_splits)

        predicted_labels = []
        for index, item in enumerate(tok_text_splits):
            for tweet_word in tweet_sc:
                item = item.replace(tweet_word, '.')
                item = self.extract_emojis(item)

            if re.match(pattern1, item) or re.match(pattern2, item) \
                    or text_splits[index] == '️':
                predicted_labels.append({'lang': 'und',
                                         'word': text_splits[index]})
            else:
                window_size = 10
                temp_str = ' '.join([text_splits[k] for k in range(
                    max(index-window_size, 0), min(size, index+window_size))])
                try:
                    lang_label = detect(temp_str)
                    if lang_label not in LANG_TYPE:
                        lang_label = 'oth'
                except:
                    # print('Error Cannot Detect', temp_str)
                    lang_label = 'oth'
                predicted_labels.append({'lang': lang_label,
                                         'word': text_splits[index]})
        return predicted_labels

    def extract_emojis(self, line):
        mod_line = ''
        for c in line:
            if c in emoji.UNICODE_EMOJI:
                mod_line += '.'
            else:
                mod_line += c
        return mod_line
