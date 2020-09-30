from subprocess import call

DATAFILE_PATH = 'temp/'


class CRF:
    def __init__(self):
        return None

    def preprocess_dataset(self, dataset, filename):
        '''
        TODO as the task in hand
        '''
        f = open(DATAFILE_PATH + filename, 'w')

        for discussion in dataset:
            if filename == 'train.data':
                ground_truths = discussion['ground_truth']
            predicted_val = discussion['predicted_ground_truth']

            for i, item in enumerate(predicted_val):
                if filename == 'train.data':
                    assert item['post_id'] == ground_truths[i]['post_id']

                    for pred_word, word in\
                            zip(item['consensus']['tokens'],
                                ground_truths[i]['consensus']['tokens']):

                        assert word['word'] == pred_word['word']
                        f.write(' '.join([word['word'], pred_word['lang'],
                                          word['lang']]) + '\n')
                else:
                    for pred_word in item['consensus']['tokens']:
                        f.write(' '.join([pred_word['word'],
                                          pred_word['lang']]) + '\n')
                f.write('\n')
        f.close()

    def postprocess_data(self, dataset, filename):
        '''
        TODO as the task in hand
        '''
        f = open(DATAFILE_PATH + filename, 'r')

        for discussion in dataset:
            predicted_val = discussion['predicted_ground_truth']

            for item in predicted_val:
                for word in item['consensus']['tokens']:
                    splits = f.readline().strip().split('\t')
                    assert word['word'] == splits[0]
                    word['lang'] = splits[-1]
                f.readline()
        return dataset

    def train_crf(self):
        c = 150  # emphirically that found 150 works better

        command = 'CRF++.58/crf_learn  -c ' + \
            str(c) + ' temp/template temp/train.data temp/model'
        call(command, shell=True)

    def test_crf(self):
        command = 'CRF++.58/crf_test -m temp/model temp/test.data >\
                   temp/results_test.data'
        call(command, shell=True)

    def rm_crf(self):
        command = 'rm -rf temp/model'
        call(command, shell=True)

    def train_and_predict(self, training_dataset, testing_dataset):
        self.preprocess_dataset(training_dataset, 'train.data')
        self.preprocess_dataset(testing_dataset, 'test.data')
        self.train_crf()
        self.test_crf()
        testing_dataset = self.postprocess_data(testing_dataset,
                                                'results_test.data')
        return testing_dataset

    def predict(self, testing_dataset):
        self.preprocess_dataset(testing_dataset, 'test.data')
        self.test_crf()
        testing_dataset = self.postprocess_data(testing_dataset,
                                                'results_test.data')
        return testing_dataset


if __name__ == '__main__':
    dataset1 = read_data('data/Dataset1.json')
    dataset2 = read_data('data/Dataset2.json')
    preprocess_dataset(dataset1+dataset2, 'train.data')

    test_dataset = read_data('data/TestData1.json')
    preprocess_dataset(test_dataset, 'test.data')
