import json

import dbpediaknowledge

if __name__ == '__main__':
    text = 'アメリカ合衆国'
    population = dbpediaknowledge.get_population(text)
    print(population)
