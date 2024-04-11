# To run: ruby life.rb
require 'colorize'

# Class to represent a being in the game
class Being
  attr_accessor :speed, :strength, :offspring

  def initialize(speed, strength)
    @speed = speed
    @strength = strength
    @offspring = 0
  end
end
class String
    def colorize(color_code)
        "\e[#{color_code}m#{self}\e[0m"
    end
    def red
        colorize(31)
    end
    def green
        colorize(32)
    end
end

# Run the game for x rounds
rounds = 5
initial_num_beings = 50
average_speed = 0
average_strength = 0

# Create 100 beings
beings = Array.new(initial_num_beings) { |i| Being.new(Random.rand(0..100), Random.rand(0..100)) }

# Function to handle reproduction for each being
def reproduce_and_update(beings, round)
  new_beings = []  # Initialize the array for the new offspring
  percent_affected=0
  percent_decrease=0
  random_effect = Random.rand(0..100)
  if random_effect <= 5
      # Randomly select a percentage of beings to be affected by the plague
      percent_affected = Random.rand(50..90)
  
      # Decrease the strength of the affected beings by a random amount
      percent_decrease = Random.rand(50..90)
      event = 1
      puts "PLAGUE - Strength drops by #{percent_decrease}% for #{percent_affected}% of beings."
  elsif random_effect <= 20
      # Randomly select a percentage of beings to be affected by the natural disaster
      percent_affected = Random.rand(25..75)
  
      # Randomly select a percentage of beings to be killed by the natural disaster
      percent_killed = Random.rand(10..percent_affected)
  
      # Decrease the strength and speed of the affected beings by a random amount
      percent_decrease = Random.rand(25..50)

      # Set the strength and speed of the killed beings to 0
      if percent_affected < (percent_killed + 5)
        disaster_name = "METEOR CRASH"
      elsif percent_affected < 30
        disaster_name = "TORNADO"
      elsif percent_killed > 35
        disaster_name = "ICE AGE"
      else
        disaster_name = "HURRICANE"
      end
      event = 2
      puts "#{disaster_name} - #{percent_killed}% of beings killed, and #{percent_affected}% of beings affected by #{percent_decrease}%."
  else
    event = 0
  end
  beings.each do |being|
    random_speed = Random.rand((being.speed-20)..(being.speed+10))
    random_strength = Random.rand((being.strength-25)..(being.strength+20))
    
    if event == 1
        affected = Random.rand(1..100)
        if (affected < percent_affected)
            #puts "Affected: #{random_strength} but #{random_strength * (100 - percent_decrease) / 100}"
            random_strength = random_strength * (100 - percent_decrease) / 100
            #puts "New Strength: #{random_strength}"
        end
    elsif event == 2
        affected = Random.rand(1..100)
        if (affected < percent_killed)
          random_strength = 0
          random_speed = 0
        elsif (affected < percent_affected)
          random_strength = random_strength * (100 - percent_decrease) / 100
          random_speed = random_speed * (100 - percent_decrease) / 100
        end
    end

    if random_speed > 100
        random_speed = 100
    end
    if random_strength > 100
        random_strength = 100
    end
    total = (random_speed + random_strength)

    if total <= 75
      being.offspring = 0
    elsif total >= 100 && total <= 150
      being.offspring = 1
    else
      being.offspring = 2
    end

    # Add offspring to the new population
    new_beings += [Being.new(random_speed, random_strength)] * being.offspring
  end
  # Replace the old population with the new offspring
  beings = new_beings

  # Ensure the population doesn't exceed 100,000
  #beings = beings.sample(100_000) if beings.count > 100_000
  return new_beings
end

# Function to calculate the average speed and average strength of alive beings
def calculate_stats(beings)
  num_beings = beings.count
  average_speed = beings.sum(&:speed) / (num_beings)
  average_strength = beings.sum(&:strength) / (num_beings)

  [average_speed, average_strength]
end

def generate_visual(round_number, number_of_humans, average_strength, average_speed, old_num_beings, old_average_strength, old_average_speed)
    puts ("   Round:" + "*" * round_number)
    if round_number == 1
        # Draw the graph
        puts ("   Alive:" + "-" * number_of_humans)
        puts ("   Speed:" + "-" * average_speed.floor)
        puts ("Strength:" + "-" * average_strength.floor)
    else
        if number_of_humans > old_num_beings
            puts ("   Alive:" + "-" * number_of_humans).green
        elsif number_of_humans < old_num_beings
            puts ("   Alive:" + "-" * number_of_humans).red
        else
            puts ("   Alive:" + "-" * number_of_humans)
        end 
        if average_speed > old_average_speed
            puts ("   Speed:" + "-" * average_speed.floor).green
        elsif average_speed < old_average_speed
            puts ("   Speed:" + "-" * average_speed.floor).red
        else
            puts ("   Speed:" + "-" * average_speed.floor)
        end
        if average_strength > old_average_strength
            puts ("Strength:" + "-" * average_strength.floor).green
        elsif average_strength < old_average_strength
            puts ("Strength:" + "-" * average_strength.floor).red
        else
            puts ("Strength:" + "-" * average_strength.floor)
        end
    end


    # Wait 1 second to view data
    sleep(1)
    # Add a gap
    puts " " * 80
end

old_num_beings = beings.count
puts "Round | # of Beings | Average Speed | Average Strength"
puts "---|---|---|---"

for round in 1..rounds

  num_beings = beings.count 
  if num_beings > 0
    old_average_speed = average_speed
    old_average_strength = average_strength
    average_speed, average_strength = calculate_stats(beings)
    to_quit = 0
  else
    average_speed = 0
    average_strength = 0
    to_quit = 1
  end

  puts "#{round} | #{num_beings} | #{average_speed.round(2)} | #{average_strength.round(2)}"
  
  generate_visual(round, num_beings, average_strength, average_speed, old_num_beings, old_average_strength, old_average_speed)

  if to_quit == 1
    break
  elsif (round != rounds)
    old_num_beings = num_beings
    beings=reproduce_and_update(beings, round)  # Die old beings, reproduce and update the new population
  end
end