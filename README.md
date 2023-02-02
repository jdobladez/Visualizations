# AirBnB - New York City Dataset - Visualization App (Group 30)

## About this app

You can use this as a basic template for your JBI100 visualization project.

## Requirements

* Python 3 (add it to your path (system variables) to make sure you can access it from the command prompt)
* Git (https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
* AirBnB Dataset: https://www.kaggle.com/datasets/arianazmoudeh/airbnbopendata (make sure to select all 26 available columns before downloading)
* Geographical dataset: http://insideairbnb.com/get-the-data/ (Ctrl+F to look for New York City, download the 'neighbourhoods.geojson' file)

## How to run this app

We suggest you to create a virtual environment for running this app with Python 3. Clone this repository 
and open your terminal/command prompt in the root folder.


open the command prompt
cd into the folder where you want to save the files and run the following commands:

```
> git clone https://github.com/jdobladez/Visualizations.git
> cd jbi100-2021-2022
> python -m venv venv

```
If python is not recognized use python3 instead

In Windows: 

```
> venv\Scripts\activate

```
In Unix system:
```
> source venv/bin/activate
```

(Instead of a python virtual environment you can also use an anaconda virtual environment.
 
Requirements:

• Anaconda (https://www.anaconda.com/) or Miniconda (https://docs.conda.io/en/latest/miniconda.html)

• The difference is that Anaconda has a user-friendly UI but requires a lot of space, and Miniconda is Command Prompt based, no UI, but requires considerably less space.

Then you should replace the lines: python -m venv venv and venv\Scripts\activate or source venv/bin/activate with the following:

```
> conda create -n yourenvname
> conda activate yourenvname
```
)

Install all required packages by running:
```
> pip install -r requirements.txt
```

Run this app locally with:
```
> python app.py
```
You will get a http link, open this in your browser to see the results. You can edit the code in any editor (e.g. Visual Studio Code) and if you save it you will see the results in the browser.

## Resources

* [Dash](https://dash.plot.ly/)
* (NGUYEN THI CAM LAI, 2022) Aribnb-preprocessing + EDA. Available [here](https://www.kaggle.com/code/nguyenthicamlai/aribnb-preprocessing-eda)
* (Mulani, S., 2020) Detection and Removal of Outliers in Python – An Easy to Understand Guide. Available [here](https://www.askpython.com/python/examples/detection-removal-outliers-in-python)
* How to calculate CSAT & What it means for your business (2021) MonkeyLearn Blog. Available [here](https://monkeylearn.com/blog/csat-calculation/)
 
