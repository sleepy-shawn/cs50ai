import csv
import sys
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.impute import SimpleImputer

# Constants
TEST_SIZE = 0.4

def main():
    """
    Main function to load data, train a model, and evaluate its performance.
    """

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train the model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)

    # Evaluate the model
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print the results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate (Sensitivity): {100 * sensitivity:.2f}%")
    print(f"True Negative Rate (Specificity): {100 * specificity:.2f}%")



from sklearn.impute import SimpleImputer

def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).
    """
    # Map months to integers
    month_map = {
        'Jan': 0, 'Feb': 1, 'Mar': 2, 'Apr': 3, 'May': 4, 'June': 5,
        'Jul': 6, 'Aug': 7, 'Sep': 8, 'Oct': 9, 'Nov': 10, 'Dec': 11
    }
    with open (filename, mode="r") as f:
        reader = csv.DictReader(f)
        labels = []
        evidence = []
        for row in reader:
            evidence.append([int(row["Administrative"]),
                float(row["Administrative_Duration"]),
                int(row["Informational"]),
                float(row["Informational_Duration"]),
                int(row["ProductRelated"]),
                float(row["ProductRelated_Duration"]),
                float(row["BounceRates"]),
                float(row["ExitRates"]),
                float(row["PageValues"]),
                float(row["SpecialDay"]),
                month_map[row["Month"]],
                int(row["OperatingSystems"]),
                int(row["Browser"]),
                int(row["Region"]),
                int(row["TrafficType"]),
                1 if row["VisitorType"] == "Returning_Visitor" else 0,
                1 if row["Weekend"] == "TRUE" else 0])

            labels.append(1 if row ["Revenue"] == 'TRUE' else 0)



    return (evidence, labels)



def train_model(evidence, labels):
    """
    Train a k-nearest neighbor model (k=1) using the provided evidence and labels.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    """
    Evaluate the model's performance by calculating sensitivity and specificity.
    """
    # Count true positives and true negatives
    true_positive = sum(1 for actual, predicted in zip(labels, predictions) if actual == predicted == 1)
    true_negative = sum(1 for actual, predicted in zip(labels, predictions) if actual == predicted == 0)

    # Calculate totals
    total_positive = labels.count(1)
    total_negative = labels.count(0)

    # Calculate sensitivity (true positive rate) and specificity (true negative rate)
    sensitivity = true_positive / total_positive if total_positive else 0
    specificity = true_negative / total_negative if total_negative else 0

    return sensitivity, specificity


if __name__ == "__main__":
    main()
