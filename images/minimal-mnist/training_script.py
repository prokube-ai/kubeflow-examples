import click
from sklearn import datasets, svm, metrics
from sklearn.model_selection import train_test_split
from datetime import datetime, timezone


@click.command()
@click.option("--gamma", default=0.001, type=float)
@click.option("--c", default=1.0, type=float)
@click.option("--kernel", default="rbf", type=str)
@click.option("--degree", default=3, type=int)
@click.option("--coef0", default=0.0, type=float)
def train_svm(gamma: float, c: float, kernel: str, degree: int, coef0: float) -> None:
    """Train an SVM model on the MNIST dataset using specified hyperparameters.

    Args:
        gamma (float): Kernel coefficient for 'rbf', 'poly', and 'sigmoid' kernels.
        c (float): Regularization parameter. The strength of the regularization is inversely
                   proportional to C. Must be strictly positive.
        kernel (str): Specifies the kernel type to be used in the algorithm. Can be 'linear',
                      'poly', 'rbf', 'sigmoid', or a custom kernel function.
        degree (int): Degree of the polynomial kernel function ('poly'). Ignored by all other
                      kernels.
        coef0 (float): Independent term in kernel function. It is only significant in 'poly'
                       and 'sigmoid'.
    """
    # Load the MNIST dataset
    digits = datasets.load_digits()

    # Split into training, validation, and test sets
    X_train, X_temp, y_train, y_temp = train_test_split(
        digits.data, digits.target, test_size=0.4, random_state=42
    )
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.5, random_state=42
    )

    # Create the SVM classifier with specified hyperparameters
    clf = svm.SVC(C=c, kernel=kernel, gamma=gamma, degree=degree, coef0=coef0)

    # Train the model
    clf.fit(X_train, y_train)

    # Make predictions and evaluate on the training set
    y_train_pred = clf.predict(X_train)
    train_accuracy = metrics.accuracy_score(y_train, y_train_pred)

    # Make predictions and evaluate on the validation set
    y_val_pred = clf.predict(X_val)
    val_accuracy = metrics.accuracy_score(y_val, y_val_pred)

    # Make predictions and evaluate on the test set
    y_test_pred = clf.predict(X_test)
    test_accuracy = metrics.accuracy_score(y_test, y_test_pred)

    # Print to std out for katib
    timestamp = (
        datetime.now().astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
        + "Z"
    )
    print(f"{timestamp} Train-Accuracy={train_accuracy:.2f}")
    print(f"{timestamp} Validation-Accuracy={val_accuracy:.2f}")
    print(f"{timestamp} Test-Accuracy={test_accuracy:.2f}")


if __name__ == "__main__":
    train_svm()
