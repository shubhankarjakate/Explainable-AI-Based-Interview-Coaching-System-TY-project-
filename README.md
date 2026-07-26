# 🎯 Explainable AI-Based Interview Coaching System

> **Your Personal AI Interview Coach that evaluates not only _what_ you answer, but _how_ you answer.**

<p align="center">
  <img src="https://img.shields.io/badge/AI-Interview%20Coach-blue?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Explainable-AI-success?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/XGBoost-R²%200.932-orange?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Python-3.10+-yellow?style=for-the-badge"/>
</p>

---

## 🚀 Overview

Technical interviews are not just about solving problems—they're also about **confidence**, **communication**, and **clarity**.

The **Explainable AI-Based Interview Coaching System** is an intelligent interview preparation platform that simulates real technical interviews using Large Language Models while providing explainable feedback on both:

- 🧠 Technical correctness of answers
- 🎤 Speaking confidence and delivery

Unlike traditional mock interview platforms, this system evaluates **both the content and communication style**, helping candidates improve holistically.

---

# ✨ Features

### 🤖 AI Interview Question Generation
- Resume-based interview questions
- Domain-specific interview preparation
- Multiple difficulty levels
  - Easy
  - Medium
  - Hard

---

### 💬 Dual Response Support

Candidates can answer using:

- ✍️ Text
- 🎙️ Voice

Voice responses are automatically converted into text for semantic evaluation.

---

### 🧠 Intelligent Answer Evaluation

Large Language Models analyze:

- Technical correctness
- Concept coverage
- Semantic understanding
- Explanation quality

instead of simple keyword matching.

---

### 🎤 Confidence Analysis

The system evaluates speaking behaviour using acoustic features such as:

- Speech Rate
- Pitch Mean
- Pitch Variation
- Pause Count
- Average Pause Duration
- Energy Level
- Jitter
- Shimmer
- Filler Word Detection

These features are used to predict the candidate's confidence level.

---

### 📊 Explainable Feedback

Instead of giving only scores, the system explains:

✅ What was good

⚠️ What needs improvement

💡 How the answer can be improved

making learning much more effective.

---

### 📈 Progress Tracking

The platform stores interview performance over time to help users monitor improvement.

---

# 🏗️ System Architecture

```
                 Resume / Domain
                        │
                        ▼
           Question Generation (LLM)
                        │
             ┌──────────┴──────────┐
             │                     │
          Text Answer        Audio Answer
             │                     │
             │              Speech-to-Text
             │                     │
             ▼                     ▼
     Content Evaluation     Speech Feature Extraction
             │                     │
             │               XGBoost Confidence Model
             └──────────┬──────────┘
                        ▼
             Explainable Feedback Engine
                        │
                        ▼
                 Performance Dashboard
```

---

# ⚙️ Workflow

1. Upload Resume **OR** Select Interview Domain
2. AI generates interview questions
3. Candidate answers via Text or Audio
4. Audio is converted to text (if required)
5. LLM evaluates technical correctness
6. Speech features are extracted
7. XGBoost predicts confidence score
8. Both evaluations are merged
9. Explainable feedback is generated
10. Progress is stored for future sessions

---

# 🧠 Technologies Used

## Artificial Intelligence

- Large Language Models (LLMs)
- Explainable AI (XAI)
- Natural Language Processing
- Machine Learning

---

## Machine Learning

- XGBoost
- Random Forest
- Ridge Regression
- Multi-Layer Perceptron (MLP)

---

## Speech Processing

- Whisper
- Librosa

---

## NLP

- spaCy
- Gemini / GPT-based evaluation

---

## Backend

- Python
- FastAPI

---

## Database

- MongoDB / PostgreSQL

---

# 📊 Speech Features Used

| Feature | Purpose |
|----------|----------|
| Pitch Mean | Voice Stability |
| Pitch Variance | Pitch Control |
| Speech Rate | Fluency |
| Pause Count | Hesitation Detection |
| Average Pause Duration | Confidence Analysis |
| Energy Mean | Speaking Intensity |
| Jitter | Voice Stability |
| Shimmer | Loudness Variation |
| Filler Words | Fluency Measurement |

---

# 📈 Model Performance

Several machine learning models were evaluated.

| Model | MAE | RMSE | R² Score |
|------|------|------|-----------|
| **XGBoost** | **0.464** | **0.715** | **0.932** ✅ |
| MLP | 0.472 | 0.714 | 0.932 |
| Random Forest | 0.477 | 0.733 | 0.928 |
| Ridge Regression | 0.676 | 0.918 | 0.887 |

🏆 **XGBoost achieved the best overall performance**, explaining **93.2%** of the variance in confidence prediction.

---

# 📂 Dataset

Because publicly available interview datasets are limited, a synthetic dataset was created.

### Dataset Statistics

- Initial Samples: **10,763**
- Final Cleaned Dataset: **8,982**
- Acoustic Features: **9**
- Labels generated using:
  - Rule-based scoring
  - LLM-assisted annotation

---

# 🎯 Explainability

This project follows Explainable AI principles by providing transparent reasoning behind every evaluation.

Instead of simply assigning scores, the system explains:

- Why confidence is high or low
- Which speech features influenced the prediction
- Which communication habits should improve
- How answers can be strengthened

---

# 📸 Future Improvements

- 🌍 Multilingual interview support
- 🎥 Video interview analysis
- 😊 Facial expression recognition
- 👀 Eye contact analysis
- 📱 Mobile application
- 📈 Personalized learning recommendations
- 🧑‍💼 HR-specific interview simulations
- ⚡ Real-time interview feedback

---

# 🎯 Applications

- Technical Interview Preparation
- Campus Placement Training
- Career Coaching
- Soft Skills Development
- HR Interview Practice
- AI-based Mock Interviews

---

# 🌟 Key Highlights

- ✅ Resume-based Interview Generation
- ✅ AI-powered Semantic Evaluation
- ✅ Speech Confidence Analysis
- ✅ Explainable AI Feedback
- ✅ XGBoost Confidence Prediction
- ✅ Progress Tracking Dashboard
- ✅ Realistic Mock Interview Experience

---

# 📖 Research

This repository is based on the research paper:

**"Explainable AI-Based Interview Coaching System"**

The research introduces a dual-analysis framework combining semantic evaluation using Large Language Models with confidence prediction using speech analytics and XGBoost, resulting in a transparent AI interview coaching platform.

---

# 👥 Authors

- Yash Maske
- Sakshi Lokhande
- Chandrakant Thakare
- Shubhankar Jakate
- Anuradha Yenkikar
- Pranjal Pandit

---

# ⭐ If you found this project useful...

Give this repository a ⭐ and help others discover AI-powered interview coaching!
