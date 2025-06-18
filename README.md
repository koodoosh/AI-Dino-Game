# 🦖 Dino AI Game – NEAT + Pygame

An AI-powered version of the classic Chrome Dino game where autonomous agents learn to jump over obstacles using **NeuroEvolution of Augmenting Topologies (NEAT)** and **reinforcement learning**. Built with Python and Pygame.

---

## 🚀 Features

- 🧠 **NEAT Algorithm**: Evolving neural networks through natural selection.
- 🏃‍♂️ **Dynamic Obstacle Avoidance**: Agents learn to jump over cacti and birds.
- 📈 **Evolution Tracking**: Watch your AI improve over generations.
- 🎮 **Pygame Visualization**: Real-time simulation of agents during training.
- 💾 **Configurable Parameters**: Easily adjust genome count, mutation rates, etc.

---

## 🛠 Tech Stack

- **Python 3.x**
- **Pygame**
- **NEAT-Python**
- **NumPy** (optional for data handling)

---

## 📂 Project Structure
📁 AI_Dino_Game/
├── img/              # Sprites for dino, cactus, background, etc.
├── dino.py              # Game logic using Pygame
├── neat_config.txt      # Configuration for NEAT evolution
├── main.py              # Main training loop using NEAT
├── ai_player.py         # Dino agent controlled by neural network
└── README.md            # You’re here!

---

## ⚙️ How It Works

- Each **Dino** is controlled by a neural network.
- Using sensors (like distance to cactus, obstacle speed), it decides when to **jump**.
- After each generation:
  - Fitness is calculated based on distance survived
  - Top performers reproduce using mutation & crossover
  - Poor performers are eliminated
- Over **100+ generations**, the AI evolves to play better and survive longer.

---


## Results
	-	#Achieved a high score of 10,000+ after ~100 generations.
	-	#Evolved agents show advanced jump timing and cactus prediction behavior.
