# -*- coding: utf-8 -*-
"""DeepLearner.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16TXzEgsQY7_DNLR4N1TUU5gxiJSLwgbu
"""

#Simple mnist digit recognition~Hello world

#importinf data


import tensorflow as tf
from keras.datasets import mnist

(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

# viewing train/test data



train_images.shape

test_images.shape

train_labels.dtype

test_labels

#Building the architecture

from keras import models
from keras import layers


network = models.Sequential()
network.add(layers.Dense(512, activation='relu', input_shape=(28 * 28,)))
network.add(layers.Dense(10, activation='softmax'))

#optimizer,loss and metrics functions

network.compile(optimizer='rmsprop',

loss='categorical_crossentropy',
metrics=['accuracy'])

# Reshaping the data to conform with the model's specification  and normalizing the image data from 0-255 to 0-1


train_images = train_images.reshape((60000, 28 * 28))
train_images = train_images.astype('float32') / 255
test_images = test_images.reshape((10000, 28 * 28))
test_images = test_images.astype('float32') / 255

#Preparing the labels
from tensorflow.keras.utils import to_categorical


train_labels = to_categorical(train_labels)
test_labels = to_categorical(test_labels)

# Training proceeds...
network.fit(train_images, train_labels, epochs=5, batch_size=128)

# Wow! the accuracy is high 0.99

# But this is for training, let's check the test accuracy...


test_loss, test_acc = network.evaluate(test_images, test_labels)
print('test_acc:', test_acc)

# Ohh the training accuracy seems to be greater than the test one, overfitting is suspected!

### Tensors

#let's look at the previous data
from keras.datasets import mnist
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

train_images.ndim

train_images.shape

train_images.dtype

# we can see that iur tensor has 60000 matrics of 28 by 28 integers and the type is 8-bit

# Let's display an image from the digits

digit = train_images[5]
import matplotlib.pyplot as plt
plt.imshow(digit, cmap=plt.cm.binary)
plt.show()

# Slicing tensor to get digits #10 to #100 (#100 isn’t included) and puts
#them in an array of shape (90, 28, 28):

my_slice = train_images[10:100]
print(my_slice.shape)

# Applying relu function on a 2D tensor x

def naive_relu(x):
  assert len(x.shape) == 2
  x = x.copy() #to avoid overwriting the original tensor
  for i in range(x.shape[0]):
    for j in range(x.shape[1]):
      x[i, j] = max(x[i, j], 0)
  return x

# Naive tensor addition

def naive_add(x, y):
  assert len(x.shape) == 2
  assert x.shape == y.shape

  x = x.copy()
  for i in range(x.shape[0]):
    for j in range(x.shape[1]):
      x[i, j] += y[i, j]
  return x

## Advanced method
import numpy as np
x=np.array([3,2])
y=np.array([1,2])

z=x+y #element-wise addition of two numpy arrays
z=np.max(z,0)  #element-wise relu

print(z)

#print(q)

########################################################
####### Binary movie rating classification example #####
########################################################




#we'll keep the top 10000 most frequently occouring words in the training data
from keras.datasets import imdb
(train_data, train_labels), (test_data, test_labels) = imdb.load_data(
num_words=10000)

# Decoding the review into english

word_index = imdb.get_word_index()
reverse_word_index = dict(
[(value, key) for (key, value) in word_index.items()])
decoded_review = ' '.join(
[reverse_word_index.get(i - 3, '?') for i in train_data[0]])
print(decoded_review)

#Encoding the integer sequences into a binary matrix

#Creates an all-zero matrix of shape (len(sequences),dimension)

import numpy as np

def vectorize_sequences(sequences, dimension=10000):
  results = np.zeros((len(sequences), dimension))

  #Set specific indices of results[i] to 1s

  for i, sequence in enumerate(sequences):
    results[i, sequence] = 1.
  return results

  # encoding the train and test data

x_train = vectorize_sequences(train_data)
x_test = vectorize_sequences(test_data)

# Let's view our encoded data


x_train[0]

# Vectorizing the labes which are originally 0s and 1s

y_train = np.asarray(train_labels).astype('float32')
y_test = np.asarray(test_labels).astype('float32')

# Model definiton 

from keras import models
from keras import layers
model = models.Sequential()
model.add(layers.Dense(32, activation='relu', input_shape=(10000,)))
model.add(layers.Dense(32, activation='relu'))
model.add(layers.Dense(32, activation='relu'))
model.add(layers.Dense(32, activation='relu'))
model.add(layers.Dense(32, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))

from tensorflow.keras import optimizers

model.compile(optimizer=optimizers.RMSprop(lr=0.001),

loss='binary_crossentropy',
metrics=['accuracy'])

# Validating the model

x_val = x_train[:10000]
partial_x_train = x_train[10000:]

y_val = y_train[:10000]
partial_y_train = y_train[10000:]

#  Training the model

model.compile(optimizer='rmsprop',
loss='binary_crossentropy',
metrics=['acc'])
history = model.fit(partial_x_train,
partial_y_train,
epochs=20,
batch_size=512,
validation_data=(x_val, y_val))

### Checking the hostory dictionary

history_dict = history.history
history_dict.keys()

## Plotting the training and validATION LOSS

import matplotlib.pyplot as plt
history_dict = history.history
loss_values = history_dict['loss']
val_loss_values = history_dict['val_loss']
acc= history_dict['acc']

epochs = range(1, len(acc) + 1)
plt.plot(epochs, loss_values, 'bo', label='Training loss')
plt.plot(epochs, val_loss_values, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

## Plotting the training and validATION acc


plt.clf()
acc_values = history_dict['acc']
val_acc_values = history_dict['val_acc']
plt.plot(epochs, acc_values, 'bo', label='Training acc')
plt.plot(epochs, val_acc_values, 'b', label='Validation acc')
plt.title('Training and validation accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

### We can see that the training loss is decreasing with increase in the epoch while the accuracy is increasing with increase in the epoch as expected.

## However, the validation loss tends to increase from epoch 4 and the training accuracy is also not increasing, 

## that's what we mentioned earlier 'Overfitting'. Let's retrain the model and fix this problem

#### Retraining woth only 4 epochs

model = models.Sequential()
model.add(layers.Dense(16, activation='relu', input_shape=(10000,)))
model.add(layers.Dense(16, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))
model.compile(optimizer='rmsprop',
loss='binary_crossentropy',
metrics=['accuracy'])

model.fit(x_train, y_train, epochs=4, batch_size=512)
results = model.evaluate(x_test, y_test)

results

### That gives a fair result with 88% accuracy, however, state-of-the-art techniques can help yield a better performance which we shall see in the near future

## Now let's save our model and use it to predict

model.save('mymodel.model')
new_model=tf.keras.models.load_model('mymodel.model')

prediction=model.predict(x_test)
print(prediction)

## The output are the likelihood of reviews being positive

####  Further experiment with different architecturing



#### Retraining woth only 4 epochs

model = models.Sequential()
model.add(layers.Dense(16, activation='relu', input_shape=(10000,)))
model.add(layers.Dense(16, activation='relu'))
model.add(layers.Dense(16, activation='relu'))
model.add(layers.Dense(16, activation='relu'))
model.add(layers.Dense(16, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))
model.compile(optimizer='rmsprop',
loss='binary_crossentropy',
metrics=['accuracy'])

model.fit(x_train, y_train, epochs=4, batch_size=512)
results = model.evaluate(x_test, y_test)

############### Classifying newswires: a multiclass classification example ##############

#classify Reuters newswires into 46(0 to 45) mutually exclusive topics.

from keras.datasets import reuters
(train_data, train_labels), (test_data, test_labels) = reuters.load_data(
num_words=10000)

train_data[10]

## Decoding the data

word_index = reuters.get_word_index()
reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])
decoded_newswire = ' '.join([reverse_word_index.get(i - 3, '?') for i in
train_data[0]])

train_labels[10]

## So 3 is the index

## Vectorizing the data

import numpy as np
def vectorize_sequences(sequences, dimension=10000):
  results = np.zeros((len(sequences), dimension))
  for i, sequence in enumerate(sequences):
    results[i, sequence] = 1.
  return results

x_train = vectorize_sequences(train_data)
x_test = vectorize_sequences(test_data)

#### Encoding the labels 

def to_one_hot(labels, dimension=46):
  results = np.zeros((len(labels), dimension))
  for i, label in enumerate(labels):
    results[i, label] = 1.
  return results
one_hot_train_labels = to_one_hot(train_labels)
one_hot_test_labels = to_one_hot(test_labels)

##### Or using the built-in keras function
from keras.utils.np_utils import to_categorical


one_hot_train_labels = to_categorical(train_labels)
one_hot_test_labels = to_categorical(test_labels)

#### Model definition

from keras import models
from keras import layers
model = models.Sequential()
model.add(layers.Dense(64, activation='relu', input_shape=(10000,)))
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(46, activation='softmax'))

## Compilation


model.compile(optimizer='rmsprop',loss='categorical_crossentropy', metrics=['accuracy'])

## Setting aside the validation set

x_val = x_train[:1000]
partial_x_train = x_train[1000:]
y_val = one_hot_train_labels[:1000]
partial_y_train = one_hot_train_labels[1000:]

#### Training


history = model.fit(partial_x_train,
partial_y_train,
epochs=20,
batch_size=512,
validation_data=(x_val, y_val))

########## Plotting the training and validation loss

import matplotlib.pyplot as plt
loss = history.history['loss']
val_loss = history.history['val_loss']
epochs = range(1, len(loss) + 1)
plt.plot(epochs, loss, 'bo', label='Training loss')
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

### Checking the hostory dictionary

history_dict = history.history
history_dict.keys()

########## Plotting the training and validation accuracy

plt.clf()
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
plt.plot(epochs, acc, 'bo', label='Training acc')
plt.plot(epochs, val_acc, 'b', label='Validation acc')
plt.title('Training and validation accuracy')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

## we notice that the model starts overfitting after 9 epochs, let's try another one

model = models.Sequential()
model.add(layers.Dense(64, activation='relu', input_shape=(10000,)))
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(46, activation='softmax'))
model.compile(optimizer='rmsprop',

loss='categorical_crossentropy',
metrics=['accuracy'])
model.fit(partial_x_train,
partial_y_train,
epochs=9,
batch_size=512,
validation_data=(x_val, y_val))
results = model.evaluate(x_test, one_hot_test_labels)
results

##### Accuracy reaches ~80%

#### Predictions


predictions = model.predict(x_test)

predictions[0].shape

np.sum(predictions[0])

##The sum of predictions is 1 because it is the likehood for each class

## Now to find the class predicted, it is the class with maximum likelihood predicted as follows

np.argmax(predictions[0])

#### So 3 is predicted

#### Alternative way of encoding the labels as integer tensor

y_train = np.array(train_labels)
y_test = np.array(test_labels)


##we therefore use sparse_categorical_crossentropy loss because the numbers are integers not categorical as they were before

#######################################################
#####  Regression (Predicting house prices) ###########
#######################################################

#### Loading the Boston house data

from keras.datasets import boston_housing
(train_data, train_targets), (test_data, test_targets) = boston_housing.load_data()

train_data.shape

test_data.shape

train_targets

train_data[0]

###Normalizing the data since the features have different scales


mean = train_data.mean(axis=0)
train_data -= mean
std = train_data.std(axis=0)
train_data /= std
test_data -= mean
test_data /= std

###  Model definition
from keras import models
from keras import layers
def build_model():
  model = models.Sequential()
  model.add(layers.Dense(64, activation='relu',

  input_shape=(train_data.shape[1],)))

  model.add(layers.Dense(64, activation='relu'))
  model.add(layers.Dense(1))
  model.compile(optimizer='rmsprop', loss='mse', metrics=['mae'])
  return model

#### VAlidation using K-fold valiation technique



import numpy as np

k=4
num_val_samples = len(train_data) // k
num_epochs = 100
all_scores = []


#preparing validation data 


for i in range(k):
  print('processing fold #', i)
  val_data = train_data[i * num_val_samples: (i + 1) * num_val_samples]
  val_targets = train_targets[i * num_val_samples: (i + 1) * num_val_samples]

  # preparing training training data from all partitions

  partial_train_data = np.concatenate(
  [train_data[:i * num_val_samples],
  train_data[(i + 1) * num_val_samples:]],
  axis=0)
  partial_train_targets = np.concatenate(
  [train_targets[:i * num_val_samples],
  train_targets[(i + 1) * num_val_samples:]],
  axis=0)
  ##build model

  model = build_model()

  ##train model
  model.fit(partial_train_data, partial_train_targets,
  epochs=num_epochs, batch_size=1, verbose=0)
  val_mse, val_mae = model.evaluate(val_data, val_targets, verbose=0)
  all_scores.append(val_mae)

all_scores

### Hence the average validation score is

np.mean(all_scores)

#### Saving the validation logs at each fold 

num_epochs = 500
all_mae_histories = []
for i in range(k):

  print('processing fold #', i)
  val_data = train_data[i * num_val_samples: (i + 1) * num_val_samples]
  val_targets = train_targets[i * num_val_samples: (i + 1) * num_val_samples]
  partial_train_data = np.concatenate(
  [train_data[:i * num_val_samples],
  train_data[(i + 1) * num_val_samples:]],
  axis=0)

  partial_train_targets = np.concatenate(
  [train_targets[:i * num_val_samples],
  train_targets[(i + 1) * num_val_samples:]],
  axis=0)
  model = build_model()
  history = model.fit(partial_train_data, partial_train_targets,
  validation_data=(val_data, val_targets),
  epochs=num_epochs, batch_size=1, verbose=0)

mae_history = history.history['val_mae']
  all_mae_histories.append(mae_history)

### Building history of successive mean k-fold validation scores 

average_mae_history = [
np.mean([x[i] for x in all_mae_histories]) for i in range(num_epochs)]

#####  Plotting vaildation scores


import matplotlib.pyplot as plt
plt.plot(range(1, len(average_mae_history) + 1), average_mae_history)
plt.xlabel('Epochs')
plt.ylabel('Validation MAE')
plt.show()

###### Not well visualized, let's remove the first 10 points that have different scales and smooth the curve

def smooth_curve(points, factor=0.9):
  smoothed_points = []
  for point in points:
    if smoothed_points:
      previous = smoothed_points[-1]
      smoothed_points.append(previous * factor + point * (1 - factor))
    else:
      smoothed_points.append(point)
  return smoothed_points





smooth_mae_history = smooth_curve(average_mae_history[10:])
plt.plot(range(1, len(smooth_mae_history) + 1), smooth_mae_history)
plt.xlabel('Epochs')
plt.ylabel('Validation MAE')
plt.show()

### Let's do the final training of the model

model = build_model()
model.fit(train_data, train_targets,
epochs=80, batch_size=16, verbose=0)
test_mse_score, test_mae_score = model.evaluate(test_data, test_targets)

test_mae_score

###  Hold-out  validation

num_validation_samples = 10000
np.random.shuffle(data)
validation_data = data[:num_validation_samples]
data = data[num_validation_samples:]
training_data = data[:]
model = get_model()
model.train(training_data)
validation_score = model.evaluate(validation_data)
# At this point you can tune your model,
# retrain it, evaluate it, tune it again...
model = get_model()
model.train(np.concatenate([training_data,
validation_data]))
test_score = model.evaluate(test_data)

##### K-fold validation

k=4
num_validation_samples = len(data) // k
np.random.shuffle(data)
validation_scores = []


for fold in range(k):
  validation_data = data[num_validation_samples * fold:
  num_validation_samples * (fold + 1)]
  training_data = data[:num_validation_samples * fold] +
  data[num_validation_samples * (fold + 1):]
  model = get_model()
  model.train(training_data)
  validation_score = model.evaluate(validation_data)
  validation_scores.append(validation_score)

validation_score = np.average(validation_scores)
model = get_model()
model.train(data)
test_score = model.evaluate(test_data)

##########   Regularization using L2 norm



from keras import regularizers
model = models.Sequential()
model.add(layers.Dense(16, kernel_regularizer=regularizers.l2(0.001),
activation='relu', input_shape=(10000,)))
model.add(layers.Dense(16, kernel_regularizer=regularizers.l2(0.001),

activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))

###########   Drop-out 


model = models.Sequential()
model.add(layers.Dense(16, activation='relu', input_shape=(10000,)))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(16, activation='relu'))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(1, activation='sigmoid'))

################   CNN     ########################

from keras import layers
from keras import models
model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))

model.summary()

##### Adding a clasifier on top of the CNN for a 10-way classification using a soft-max function


model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(10, activation='softmax'))

## new model looks like 

model.summary()

#### Training the CNN on MNIST 

from keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

train_images = train_images.reshape((60000, 28, 28, 1))
train_images = train_images.astype('float32') / 255
test_images = test_images.reshape((10000, 28, 28, 1))
test_images = test_images.astype('float32') / 255
train_labels = to_categorical(train_labels)
test_labels = to_categorical(test_labels)
model.compile(optimizer='rmsprop',
loss='categorical_crossentropy',
metrics=['accuracy'])
model.fit(train_images, train_labels, epochs=5, batch_size=64)

#########   Evaluating on the test set


test_loss, test_acc = model.evaluate(test_images, test_labels)

test_acc

###  Wow ! the accuracy is about 99%, that's better than the previuos one with the densely connected layers. That's because the CNN extracts more infromation from the image they extract local patterns unlike dense layers for global pattern