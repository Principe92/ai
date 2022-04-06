module pokorie


import DataStructures.PriorityQueue
import DataStructures.enqueue!
import DataStructures.dequeue!
import DataStructures.pop!
import DataStructures.size

using Main:  State, Action, actions, result, terminal

function manhattanDistance(state::State)

    misplaced = 0

    for index in 1:16
        tile = state.ordering[index]
        if (tile != index && tile != 16)
            row1 = div((index + 3), 4)
            col1 = (index - 1) % 4 + 1
            row2 = div((tile + 3), 4)
            col2 = (tile - 1) % 4 + 1
            misplaced += abs(row2 - row1) + abs(col2 - col1)

            if (misplaced > 1)
                misplaced += linearConflict(state, index)
            end
        end
    end

    return misplaced
end

function linearConflict(state::State, index::Int)

    row = div((index + 3), 4)
    col = (index - 1) % 4 + 1

    misplaced = 0

    tileAtIndex = state.ordering[index]

    # look at rows
    for i in 1:4
        tileIndex = (4 * (row-1)) + i

        if (tileIndex != index && tileIndex != 16)
            tileAtPosition = state.ordering[tileIndex]

            # Tile is in wrong position, but should be at position
            if (tileAtPosition != tileIndex && tileAtPosition == index && tileAtIndex == tileIndex)
                misplaced += 1
            end
        end
    end

    # look at columns
    for i in 1:4
        tileIndex = (4 * (i-1)) + col

        if (tileIndex != index && tileIndex != 16)
            tileAtPosition = state.ordering[tileIndex]

            # Tile is in wrong position, but should be at position
            if (tileAtPosition != tileIndex && tileAtPosition == index && tileAtIndex == tileIndex)
                misplaced += 1
            end
        end
    end

    return misplaced
end

"Return a string represented the moves necessary to solve the puzzle"
function findSolution(state::State)
  if terminal(state)
    return ""
  end
  
  # To enact a* breadth-first search the frontier is stored in a priority queue
  frontier = PriorityQueue{Tuple{State,Int},Int}()
  enqueue!(frontier, (state, 0), 0)
  
  # For efficiency we will store the state that have either been
  # expored or added to the frontier in a Set.
  exploredOrFrontier = Set{State}([state])
  
  # To be able to reconstruct the path from the root of the tree,
  # which represents the initial state, and the solved state we need
  # to store how we get to each state.  The key will be a state
  # and the value stores that state and action that result is the
  # new state being added to the frontier.
  parent = Dict{State,Tuple{State,Action}}()
  
  while !isempty(frontier)

    data = dequeue!(frontier)
    currentState = data[1]
    depth = data[2]

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

        newDepth = depth + 1;

        h = manhattanDistance(newState)
        f = h + newDepth
        
        enqueue!(frontier, (newState, newDepth), f)
        push!(exploredOrFrontier, newState)
        
      end
    end
  end
  
end
  
end
