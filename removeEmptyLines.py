with open('trainingWithLinebreaks.txt', 'r') as file:
    with open('trainingWithoutLinebreaks.txt', 'w') as resultFile:
        for line in file:
            if not line.isspace():
                resultFile.write(line)