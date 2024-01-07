# Descriptions

### Knowledge-Driven Modulation of Neural Networks with Attention Mechanism for Next Activity Prediction (Preparing to submit)

This repository contains developed scripts for our proposed approach of predictive process monitoring.

We split the implementation into two folders for (i) synthetic and (ii) real-logs. For each folder, you can implement our approach by running 'run_experiments.py' file. 

You can also set your own parameters in 'log_utils.py' and 'shared_variables.py files located in the folder '~\src\commons'

We also provide a summarized result of our experiments in 'performance.csv' file, which is presented in our paper. 

## Input/Output files

The used event logs and BPMN models in the paper are located in the folder '~\data\input'.

Then, after running the script, trained models and results of predictive process monitoring will be saved in the folder '~\data\output'.

We also uploaded our trained models used in the paper in the folder '~\data\output_old'. The result files after evaluation which used in our paper are downloadable in this link: https://drive.google.com/file/d/12_qesWq_mu6i0Tb4ckZyzCHpJOwdMcP2/view?usp=sharing.


## How to train/evaluate

The main implementation script is the 'run_experiments.py' file. 

You can run the script in command line by 
(i) firstly go to the directory, e.g., using "cd C:\Users\ADMIN\~\KB-Modulation\implementation_real_logs", and then 
(ii) implementing "python run_experiments.py --log 'sepsis_cases_1.csv' --train". Here, the option '--train' is only for training a model and, otherwise, you can select one among ['--train', '--evaluation' (for evaluation), '--full_run' (for both)]. 

In addition, an option 'weight' can allow you to configure the weight (importance) of BK in evaluation stage, e.g., "python run_experiments.py --log 'sepsis_cases_1.csv' --evaluation --weight '0'" .

If you want to run the script using tools like Pycharm or VScode, in line 62-64 in 'run_experiments.py', you can configure (1) only training by setting 'default = True' in line 62, or (2) only evaluation by setting 'default = True' in line 63, or (3) both by setting 'default = True' in line 64.

About the other parameters, we encourge to fix it, i.e., don't touch it. Some of them are not available, and we are now constructing it for an extended work.
