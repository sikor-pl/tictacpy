import pickle


with open('tictactoe_q_model_O.pkl', 'rb') as f:
    ai_model = pickle.load(f)
    for k,v in ai_model.items():
        print(f'{k}: {v}')