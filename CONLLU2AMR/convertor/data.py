def load_data(path, type_of_data):
    data = []
    with open(path, 'r', encoding='utf-8') as file:
        if type_of_data == 'DP':
            dp = []
            text = ''
            for line in file:
                line = line.strip('\n')
                if len(line) != 0:
                    if '# text =' in line:
                        text = line.replace('# text = ', '')
                    else:
                        dp.append(line.split('\t'))
                else:
                    data.append([text, dp])
                    dp = []
                    text = ''

            if len(dp) != 0 and text != '':
                data.append([text, dp])
        if type_of_data == 'AMR':
            print('This option is developing')
    return data


def writeData(amrs, outputPath):
    with open(outputPath, "w", encoding="utf-8", newline='') as data_converted:
        for text in amrs:
            data_converted.writelines('# text = ' + text[0] + '\n')
            amr = text[1].split('\n')
            for i in amr:
                data_converted.writelines(i + '\n')
            data_converted.writelines('\n')


if __name__ == '__main__':
    path = '/home/dao/PycharmProjects/AMR/DP2AMR/new_dp_amr.conllu'
    data = load_data(path, 'DP')
    for d in data:
        print(d)
