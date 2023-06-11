# No_Teacher_Tic_Tac_Toe_Learner
A self learning Tic-Tac-Toe Learner algorithm (learning from their own experience)

#### `Learning task: The learner should learn to play the game of Tic Tac Toe with the “User”. The goal of the learner is to win or at least draw the games played. The exact type of knowledge to be learned in our case is a function that chooses the best move for any board state (given, it falls under legal moves). Now, to design a learning system, we need to choose a type of training experience from which our system will learn.`
`There are two modes:`
1) **Teacher mode:** In our approach, we use data samples containing the sequence of board states of each game and their corresponding assigned value (based on whether the game ended in a win, loss, or draw). The learning will rely on this external source of knowledge and will be only as good as the teacher is (in our case, the training samples from the games played in the past).
2) **No teacher mode:** The learner has complete control on board state choosing. It generates its own data by playing against itself and based on these will improve its game. For example, experimenting with novel board states that it had never considered playing and improving its skills.
We are using both the approaches in this homework, and thus we will have the two following modes:

`Mode1: Teacher`
Task T: Playing Tic Tac Toe with the opponent.
Performance measure P: Number of games won.
Training experience E: External source of Training data.

---

`Mode2: No teacher`
Task T: Playing Tic Tac Toe with the opponent.
Performance measure P: Number of games won.
Training experience E: Games played against itself

---

• The target function we will use is a evaluation function that will assign better score to a better board state. The value of the target function V be defined as following, [V: B —> R]:
• V( b = Terminal board state) = 100 … where the game is won by the learner
• V( b = Terminal board state) = -100 … where the game is lost by the learner
• V( b = Terminal board state) = 0 … where the game is a draw
• When b is not equal to terminal board state, the following applies:
• V(b) = V(b’) … Where b’ is the board corresponding to the next best move
• V, being the target function, our approximate actual function will be V*. V* is the function actually learned by our program.


• The representation of the target function: We have used a simple representation in the program, which is a linear combination of the following board features:

1) X1 = The number of rows, columns and diagonals where there is only 1 ‘x’
2) X2 = The number of rows, columns and diagonals where there is only 1 ‘o’
3) X3 = The number of rows, column and diagonals where there are only 2 ‘x’s
4) X4 = The number of rows, columns and diagonals where there are only 2 ‘o’s
5) X5 = The number of rows, columns and diagonals where there are 3 ‘x’s
6) X6 = The number of rows, columns and diagonals where there are 3 ‘o’s


**Thus our actual function V* will be as follows:**

`V* = w0 + w1*X1 + w2*X2 + w3*X3 + w4*X4 + w5*X5 + w6*X6`

The trade offs we considered in formulating this learning task are:

1) The selection of the target function representation matters in how close we can get to the V.
But since the more expressive and complicated the function becomes, more is the data needed by the system, thus we used a simpler representation.
2) The weights will determine the importance of each of the board features in determining the value of the board. Here, we used the number of 1’x’ and the number of 1’o’ as two parameters x1, and x2. However there might be better features to choose like, the number of number of ‘x’s in the corner of the board or at the center.
3) In the ‘No teacher mode’, the correctness of the moves were inferred from the fact that the game was eventually won or lost, posing a problem of credit assignment. That is, its hard to determine which move deserves the credit or the blame for the win or loss.
4) The main disadvantage of the ‘Teacher mode’ is that, the learner only gets as smart as the teacher is. If it encounters anything beyond the scope of the teacher, it will falter and likely fail.


Generating random legal board positions: This is crucial as our state space is small enough to explore. When the experience generator outputs a new initial board state, after taking the current hypothesis, it helps the performance system to explore particular regions of the state space, thus improving the learning of the entire system. This may only be a disadvantage if the state space is too vast.

Generating a position by picking a board state from the previous game, then applying one of the moves, that was not executed: This approach also helps the learning system to explore, but with a limitation of having to start from the already seen starting position.

A strategy of our own design: One strategy might be to pit the learner against a random player, this will help the learner system to explore all the possible positions, but with a disadvantage that it might not perform well at expert level games. For this, we can make the learner system replay expert games, by selecting board positions from expert games.

Explanation for weights: #1) x1 = When there is only an 'x' in the entire row, column or diagonal #2) x2 = When there is only an 'o' in the entire row, column or diagonal #3) x3 = When there are 2 'x's in the row, column or diagonal #4) x4 = When there are 2 'o's in the row, column or diagonal #5) x5 = When there are 3 'x's in the row, column or diagonal #6) x6 = When there are 3 'o's in the row, column or diagonal

1) Teacher: Weights1: [10.363128069258693, 0.3802749878308054, 6.135586822914178, -2.8552512556106366, -8.628009937720234, 66.75915687766671, -90.45579746657663]

The weights corresponding to the x5 and x6 features are promoting the learner (‘x’) to maximise three consecutive ‘x’s and minimize three consecutive ‘o’s. Similar pattern can be observed for x3 and x4.

2) No teacher: Weights1: [15.19, 1.28, -1.8, 2.01, -2.2, 83.32, -69.89]

The same observation can be made for the No teacher mode, where the highest weight corresponds to getting three consecutive ‘x’s for the learner(‘x’) and the least weight corresponds to when the learner loses the game to the opponent. Similarly, the weights corresponding to having 2 ‘x’s in a row, column or diagonal is positive as opposed to the negative value for x4, which states that the learner tries to maximise the chances of having 2 ‘x’s in order to have a win and minimizes the chance of having 2 ‘o’s of the opponent.

