
# ASR Projects from group I
This README file outlines the directory structure which you are currently in.
In the structure, three ASR projects can be found with corresponding .md-files each which explain the best WERs and the used data for it.
Generally spoken, all ASR systems are GMM-HMM models.

NOTE: some of the undermentioned directories are not on git.
We are currently working on bringing a basic train/test setup on git.
Please request bigger material from the authors, if the ALC or Ph@ttSessionz corpus are needed specifially

## Basic structure
The main directory structure is as follows:
- *start.sh* file to launch the ASR UI
- *scripts* directory containing the project scripts (*NB*: If necessary each script can be executed separately. See the table below for more information regarding 
each script).
- *kaldi* directory which contains `path.sh` file, `steps/` and `utils/` folder
- *conf* directory for kaldi configurations 
- *forced_aligned* directory for comparison between MAUS and the kaldi-based ASR model forced alignments (extra task, that goes beyond the ASR)
- *ASR1_phatts*, *ASR2_digits* and *ASR3_ALC* directories which represent three different ASR projects (for more details see the respective .md file)  


## Usage
There are two possible usage scenarios:
1. Building the ASR by relying on the user UI by executing *start.sh*
2. Running micro scripts separately (see the paragraph below).

### Macro scripts
There are several microscripts that can be run separately (for scripts description see table below).
Below there are scripts listed which support UI scenario. 

- *start.sh*: This script launches ASR UI and prepares data
- *lexicon_FK.sh*: Creates a lexicon based on the tasks 4...13 of the Graz kaldi tutorial.
- *lang_model.sh*: This script either generates a trigram model of training data by using kenlm, or selects an existing language model for the specific ASR-task.
- *mfccs_sepDir.sh*: This script calculates mfccs for the utterances in the given path.
- *prepare_mono.sh*: Performs commands for preparing data for mono model training.
- *prepare_tri.sh*: Performs commands for preparing data for triphone model training.
- *monophone_viterbi.sh*: Performs viterbi training (monophone).
- *triphone_viterbi.sh*: Performs viterbi training (triphone).
- *triphone_evaluation.sh*: Creates test & lattice graph (mono).
- *monophone_evaluation.sh*: Creates test & lattice graph(tri). 

### Running micro scripts seperately
| Script                     |    What does it do?                  | Tasks in the Graz tutorial |
|----------------------------|--------------------------------------|----------------------------|
| task0\_1.py                |Prepares an index of audo files and an index of trascriptions. | task 1 & 2 |
| task2.py                   | Prepares the list of all utterances\n per speaker. | task 2                     |                          
| task4.py                   | Creates a dictionary containing 1 \n lemma per line and respective \n canonical transcription. | task 4                     |   
| task6.py                   | Creates nonsilence\_phones.txt file    | task 6                     |
| normalize\_phonemes\_in\_lex.py | Performs phoneme normalization.       | None                       |
| task12.sh                   | Performs prepare\_lang.sh script       | task 12                    |
| task13.sh                   | Performs sym2int.pl script            | task 13                    |
| train\_mono.sh               | Performs viterbi training (monophone).| task 29                    |
| train\_tri.sh                | Performs viterbi training (triphone). | task 37                    |
| task31-32.sh                | Performs micro tasks 31&32            | task 31 & 32               |
| task34.sh                   | Finds best path & computes wer        | task 34                    |

### Special scripts
- *plotSubtree.sh*: Plots the phonetical subtree of any specific triphone.
- *plotLanguageModel.sh*: This script plots a language model named G.fst into a PDF file in the same directory location 
- *amount_phonemes.py*: Prints amount of all phones and words.
- *replace_spaces_tab.py*: This script replaces all \"    \" with a \'\\t\' symbol. The amount of spaces to replace can be chosen.
- *relocateMFCCsAfterRenaming.py*: This script goes through all feats- .ark files and places the correct path in the corresponding .scp files.
- *create_adHoc_Gfst.sh*: Creates an ad hoc grammar in a G.fst file.
- *check_ifUttsInSet.py*: This script checks, if given utterances, e.g. a test set, are in a provided set, e.g. a training set. 

## What we did
We created three different ASR projects which can be found in the `groupI` directory. 
The first project was ASR1_phatts which is based on **Phattsessionz** corpus. 
The second one was the ASR2_digits which consists of utterances of the **Phattsessionz** corpus that contains digits from "Null" to "Zwanzig". 
The third one was the ASR3_ALC which contains the utterances from **ALC** corpus.     
To learn more about details and results see the corresponding .md files in the `groupI` folder.

## Requirements
As can be seen above, there are both shell as well as Python scripts, which can be executed.
For the shell, there are no requirements. Note however, that we wrote the scripts for Bash. We do not know, if they also work with other shell types.
We developed and executed the scripts on Ubuntu 20.04.5 LTS
Regarding Python, we used version 3.8.10 for development. These are the requirements for packages:
numpy==1.21.3
pandas==1.3.4
praatio==5.1.1
matplotlib==3.5.0


## Forced alignment
As an extra task, there is forced alignment performed. For this, we used models built by means of kaldi.
The outcome was compared with MAUS forced aligner.
Feel free to contact us to learn more about results.

## These are the geniusses who created this project
Group I of the "WP 1.2 Sprachtechnologie" course, consisting of **Alena**, **Anton** and **Frederick**, created this ASR and forced alignment project.
Feel free to contact us for any questions.
Contact: alena.makhneva@campus.lmu.de, anton.gadringer@campus.lmu.de, Frederick.Kukla@campus.lmu.de
