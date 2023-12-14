# SparkBoard  

<p align="center">
  <img src="https://github.com/CSE583-Electric-Cooking/e-cook/assets/147548462/0ff0637b-a1c1-49c1-9be0-27fb78d14a03" width="200" />
</p>

This is a repository for the CSE 583 class project. The purpose of this project is to develop a software to analyze, synthesize, and process data from electric meter sensors along with individual surveys to understand trends with regards to power quality when electric cooking events are occuring in informal communities in Kampala, Uganda. The software will output a dashboard with data visualization to assist researchers, inform policies, enable decision-making for electric utilities, and provide usage information for community members.  

https://docs.google.com/presentation/d/1Eioyd7BJhzDEZN0DP9kcuu4rF51_Ng9KOpNJeVF1xq0/edit

## Repo Structure
This following is the tree for this project:
```
CSE583-Electric-Cooking/
├── assets/
│   └── style.css
├── data/
│   ├── A2EI/
│   ├── Kosko/
│   └── Surveys/
├── doc/
│   ├── Component Specification.md
│   ├── Electric Cooking Technology Review.pdf
│   ├── Electric Cooking Technology Review.pptx
│   ├── Functional Design.md/
│   └── Interaction Diagram.pdf
├── example/
│   └── example.md
├── sparkboard/
│   ├── images/
│   ├── tests/
│   │   ├──__init__.py
│   │   └──test_main.py
│   ├── plotting/
│   │   ├──__init__.py
│   │   └──plotting.py
│   ├── __init__.py
│   ├── plotting.py
│   ├── process_a2ei.py
│   ├── process_kosko.py
│   ├── process_survey.py
│   └── setup.py
│   └── data_processing/
├── LICENSE
├── README.md
├── dashboard.py   
└── environment.yml
```

## How to run the dashboard  
1. Download the repository onto your local system.  
2. Do the following commands in your terminal:  
```
 1  git clone git@github.com:CSE583-Electric-Cooking/e-cook.git
 2  cd e-cook/
 3  conda env create -f environment.yml
 4  conda activate ecook  
 5  python dashboard.py
```  
3. Click the hyperlink that appears on the shell screen to open `SparkBoard` in your web browser.
4. Toggle between the meter data sets (A2EI and Kosko) and the survey data to see different visualizations of the data. Refer to the examples folder for further information on how to use the software package.

### Caution: OS Compatibility
The software is currently undergoing testing for compatibility across multiple OS platforms. Please note, that macOS users may currently experience failures when running tests involving image comparison. These failures will need to undergo thorough review by the development team to diagnose issues. Subsequent versions intend to resolve this issue.


[![Python Package using Conda](https://github.com/CSE583-Electric-Cooking/e-cook/actions/workflows/python-package-conda.yml/badge.svg)](https://github.com/CSE583-Electric-Cooking/e-cook/actions/workflows/python-package-conda.yml)
