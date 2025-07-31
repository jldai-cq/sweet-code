import json
import matplotlib
import numpy as np

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, precision_recall_fscore_support
from sklearn.metrics import classification_report, precision_score, recall_score, f1_score

# 确保类别对齐
labels = ['are', 'con', 'hon', 'ali', 'sup', 'val']

y_true = []  # 真实关系标签
y_pred = []  # 预测关系标签
NULL_SAMPLES = 0    # 预测关系中不存在关系的样本数
RELATIONS = 6 # 关系类型数量

path = './results_final.json'
with open(path, 'r', encoding='utf-8') as file:
    data = json.load(file)
for item in data:
    gold_relation = item['triple']['relation']
    pred_relation = item['output']['relation']
    if pred_relation == 'NULL':
        NULL_SAMPLES += 1
    y_true.append(gold_relation)
    y_pred.append(pred_relation)

cm = confusion_matrix(y_true, y_pred, labels=labels)  # 显式指定标签顺序
# 创建混淆矩阵的可视化对象
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
# 生成混淆矩阵的图像, 可设置图形颜色
disp.plot(cmap=plt.cm.Blues)
# 旋转x轴标签，提高可读性
plt.xticks(rotation=45) # x轴旋转45°
plt.yticks(rotation=0)  # y轴水平
plt.tight_layout()  # 自动调整布局
plt.savefig('AgRel-2-confusion-matrix.png')


# 获取每个类别的precision/recall/f1/support
precision, recall, f1, support = precision_recall_fscore_support(y_true, y_pred, labels=labels, zero_division=0)
# 初始化字典存储 TP、FP、FN
results = {label: {'TP': 0, 'FP': 0, 'FN': 0} for label in labels}
# 通过 precision, recall 和 support 反推出 TP、FP 和 FN
for i, label in enumerate(labels):
    TP = int(support[i] * recall[i])  # recall = TP / (TP + FN)
    FN = support[i] - TP             # FN = 支持数 - TP
    FP = int(TP / precision[i]) - TP if precision[i] > 0 else 0  # precision = TP / (TP + FP)
    results[label]['TP'] = TP
    results[label]['FP'] = FP
    results[label]['FN'] = FN
    results[label]['support'] = support[i]

# 输出结果
ALL_TP = 0
ALL_SAMPLES = 0
for label in labels:
    ALL_TP += results[label]['TP']
    ALL_SAMPLES += results[label]['support']

micro_P = ALL_TP/(ALL_SAMPLES-NULL_SAMPLES) if ALL_SAMPLES-NULL_SAMPLES > 0 else 0
micro_R = ALL_TP/ALL_SAMPLES if ALL_SAMPLES > 0 else 0
micro_F1 = (2 * micro_P * micro_R) / (micro_P + micro_R) if (micro_P + micro_R) > 0 else 0

# 将结果保存到文本文件
with open('metrics.txt', 'w', encoding='utf-8') as f:
    f.write("----------------------------- 方法1-手动计算 -----------------------------\n")
    f.write("----------------------------- micro（微平均）-----------------------------\n")
    f.write(f"micro_P: {micro_P * 100:.2f}%\n")
    f.write(f"micro_R: {micro_R * 100:.2f}%\n")
    f.write(f"micro_F1: {micro_F1 * 100:.2f}%\n\n")

    f.write(f"micro_P: {micro_P :.2f}\n")
    f.write(f"micro_R: {micro_R :.2f}\n")
    f.write(f"micro_F1: {micro_F1 :.2f}\n\n")

    precision_score_average_Single = precision_score(y_true, y_pred, labels=labels, average=None, zero_division=0)
    recall_score_average_Single = recall_score(y_true, y_pred, labels=labels, average=None, zero_division=0)
    f1_score_average_Single = f1_score(y_true, y_pred, labels=labels, average=None, zero_division=0)
    macro_P = np.sum(precision_score_average_Single) / RELATIONS
    macro_R = np.sum(recall_score_average_Single) / RELATIONS
    macro_F1 = np.sum(f1_score_average_Single) / RELATIONS

    f.write("----------------------------- macro（宏平均）-----------------------------\n")
    f.write(f"macro_P: {macro_P * 100:.2f}%\n")
    f.write(f"macro_R: {macro_R * 100:.2f}%\n")
    f.write(f"macro_F1: {macro_F1 * 100:.2f}%\n\n")

    f.write(f"macro_P: {macro_P :.2f}\n")
    f.write(f"macro_R: {macro_R :.2f}\n")
    f.write(f"macro_F1: {macro_F1 :.2f}\n\n")

    f.write("----------------------------- 方法2-自动计算（classification_report）-----------------------------\n")
    # 方法2
    measure_result = classification_report(y_true, y_pred, labels=labels, zero_division=0)   # 计算macro需要labels去掉NULL
    # print('measure_result = \n', measure_result)
    f.write(f"measure_result: {measure_result}\n")