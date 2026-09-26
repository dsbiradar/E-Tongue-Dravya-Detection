# E-Tongue Based Dravya Detection

## Machine Learning-Based Ayurvedic Substance Classification Using an Electronic Tongue

An integrated **IoT, Machine Learning, and Web Application** system for automated identification and classification of Ayurvedic substances (Dravya) in liquid form using measurable chemical parameters such as **pH, Total Dissolved Solids (TDS), and Electrical Conductivity (EC)**.

---

## 📌 Overview

Identification of Ayurvedic substances traditionally depends on sensory evaluation, visual inspection, and expert knowledge. These methods can be subjective and may be difficult to apply consistently, particularly for liquid substances.

This project proposes an **Electronic Tongue (E-Tongue)** based system that combines sensor-based data acquisition with Machine Learning techniques for automated Dravya classification.

The system collects chemical measurements from liquid samples using **pH, TDS, and EC sensors**. An **Arduino UNO** collects the sensor readings and sends the data to a computer through serial communication.

The collected data is processed using multiple Machine Learning classification algorithms. The best-performing trained model is then used to predict the type of Ayurvedic Dravya.

A **Flask-based web application** provides a user-friendly interface for real-time input and prediction, while a **2×16 LCD display** provides sensor readings and prediction results on the hardware side.

---

## 🎯 Objectives

The main objectives of this project are:

- To design and develop an Electronic Tongue based system for Ayurvedic Dravya classification.
- To measure chemical properties of liquid samples using pH, TDS, and EC sensors.
- To create a structured dataset using measurable sensor parameters.
- To apply and evaluate multiple Machine Learning classification algorithms.
- To identify the best-performing Machine Learning model.
- To train and test the models for reliable prediction.
- To develop a Flask-based web application for real-time input and prediction.
- To reduce dependency on manual sensory evaluation.
- To provide faster and more consistent Dravya classification.

---

## 🔬 What is an Electronic Tongue?

An **Electronic Tongue (E-Tongue)** is a sensor-based system designed to analyze the chemical characteristics of liquid samples.

In this project, the E-Tongue uses:

- **pH Sensor** – Measures the acidity or alkalinity of the sample.
- **TDS Sensor** – Measures Total Dissolved Solids in the liquid.
- **EC Sensor** – Measures Electrical Conductivity.

The sensor readings provide measurable features that are used as input for Machine Learning based classification.

---

## 🏗️ System Architecture

```text
                   Ayurvedic Liquid Sample
                            │
                            ▼
                  ┌───────────────────┐
                  │   E-Tongue       │
                  │     Sensors      │
                  │                   │
                  │  • pH Sensor      │
                  │  • TDS Sensor     │
                  │  • EC Sensor      │
                  └─────────┬─────────┘
                            │
                            ▼
                  ┌───────────────────┐
                  │    Arduino UNO    │
                  │  Data Collection  │
                  └─────────┬─────────┘
                            │
                    Serial Communication
                            │
                            ▼
                  ┌───────────────────┐
                  │     Computer      │
                  │  Sensor Dataset   │
                  └─────────┬─────────┘
                            │
                            ▼
                  ┌───────────────────┐
                  │ Machine Learning  │
                  │     Models        │
                  │                   │
                  │ Random Forest     │
                  │ SVM               │
                  │ KNN               │
                  │ Logistic Reg.     │
                  │ Decision Tree     │
                  └─────────┬─────────┘
                            │
                            ▼
                  ┌───────────────────┐
                  │ Best Performing   │
                  │    ML Model       │
                  └─────────┬─────────┘
                            │
                ┌───────────┴───────────┐
                │                       │
                ▼                       ▼
       ┌──────────────────┐    ┌──────────────────┐
       │  Flask Web App   │    │    2×16 LCD      │
       │                  │    │                  │
       │ Real-Time Input  │    │ Sensor Readings  │
       │ & Prediction     │    │ & Prediction     │
       └──────────────────┘    └──────────────────┘
```

---

## ⚙️ How the System Works

The complete system works through the following stages:

### 1. Liquid Sample

An Ayurvedic liquid sample is provided to the Electronic Tongue sensing system.

### 2. Sensor Measurement

The pH, TDS, and Electrical Conductivity sensors measure the chemical properties of the sample.

### 3. Arduino Data Acquisition

The **Arduino UNO** collects the real-time sensor readings and acts as the main controller.

### 4. Data Transfer

The collected sensor data is transferred to the computer through **serial communication**.

### 5. Machine Learning Processing

The sensor values are provided to trained Machine Learning models for classification.

### 6. Dravya Prediction

The selected best-performing Machine Learning model predicts the corresponding Ayurvedic substance.

### 7. Web Application

The Flask application provides a user-friendly interface for real-time input and displays the predicted Dravya.

### 8. LCD Display

A **2×16 LCD display** can show real-time sensor readings and prediction results directly on the hardware.

---

## 🤖 Machine Learning

The project evaluates multiple Machine Learning classification algorithms to identify an effective model for Ayurvedic Dravya classification.

### Algorithms Used

| Algorithm | Purpose |
|---|---|
| Random Forest | Classification using multiple decision trees |
| Support Vector Machine (SVM) | Classification by finding suitable decision boundaries |
| K-Nearest Neighbors (KNN) | Classification based on nearby data points |
| Logistic Regression | Classification using learned relationships between features |
| Decision Tree | Classification using decision-based rules |

The models are trained and evaluated using the customized Dravya dataset, and the best-performing model is selected for final prediction.

---

## 📊 Input Parameters

The primary sensor parameters used by the system are:

| Parameter | Description |
|---|---|
| pH | Indicates acidity or alkalinity of the liquid |
| TDS | Measures Total Dissolved Solids |
| EC | Measures Electrical Conductivity |

These parameters are used as measurable chemical features for Machine Learning based classification.

---

## 🌿 Ayurvedic Dravya Classification

The system is designed to classify different Ayurvedic substances using their measured sensor characteristics.

Examples included in the project are:

- Tulsi
- Neem
- Karanda

The classification performance depends on the quality of the dataset, sensor measurements, and operating conditions.

---

## 🌐 Flask Web Application

The project includes a **Flask-based web application** that connects the Machine Learning model with the user interface.

### Flask is used to:

- Receive input values.
- Connect the web interface with the trained ML model.
- Process prediction requests.
- Obtain the predicted Dravya.
- Display the prediction to the user.

### Web Application Flow

```text
User / Sensor Input
        ↓
pH + TDS + EC
        ↓
Flask Web Application
        ↓
Trained ML Model
        ↓
Prediction
        ↓
Dravya Result
```

---

## 🔌 IoT / Hardware Components

The hardware side of the system consists of:

- Arduino UNO
- pH Sensor
- TDS Sensor
- Electrical Conductivity Sensor
- 2×16 LCD Display
- DC Power Supply

### Role of Arduino UNO

Arduino UNO acts as the main controller of the hardware system.

It:

1. Collects sensor readings.
2. Handles the sensor data.
3. Provides the readings for further processing.
4. Supports real-time interaction with the sensing system.

---

## 💻 Software Technologies

### Programming Languages

- Python
- HTML
- CSS
- JavaScript

### Machine Learning

- Random Forest
- Support Vector Machine
- K-Nearest Neighbors
- Logistic Regression
- Decision Tree

### Web Framework

- Flask

### Development Tools

- Visual Studio Code
- Anaconda IDE

### Dataset

- Customized Ayurvedic Dravya Dataset

---

## 🧰 Hardware Requirements

The project presentation specifies the following basic system requirements:

- Processor: Core i3 or above
- RAM: 8 GB
- Hard Disk: 400 GB
- Monitor: 15-inch VGA Color
- Mouse: Logitech

---

## 📂 Project Structure

```text
E-Tongue-Dravya-Detection/
│
├── static/
│   └── Static files for the Flask web application
│
├── templates/
│   └── HTML templates for the Flask web application
│
├── app.py
│   └── Flask web application
│
├── best_dravya_model.pkl
│   └── Trained Machine Learning model
│
├── real_dravya_dataset.csv
│   └── Dravya sensor dataset
│
├── training.ipynb
│   └── Machine Learning training and evaluation notebook
│
├── algorithm_comparison.png
│   └── Machine Learning algorithm comparison
│
├── run.bat
│   └── Application launch script
│
└── .gitignore
    └── Git ignored files and folders
```

---

## 🚀 Running the Project

### Prerequisites

Before running the software component, make sure the required Python environment and project dependencies are available.

The repository contains:

- Flask application
- Trained Machine Learning model
- Dataset
- Training notebook
- Web application templates
- Static files
- Application launch script

### Run Using the Project Script

The repository includes:

```text
run.bat
```

This script is provided as the project launch script for the application.

### Run the Flask Application Directly

The main Flask application is:

```text
app.py
```

The exact Python packages and environment configuration should match the project environment used during development.

---

## 📈 Model Evaluation

The project evaluates several classification algorithms and compares their performance.

The comparison visualization is available in:

```text
algorithm_comparison.png
```

The model selected for final prediction is stored as:

```text
best_dravya_model.pkl
```

The Machine Learning training and evaluation process is available in:

```text
training.ipynb
```

---

## 📁 Dataset

The project uses a customized dataset containing sensor measurements associated with Ayurvedic Dravya samples.

The primary sensor features are:

```text
pH
TDS
EC
```

Dataset file:

```text
real_dravya_dataset.csv
```

The dataset is used for training and evaluating the classification models.

---

## ✅ Advantages

The proposed system provides the following advantages:

- Objective and data-driven classification.
- Reduced dependency on manual expertise.
- Faster identification.
- Real-time prediction.
- Improved consistency.
- Integration of IoT sensing and Machine Learning.
- User-friendly Flask web interface.
- Hardware-based sensor measurement.
- Automated classification of Ayurvedic liquid substances.

---

## ⚠️ Limitations

The current system has some limitations:

- Model performance depends on the quality and size of the dataset.
- Sensor calibration can affect measurements.
- Sensor noise can affect prediction performance.
- Substances with similar chemical characteristics may be difficult to distinguish.
- Performance may vary under real-world conditions.
- The current system primarily uses pH, TDS, and EC parameters.
- More data and model improvements are required to improve reliability and generalization.

---

## 🔮 Future Scope

The system can be extended in several ways:

### 📚 Dataset Expansion

Add more Ayurvedic substances and increase the number of samples for each substance.

### 🧪 Additional Sensors

Integrate additional sensing technologies to capture more chemical characteristics.

### 🤖 Improved Machine Learning

Explore improved Machine Learning techniques and optimize the classification models.

### 📱 Mobile Application

Develop a mobile application for easier access to the prediction system.

### ☁️ Cloud Integration

Connect the system to cloud services for scalable data storage and processing.

### 🔋 Portable Device

Develop a compact and portable Electronic Tongue device for practical field usage.

### 🌐 Multilingual Support

Provide support for multiple languages to improve accessibility.

### 🎯 Improved Generalization

Increase dataset diversity and improve model robustness for real-world conditions.

---

## 🌱 Real-World Potential

The project demonstrates the integration of:

```text
IoT Sensors
     +
Arduino
     +
Machine Learning
     +
Flask Web Application
     ↓
Automated Ayurvedic Dravya Classification
```

This approach demonstrates how sensor-based measurements and Machine Learning can be combined to support automated classification of Ayurvedic liquid substances.

---

## 🔐 Important Note

The system is developed for **academic and research purposes**.

The Machine Learning predictions are based on the available dataset and sensor measurements. The project should not be treated as a replacement for qualified Ayurvedic, medical, laboratory, or quality-control professionals.

The project results are expected to be strongest under controlled dataset and measurement conditions.

---

## 📚 References

1. P. W. Ruch et al., **"A Portable Potentiometric Electronic Tongue Leveraging Smartphone and Cloud Platforms,"** 2019.

2. J. X. Leon-Medina et al., **"Yogurt Classification Using an Electronic Tongue System and Machine Learning Techniques,"** 2022.

3. J. X. Leon-Medina et al., **"New Electronic Tongue Sensor Array System for Accurate Classification of Liquor Beverages,"** 2023.

4. J. X. Leon-Medina et al., **"Intelligent Electronic Tongue System for the Classification of Genuine and Adulterated Honey,"** 2023.

5. W. Zheng et al., **"A Data Processing Method for Electronic Tongue Based on CMTP-CNN,"** 2022.

6. **"Electronic Tongue Based Classification of Mineral Water Samples,"** 2024.

7. A. A. Rumaila et al., **"Electronic Tongue for Determining the Limit of Detection of Food-Borne Pathogens,"** 2023.

8. J. Liu et al., **"Bioinspired Integrated Triboelectric Electronic Tongue for Advanced Taste Recognition,"** 2024.

---

## 👩‍💻 Author

### Dhaneshwari S Biradar

B.Tech – Computer Science and Engineering  
Sharnbasva University, Kalaburagi, Karnataka

**GitHub:**  
https://github.com/dsbiradar

---

## ⭐ Project Summary

**E-Tongue Based Dravya Detection** combines **Electronic Tongue sensors, Arduino UNO, Machine Learning, and Flask** to develop an automated system for Ayurvedic liquid substance classification.

```text
pH + TDS + EC
      ↓
Electronic Tongue
      ↓
Arduino UNO
      ↓
Sensor Data
      ↓
Machine Learning
      ↓
Dravya Prediction
      ↓
Flask Web Application
