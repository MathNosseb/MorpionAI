import napoleon
import json
import random
import minimax
#1 = IA soit O; -1 = Joueur ou IA2 soit X
#creation du board
board = [0]*9
architecture = [9,18,1]
log_path = "log.txt"
data_path = "data.txt"

IA = napoleon.Napoleon(architecture,0.5,100)

#charger des poids si connus
try:
    with open(log_path,"r") as log:
        data = json.load(log)
        new_weights = data["weights"]
        new_biases = data["biases"]
except Exception as e:
    print(e)
    print("pas de fichier ou pas de contenu de log")
    new_weights,new_biases = 0,0
    print("problème réglé")

def full_board(board):
    full = True
    for i in range(9):
        if board[i] == 0:
            full = False
    return full

def verif_gagnant(board):
    #verification des lignes
    for i in range(3):
        if board[i * 3] == board[i * 3 + 1] == board[i * 3 + 2] == -1:
            return -1
        elif board[i * 3] == board[i * 3 + 1] == board[i * 3 + 2] == 1:
            return 1
    # Vérifier les colonnes
    for i in range(3):
        if board[i] == board[i + 3] == board[i + 6] == -1:
            return -1
        elif board[i] == board[i + 3] == board[i + 6] == 1:
            return 1
    # Vérifier les diagonales
    if board[0] == board[4] == board[8] == -1:
        return -1
    if board[2] == board[4] == board[6] == -1:
        return -1
    if board[0] == board[4] == board[8] == 1:
        return 1
    if board[2] == board[4] == board[6] == 1:
        return 1
    return False

def print_board(board):
    print(board[:3])
    print(board[3:6])
    print(board[6:9])

def generate_data():
    final_board = []
    
    part_count = 0
    Victory = False
    while not Victory:
        part_count +=1
        temp = []
        temp_board = [0]*9
        for i in range(9):
            
            #pas l'ia
            output = random.randint(0,8)
            while not temp_board[output] == 0:
                output = random.randint(0,8)
            
            temp_board[output] = -1
            if verif_gagnant(temp_board) == -1:
                final_board+=temp.copy()
                Victory = True
                return
            if verif_gagnant(temp_board) == 1:
                
                return
            if full_board(temp_board):

                return
            
            #ia
            output = random.randint(0,8)
            while not temp_board[output] == 0:
                output = random.randint(0,8)
            
            temp_board[output] = -1

            temp.append(list(temp_board)+[output/10])
            if verif_gagnant(temp_board) == -1:
                final_board+=temp.copy()
                Victory = True
                return
            if verif_gagnant(temp_board) == 1:
                return
            if full_board(temp_board):

                return


    print(final_board)
    print("nombre de partie",part_count)
    with open(data_path,"w") as data:
        data.write(str(final_board))
def predict_best_move(board):
    output = IA.try_network([board + [0]], new_weights, new_biases)[0][1]
    
    # Convertir la sortie en un indice valide
    predicted_move = int(output[0] * 9)  # Éviter les valeurs hors limites
    
    # Liste des cases disponibles
    available_moves = [i for i, val in enumerate(board) if val == 0]

    if not available_moves:
        return None  # Aucun coup possible
    if not board[predicted_move] == 0:
        predicted_move = random.choice(available_moves)
    return predicted_move



def train_with_generate_data():
    global new_weights,new_biases
    with open(data_path,"r") as data:
        dataset = data.readlines()[0]
        
        new_weights, new_biases = IA.train(eval(dataset),new_weights,new_biases)
        with open(log_path, "w") as f:#enregistrement de weights et biases
            json.dump({"weights": new_weights, "biases": new_biases}, f)

            
def vs_train():
    final_board = []
    max_train = 10
    part_count = 0
    Victory_count = 0
    Victory = False
    while not Victory:
        part_count+=1
        if part_count >= max_train:
            print("pas de victoire")
            Victory = True
        temp = []
        temp_board = [0]*9
        for i in range(9):
            
            #pas l'ia
            output = abs(minimax.best_move(temp_board))
            while not temp_board[output] == 0:
                output = abs(minimax.best_move(temp_board))
            
            temp_board[output] = 1
            if verif_gagnant(temp_board) == -1:
                final_board+=temp.copy()
                Victory_count+=1
                Victory = True
                break
            if verif_gagnant(temp_board) == 1:
                final_board += [x[:-1] + [-x[-1]] for x in temp]  # Inverser le score
                break
            if full_board(temp_board):

                break

            #ia
            output = abs(int(predict_best_move(temp_board)))
            
            temp_board[output] = -1
            temp.append(list(temp_board)+[output/10])
            if verif_gagnant(temp_board) == -1:
                final_board+=temp.copy()
                Victory_count+=1
                Victory = True
                break
            if verif_gagnant(temp_board) == 1:
                final_board += [x[:-1] + [-x[-1]] for x in temp]  # Inverser le score
                break
            if full_board(temp_board):
                break



    print(Victory_count)
    print("nombre de partie",part_count)
    with open(data_path,"w") as data:
        data.write(str(final_board))



with open(data_path,"r") as data:
    if data.readlines() == []:
        generate_data()
        print("generation des données terminé")

for i in range(10):
    vs_train()
    train_with_generate_data()
print("fin")