# 🌱 Zenvironment

A family-friendly mindfulness app that uses AI to create personalized nature-based meditation and recharge activities. Share your surroundings through photos, audio, or text, and get customized mindfulness exercises designed to help you connect with nature.

## 🎯 Project Role

Zenvironment helps families find moments of peace and mindfulness in their natural surroundings. Using Google's Gemma 3n multimodal AI model, the app analyzes your environment and suggests tailored activities like breathing exercises, sensory scavenger hunts, and nature meditations.

## 🛠️ Tech Stack

- **Python** - Backend language
- **Gradio** - Web interface framework
- **Transformers** (Hugging Face) - AI model integration
- **PyTorch** - Machine learning framework
- **Gemma 3n** - Google's multimodal AI model for generating personalized activities
- **PIL** - Image processing

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8 or higher
- GPU recommended for optimal AI model performance

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd gemma-3n-challenge
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download the Gemma 3n model**
   - The app expects the model at: `models/gemma-3n-transformers-gemma-3n-e2b-it-v2`
   - Follow Hugging Face instructions to download the Gemma 3n model to this path

## 🏃‍♂️ Local Deployment & Usage

### Run the Application
```bash
python app.py
```

The app will launch on `http://localhost:7860`

### How to Use
1. **Start a Session**: Describe your surroundings or upload a photo/audio
2. **Get Activities**: The AI will suggest 2-3 personalized mindfulness activities
3. **Complete Session**: Follow the guided activities and provide feedback
4. **Track Progress**: View your session history and favorite activities

### Features
- 📸 **Photo Analysis**: Upload images of your environment for context-aware suggestions
- 🎤 **Audio Input**: Describe your surroundings verbally
- ✍️ **Text Description**: Share details about your location and mood
- 🧘‍♀️ **20+ Activities**: From breathing exercises to nature scavenger hunts
- 👨‍👩‍👧‍👦 **Family-Friendly**: Activities designed for all ages

## 📱 Usage Example

1. Upload a photo of a forest trail
2. Add description: "Taking a break during our family hike"
3. Get personalized activities like:
   - 5-minute mindful breathing with nature sounds
   - Forest sensory scavenger hunt
   - Tree meditation exercise

---

*Built for the Gemma 3n Challenge - helping families find peace in nature through AI-powered mindfulness.*
