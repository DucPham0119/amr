import csv


def readDataAMR(AMRPath):
    sentences = []
    sentence = []
    f = open(AMRPath, 'r', encoding='utf-8')
    data = f.readlines()
    for row in data:
        if not row.startswith('#') and row.strip():
            words = row.split()
            # chuyển (t ----thành---> (
            # chuyển t) ----thành---> t )
            i = 0
            count = 0
            while i < len(words):
                if '(' in words[i]:
                    words[i] = '('
                    i += 1
                elif len(words[i]) > 1 and ')' in words[i]:
                    words[i] = words[i].replace(')', '', 1)
                    count += 1
                else:
                    i += 1
            for i in range(0, count):
                words.insert(len(words), ')')
            # tách từ
            index = 0
            for i in range(0, len(words)):
                if words[i] == '/':
                    index = i
                    break
                if words[i] == '-':
                    words[i] = 'không'
            word = ''
            k = 0
            for i in range(index + 1, len(words)):
                if words[i] == ')':
                    k = i
                    break
                word += words[i] + " "
            # ko lay /
            if index == 0: index += 1
            start = words[0:index]
            if word != '':
                start.insert(index, word.strip())
            end = words[k:len(words)] if k else []
            words = start + end
            sentence += words
        elif not row.strip():
            sentences.append(sentence)
            sentence = []

    if len(sentence) > 0:
        sentences.append(sentence)
    return sentences


def readDP(DPPath):
    f = open(DPPath, 'r', encoding='utf-8')
    data = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE)
    # print(data)
    words = []
    word = []
    dp = []
    dps = []
    for row in data:

        if len(row) > 0 and row[0] and '#' not in row[0]:
            word.append(row[1])
            dp.append(row[4])
        elif len(row) <= 0:
            words.append(word)
            word = []
            dps.append(dp)
            dp = []
    if len(word) > 0:
        words.append(word)
        dps.append(dp)
    return words, dps


def convert(sentences, words):
    punctuation = []
    wd = []
    label = []
    result = []
    DP = []
    for i in range(0, len(sentences)):
        text = sentences[i]
        res = []
        dp = []
        for j in range(0, len(words[i])):
            res.append('_')
            dp.append('_')
        for idex in range(0, len(text)):
            if text[idex] == '(':
                punctuation.append(text[idex])
            elif ':' in text[idex]:
                label.append(text[idex][1:])
                if 'mode-' in text[idex]:
                    wd.append('-' + str(len(words[i])))
            elif text[idex] == ')' and len(wd) > 1:
                punctuation.pop()
                w = wd.pop()
                w1 = wd[len(wd) - 1]
                w1_id = 0
                w_id = 0
                if w1 != 'không':
                    w1_id = int(w1.split('-')[-1])
                if w != 'không':
                    w_id = int(w.split('-')[-1])
                res[w_id - 1] = w1_id
                dp[w_id - 1] = label.pop() if len(label) > 0 else ''
            else:
                wd.append(text[idex])

        punctuation = []
        label = []
        wd = []
        result.append(res)
        DP.append(dp)
        res = []
        dp = []
    return result, DP


def writeData(res, label, dp, word, outputPath):
    with open(outputPath, "w", encoding="utf-8", newline='') as data_converted:
        data_writer = csv.writer(data_converted, delimiter="\t")

        for idSentence in range(0, len(res)):
            if "\"" in word[idSentence]:
                id = word[idSentence].index("\"")
                word[idSentence][id] = "\'\'"
            text = "# text = " + " ".join(word[idSentence])
            data_writer.writerow([text])
            for i in range(0, len(res[idSentence])):
                row = [(i + 1), word[idSentence][i], '_', '_', dp[idSentence][i], '_', res[idSentence][i],
                       label[idSentence][i], '_', '_']

                data_writer.writerow(row)
            data_writer.writerow("")


def main():
    amrPath = './data/amr.txt'
    dpPath = './data/dp.conllu'
    outputPath = './data/result_conllu.conllu'
    sentences = readDataAMR(amrPath)
    data, dps = readDP(dpPath)
    result, DP = convert(sentences, data)

    writeData(result, DP, dps, data, outputPath)
    print("convert AMR to CONLLU success!")


if __name__ == '__main__':
    main()
