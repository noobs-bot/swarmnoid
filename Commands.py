from Move_Direction import command_bot

def main():
    bot1_pick_path = {1: [(3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8)]}
    bot1_return_path = {1: [(3, 8), (3, 7), (3, 6), (3, 5), (3, 4), (3, 3), (3, 2), (3, 1)]}
    
    print("Picking the oraganic waste")
    print(command_bot(bot1_pick_path))
    
    print("taking the waste to location")
    print(command_bot(bot1_return_path))


if __name__ == "__main__":
    main()
