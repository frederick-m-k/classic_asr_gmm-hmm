# ASR project 2 of group I

This README file outlines the second ASR project of group I.
The project can be found in the following directory: `ASR2_digits/`
In here, the data used for training, building the lexicon, creating the language model and training will be explained.
The Graz tutorial for kaldi was used to create this project.

The other ASR projects can be found in other README files.


## Short overview over the results
Firstly, a short overview over the results is given in the following table.
Afterwards, the steps done to get to those results are explained in detail.
| Training | Testing | model type | result in WER | lmwt | notes |
| 6522 digit utterances from phattsessionz | 200 digit utterances (present in training) | monophone | 43.04 | 50, 55, 60 | sanity check, 200 spks in train |
|  - '' -  | 20 digit utterances from ALC | monophone | 31.25 | 5 | |
|  - '' -  | same as in row 1 | triphone | 34.72 | 50, 55, 60, 65 | sanity check |
|  - '' -  | same as in row 2 | triphone | 32.08 | 45 | |


## Preparations for a monophone model
As for the first step, a monophone model has been created.
Therefore, a subset of the **Phattsessionz** corpus was used as training material. The utterances excluded per default were those which had a * or a ~ in their transcript. Those show a technical error or a not correctly spoken start or end of an utterance. Additionally, only utterances which consisted of spoken *digits*, meaning digits from 'NULL' to 'ZWANZIG' (including the variant 'ZWO'), were included as training material.
In whole, the training material consisted of **6522 utterances** spoken by **200 different speakers**.
13 MFCCs have been calculated along with their deltas and delta-deltas, resulting in 39 MFCCs which have been normalized.

The above explained data can be found in the `ASR2_digits/train` directory


## Building the lexicon
For the lexicon, a simple one, including only entries for the german digits between 'NULL' and 'ZWANZIG', with the variant 'ZWO'.

### Normalizing the utterance transcripts
One thing to mentioned here is the normalization of the utterance transcripts.
All silence words have been replaced with the silence word *!SIL* and all silence phones with the phonem *SIL*.
With this, only one silence word and phone exists.

All normalization of words and phonemes can be found in the `scripts/normalize_config.json` file.

### Actually creating the lexicon
The g2p provided by the IPS (`g2p.pl`) was used to create the actual lexicon entries.
This results in a lexicon consisting of **28 distinct entries**.
From there, the nonsilence phones were extracted. 
Overall, 62 nonsilence phones are present in the lexicon.
As mentioned above, the silence phone *SIL* was used solely to represent silences. A symbol for unknown phonemes and words has been included as well, *UNK:<UNK>*.

The above explained data can be found in `ASR1_phatts/local/dict`


## Creating the language model
For the language model, an ad-hoc grammar consisting of the known german digits was created.
In this ad-hoc grammar, every utterance has to start with a silence word *!SIL* and also end with one. In between, there are equal possibilites for every digit to occur.
Here, you can see a drawing of the ad-hoc grammar:
![drawing of the ad-hoc grammar for the digits language model](ASR2_digits/lang_test/G.png)

The script to create the ad-hoc grammar is `scripts/utils/create_adHoc_Gfst.sh`.
The generated `G.fst` file is `ASR2_digits/lang_test/G.fst`


## Training the monophone model
To train the above built monophone model, the key component is the Viterbi training.
Beforehand, the Viterbi has be prepared, meaning building the first model, aligning it on the data and estimating the model parameters once. This can be found in the `scripts/prepare_mono.sh` script.
Afterwards, the actual Viterbi training starts. In there, for every iteration (e.g. 30) a new model is created, its parameters are gathered and estimated again. This is done in the script `scripts/train_mono.sh`.


## Testing the monophone model
The test the monophone model, different test sets have been used.
The script, used for testing, is `scripts/monophone_evaluation.sh`.

1. Evaluating on Phattsessionz
For the first evaluation, a subset of the **Phattsessionz** corpus was used again. The test set includes *200 randomly selected utterances* from the corpus. In there, *27 utterances* are also included in the training set.
After calculating the MFCCs, the testing started.
For this, a lattice graph containing the acoustic model, the lexicon, the language model and the context was created.
Then this lattice graph evaluated the MFCCs of the test set. The result of this is a transcription.
Then, the WER (Word Error Rate) was calculated between the result of the testing and the correct transcriptions.
The best WER for this sanity check was found for a language model weight of 50, 55 and 60 (or rather an inverted acoustic weight of 1/50, 1/55 or 1/60): 43.04
The results are in the `ASR2_digits/exp/monophone/decode_test_sanity/`.

2. Evaluating on **ALC**
The **ALC** corpus actually contains *20 utterances* which consist only of spoken digits. Those were used to build a test set.
The process for testing is the same as for the evaluation above.
The best WER for this evaluation is, for a language model weight of 5: 31.25


## Training the triphone model
To achieve better result, a triphone model can be used on top of the monophone model.
For this, the scripts `scripts/prepare_tri.sh` and `scripts/train_tri.sh` can be run.
They will create triphone decision trees, build triphones, and start the Viterbi training which is essentially the same as the one for the monophone model.
The triphone model for this ASR project was trained on the same data as the monophone model.


## Testing the triphone model
The evaluation of a triphone model is the same as for a monophone model.
It can be found in the script `scripts/triphone_evaluation.sh`.
Yet again, multiple test sets have been created to evaluate the trained model.

1. Evaluating on Phattsessionz
For this first evaluation, the evaluation on **Phattsessionz**, the same test set has been used for both monophone and triphone.
The best WER for this is, for a language model weight of 50, 55, 60 or 65: 34.72

2. Evaluating on **ALC**
The same test set used to evaluate the monophone model on the **ALC** corpus, was used to evaluate the triphone model as well.
The best WER is, for a language model weight of 45: 32.08


## Who are the geniusses who created this project?
Group I, consisting of Alena, Anton and Frederick
