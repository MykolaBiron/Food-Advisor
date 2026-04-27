# 🍽️ FoodAdvisor

An AI-powered nutrition tracking application that uses deep learning to identify food from images and automatically track nutritional intake. Simply upload a photo of your meal, and FoodAdvisor will recognize the food, calculate the nutritional values, and help you maintain your health goals.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Visit%20FoodAdvisor-brightgreen?style=for-the-badge)](https://food-advisor-production-3924.up.railway.app)

![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

## ✨ Features

### 🤖 AI-Powered Food Recognition
- **Deep Learning Model**: Trained CNN model capable of recognizing 101 different food categories
- **Image Classification**: Upload a photo and get instant food identification
- **Confidence Scoring**: Model provides confidence levels for predictions
- **User Correction System**: Collect feedback on incorrect predictions to improve the model through RLHF (Reinforcement Learning from Human Feedback)

### 📊 Comprehensive Nutrition Tracking
- **Automatic Nutritional Analysis**: Retrieves detailed nutrition data via Nutritionix API
- **Macronutrient Breakdown**: Track calories, proteins, carbohydrates, and fats
- **Portion Size Adjustment**: Customize serving sizes (small, medium, large)
- **Daily Meal History**: View all meals logged throughout the day with timestamps

### 👤 Personalized Health Profiles
- **Custom Calorie Targets**: Calculates daily caloric needs based on:
  - Age, sex, height, and weight
  - Activity level (low, moderate, high)
  - Workout frequency (0-1, 2-3, 4+ times per week)
  - Health goals (lose weight, maintain, gain weight)
- **Macronutrient Goals**: Personalized protein, carb, and fat targets
- **Weight Tracking**: Log and visualize weight changes over time
- **Progress Visualization**: Interactive graphs showing weight trends

### 📈 Analytics & Insights
- **Visual Progress Charts**: Matplotlib-generated graphs for weight tracking
- **Meal Statistics**: View nutritional summaries for each meal
- **Daily Progress**: Track progress toward daily nutritional goals
- **Historical Data**: Access past meals and nutritional data

### 🔐 User Management
- **Secure Authentication**: User registration and login system
- **Profile Management**: Create and customize personal health profiles
- **Data Privacy**: User-specific data isolation and protection

## 🛠️ Technologies

### Backend
- **Django 5.2.6**: Python web framework for robust backend architecture
- **PostgreSQL**: Relational database for data persistence
- **Gunicorn**: WSGI HTTP server for production deployment
- **WhiteNoise**: Static file serving for Django applications

### Machine Learning & AI
- **TensorFlow 2.20.0**: Deep learning framework
- **Keras**: High-level neural networks API
- **NumPy & Pandas**: Data manipulation and numerical computing
- **scikit-learn**: Machine learning utilities
- **Pillow**: Image processing library

### Frontend
- **React 18**: Modern JavaScript library for building user interfaces
- **TypeScript**: Type-safe JavaScript development
- **Vite**: Fast build tool and development server
- **TailwindCSS**: Utility-first CSS framework
- **React Router**: Client-side routing
- **TanStack Query**: Server state management

### Data & APIs
- **Nutritionix API**: Real-time nutritional data retrieval
- **Requests**: HTTP library for API calls

### Visualization
- **Matplotlib**: Python plotting library for weight graphs

### Development & Deployment
- **Railway**: Cloud platform for deployment
- **python-decouple**: Environment variable management
- **dj-database-url**: Database URL parsing

## 🏗️ Process (How I Built the App)

### 1. **Planning & Architecture** 
I started by defining the core problem: manually tracking nutrition is tedious and time-consuming. The solution was to leverage AI for automatic food recognition combined with a comprehensive tracking system. I designed a full-stack architecture with Django handling the backend and ML model serving, while React provided a responsive frontend.

### 2. **Dataset & Model Selection**
Initially, I planned to train a CNN from scratch, but after research and experimentation, I opted for transfer learning:
- **Dataset**: Food101 dataset containing 101 food categories
- **Base Model**: Fine-tuned ImageNet pre-trained model
- **Training Process**: Conducted extensive experimentation in Jupyter notebooks (`CNN_model.ipynb`)
- **Model Performance**: Achieved ~69% Top-1 accuracy, which is reasonable given the complexity of food recognition and dataset limitations

### 3. **Backend Development**
Built a robust Django application with:
- **Database Models**: Designed normalized schema for Users, Profiles, Meals, FoodItems, and WeightEntries
- **ML Integration**: Created prediction functions (`prediction_funcs.py`) that load the Keras model and process images
- **API Integration**: Implemented Nutritionix API client (`nutrition_api.py`) for fetching nutritional data
- **Business Logic**: 
  - Developed calorie calculation algorithms based on Mifflin-St Jeor equation
  - Implemented macronutrient distribution (24% protein, 50% carbs, 26% fats)
  - Created portion size multipliers for serving adjustments

### 4. **Frontend Development**
Developed a modern React/TypeScript interface:
- **Component Architecture**: Built reusable UI components with shadcn/ui library
- **Responsive Design**: Used TailwindCSS for mobile-first, responsive layouts
- **Type Safety**: Implemented TypeScript for better developer experience and fewer runtime errors
- **Build Optimization**: Configured Vite for fast development and optimized production builds

### 5. **Machine Learning Pipeline**
Established a continuous improvement workflow:
- **Prediction Correction System**: Users can correct misidentified foods
- **Data Collection**: Store incorrect predictions with correct labels (`CorrectedPrediction` model)
- **Export Functionality**: Created Django management command to export feedback data
- **RLHF Preparation**: Designed the system for future model retraining with human feedback

### 6. **User Experience Features**
- **Personalization Engine**: Implemented sophisticated calorie and macro calculations considering multiple factors
- **Visual Feedback**: Generated dynamic weight tracking graphs using Matplotlib
- **Meal Management**: Built intuitive interfaces for viewing, editing, and saving meals
- **Form Validation**: Implemented comprehensive validation for user inputs

### 7. **Testing & Optimization**
- **Model Evaluation**: Created evaluation functions and tracked accuracy metrics
- **Performance Analysis**: Built project size analyzer to optimize deployment
- **Database Optimization**: Implemented efficient queries and proper indexing
- **Static File Handling**: Configured WhiteNose for efficient static file serving

### 8. **Deployment & Production**
- **Railway Platform**: Deployed on Railway for scalable cloud hosting
- **Environment Management**: Used python-decouple for secure configuration
- **Database Migration**: Configured PostgreSQL for production with proper migrations
- **Static Files**: Set up WhiteNoise for production static file serving
- **Build Scripts**: Created automated build scripts for streamlined deployment

### 9. **Continuous Improvement**
The app is designed for evolution:
- **Feedback Loop**: Collecting user corrections for future model improvements
- **Modular Architecture**: Easy to add new features and food categories
- **Scalable Design**: Database and API structure support growth
- **Jupyter Notebooks**: Maintaining notebooks for model experimentation and retraining

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Node.js 16+
- PostgreSQL

### Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/FoodAdvisor.git
cd FoodAdvisor
```

2. Install Python dependencies
```bash
pip install -r requirements.txt
```

3. Install frontend dependencies
```bash
npm install
```

4. Set up environment variables
Create a `.env` file with:
```
SECRET_KEY=your-secret-key
DATABASE_URL=your-database-url
NUTRITIONIX_APP_ID=your-app-id
NUTRITIONIX_API_KEY=your-api-key
```

5. Run migrations
```bash
python manage.py migrate
```

6. Start the development server
```bash
# Backend
python manage.py runserver

# Frontend (in another terminal)
npm run dev
```

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

---

**Visit FoodAdvisor**: [https://food-advisor-production-3924.up.railway.app](https://food-advisor-production-3924.up.railway.app)
