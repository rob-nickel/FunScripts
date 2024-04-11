# To run: ruby word_search.rb

# Example usage
words = ["eat", "tat", "tart"]
board = [
  ['t','a','t','h','t'],
  ['t','a','a','a','t'],
  ['t','a','e','a','t'],
  ['m','a','a','a','n'],
  ['t','a','t','r','t'],
  ['t','r','a','t','e']
]

# Function to find words in the board
def find_words(board, words)
  # Check each word in the words array
  words.each do |word|
    # Check for horizontal matches
    find_horizontal(board, word)
    # Check for vertical matches
    find_vertical(board, word)
    # Check for diagonal matches
    find_diagonal(board, word)
  end
end

# Helper function to find horizontal words
def find_horizontal(board, word)
  # Check each row in the board
  board.each.with_index do |row, row_num|
    current_index = 0
    while current_index < row.length
      # Check if the first character matches the word
      if row[current_index] == word[0]
        match_count = 1
        # Check remaining characters for a match
        while match_count < word.length && (current_index + match_count) < row.length
          if row[current_index+match_count] == word[match_count]
            match_count += 1
          else
            break
          end
        end
        match_count_backwards = 1
        while match_count_backwards < word.length && (current_index - match_count_backwards) >= 0
          if row[(current_index-match_count_backwards)] == word[match_count_backwards]
            match_count_backwards += 1
          else
            break
          end
        end
        # If the entire word is found, print the match
        if match_count == word.length
          puts "#{word} found horizontally in row #{1 + row_num}"
        end
        if match_count_backwards == word.length
          puts "#{word} found horizontally backwards in row #{1 + row_num}"
        end
      end
      current_index += 1 # Move to the next character in the row
    end
  end
end

# Helper function to find vertical words
def find_vertical(board, word)
  # Check each column in the board
  board.transpose.each.with_index do |column, column_num|
    current_index = 0
    while current_index + word.length <= column.length
      if column[current_index] == word[0]
        match_count = 1
        while match_count < word.length && current_index < column.length
          if column[current_index+match_count] == word[match_count]
            match_count += 1
          else
            break
          end
        end
        match_count_backwards = 1
        while match_count_backwards < word.length && (current_index - match_count_backwards) >= 0
          if column[(current_index-match_count_backwards)] == word[match_count_backwards]
            match_count_backwards += 1
          else
            break
          end
        end
        if match_count == word.length
          puts "#{word} found vertically in column #{(1 + column_num)}"
        end
        if match_count_backwards == word.length
          puts "#{word} found vertically backwards in column #{(1 + column_num)}"
        end
      end
      current_index += 1
    end
  end
end

# Helper function to find diagonal words
def find_diagonal(board, word)
  # Define the directions (up-left, up-right, down-left, and down-right)
  directions = [[-1,-1],[-1,1],[1,-1],[1,1]]

  board.each_with_index do |row, row_idx|
    row.each_with_index do |cell, col_idx|
      if cell == word[0] 
        # Iterate through each direction
        directions.each.with_index do |(dir_row, dir_col), dir_idx|
          # Create an array to store the characters found along this diagonal
          char_array = [cell]

          # Start at the current cell position
          i = row_idx + dir_row
          j = col_idx + dir_col
          k = 1 #letter number

          while(i >=0 && i < board.length) && (j >= 0 && j < board[i].length)
            if board[i][j] == word[k]
              char_array << board[i][j]
              i += dir_row
              j += dir_col
              k += 1
            else
              break
            end
          end

          if (char_array.size == word.length)
            if (dir_idx == 0)
              direction_word = "up and left"
            elsif (dir_idx == 1)
              direction_word = "up and right"
            elsif (dir_idx == 2)
              direction_word = "down and left"
            else
              direction_word = "down and right"
            end
            puts "#{word} found diagonally #{direction_word} starting at row #{(1 + row_idx)} and column #{(1 + col_idx)}"
          end
        end
      end
    end
  end
end

# Call the find_words function
find_words(board, words)
