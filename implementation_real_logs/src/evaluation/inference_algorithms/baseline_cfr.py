"""
this script takes as input the LSTM or RNN weights found by train.py
change the path in the shared_variables.py to point to the h5 file
with LSTM or RNN weights generated by train.py
The script is expanded to also use the Resource attribute
"""

from __future__ import division
import csv
from pathlib import Path

import pandas as pd
from jellyfish import damerau_levenshtein_distance
import distance
from tensorflow import keras

from src.commons.log_utils import LogData
from src.commons.utils import extract_trace_sequences
from src.evaluation.prepare_data import get_predictions
from src.training.train_common import CustomTransformer


def run_experiments(log_data: LogData, compliant_traces: pd.DataFrame, maxlen, predict_size, char_indices,
                    target_char_indices, target_indices_char, char_indices_group, target_char_indices_group,
                    target_indices_char_group, model_file: Path, output_file: Path):
    # Load model, set this to the model generated by train.py
    model = keras.models.load_model(model_file, custom_objects={'CustomTransformer': CustomTransformer})

    with open(output_file, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(["Prefix length", "Ground truth", "Predicted", "Damerau-Levenshtein", "Jaccard",
                             "Ground Truth Group", "Predicted Group", "Damerau-Levenshtein Resource",
                             "Ground truth outcome", "Predicted outcome", "Outcome diff."])

    for prefix_size in range(log_data.evaluation_prefix_start, log_data.evaluation_prefix_end+1):
        print("Prefix size: " + str(prefix_size))

        for trace_name, trace in compliant_traces.groupby(log_data.case_name_key):
            lines, lines_group, outcomes = extract_trace_sequences(log_data, [trace_name])
            line = lines[0]
            line_group = lines_group[0]
            outcome = outcomes[0]

            if len(line) < prefix_size:
                continue  # Make no prediction for this case, since this case has ended already

            cropped_line = ''.join(line[: prefix_size])
            cropped_line_group = ''.join(line_group[: prefix_size])

            ground_truth = ''.join(line[prefix_size: prefix_size+predict_size])
            ground_truth_group = ''.join(line_group[prefix_size: prefix_size+predict_size])
            ground_truth_o = outcome

            predicted = ''
            predicted_group = ''
            predicted_outcome = ''

            for i in range(predict_size - prefix_size):
                enc = encode_with_group(cropped_line, cropped_line_group, maxlen, char_indices, char_indices_group)
                y = model.predict(enc, verbose=0)  # make predictions
                # split predictions into separate activity, resource and outcome predictions
                y_char = y[0][0]
                y_group = y[1][0]
                y_o = y[2][0][0]

                # undo one-hot encoding
                prediction, prediction_group = get_predictions(cropped_line, cropped_line_group, y_char, y_group,
                                                               target_indices_char, target_char_indices,
                                                               target_indices_char_group, target_char_indices_group)
                predicted_outcome = '1' if y_o >= 0.5 else '0'

                if prediction == '!':
                    # end of case was just predicted, therefore, stop predicting further into the future
                    break

                cropped_line += prediction
                cropped_line_group += prediction_group
                predicted += prediction
                predicted_group += prediction_group

            output = []
            if len(ground_truth) > 0:
                output.append(prefix_size)
                output.append(ground_truth)
                output.append(predicted)
                dls = 1 - \
                    (damerau_levenshtein_distance(predicted, ground_truth) / max(len(predicted), len(ground_truth)))
                if dls < 0:
                    dls = 0
                output.append(dls)
                output.append(1 - distance.jaccard(predicted, ground_truth))

                output.append(ground_truth_group)
                output.append(predicted_group)
                dls_res = 1 - \
                    (damerau_levenshtein_distance(predicted_group, ground_truth_group)
                     / max(len(predicted_group), len(ground_truth_group)))
                if dls_res < 0:
                    dls_res = 0
                output.append(dls_res)

                output.append(ground_truth_o)
                output.append(predicted_outcome)
                output.append('1' if ground_truth_o == predicted_outcome else '0')

            if output:
                with open(output_file, 'a', newline='') as csvfile:
                    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    spamwriter.writerow(output)
