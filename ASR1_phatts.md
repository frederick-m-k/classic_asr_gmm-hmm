# ASR project 1 of group I

This README file outlines the first ASR project of group I.
The project can be found in the following directory: `ASR1_phatts/`
In here, the data used for training, building the lexicon, creating the language model and training will be explained.
The Graz tutorial for kaldi was used to create this project.

The other ASR projects can be found in other `.md` files.
A general overview over the whole directory structure and the scripts used to create the project is in the `README.md` file.

## Short overview over the results
Firstly, a short overview over the results is given in the following table.
Afterwards, the steps done to get to those results are explained in detail.

| Training | Testing | model type | result in WER | lmwt | notes |
| whole phattsessionz (119924 utts) | 100 utts from phattsessionz (included in training) | monophone | 31.18 | 25 | sanity check for the acoustic model |
|  - '' -  | 296 utts from ALC (not in training) | monophone | 81.72 | 25 | |
|  - '' -  | 100 different utts from ALC (not in training) | monophone | 75.54 | 50 | |
|  - '' -  | same as in row 1 | triphone | 15.5 | 25 | sanity check for acoustic model |
|  - '' -  | same as in row 2 | triphone | 70.83 | 25 | |
|  - '' -  | same as in row 3 | triphone | 61.17 | 50 | |

## Preparations for a monophone model
As for the first step, a monophone model has been created.
Therefore, the **whole Phattsessionz** corpus was used as training material. The only utterances excluded were those which had a * or a ~ in their transcript. Those show a technical error or a not correctly spoken start or end of an utterance.
In whole, the training material consisted of **119924 utterances** spoken by **1019 different speakers**.
13 MFCCs have been calculated along with their deltas and delta-deltas, resulting in 39 MFCCs which have been normalized.

The above explained data can be found in the `ASR1_phatts/train` directory


## Building the lexicon
For the lexicon, a mixed version of both **ALC** and **Phattsessionz** has been used. This means, all utterances from the **ALC** and all utterances from the **Phattsessionz** corpus have gathered together.

### Normalizing the utterance transcripts
One thing to mentioned here is the normalization of the utterance transcripts.
All silence words have been replaced with the silence word *!SIL* and all silence phones with the phonem *SIL*.
With this, only one silence word and phone exists.
Furthermore, the **ALC** corpus currently used on the server has some weird usage of Umlaute *Ä*, *Ü*, and *Ö*.
They are written as *"A*, *"U*, and *"O*. This was normalized to the correct display of the Umlaute as well.

All normalization of words and phonemes can be found in the `scripts/normalize_config.json` file.

### Actually creating the lexicon
The g2p provided by the IPS (`g2p.pl`) was used to create the actual lexicon entries.
This results in a lexicon consisting of **18923 distinct entries**.
From there, the nonsilence phones were extracted. 
Some phoneme normalization has been done as well. The seven least frequent phonemes have been converted to more common, acoustically similar, phonemes. These convertion can be found in `scripts/normalize_config.json`.
Overall, 62 nonsilence phones are present in the lexicon.
As mentioned above, the silence phone *SIL* was used solely to represent silences. A symbol for unknown phonemes and words has been included as well, *UNK:<UNK>*.

The above explained data can be found in `ASR1_phatts/local/dict`


## Creating the language model
Regarding the language model, all utterances from **Phattsessionz** and from **ALC** are included.
All occurrences of the silence word *!SIL* are excluded.
The above mentioned normalization of the transcritps are naturally used here as well.
A bigram was created using the `lmplz` command from `kenlm`.
The resulting `.arpa` file is `lang_mod/alcAndPhatts_bi.arpa`


## Training the monophone model
To train the above built monophone model, the key component is the Viterbi training.
Beforehand, the Viterbi has be prepared, meaning building the first model, aligning it on the data and estimating the model parameters once. This can be found in the `scripts/prepare_mono.sh` script.
Afterwards, the actual Viterbi training starts. In there, for every iteration (e.g. 30) a new model is created, its parameters are gathered and estimated again. This is done in the script `scripts/train_mono.sh`.


## Testing the monophone model
The test the monophone model, different test sets have been used.
The script, used for testing, is `scripts/monophone_evaluation.sh`.

1. Evaluating on a subset of the training set
For a sanity check of the acoustic model, a subset of the whole training set, including *100 utterances*, was used to create a test set.
After calculating the MFCCs, the testing started.
For this, a lattice graph containing the acoustic model, the lexicon, the language model and the context was created.
Then this lattice graph evaluated the MFCCs of the test set. The result of this is a transcription.
Then, the WER (Word Error Rate) was calculated between the result of the testing and the correct transcriptions.
The best WER for this sanity check was found for a language model weight of 25 (or rather an inverted acoustic weight of 1/25): 31.18%
The results are in the `ASR1_phatts/exp/wholeLex/decode_test_smallPhatts/`.

2. Evaluating on new data
To actually test the ASR model, new data, which has not been present in training, has to be used.
For this, a small subset of the **ALC** corpus, *296 utterances* were used to build a test set.
The process for testing is the same as for the sanity check above.
The best WER for this evaluation is, yet again for a language model weight of 25: 81.27%

3. Evaluating again on the **ALC** corpus
A third evaluation was done for the monophone model. This test set is from the **ALC** corpus, is therefore not in the training set and consists of *100 random utterances*.
The process for evaluation is the same as in the two numbered points above.
The best WER for this evaluation is for a language model weight of 50: 75.54%


## Training the triphone model
To achieve better result, a triphone model can be used on top of the monophone model.
For this, the scripts `scripts/prepare_tri.sh` and `scripts/train_tri.sh` can be run.
They will create triphone decision trees, build triphones, and start the Viterbi training which is essentially the same as the one for the monophone model.
The triphone model for this ASR project was trained on the same data as the monophone model.


## Testing the triphone model
The evaluation of a triphone model is the same as for a monophone model.
It can be found in the script `scripts/triphone_evaluation.sh`.
Yet again, multiple test sets have been created to evaluate the trained model.

1. Subset of the training set
As for the monophone model, a sanity check has been done for the triphone model.
The same test set has been used for both monophone and triphone.
The best WER for this sanity check is, for a language model weight of 25: 15.5%

2. Evaluating on new data
The same test set used to acutally evaluate the monophone model, was used to evaluate the triphone model as well.
The best WER is, for a language model weight of 25, yet again: 70.83%

3. Evaluating again on the **ALC** corpus
The same test set is the same as in the third evaluation of the monophone evaluation.
The best WER is for a language model weight of 50: 61.17%

## Who are the geniusses who created this project?
Group I, consisting of Alena, Anton and Frederick
