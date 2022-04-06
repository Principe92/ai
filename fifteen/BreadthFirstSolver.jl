module BreadthFirstSolver

# Load the queue and appropriate functions from the DataStructures module
import DataStructures.Queue
import DataStructures.enqueue!
import DataStructures.dequeue!
import DataStructures.pop!
import DataStructures.size

# The State, Action and all of there methods are in the Main module
# and need to be loaded
using Main:  State, Action, actions, result, terminal

"Return a string represented the moves necessary to solve the puzzle"
function findSolution(state::State)
  if terminal(state)
    return ""
  end
  
  # To enact breadth-first search the frontier is stored in a queue
  frontier = Queue{State}()
  enqueue!(frontier, state)
  
  # For efficiency we will store the state that have either been
  # expored or added to the frontier in a Set.
  exploredOrFrontier = Set{State}([state])
  
  # To be able to reconstruct the path from the root of the tree,
  # which represents the initial state, and the solved state we need
  # to store how we get to each state.  The key will be a state
  # and the value stores that state and action that result is the
  # new state being added to the frontier.
  parent = Dict{State, Tuple{State, Action}}()
  
  while !isempty(frontier)
    currentState = dequeue!(frontier)
    
    for action in actions(currentState)
      newState = result(currentState, action)
      if !in(newState, exploredOrFrontier)
        parent[newState] = (currentState, action)
        
        if terminal(newState)
          # Build a path from the root to the start state
          path = ""
          current = newState
          while current in keys(parent)
            move = parent[current][2]
            path = string(move.direction, path)
            current = parent[current][1]
          end
          return path
        end
        
        enqueue!(frontier, newState)
        push!(exploredOrFrontier, newState)
        
      end
    end
  end
  
end
  
end
