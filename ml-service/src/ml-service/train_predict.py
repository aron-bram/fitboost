import predictor

embedding_model = predictor.download_embedding_model()

data = predictor.load_csv_data()

data = predictor.preprocess_data(data, embedding_model)

X_train, X_test, y_train, y_test = predictor.define_splits(data)

model = predictor.train(X_train, y_train)

accuracy = predictor.test(model, X_test, y_test)

prediction = predictor.predict(model, embedding_model)

predictor.write(model)
