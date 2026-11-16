"""Static figures for the empirical report; no modeling or selection here."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import roc_curve, precision_recall_curve, confusion_matrix


def build_figures(output, models, probs, parts, selected, calibration):
    output = Path(output)
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
    labels = {"mode_baseline": "Baseline theo phương thức", "logistic_regression": "Logistic regression", "hist_gradient_boosting": "Histogram gradient boosting"}
    colors = ["#7b8793", "#197e8a", "#b45e32"]
    te = parts["test"]
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.7), constrained_layout=True)
    for (name, model), color in zip(models.items(), colors):
        p = probs[(name, "test")]
        fpr, tpr, _ = roc_curve(te.late_delivery_risk, p)
        precision, recall, _ = precision_recall_curve(te.late_delivery_risk, p)
        axes[0].plot(fpr, tpr, label=labels[name], color=color)
        axes[1].plot(recall, precision, color=color)
    axes[0].plot([0, 1], [0, 1], "--", color="#c2c7cb", linewidth=1)
    axes[1].axhline(te.late_delivery_risk.mean(), color="#c2c7cb", linestyle="--")
    axes[0].set(xlabel="Tỷ lệ cảnh báo sai", ylabel="Tỷ lệ phát hiện đơn trễ", title="ROC trên tập kiểm tra", xlim=(0, 1), ylim=(0, 1.02))
    axes[1].set(xlabel="Recall", ylabel="Precision", title="Precision và recall trên tập kiểm tra", xlim=(0, 1), ylim=(0, 1.02))
    axes[0].legend(loc="lower right", fontsize=8)
    fig.savefig(output / "figures/roc_pr_test.png", dpi=180)
    plt.close(fig)
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.7), constrained_layout=True)
    axes[0].plot([0, 1], [0, 1], "--", color="#b8bec3")
    axes[0].plot(calibration.mean_probability, calibration.late_rate, "o-", color="#197e8a")
    axes[0].set(xlabel="Xác suất dự báo trung bình", ylabel="Tỷ lệ trễ quan sát", title="Đối chiếu xác suất theo nhóm", xlim=(0, 1), ylim=(0, 1.02))
    cm = confusion_matrix(te.late_delivery_risk, probs[(selected, "test")] >= .5)
    axes[1].imshow(cm, cmap="Blues")
    for i in range(2):
        for j in range(2):
            axes[1].text(j, i, f"{cm[i,j]:,}", ha="center", va="center", color="white" if cm[i,j] > cm.max()*.5 else "black", fontsize=13)
    axes[1].set(xticks=[0, 1], yticks=[0, 1], xticklabels=["Không trễ", "Trễ"], yticklabels=["Không trễ", "Trễ"], xlabel="Dự báo", ylabel="Thực tế", title="Ma trận nhầm lẫn tại ngưỡng 0,5")
    fig.savefig(output / "figures/calibration_confusion_test.png", dpi=180)
    plt.close(fig)
