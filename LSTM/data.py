import csv
import glob

import numpy as np
import torch
from transformers import AutoModel, AutoTokenizer

phobert = AutoModel.from_pretrained("vinai/phobert-base")
tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base")


def load_data(path, labelAMR, labelPOS, phoBert):
    text_files = glob.glob(f"{path}/*.conllu")
    input_data = []
    output_data = []

    for fpath in text_files:
        with open(fpath, 'r', encoding='utf-8') as file:
            ip = []
            op = []
            for line in file:
                line = line.strip('\n')
                if len(line) != 0:
                    if '# text =' not in line:
                        ln = line.split('\t')
                        row = [int(ln[0])] + phoBert[ln[1]] + [labelPOS[ln[4].upper()]]
                        ip.append(row)
                        idx = int(ln[6]) if ln[6] != '_' else 0
                        op.append([idx, labelAMR[ln[7]]])
                else:
                    input_data.append(ip)
                    output_data.append(op)
                    ip = []
                    op = []

            if len(ip) != 0 and len(op) != 0:
                input_data.append(ip)
                output_data.append(op)

    return input_data, output_data


def loadLabel(path):
    label = {}
    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip('\n')
            if line not in label:
                label[line] = len(label) + 1
    result = {key: value / len(label) for key, value in label.items()}
    return result


def loadPhoBert(path):
    label = {}
    with open(path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip('\n')
            row = line.split('[')
            text = row[0].replace('\t', '')
            pBert = row[1:][0].replace(']', '').split(',')
            pBert = list(map(float, pBert))
            if text not in label:
                label[text] = pBert
    return label


def replace_text_to_number(data, f, text):
    input_ids = torch.tensor([tokenizer.encode(data)])
    with torch.no_grad():
        features = phobert(input_ids)
        if data not in text:
            f.writelines(data + "\t" + str(features[1][0].tolist()) + "\n")
            text.append(data)


def phoBertToFile(path, filePath):
    text_files = glob.glob(f"{path}/*.conllu")
    text = []
    f = open(filePath, "w", encoding="UTF-8", newline='')
    for fpath in text_files:
        with open(fpath, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip('\n')
                if len(line) != 0:
                    if '# text =' not in line:
                        ln = line.split('\t')
                        replace_text_to_number(ln[1], f, text)


def getKeyFromValue(key_list, val_list, value):
    if value in val_list:
        pos = val_list.index(value)
        return key_list[pos]
    return 0


def writeData(filePath, data_x, data_y, phoBert, labelPos, labelAMR):
    key_phoBert = list(phoBert.keys())
    val_phoBert = list(phoBert.values())
    key_pos = list(labelPos.keys())
    val_pos = list(labelPos.values())
    key_amr = list(labelAMR.keys())
    val_amr = list(labelAMR.values())
    with open(filePath, "w", encoding="utf-8", newline='') as data_converted:
        data_writer = csv.writer(data_converted, delimiter="\t")
        for i in range(0, len(data_x)):
            data_writer.writerow(["# id = " + str(i)])
            seq = data_x[i]
            seq_out = data_y[i]
            for j in range(len(seq)):
                row = seq[j]
                if row[0] != 0.0:
                    idx = j + 1
                    phoBert_value = list(row[1:len(row) - 1])
                    text = getKeyFromValue(key_phoBert, val_phoBert, phoBert_value)
                    if text == "\"":
                        text = "\'\'"
                    pos_value = row[len(row) - 1]
                    pos = getKeyFromValue(key_pos, val_pos, pos_value)
                    id_y = int(seq_out[j][0])
                    if id_y == 0:
                        id_y = '_'
                    amr = getKeyFromValue(key_amr, val_amr, seq_out[j][1])
                    row = [idx, text, '_', '_', pos, '_', id_y, amr, '_', '_']
                    data_writer.writerow(row)
                else:
                    break
            data_writer.writerow("")


if __name__ == "__main__":
    phoBertToFile('./data', './data/phoBert.txt')
    labelPhoBert = loadPhoBert('./data/phoBert.txt')
