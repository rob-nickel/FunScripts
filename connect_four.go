// to run: go run connect_four.go 
package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

func printBoard(board [][]rune) {
  fmt.Println()
	for _, row := range board {
		for _, col := range row {
			fmt.Print(string(col) + " ")
		}
		fmt.Println()
	}
	fmt.Println("1 2 3 4 5 6 7")
}

func getColumnInput(player string, board [][]rune) int {
	reader := bufio.NewReader(os.Stdin)
	fmt.Print("Player " + player + ", choose a column (1-7): ")
	input, _ := reader.ReadString('\n')

	// Remove newline and convert string to integer
	input = input[:len(input)]
	column, err := strconv.Atoi(input)
	if err != nil || column < 1 || column > 7 || board[0][column - 1] != ' '{
		fmt.Println("Invalid input. Please enter a number between 1 and 7.")
		return getColumnInput(player, board) // Get input again
	}

	return column
}

func checkWin(board [][]rune) rune {
    // Check horizontal wins
    for row := 0; row < len(board); row++ {
        for col := 0; col < len(board[0])-3; col++ {
            if board[row][col] != ' ' &&
                board[row][col] == board[row][col+1] &&
                board[row][col] == board[row][col+2] &&
                board[row][col] == board[row][col+3] {
                return board[row][col]
            }
        }
    }

    // Check vertical wins
    for row := 0; row < len(board)-3; row++ {
        for col := 0; col < len(board[0]); col++ {
            if board[row][col] != ' ' &&
                board[row][col] == board[row+1][col] &&
                board[row][col] == board[row+2][col] &&
                board[row][col] == board[row+3][col] {
				return board[row][col]
            }
        }
    }

    // Check diagonal wins (top-left to bottom-right)
    for row := 0; row < len(board)-3; row++ {
        for col := 0; col < len(board[0])-3; col++ {
            if board[row][col] != ' ' &&
                board[row][col] == board[row+1][col+1] &&
                board[row][col] == board[row+2][col+2] &&
                board[row][col] == board[row+3][col+3] {
			  	return board[row][col]
            }
        }
    }

    // Check diagonal wins (bottom-left to top-right)
    for row := 3; row < len(board); row++ {
        for col := 0; col < len(board[0])-3; col++ {
            if board[row][col] != ' ' &&
                board[row][col] == board[row-1][col+1] &&
                board[row][col] == board[row-2][col+2] &&
                board[row][col] == board[row-3][col+3] {
				return board[row][col]
            }
        }
    }

    return ' ' // No win found
}

func main() {
	// Example usage
	board := [][]rune{
		{' ', ' ', ' ', ' ', ' ', ' ', ' '},
		{' ', ' ', ' ', ' ', ' ', ' ', ' '},
		{' ', ' ', ' ', ' ', ' ', ' ', ' '},
		{' ', ' ', ' ', ' ', ' ', ' ', ' '},
		{' ', ' ', ' ', ' ', ' ', ' ', ' '},
		{' ', ' ', ' ', ' ', ' ', ' ', ' '},
		{' ', ' ', ' ', ' ', ' ', ' ', ' '},
	}

	currentPlayer := 'X'

	for {
		column := getColumnInput(string(currentPlayer), board)

		// Add piece to column
		for i := 0; i <= 6; i++ {
			if board[6-i][column-1] == ' ' {
				board[6-i][column-1] = currentPlayer
				break
			}
		}

		printBoard(board)

		winner := checkWin(board)  
		if winner != ' '{
			fmt.Println("Player " + string(winner) + " has won!")
		}
		if currentPlayer == 'X' {
			currentPlayer = 'O'
		} else {
			currentPlayer = 'X'
		}
	}
}
