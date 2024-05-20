# To run: ruby boggle.rb
# enter each row for the board you want as arguments when you call the program
require 'set'

def find_all_non_overlapping_groups(board, words)
    all_letters = (0...board.size).to_a.product((0...board[0].size).to_a)
    words = words.sort_by { |word, _| -word.size } # Sort by descending length

    # Convert board to a bitmask
    board_bits = (1 << board.size * board[0].size) - 1

    # Set to keep track of explored groups
    explored_groups = Set.new

    def recursive_search(current_group, remaining_words, all_letters, board_bits, board, explored_groups)
        return [current_group.dup] if remaining_words.empty? # Base case: We've used all words

        results = []
        remaining_words.each_with_index do |(word, paths), i|
            paths.each_with_index do |path, j|
            
                # Check if combining the word with the current group would overlap
                if current_group.all? { |w, p| (path & p).empty? }
                    new_group = current_group + [[word, path]]
                    new_remaining_words = remaining_words.dup
                    new_remaining_words.delete_at(i)

                    # If combined path of the new group covers all letters, it's a valid solution
                    if new_group.map { |_, path| path }.flatten(1).to_set == all_letters.to_set
                        # Check if this configuration has been explored
                        if !explored_groups.include?(new_group.map(&:first).sort)
                            results << new_group 
                            explored_groups.add(new_group.map(&:first).sort)
                        end
                    else
                        # Update the board bitmask based on the newly added word's positions
                        new_board_bits = board_bits
                        path.each do |coords|
                            x, y = coords
                            #puts "x #{x}, y #{y}, board size #{board[0].size}"
                            new_board_bits &= ~(1 << (x * board[0].size + y))
                        end

                        # If the new board bitmask is not zero, proceed with recursion
                        if new_board_bits != 0
                            results += recursive_search(new_group, new_remaining_words, all_letters, new_board_bits, board, explored_groups)
                        end
                    end
                end
            end
        end
        results
    end

    recursive_search([], words.to_a, all_letters, board_bits, board, explored_groups) # Start with an empty group and all possible words
end

class BoggleBoard
    def initialize(board)
        @board = board.map(&:chars)
        @words = {} # Use a hash to store words and their paths
    end
  
    # Function to find all words in the board
    def find_words(dictionary)
        @dictionary = dictionary.to_set
    
        # Optimization: Precalculate prefixes for faster lookup
        @prefixes = Set.new
        @dictionary.each { |word| word.size.times { |i| @prefixes.add(word[0..i]) } }
    
        @words = Hash.new { |hash, key| hash[key] = [] } # Initialize words hash with default empty array
    
        @board.each_with_index do |row, i|
            row.each_with_index do |char, j|
                find_word([i, j], char, [[i, j]])
            end
        end
        @words
    end
  
    private
  
    # Helper function to find a word starting from a given position
    def find_word(position, word, path)
        return unless @prefixes.include?(word) # Prefix optimization

        if @dictionary.include?(word)
            @words[word] << path # Store the word and its path in the hash
        end

        directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
        directions.each do |direction|
            new_position = [position[0] + direction[0], position[1] + direction[1]]
            next if new_position[0] < 0 || new_position[0] >= @board.size || 
                    new_position[1] < 0 || new_position[1] >= @board[0].size ||
                    path.include?(new_position)

            new_char = @board[new_position[0]][new_position[1]]
            find_word(new_position, word + new_char, path + [new_position])
        end
    end
end
  
# Make board from command line
args = ARGV
board_commandline = []
if !args.empty?
    args.each do |arg|
        board_commandline.append(arg)
    end
    puts "Printing the Board:"
    puts board_commandline
    puts
end

# Example usage:
board1 = [
    "bat",
    "gso",
    "gyp"
]

if board_commandline == []
    board = board1
else
    board = board_commandline
end

board_size = [board.length, board.map(&:length).max]
#puts "board size: #{board_size}"

boggle_board = BoggleBoard.new(board)

# Load the dictionary from a file
dictionary = File.readlines('/usr/share/dict/words').map(&:chomp)

# Filter the dictionary to include only words over a certain length
dictionary.select! { |word| word.length > 3 }
puts "Now finding words!"

#puts dictionary

# Find all words
all_words = boggle_board.find_words(dictionary)
#puts all_words
sorted_words = all_words.sort_by { |word, _| +word.size } # Sort by ascending length
sorted_words.each do |word,_|
    puts word
end