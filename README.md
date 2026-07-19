# Sensor Fault Detection Platform

## Problem statement

Trucks (like Scania trucks) use something called an **APS — Air Pressure System**. It uses compressed air to power important parts of the truck, like the brakes and the gear shifter. If the APS fails, it can cause serious safety issues and expensive downtime.

Truck sensors constantly record data about the APS (pressure readings, temperatures, and other signals). The goal of this project is to predict whether a truck's APS is likely to fail — **before** it actually breaks down — using this sensor data.

Why does this matter so much? Because the two mistakes you can make are **not equally costly**:

- **Missed failure (false negative):** The model says "the truck is fine," but the APS actually fails. This can lead to accidents, breakdowns on the road, or very expensive emergency repairs.
- **Unnecessary inspection (false positive):** The model says "check this truck," but it turns out to be fine. This costs some time and money for an inspection — annoying, but nowhere near as costly or dangerous as a missed failure.

Because a missed failure is far more expensive and dangerous than a false alarm, **a simple accuracy-focused model isn't good enough**. A model can score high on "accuracy" just by predicting "no failure" almost every time (since failures are rare compared to healthy trucks), while still missing the failures that actually matter. This project instead needs to focus on **minimizing the cost of missed failures**, using techniques suited for imbalanced, high-stakes data — not just overall accuracy.

This system takes raw sensor data collected from trucks, cleans and prepares it, trains a model to catch APS failures early, and keeps that model working reliably over time — so failures can be caught and fixed before they cause real damage.

## Status

Phase 0 — project skeleton and packaging. Built with uv, src layout.

## Tech stack (planned)

Python, uv, MongoDB Atlas, AWS S3, scikit-learn, MLflow, DVC, FastAPI,
Docker, GitHub Actions, EC2/SageMaker.