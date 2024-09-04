# Optimizing Arsenal's Formation: A Comparative Analysis with EPL's Big 6 Teams

This repository contains the final project for the MSc Data Science program titled **"Optimizing Arsenal's Formation: A Comparative Analysis with EPL's Big 6 Teams"**. The project aims to enhance the strategic formation of Arsenal Football Club by comparing their tactics with other top teams in the English Premier League (EPL) and providing data-driven recommendations.

## Table of Contents

- [Project Overview](#project-overview)
- [Motivation](#motivation)
- [Objectives](#objectives)
- [Methodology](#methodology)
- [Results and Findings](#results-and-findings)
- [Conclusions and Future Work](#conclusions-and-future-work)
- [Installation and Usage](#installation-and-usage)
- [References](#references)
- [Acknowledgments](#acknowledgments)

## Project Overview

This project compares Arsenal Football Club's formation with those of the "Big 6" teams of the English Premier League (EPL)—Manchester City, Manchester United, Liverpool, Chelsea, and Tottenham Hotspur—in order to optimize it. Using advanced statistical metrics, match performance data, and tactical analysis, the study identifies important patterns, strengths, and weaknesses in Arsenal's current formation strategies in comparison to their rivals.

## Motivation

Achieving a competitive advantage in one of the toughest football leagues in the world is the driving force behind optimizing Arsenal's formation compared to the Premier League's Big 6 teams. With the EPL known for its intense competition, improving team performance using data-driven strategies is imperative. This research aims to provide Arsenal with practical strategies to adapt to different opponents and game situations, increase tactical adaptability, and make intelligent choices about player roles and positions.

## Objectives

The main objectives of the project are as follows:

1. **Data Collection and Preprocessing**: Collect and sanitize performance data from the major Premier League teams - Arsenal, Manchester City, Tottenham Hotspur, Manchester United, Chelsea, and Liverpool.
2. **Data Categorization**: Organize the collected data into structured data frames for analysis.
3. **Feature Engineering**: Prepare data for machine learning by encoding categorical variables and selecting relevant features.
4. **Model Training and Evaluation**: Train predictive models to determine how different formations affect a team's performance.
5. **Performance Analysis**: Evaluate the models' performance and identify the optimal formation for Arsenal.
6. **Reporting**: Draft a comprehensive report providing the best formations and strategies that can improve Arsenal's performance.

## Methodology

The methodology of the project involves several key steps:

1. **Data Collection**: Data was collected from FBref, a well-known resource for in-depth football statistics, for the 2023-2024 season. The data includes performance metrics, formation data, and tactical decisions.
   
2. **Exploratory Data Analysis (EDA)**: EDA was conducted to understand the patterns, correlations, and anomalies in the dataset using various statistical and visualization techniques.
   
3. **Model Building**: Three machine learning models—Support Vector Machine (SVM), Random Forest, and Gradient Boosting Machine (GBM)—were employed to predict match outcomes and recommend optimal formations.
   
4. **Model Evaluation**: The models were evaluated using accuracy, precision, recall, and F1-score metrics to determine their effectiveness in predicting optimal formations.

## Results and Findings

- **Support Vector Machine (SVM)**: The SVM model showed moderate predictive performance with an accuracy of 50%, indicating potential improvements in precision, recall, and F1-score.
- **Random Forest Model**: The Random Forest model demonstrated lower accuracy (31.67%) and F1-score (21.78%), suggesting that further model tuning and data preprocessing are needed.
- **Gradient Boosting Model**: The Gradient Boosting model also displayed low accuracy (30%) and F1-score (23.89%), highlighting the need for more sophisticated modeling techniques and feature engineering.

Based on the findings, the project proposes an optimized formation for Arsenal that could enhance both offensive and defensive effectiveness.

## Conclusions and Future Work

While the SVM, Random Forest, and Gradient Boosting models provided some insights, they showed limited predictive potential. Future work could focus on:

1. **Improving Data Quality and Feature Engineering**: Incorporate more relevant features and use dimensionality reduction techniques.
2. **Balancing Model Complexity and Overfitting**: Use advanced hyperparameter tuning strategies to enhance model performance.
3. **Exploring Alternative or Hybrid Models**: Consider deep learning techniques or hybrid models for better prediction accuracy.
4. **Implementing Advanced Modeling Techniques**: Further exploration into deep learning frameworks could yield more refined results.

## Installation and Usage

To use the code provided in this repository:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/arsenal-formation-optimization.git
    cd arsenal-formation-optimization
    ```

2. **Install the required dependencies**:
    Make sure you have Python installed. Install the necessary libraries using pip:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Python script**:
    Execute the `final_project_1 (6).py` script to reproduce the results.
    ```bash
    python final_project_1 (6).py
    ```

## References

Please refer to the final report for a comprehensive list of references used in this project.

## Acknowledgments

I would like to express my sincere thanks to my supervisor, John Evans, for his guidance and support throughout this project. Additionally, gratitude is extended to the University of Hertfordshire, my colleagues, and my family for their unwavering support.

---

This project is submitted in partial fulfillment of the requirement for the degree of Master of Science in Data Science at the University of Hertfordshire.

