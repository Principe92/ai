import Base.show


"State for Nim"
struct State
    entries::Array{UInt, 1}
    player::UInt
end

"Create a new game of Nim"
function initial()
    array = [0,0,0]
    init = State(array, 1)

    for pile in 1:3
        num = rand(1:100)
        init.entries[pile] = num
    end

    return init
end


struct Action
    sticks::UInt #Number of sticks selected by a player
    pile::UInt #Selected pile
end


function actions(state::State)
    possible = Action[]

    for pile in 1:3
        if (state.entries[pile] > 0)
            # add pile eligible for selection
            push!(possible, Action(state.entries[pile], pile))
        end
    end

    return possible
end

function result(state::State, action::Action)
    entries = copy(state.entries)

    #remove sticks from pile
    entries[action.pile] -= action.sticks 

    return State(entries, 3-state.player)
end

function cost(state::State, action::Action)
    return 0
end

function terminal(state::State)
    if (score(state) != 0)
        return true
    else
        return false
    end
end

"Return 1 if no sticks available, else 0"
function score(state::State)
    
    for pile in 1:3
        if (state.entries[pile] > 0)
            # we still have piles left
            return 0
        end
    end

    return 1
end

function player(state::State)
    return state.player
end

function show(io::IO, state::State)
    
    for pile in 1:3
        piles = state.entries[pile]
        println(io, "Pile #$pile: $piles stick(s) left")
    end
end

function show(io::IO, action::Action)
    sticks = action.sticks
    pile = action.pile
    print(io, "$sticks stick(s) from Pile #$pile")
end