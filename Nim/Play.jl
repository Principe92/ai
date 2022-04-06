include("Nim.jl")

function play()
    current = initial()
    turn = 1
    println(current)

    while !terminal(current)
        println("Turn $turn")
        turn += 1

        nextPlayer = player(current)
        println("Player $nextPlayer to pick sticks")
        println()

        options = actions(current)

        println("Pick sticks from the following piles")

        for option in options
            pile = option.pile
            println("Pile $pile")
        end

        println()
        
        done = false
        pileIndex = 0
        sticks = 0

        #retrieve pile number
        while !done
            try
                print("Enter pile number (1-3): ")
                num = parse(Int, readline())

                if (isinteger(num) && num > 0 && num < 4)
                    pileIndex = num

                    #check pile can be selected
                    for option in options
                        if (option.pile == pileIndex)
                            done = true
                        end
                    end
                end
            catch
            end
        end

        done = false

        #retrieve number of sticks
        while !done
            try
                sticksLeft = 0;

                #find sticks sticks
                for option in options
                    if (option.pile == pileIndex)
                        sticksLeft = option.sticks
                    end
                end
                
                print("Enter number of sticks to pick (1 - $sticksLeft): ")
                num = parse(Int, readline())

                if (isinteger(num) && num > 0 && num <= sticksLeft)
                    sticks = num
                    done = true
                end
            catch
            end
        end


        action = Action(sticks, pileIndex)

        println("Player $nextPlayer picks $action")
        println()

        current = result(current, action)

        println(current)
    end

    if current.player == 1
        println("The winner is player 1!")
    else
        println("The winner is player 2!")
    end

end