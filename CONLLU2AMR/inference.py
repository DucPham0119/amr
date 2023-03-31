from convertor.convertor import convert
from convertor.data import load_data, writeData


if __name__ == '__main__':
    path = './f8.conllu'
    outputPath = './amr_f8.txt'
    type_of_data = 'DP'
    data = load_data(path, type_of_data)
    amrs = []
    for d in data:
        text = d[0]
        dp = d[1]
        # print(dp)
        # print(text)
        amr = convert(text, dp)
        amrs.append(amr)

    # print(len(amrs))
    writeData(amrs, outputPath)
