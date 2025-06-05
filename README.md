# HPC_Final
 
This is the final project of group 02 of the High Performance Computing course at University of Economics Ho Chi Minh City.

Our project involves preprocessin data, training and testing deep learning models, which are LSTM, GRU and BiLSTM to predict stock price of five stock codes: LCID, LYFT, NVDA, QBTS, TSLA. Additionally, we also build a web application to display the prediction results.

## Project overview
The project's folder structure is as follows:
```
└── 📁app
└── 📁data
└── 📁model
└── 📁notebooks
└── 📁utils
```
- The app folder contains the web application built with FastAPI and Reflex.
- The data folder contains the raw data and the preprocessed data.
- The model folder contains the trained models.
- The notebooks folder contains the Jupyter notebooks for data preprocessing and model training.
- The utils folder contains the helper functions for data preprocessing and model training.

## Getting Started
These instructions will help you set up this project on your local machine for development and testing purposes.

### Installing
A ```requirements.txt``` file is provided to install the required packages. Also, a virtual environment is recommended to avoid conflicts with other packages.
```bash
pip install -r requirements.txt
```

## Running the app
To run the stock app, navigate to the app directory and run the following command:
```bash
reflex run
```
You should see the app running at: http://localhost:3000

## Contributing
Special thanks to our collaborators for their support in this project
1. Nguyễn Thị Ngọc Diệp
2. Nguyễn Huy Hoàng
3. Nguyễn Hữu Thanh
4. Võ Yến Nhi

## Acknowledgments
We would like to express our sincere gratitude to Dr. Nguyễn Quốc Hùng for his lectures in *High Performance Computing* course, for his support and guidance throughout this project.