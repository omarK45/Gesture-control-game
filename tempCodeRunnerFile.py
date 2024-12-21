
# Train the SVM
svm = SVC(kernel='rbf', C=1.0, gamma='scale')
svm.fit(X_train, y_train)

# Evaluate the SVM
print("Accuracy:", svm.score(X_test, y_test))