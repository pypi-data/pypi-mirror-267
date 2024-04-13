import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score
from sklearn.preprocessing import LabelBinarizer
from io import BytesIO

class ModelEvaluator:
    @staticmethod
    def accuracy(y_true, y_pred):
        acc = accuracy_score(y_true, y_pred)
        print(f"Acurácia do modelo = {acc * 100.0:.2f}%")
        return acc

    @staticmethod
    def flatten_classification_report(report, prefix="", suffix=""):
        flat_report = {}
        for key, value in report.items():
            if isinstance(value, dict):
                for metric, metric_value in value.items():
                    new_key = f"{prefix} {key} {metric} {suffix}".strip()
                    flat_report[new_key] = metric_value
            else:
                new_key = f"{prefix} {key} {suffix}".strip()
                flat_report[new_key] = value
        return flat_report

    @staticmethod
    def classification_report_img_generator(y_true, y_pred):
        report = classification_report(y_true, y_pred, output_dict=True)
        report_df = pd.DataFrame(report).transpose()
        report_df = report_df.drop(columns=["support"])
        
        fig, ax = plt.subplots(figsize=(4, 3))
        sns.heatmap(report_df, cmap="Greens", linewidths=0.5, annot=True, ax=ax)
        ax.set_title("Classification Report")

        img = BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight')
        plt.close(fig)
        img.seek(0)
        return img, report

    @staticmethod
    def confusion_matrix_img_generator(y_true, y_pred):
        cnf_matrix = confusion_matrix(y_true, y_pred)
        report_df = pd.DataFrame(classification_report(y_true, y_pred, output_dict=True)).transpose()
        cnf_matrix_df = pd.DataFrame(cnf_matrix, index=report_df.index[:-3].values, columns=report_df.index[:-3].values)
        cnf_matrix_normalized = cnf_matrix_df / cnf_matrix_df.sum(axis=1).values[:, np.newaxis]

        fig, ax = plt.subplots()
        sns.heatmap(cnf_matrix_normalized, cmap="Greens", linecolor="white", linewidths=0.5, annot=True, fmt=".0%", cbar=False, square=True, ax=ax)
        ax.set_title("Confusion Matrix")

        img = BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight')
        plt.close(fig)
        img.seek(0)
        return img, cnf_matrix_normalized

    @staticmethod
    def roc_auc(y_true, y_pred):
        lb = LabelBinarizer()
        lb.fit(y_true)
        y_test = lb.transform(y_true)
        y_pred = lb.transform(y_pred)
        auc_roc = roc_auc_score(y_test, y_pred, average="weighted", multi_class="ovr")
        print(f"ROC_AUC do modelo = {auc_roc * 100.0:.2f}%")
        return auc_roc
