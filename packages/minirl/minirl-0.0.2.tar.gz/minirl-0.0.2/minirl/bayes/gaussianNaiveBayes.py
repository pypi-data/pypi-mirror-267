import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass

@dataclass
class GaussianNaiveBayes:
    features: np.ndarray
    labels: np.ndarray

    def likelihood(self, data: float, mean: float, var: float) -> float:
        """Calculates the Gaussian likelihoodof the data"""

        eps = 1e-4 # prevent division by zero

        coeff = 1 / np.sqrt(2* np.pi * var + eps) # \frac{1}{\sqrt{}2\piσ_y^2}
        expoent = np.exp(-np.square(data - mean)/(2 * var + eps)) # \exp(-\frac{(x_i-μ_y)^2}{2σ_y^2}

        return coeff * expoent

    def fit(self) -> None:
        """Fits the Gaussian Naive Bayes model"""

        self.unique_labels = np.unique(self.labels)

        """
        self.features =
        [
            [1, 2, 3], # label 0
            [4, 5, 6], # label 1
            [7, 8, 9]  # ...
        ]
        """

        self.params = []
        for label in self.unique_labels:
            label_features = self.features[self.labels == label]
            print(label_features)
            self.params.append([(col.mean(), col.var()) for col in label_features.T])

    def predict(self, features: np.ndarray) -> np.ndarray:
        """Predict inference using the Gaussian Naive Bayes model, Theorem: P(A | B) = P(B | A) * P(a) / P(B)"""

        num_samples, _ = features.shape
        predictions = np.empty(num_samples)
        for idx, feature in enumerate(features):
            posteriors = []
            for label_idx, label in enumerate(self.unique_labels):
                prior = (self.labels == label).mean()

                # likelihood - NAIVE assumption (independence)
                # P(a1, a2, a3 | label) = P(a1 | label) * P(a2 | label) * P(a3 | label)
                likelihood = np.prod(
                    [
                    self.likelihood(ft, m, v) for ft, (m, v)in zip(feature, self.params[label_idx])
                    ]
                )

                posteriors.append(prior * likelihood)

            predictions[idx] = self.unique_labels[np.argmax(posteriors)]

        return predictions


    def plot(self):
        pass

np.random.seed(42)

# Create random data
data = np.random.normal(loc=0, scale=1, size=(100, 2))
print(data)
labels = np.array([0]*50 + [1]*50)

# gnb = GaussianNaiveBayes(features=data, labels=labels)
# gnb.fit()
# gnb.predict(features=data)
