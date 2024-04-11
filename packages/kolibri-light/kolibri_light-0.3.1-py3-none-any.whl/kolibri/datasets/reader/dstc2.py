# Copyright 2017 Neural Networks and Deep Learning lab, MIPT
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, softwaredata
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import copy
import json
from logging import getLogger
from pathlib import Path
from typing import Dict, List

from overrides import overrides

from kolibri.datasets.reader import DatasetReader
from kdmt.download import download_decompress

log = getLogger(__name__)

class DSTC2DatasetReader(DatasetReader):
    """
    Contains labelled dialogs from Dialog State Tracking Challenge 2
    (http://camdial.org/~mh521/dstc/).

    There've been made the following modifications to the original dataset:

       1. added api calls to restaurant database

          - example: ``{"text": "api_call area=\"south\" food=\"dontcare\"
            pricerange=\"cheap\"", "dialog_acts": ["api_call"]}``.

       2. new actions

          - bot dialog actions were concatenated into one action
            (example: ``{"dialog_acts": ["ask", "request"]}`` ->
            ``{"dialog_acts": ["ask_request"]}``)

          - if a slot key was associated with the dialog action, the new act
            was a concatenation of an act and a slot key (example:
            ``{"dialog_acts": ["ask"], "slot_vals": ["area"]}`` ->
            ``{"dialog_acts": ["ask_area"]}``)

       3. new train/dev/test split

          - original dstc2 consisted of three different MDP policies, the original
            train and dev datasets (consisting of two policies) were merged and
            randomly split into train/dev/test

       4. minor fixes

          - fixed several dialogs, where actions were wrongly annotated
          - uppercased first letter of bot responses
          - unified punctuation for bot responses
    """

    url = 'https://www.dropbox.com/s/73ewq2iyr3twh7z/dstc2_v2.tar.gz?dl=1'

    @staticmethod
    def _data_fname(datatype):
        assert datatype in ('trn', 'val', 'tst'), "wrong datatype name"
        return f"dstc2-{datatype}.jsonlist"

    @overrides
    def read(self, data_path: str, dialogs: bool = False) -> Dict[str, List]:
        """
        Downloads ``'dstc2_v2.tar.gz'`` archive from ipavlov internal server,
        decompresses and saves files to ``data_path``.

        Parameters:
            data_path: path to save DSTC2 dataset
            dialogs: flag which indicates whether to output list of turns or
             list of dialogs

        Returns:
            dictionary that contains ``'train'`` field with dialogs from
            ``'dstc2-trn.jsonlist'``, ``'valid'`` field with dialogs from
            ``'dstc2-val.jsonlist'`` and ``'test'`` field with dialogs from
            ``'dstc2-tst.jsonlist'``. Each field is a list of tuples ``(x_i, y_i)``.
        """
        required_files = (self._data_fname(dt) for dt in ('trn', 'val', 'tst'))
        if not all(Path(data_path, f).exists() for f in required_files):
            log.info(f"[downloading data from {self.url} to {data_path}]")
            download_decompress(self.url, data_path)

        self.data = {
            'train': self._read_from_file(
                Path(data_path, self._data_fname('trn')), dialogs),
            'valid': self._read_from_file(
                Path(data_path, self._data_fname('val')), dialogs),
            'test': self._read_from_file(
                Path(data_path, self._data_fname('tst')), dialogs)
        }


    @classmethod
    def _read_from_file(cls, file_path, dialogs=False):
        """Returns data from single file"""
        log.info(f"[loading dialogs from {file_path}]")

        utterances, responses, dialog_indices = \
            cls._get_turns(cls._iter_file(file_path), with_indices=True)

        data = list(map(cls._format_turn, zip(utterances, responses)))

        if dialogs:
            return [data[idx['start']:idx['end']] for idx in dialog_indices]
        return data

    @staticmethod
    def _format_turn(turn):
        turn_x, turn_y = turn
        x = {'text': turn_x['text'],
             'intents': turn_x['dialog_acts']}
        if turn_x.get('db_result') is not None:
            x['db_result'] = turn_x['db_result']
        if turn_x.get('episode_done'):
            x['episode_done'] = True
        y = {'text': turn_y['text'],
             'act': turn_y['dialog_acts'][0]['act']}
        return (x, y)

    @staticmethod
    def _iter_file(file_path):
        for ln in open(file_path, 'rt', encoding='utf8'):
            if ln.strip():
                yield json.loads(ln)
            else:
                yield {}

    @staticmethod
    def _get_turns(data, with_indices=False):
        utterances = []
        responses = []
        dialog_indices = []
        n = 0
        num_dialog_utter, num_dialog_resp = 0, 0
        episode_done = True
        for turn in data:
            if not turn:
                if num_dialog_utter != num_dialog_resp:
                    raise RuntimeError("Datafile in the wrong format.")
                episode_done = True
                n += num_dialog_utter
                dialog_indices.append({
                    'start': n - num_dialog_utter,
                    'end': n,
                })
                num_dialog_utter, num_dialog_resp = 0, 0
            else:
                speaker = turn.pop('speaker')
                if speaker == 1:
                    if episode_done:
                        turn['episode_done'] = True
                    utterances.append(turn)
                    num_dialog_utter += 1
                elif speaker == 2:
                    if num_dialog_utter - 1 == num_dialog_resp:
                        responses.append(turn)
                    elif num_dialog_utter - 1 < num_dialog_resp:
                        if episode_done:
                            responses.append(turn)
                            utterances.append({
                                "text": "",
                                "dialog_acts": [],
                                "episode_done": True}
                            )
                        else:
                            new_turn = copy.deepcopy(utterances[-1])
                            if 'db_result' not in responses[-1]:
                                raise RuntimeError(f"Every api_call action"
                                                   f" should have db_result,"
                                                   f" turn = {responses[-1]}")
                            new_turn['db_result'] = responses[-1].pop('db_result')
                            utterances.append(new_turn)
                            responses.append(turn)
                        num_dialog_utter += 1
                    else:
                        raise RuntimeError("there cannot be two successive turns of"
                                           " speaker 1")
                    num_dialog_resp += 1
                else:
                    raise RuntimeError("Only speakers 1 and 2 are supported")
                episode_done = False

        if with_indices:
            return utterances, responses, dialog_indices
        return utterances, responses



if __name__ =="__main__":
    dstc=DSTC2DatasetReader()

    dstc.read('my_data')

    from pprint import pprint

    for dialog in dstc.gen_batches(batch_size=1, data_type='train'):
        turns_x, turns_y = dialog

        print("User utterances:\n----------------\n")
        pprint(turns_x[0], indent=4)
        print("\nSystem responses:\n-----------------\n")
        pprint(turns_y[0], indent=4)

