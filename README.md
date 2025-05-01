# CliniPredict

*CliniPredict* is an AI-powered Flask application designed to help healthcare organizations efficiently analyze and act on diverse feedback sources using Microsoft's AutoGen agent framework.

## Overview

Hospitals and clinics collect feedback through a variety of channels—surveys, doctor's notes, call centers, social media, and more. However, traditional approaches to feedback analysis are slow, manual, and prone to bias, especially with non-numerical and multilingual data.

CliniPredict solves this with a robust AI system powered by AutoGen, enabling real-time, accurate, and scalable feedback interpretation across multiple formats and languages.

## Features

- *Multi-format Input Processing*: Analyze text, audio, video, and image-based feedback.
- *Multilingual Support*: Automatically detects and processes input in multiple languages.
- *Agentic AI Architecture*: Utilizes a team of specialized AutoGen agents for different tasks.
  - AudioProcessorAgent: Transcribes spoken feedback from multilingual audio.
  - VideoProcessorAgent: Extracts and transcribes feedback from videos.
  - TextAnalysisAgent: Classifies and interprets unstructured text.
- *Real-Time Analysis*: Reduces "Time to Metrics" by automating transcription and sentiment classification.
- *Bias Reduction*: Minimizes human labeling errors through consistent AI-driven interpretation.

## Why CliniPredict?

Unlike traditional platforms like Medallia and Press Ganey that focus on numerical ratings, CliniPredict supports:
- Unstructured feedback
- Interviews
- Social media content (YouTube, Instagram, Twitter/X, Facebook)
- Multilingual and multimedia formats

## Built With

- [Flask](https://flask.palletsprojects.com/) – Web application framework
- [AutoGen](https://github.com/microsoft/autogen) – Multi-agent AI framework by Microsoft
- [OpenAI](https://openai.com/) – Language models powering natural language understanding
- [Gemini](https://ai.google.dev/gemini) – Used for content processing and transcription

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/clinipredict.git
   cd clinipredict
