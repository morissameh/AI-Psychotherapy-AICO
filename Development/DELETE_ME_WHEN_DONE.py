from ML_MODEL import Model
model = Model()
model.load_pretrained()
print(model.Chain('Hello'))
# That was the model