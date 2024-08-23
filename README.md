# Connect 4 Classifier

This project features a neural network classifier built using TensorFlow and Keras. The model is trained to predict the best possible column to make a move in a game of Connect 4 based on the current state of the board. Because it's just a classifier, it's not truly playing, just step-wise predicting the next column. Nevertheless, the results are interesting.

## Overview

- **Input:** A Connect 4 board state.
- **Output:** The best predicted column (1-7) to place your next move.

## Live Demo

You can play against the neural network and see it in action [here](https://connect-4-online.vercel.app/). Note: The AI seems to play somewhat decently, but it has its quirks, such as the lack of the important knowledge of making the winning move! You have to be a pretty poor player to lose, so the AI always moves first to give it a chance.
