"""
precision_recall_fscore_support: each relation type value, not total value.
classification_report: finally value
"""

from sklearn.metrics import precision_recall_fscore_support, accuracy_score, classification_report
import numpy as np

y_true = ['John', 'Jane', 'Bob', 'Paris', '代']
y_pred = ['John', 'Jane', 'Bob', 'New York', '刘']


"""
1、Macro
precision_recall_fscore_support: 单个类别各自的p、r、f1分数
"""
# 获取真实标签中的唯一类别（排除'New York'）
valid_labels = np.unique(y_true)

# 限定计算范围 + 定义零除处理
precision, recall, f1, _ = precision_recall_fscore_support(
    y_true, y_pred, 
    labels=valid_labels,  # 关键：仅计算真实存在的类别
    zero_division=0       # 安全处理零除
)
accuracy = accuracy_score(y_true, y_pred)

print("精度:", precision)  # 输出: [1. 1. 1. 0.]
print("召回率:", recall)   # 输出: [1. 1. 1. 0.]
print("F1:", f1)           # 输出: [1. 1. 1. 0.]
print("准确率:", accuracy) # 输出: 0.75



"""
2、Micro
"""
precision_micro, recall_micro, f1_micro, _ = precision_recall_fscore_support(
    y_true, y_pred, average='micro', zero_division=0
)
print(f"微平均精度: {precision_micro:.2f}")  # 0.75
print(f"微平均召回率: {recall_micro:.2f}")   # 0.75
print(f"微平均F1: {f1_micro:.2f}")         # 0.75



"""
3、最终p、r、f1
classification_report: 计算所有类别最终的p、r、f1分数
"""
measure_result = classification_report(y_true, y_pred, zero_division=0)
print(f"measure_result:\n {measure_result}")

"""
measure_result:
               precision    recall  f1-score   support

         Bob       1.00      1.00      1.00         1
        Jane       1.00      1.00      1.00         1
        John       1.00      1.00      1.00         1
    New York       0.00      0.00      0.00         0
       Paris       0.00      0.00      0.00         1

    accuracy                           0.75         4
   macro avg       0.60      0.60      0.60         4
weighted avg       0.75      0.75      0.75         4
"""


"""
4、分类任务混淆矩阵图形
"""
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
# matplotlib 中文支持
# import matplotlib.font_manager as fm
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题



# 1. 显式指定标签顺序
# labels = ['are', 'con', 'hon', 'ali', 'sup', 'val']
# cm = confusion_matrix(y_true, y_pred, labels=labels)
cm = confusion_matrix(y_true, y_pred)
# 2. 创建混淆矩阵的可视化对象
# disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
# 3. 生成混淆矩阵的图像, 可设置图形颜色
disp.plot(cmap=plt.cm.Blues)
# 4. 旋转x轴标签，提高可读性
plt.xticks(rotation=45) # x轴旋转45°
plt.yticks(rotation=0)  # y轴水平
# 5. 自动调整布局
plt.tight_layout()
# 6. 保存图片
plt.savefig('confusion-matrix-noDisplay-labels.png')

"""
说明：以上绘制的图片横坐标和纵坐标的关系标签是使用整数0/1/2/……代替的
如需使用真实relation type代替，则ConfusionMatrixDisplay()中需使用display_labels参数
"""

# 1. 显式指定标签顺序
labels = ['John', 'Jane', 'Bob', 'Paris', '代']
cm = confusion_matrix(y_true, y_pred, labels=labels)
# 2. 创建混淆矩阵的可视化对象
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
# 3. 生成混淆矩阵的图像, 可设置图形颜色
disp.plot(cmap=plt.cm.Blues)
# 4. 旋转x轴标签，提高可读性
plt.xticks(rotation=90, fontsize=10)    # x轴旋转45°，字体大小10
plt.yticks(rotation=0, fontsize=10)     # y轴水平
plt.title(f"confusion_matrix")           # 标题

# 5. 自动调整布局
plt.tight_layout()
# 6. 保存图片
plt.savefig('confusion-matrix-display-labels.png')