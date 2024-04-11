import argparse
import pickle
import csv
from typing import Mapping, List, Any

from catboost.core import CatBoostClassifier

from shark_atplab import settings
from shark_atplab.core.alf_scoring import get_google_distance_score
from shark_atplab.core.utils import read_fasta_file, form_sequence_pairs
from shark_atplab.dive.run import run_normal, run_sparse


class Prediction:
    def __init__(self, q_sequence_id_map: Mapping[str, str], t_sequence_id_map: Mapping[str, str]):
        """
        Either of the two parameters should have a value

        :param(dict[str, str]) q_sequence_id_map: Key -> Sequence ID; Value -> Sequence
        :param(dict[str, str]) t_sequence_id_map: Key -> Sequence ID; Value -> Sequence
        """
        self._pred_models = self.load_model()
        _id_seq_pair = form_sequence_pairs(q_sequence_id_map, t_sequence_id_map)
        self.unique_sequence_pairs: list = list(_id_seq_pair.values())

    @staticmethod
    def load_model() -> List[CatBoostClassifier]:
        """Load model from pickled file obj whose path should be available in environment"""
        with open(settings.DIVE_MODEL_PKL_PATH, mode='rb') as fp:
            models_pkl_loaded = pickle.load(fp)
        if not isinstance(models_pkl_loaded, list) and len(models_pkl_loaded) == 10:
            raise Exception('The model object should be a list of 10 CatBoostClassifier')
        for model in models_pkl_loaded:
            if not isinstance(model, CatBoostClassifier):
                raise Exception('The models should be CatBoostClassifier')
        return models_pkl_loaded

    @staticmethod
    def compute_input_vector(sequence1: str, sequence2: str) -> List[float]:
        """
        Compute input feature set for a given sequence pair

        :return(list): Similarity scores for k from 1 to 10 in ascending order
            To be used as input vector
        """
        k_mer__threshold_map = {5: 0.95, 6: 0.9, 7: 0.9, 8: 0.85, 9: 0.85, 10: 0.85}
        similarity_scores_k = []
        for k in range(1, 11):
            if k == 1:
                similarity_score = run_sparse(sequence1, sequence2, k)
            elif k in [2, 3, 4]:
                similarity_score = get_google_distance_score(sequence1, sequence2, k)
            else:
                similarity_score = run_normal(sequence1, sequence2, k, k_mer__threshold_map[k])
            similarity_scores_k.append(similarity_score)
        return similarity_scores_k

    def _predict_pairwise(self, similarity_scores_k: List[float]) -> float:
        """
        Similarity prediction for a pair of sequence
        Given a list of k-wise similarity score of two sequences; predict the likelihood of similar/non-similar

        :param(list of float) similarity_scores_k: Similarity scores for a sequence pair
        :return(list of float): Final likelihood of similarity
        """
        if len(similarity_scores_k) != 10:
            raise Exception('Input vector hash-map for prediction should be of size 10')
        sim_probabilities = []
        for model in self._pred_models:
            pred_proba = model.predict_proba(similarity_scores_k)
            sim_probabilities.append(pred_proba[1])
        sim_pred_proba = round(sum(sim_probabilities) / len(sim_probabilities), settings.ROUND_OFF_DP)
        return sim_pred_proba

    def predict(self) -> List[Mapping[str, Any]]:
        """
        Similarity prediction for all unique pairs of sequence
        Make pair-wise prediction (similar/non-similar) after computing feature vector across k-lengths

        :return(list of dict[str, Any]): Each dict obj in the list corresponds to one unique pair.
            Keys -> 'seq_id1', 'sequence1', 'seq_id2', 'sequence2' : all string values
                'similarity_scores_k' : List of float scores
                'pred_proba' : float
        """
        output = []
        for unique_pair in self.unique_sequence_pairs:
            pairwise_out_data = unique_pair.copy()
            pairwise_out_data['similarity_scores_k'] = self.compute_input_vector(unique_pair['sequence1'],
                                                                                 unique_pair['sequence2'])
            pairwise_out_data['pred_proba'] = self._predict_pairwise(pairwise_out_data['similarity_scores_k'])
            output.append(pairwise_out_data)
        return output


def run_prediction_for_sequences(query_fasta_file: str, target_fasta_file: str):
    """
    Read a list of sequences from a fasta file and output results in CSV format
    CSV Column Headers:
        1. "Query": Sequence from Query list
        2. "Target": Sequence from Target list
        5..14: "SHARK-Score (k=*)": Similarity score between the two sequences for specific k-value
        15. "SHARK-Dive": Aggregated similarity score over all lengths of k-mer

    :param(str) query_fasta_file: Absolute path to first sequence fasta file
    :param(str) target_fasta_file: Absolute path to second sequence fasta file
    """
    id_sequence_map1 = read_fasta_file(file_path=query_fasta_file)
    id_sequence_map2 = read_fasta_file(file_path=target_fasta_file)

    predictor = Prediction(id_sequence_map1, id_sequence_map2)
    output = predictor.predict()
    file_out_path = "{}/shark_dive_predict_out__{}_{}.csv".format(settings.DATA_DIR,
                                                                  query_fasta_file.split('/')[-1],
                                                                  target_fasta_file.split('/')[-1])
    with open(file=file_out_path, mode='w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        headers = ['Query', 'Target']
        headers.extend(['SHARK-Score (k={})'.format(k) for k in range(1, 11)])
        headers.append('SHARK-Dive')
        csv_writer.writerow(headers)
        for sequence_pair_result in output:
            csv_row = [
                sequence_pair_result['seq_id1'],
                sequence_pair_result['seq_id2'],

            ]
            csv_row.extend(sequence_pair_result['similarity_scores_k'])
            csv_row.append(sequence_pair_result['pred_proba'])
            csv_writer.writerow(csv_row)
    print("Output stored at {}".format(file_out_path))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='DIVE-Predict: Given some query sequences, '
                                                 'compute their similarity from the list of target sequences;'
                                                 'Target is supposed to be major database of protein sequences')
    parser.add_argument('query', help='Absolute path to fasta file for the query set of input sequences', type=str)
    parser.add_argument('target', help='Absolute path to fasta file for the target set of input sequences', type=str)
    args = parser.parse_args()
    run_prediction_for_sequences(args.query, args.target)
