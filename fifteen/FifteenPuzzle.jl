import Base.show
import Printf.@printf

"State for the 15 puzzle"
struct State
  # Stored an 1D-array with entries 1..16
  # The first four entries are the first row, etc.
  # 16 represents the empty square
  ordering::Array{Int, 1}   
end

"Create State instance for the solved state"
initial() = State(collect(1:16))

"Create a random state by performing numMoves random moves"
function initial(numMoves::Int)
  state = initial()
  for repeat in 1:numMoves
    state = result(state, rand(actions(state)))
  end
  return state
end

"Action for the 15 puzzle"
struct Action
  # U, D, L, or R for direction to move a tile into empty spot
  direction::Char
end

"Return possible actions from a given state"
function actions(state::State)
  # Array of possible actions
  possible = Action[]
  
  # Find the row and column of the empty location
  emptyLocation = findfirst(isequal(16), state.ordering)
  row = (emptyLocation+3) ÷ 4
  col = (emptyLocation-1) % 4 + 1
  
  if row > 1
    push!(possible, Action('D'))
  end
  if row < 4
    push!(possible, Action('U'))
  end
  if col > 1
    push!(possible, Action('R'))
  end
  if col < 4
    push!(possible, Action('L'))
  end
  
  return possible
end

"Return the result of applying the action to the state"
function result(state::State, action::Action)
  # Find the row and column of the empty location
  emptyLocation = findfirst(isequal(16), state.ordering)
  row = (emptyLocation+3) ÷ 4
  col = (emptyLocation-1) % 4 + 1
  
  # Copy the array storing the tile locations to modify
  ordering = copy(state.ordering)
  
  # Find the index of the location that the empty
  # tile will be moved to
  newLocation = 0
  if action.direction == 'U'
    newLocation = 4*row+col-4+4
  elseif action.direction == 'D'
    newLocation = 4*row+col-4-4
  elseif action.direction == 'L'
    newLocation = 4*row+col-4+1
  else
    newLocation = 4*row+col-4-1
  end
  
  # Swap the entires of the current and future location of the
  # empty location
  entry = ordering[newLocation]
  ordering[emptyLocation] = entry
  ordering[newLocation] = 16
  
  return State(ordering)
end

"Return the result of applying a sequence of moves represented as a string"
function result(state::State, sequence::String)
  for action in sequence
    state = result(state, Action(action))
  end
  return state
end

"There is no cost"
function cost(state::State, action::Action)
  return 0
end

"Check if the terminal state is reached by seeing if the tiles are in the solved state"
function terminal(state::State)
  return state.ordering == collect(1:16)
end

"There is no score for this puzzle"
function score(state::State)
  return 0
end

"This is a single player game"
function player(state::State)
  return 1
end

"Display the state"
function show(io::IO, state::State)
  for row in 1:4
    for col in 1:4
      entry = state.ordering[4*row+col-4]
      if entry != 16
        @printf(io, "%3d", entry)
      else
        print(io, "   ")
      end
    end
    
    if row < 4
      println(io)
    end
  end
end

"Display the action"
function show(io::IO, action::Action)
  print(io, action.direction)
end
