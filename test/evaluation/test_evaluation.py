from io import StringIO
from unittest import TestCase
from unittest.mock import MagicMock, patch

import pandas

from src.openBioLink.evaluation.evaluation import Evaluation
from src.openBioLink.evaluation.metricTypes import ThresholdMetricType, RankMetricType

from src.openBioLink.evaluation.models.model import Model
from src.openBioLink.evaluation.models.pykeen_models import TransR_PyKeen


class TestEvaluation(TestCase):
    @patch("src.openBioLink.evaluation.evaluation.utils.calc_corrupted_triples")
    def test_evaluate(self, mocked_calc_corrupted_triples):
        #given
        ranked_examples_head = pandas.read_csv(StringIO("GO_GO:0000006,PART_OF,GO_GO:0000006,1.922283\n" +
                                                        "GO_GO:0000003,PART_OF,GO_GO:0000006,2.189748\n" +
                                                        "GO_GO:0000002,PART_OF,GO_GO:0000006,3.179066\n" +
                                                        "GO_GO:0000001,PART_OF,GO_GO:0000006,3.620234\n"),
                                               names=['id1', 'edge', 'id2', 'score'])
        sorted_indices_head = [0, 3, 2, 1]

        ranked_examples_head2 = pandas.read_csv(StringIO("GO_GO:0000001,PART_OF,GO_GO:0000002,1.263816\n" +
                                                         "GO_GO:0000002,PART_OF,GO_GO:0000002,2.264960\n" +
                                                         "GO_GO:0000006,PART_OF,GO_GO:0000002,3.537443\n" +
                                                         "GO_GO:0000003,PART_OF,GO_GO:0000002,4.244024\n"),
                                               names=['id1', 'edge', 'id2', 'score'])
        sorted_indices_head2 = [3, 2, 0, 1]

        ranked_examples_tail = pandas.read_csv(StringIO("GO_GO:0000003,PART_OF,GO_GO:0000003,2.264960\n" +
                                                        "GO_GO:0000003,PART_OF,GO_GO:0000002,4.244024\n" +
                                                        "GO_GO:0000003,PART_OF,GO_GO:0000006,4.899477\n" +
                                                        "GO_GO:0000003,PART_OF,GO_GO:0000001,5.633906\n"),
                                               names=['id1', 'edge', 'id2', 'score'])
        sorted_indices_tail = [1, 2, 3, 0]

        ranked_examples_tail2 = pandas.read_csv(StringIO("GO_GO:0000001,PART_OF,GO_GO:0000002,1.263816\n" +
                                                        "GO_GO:0000001,PART_OF,GO_GO:0000003,1.605833\n" +
                                                        "GO_GO:0000001,PART_OF,GO_GO:0000001,2.264960\n" +
                                                        "GO_GO:0000001,PART_OF,GO_GO:0000006,2.484512\n" ),
                                               names=['id1', 'edge', 'id2', 'score'])
        sorted_indices_tail2 = [3, 2, 1, 0]



        examples_head = pandas.read_csv(StringIO("GO_GO:0000006,PART_OF,GO_GO:0000006,0\n" +
                                                 "GO_GO:0000003,PART_OF,GO_GO:0000006,1\n" +
                                                 "GO_GO:0000002,PART_OF,GO_GO:0000006,0\n" +
                                                 "GO_GO:0000001,PART_OF,GO_GO:0000006,0\n"),
                                        names=['id1', 'edge', 'id2', 'value'])

        examples_head2 = pandas.read_csv(StringIO("GO_GO:0000001,PART_OF,GO_GO:0000002,1\n" +
                                                  "GO_GO:0000002,PART_OF,GO_GO:0000002,0\n" +
                                                  "GO_GO:0000006,PART_OF,GO_GO:0000002,0\n" +
                                                  "GO_GO:0000003,PART_OF,GO_GO:0000002,0\n"),
                                        names=['id1', 'edge', 'id2', 'value'])

        examples_tail = pandas.read_csv(StringIO("GO_GO:0000003,PART_OF,GO_GO:0000003,1\n" +
                                                 "GO_GO:0000003,PART_OF,GO_GO:0000002,0\n" +
                                                 "GO_GO:0000003,PART_OF,GO_GO:0000006,1\n" +
                                                 "GO_GO:0000003,PART_OF,GO_GO:0000001,0\n"),
                                        names=['id1', 'edge', 'id2', 'value'])

        examples_tail2 = pandas.read_csv(StringIO("GO_GO:0000001,PART_OF,GO_GO:0000002,1\n" +
                                                  "GO_GO:0000001,PART_OF,GO_GO:0000003,0\n" +
                                                  "GO_GO:0000001,PART_OF,GO_GO:0000001,0\n" +
                                                  "GO_GO:0000001,PART_OF,GO_GO:0000006,0\n" ),
                                        names=['id1', 'edge', 'id2', 'value'])

        corrupted_heads_dict = {('GO_GO:0000003','PART_OF',"GO_GO:0000006"): examples_head,
                                ('GO_GO:0000001','PART_OF','GO_GO:0000002'):examples_head2

        }
        corrupted_tails_dict = {('GO_GO:0000003','PART_OF',"GO_GO:0000006"): examples_tail,
                                ('GO_GO:0000001','PART_OF','GO_GO:0000002'):examples_tail2

        }
        mocked_calc_corrupted_triples.return_value = (corrupted_heads_dict, corrupted_tails_dict)

        test_examples = pandas.concat([examples_head, examples_tail]).reset_index(drop=True)
        ranked_test_examples = pandas.concat([ranked_examples_head, ranked_examples_tail]).reset_index(drop=True)
        sorted_test_indices = sorted_indices_head + [x+len(sorted_indices_head) for x in sorted_indices_tail]

        model = TransR_PyKeen()
        model.get_ranked_predictions = MagicMock(side_effect=lambda x:
            (ranked_examples_head,sorted_indices_head) if x is examples_head
            else (ranked_examples_head2,sorted_indices_head2) if x is examples_head2
            else (ranked_examples_tail,sorted_indices_tail) if x is examples_tail
            else (ranked_examples_tail2,sorted_indices_tail2) if x is examples_tail2
            else (ranked_test_examples,sorted_test_indices) if x is test_examples
            else None
        )
        metrics = [RankMetricType.HITS_AT_K, RankMetricType.HITS_AT_K_UNFILTERED, RankMetricType.MRR, RankMetricType.MRR_UNFILTERED,
                   ThresholdMetricType.ROC, ThresholdMetricType.ROC_AUC, ThresholdMetricType.PR_REC_CURVE, ThresholdMetricType.PR_AUC]

        #when
        e = Evaluation(model, test_set_path='foo2.csv')
        e.test_examples = test_examples
        result = e.evaluate(metrics, nodes_path='foo.csv')

        #then
        assert result is not None