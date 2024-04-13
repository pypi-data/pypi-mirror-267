import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.autograd import grad

class BatchIntegratedGradients:
    def __init__(self, model):
        self.model = model

    def preds_and_grads(self, inputs, baselines=None, n_steps=500, target=1):
        if baselines is None:
            baselines = torch.zeros_like(inputs)

        alphas = torch.linspace(0, 1, n_steps).tolist()

        scaled_features = tuple(
            torch.cat(
                [baseline + alpha * (input - baseline) for alpha in alphas], dim=0
            ).requires_grad_()
            for input, baseline in zip(inputs, baselines)
        )

        preds = self.model(scaled_features[0])[:, target]
        grads = grad(outputs=torch.unbind(preds), inputs=scaled_features)

        return preds, grads

    def BatchIG_Values(self, inp_idx, data, time_steps, n_steps):
        inp = []
        i = 0
        while i <= time_steps:
            inp.append([data[inp_idx + i : inp_idx + i + 1]])
            i += 1
        batch_gradients = []
        preds = []
        time_interval_gradients = []
        for i in range(len(inp) - 1):
            a, b = self.preds_and_grads(inp[i + 1], baselines=inp[i], n_steps=n_steps)
            batch_gradients.append(b[0].mean(0) * (np.array(inp[i + 1][0]) - np.array(inp[i][0])))
            time_interval_gradients.append(b[0])
            preds.append(a)
        return batch_gradients, preds, time_interval_gradients

    @staticmethod
    def SummaryPlot(tensor_data, feature_names, feature_indices):
        average_values = []
        colors = []
        for index in feature_indices:
            feature_data = []
            for tensor in tensor_data:
                transposed_tensor = tensor.T
                feature_data.extend(transposed_tensor[index])
            average_value = np.sum(feature_data)
            average_values.append(average_value)
            if average_value >= 0:
                colors.append('green')
            else:
                colors.append('red')

        plt.rcParams.update({'font.size': 19, 'font.weight': 'bold'})
        plt.figure(figsize=(56, 16))
        plt.bar(np.arange(len(feature_indices)), average_values, color=colors,
                tick_label=[feature_names[i] for i in feature_indices])
        plt.xlabel('Selected Features', fontsize=40)
        plt.ylabel('Average Gradient Value', fontsize=40)
        plt.title('Batch Integrated Gradients: Summary Plot', fontsize=40)
        plt.show()

    @staticmethod
    def BGradientPlot(tensor_data, feature_names, feature_indices):
        all_data = [[] for _ in feature_indices]
        for tensor in tensor_data:
            transposed_tensor = tensor.T
            for i, index in enumerate(feature_indices):
                all_data[i].extend(transposed_tensor[index])

        for i, data in enumerate(all_data):
            plt.plot(data, label=feature_names[feature_indices[i]])

        plt.rcParams.update({'font.size': 6, 'font.weight': 'bold'})
        plt.legend()
        plt.xlabel('Riemann Steps')
        plt.ylabel('Gradient Value')
        plt.title('Batch Integrated Gradients: Gradient Plot')
        plt.show()