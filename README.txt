Data Analyst Project – Sales Insights

This project uses a sample .csv file from a website to create an SQLite database, allowing me to practice SQL.
The conversion process is handled in the Python file db_loader.py, which contains a class that builds the database from the .csv file using SQLAlchemy for database operations.

An instance of the DB loader is created in the notebook file Sales_Insights_Dashboard.ipynb, where we use tables to visualize and explore the following real-life objectives:
1) Load sales data into SQLite using SQLAlchemy
2) Write SQL queries to answer questions such as:
    - What are the top-selling products?
    - Which customers spend the most?
    - How do sales vary by month or region?
3) Use Python (Pandas) to process query results
4) Visualize data using Matplotlib or Seaborn
5) Export cleaned tables for future machine learning use



Study Notes:

VIRTUAL ENVIRONMENT
Create a virtual environment is important and will help you avoid common headaches later.
A virtual environment is like a clean, isolated container for Python projects. It keeps all the packages (like pandas, scikit-learn, tensorflow, etc.) separate just for that one project.
Imagine you're working on:
Project A, which needs TensorFlow 2.10
Project B, which needs TensorFlow 2.14
If you install both globally (on your system), they'll conflict. A virtual environment solves this by letting each project use its own dependencies, without affecting other projects or your system Python.


HOW TO CREATE AN VE?
- python -m venv venv		(This command creates a folder called venv/ Inside it: a private copy of Python and a blank space for packages)
- .\venv\Scripts\activate	(Activates the venv)
	if errors do this:
		- Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
		- .\venv\Scripts\Activate.ps1
- pip freeze > requirements.txt
This saves your environment’s dependencies to a requirements.txt file, so you (or others) can recreate it later.


Package			Purpose
numpy, pandas		Data handling
matplotlib, seaborn	Visualizations
scikit-learn		Machine learning models
tensorflow		Deep learning
shap			Model explainability
sqlalchemy		SQL database connection from Python
ipython, jupyter	Notebook support







