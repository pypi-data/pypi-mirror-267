import os
import matplotlib.pyplot as plt
os.environ["KERAS_BACKEND"] = "tensorflow"

import numpy as np
import random

import tensorflow as tf
import keras
from keras import layers
import matplotlib.pyplot as plt
import math

def one_point_crossover(parent1, parent2):
    """
        Applies one-point crossover to two parent arrays.

    A single crossover point is randomly selected on both parent arrays.
    Data beyond this crossover point is swapped between the parents to create two children.

    Args:
        parent1 (array-like): The first parent array.
        parent2 (array-like): The second parent array.

    Returns:
        numpy.ndarray: An array representing the first child.
    """
    parent1_tensor = tf.constant(parent1)
    parent2_tensor = tf.constant(parent2)

    child1 = tf.TensorArray(dtype=parent1_tensor.dtype, size=tf.size(parent1_tensor))

    departure_point = random.randint(0, tf.size(parent1_tensor))


    for i in range(departure_point):
        child1 = child1.write(i, parent1_tensor[i])

    for i in range(departure_point, tf.size(parent2_tensor)):
        child1 = child1.write(i, parent2_tensor[i])


    return child1.stack()

def several_points_crossover(parent1, parent2, number_points):
    """
    Applies several points crossover to two parent arrays.

    Multiple crossover points are randomly selected on both parent arrays.
    Data beyond each crossover point is swapped between the parents to create two children.

    Args:
        parent1 (array-like): The first parent array.
        parent2 (array-like): The second parent array.
        number_points (int): The number of crossover points.

    Returns:
        numpy.ndarray: An array representing the first child.

    """
    # Create tensors for the parents
    parent1_tensor = tf.constant(parent1)
    parent2_tensor = tf.constant(parent2)

    child1 = tf.TensorArray(dtype=parent1_tensor.dtype, size=len(parent1))
    # Randomly choose crossing points
    points = sorted(random.sample(range(1, len(parent1)), number_points))

    parent_iter = iter((parent2_tensor, parent1_tensor,parent2_tensor, parent1_tensor, parent2_tensor, parent1_tensor, parent2_tensor,parent1_tensor, parent2_tensor, parent1_tensor))

    current_parent = parent1_tensor

    for i, gene in enumerate(parent1_tensor):
        if i in points:
            current_parent = next(parent_iter)
        child1 = child1.write(i, gene if tf.reduce_all(tf.math.equal(current_parent, parent1_tensor)) else tf.gather(parent2_tensor, i))

    return child1.stack()

def several_points_crossover_v2(parent1, parent2):

    """
    Applies several points crossover to two parent arrays.

    For each index in the parent arrays, a random choice is made between the corresponding elements of
    the parents based on a randomly generated sequence of 1s and 2s.

    Args:
        parent1 (tf.Tensor): The first parent array.
        parent2 (tf.Tensor): The second parent array.

    Returns:
        list: A list representing the child array generated from crossover.

    """

    p1 = parent1.numpy()
    p2 = parent2.numpy()
    child = []
    where = [random.randint(1, 2) for _ in range(len(p1))]

    for i in range(len(p1)):
        if where[i]==1 :
            child.append(p1[i])
        else :
            child.append(p2[i])
    return child



def gaussian_noise_1(parent, mean, std, n):
    """
        Applies Gaussian noise to randomly selected points on both parent arrays.

    Args:
        parent (np.ndarray): Array representing the parent.
        mean (float): Mean of the Gaussian noise distribution.
        std (float): Standard deviation of the Gaussian noise distribution.
        n (int): Number of points to be randomly selected on each parent array.

    Returns:
        np.ndarray: Array representing the first child.

    """
    p = parent.numpy()
    noise = np.random.normal(mean, std, len(p))
    points = sorted(random.sample(range(len(p)), n))
    child = p[:]

    for i in range(len(p)):
        if i in points:
            child[i] += noise[i]
    return child


def mean_parents(parent1, parent2):
    """
 Compute the mean of the values of two parent arrays.

    Args:
        parent1 (np.ndarray): The first parent array.
        parent2 (np.ndarray): The second parent array.

    Returns:
        np.ndarray: An array representing the child with values equal to the mean of the values
                   of the corresponding parents.
    """

    p1 = parent1.numpy()
    p2 = parent2.numpy()
    child = []

    for i in range(len(p1)):
        child.append((p1[i]+p2[i])/2)

    return child


def mean_parents1(*parents):
    """
    Compute the mean of the values of the parents arrays.

    Args:
        *parents: Variable number of parent arrays.

    Returns:
        np.ndarray: An array representing the child with values equal to the mean of the values
                   of the corresponding parents.
   """
    num_parents = len(parents)
    child = np.zeros_like(parents[0].numpy())

    for parent in parents:
        p = parent.numpy()
        child += p

    child /= num_parents

    return child


def one_selection(parent, std, m):
    """
   Introduces Gaussian noise to the selected parent vector for decoding.

    Args:
        parent (np.ndarray): The encoded vector of the selected parent.
        std (float): Standard deviation of the Gaussian noise.
        m (float): Mean of the Gaussian noise.

    Returns:
        np.ndarray: A stack of 4 output vectors, each containing Gaussian noise introduced for decoding.

    Note:
   """

    output1 = gaussian_noise_1(parent, m, std+1, 30)
    output2 = gaussian_noise_1(parent, m, std+2, 30)/2
    output3 = gaussian_noise_1(parent, m, std+3, 30)/6
    output4 = gaussian_noise_1(parent, m, std+4, 30)/3

    x_modified = []
    x_modified.append(output1)
    x_modified.append(output2)
    x_modified.append(output3)
    x_modified.append(output4)

    x_to_decode = tf.stack(x_modified, axis = 0)

    return x_to_decode

def two_selections(parent1, parent2):
    """
    Introduces genetic operations to two selected parents for decoding.

    Args:
        parent1 (tf.Tensor): The first parent array.
        parent2 (tf.Tensor): The second parent array.

    Returns:
        tf.Tensor: A stack of 4 output tensors, each representing a genetic operation applied to the parents.

    """

    output1 = several_points_crossover_v2(parent1, parent2)
    output2 = one_point_crossover(parent1, parent2)
    output3 = mean_parents(parent1, parent2)
    output4 = several_points_crossover(parent1,parent2, 7)

    x_modified = []
    x_modified.append(output1)
    x_modified.append(output2)
    x_modified.append(output3)
    x_modified.append(output4)

    x_to_decode = tf.stack(x_modified, axis = 0)

    return x_to_decode

def multiple_selections(*parents):
    """
    Introduces genetic operations to multiple selected parents for decoding.

    Applies several genetic operations, including crossover and mutation, to pairs of selected parents.
    From each pair of parents, four outputs are generated using different genetic operations.
    Then, three outputs are randomly selected from all generated outputs, and the mean of all parents is calculated.
    The selected outputs and the mean of parents are stacked together for decoding.

    Args:
        *parents: Variable number of parent arrays.

    Returns:
        tf.Tensor: A stack of selected output tensors and the mean of all parent tensors.

    Note:
        This function assumes that all 'parents' are TensorFlow tensors.
    """

    outputs = []

    for parent1, parent2 in zip(parents[:-1], parents[1:]):
        output1 = several_points_crossover_v2(parent1, parent2)
        output2 = one_point_crossover(parent1, parent2)
        output3 = mean_parents(parent1, parent2)
        output4 = several_points_crossover(parent1, parent2, 7)

        outputs.extend([output1, output2, output3, output4])

    # Select 3 random elements from 'outputs' list + mean of all parents
    selected_outputs = random.sample(outputs, 3)
    selected_outputs.append(mean_parents1(*parents))


    x_to_decode = tf.stack(selected_outputs, axis=0)

    return x_to_decode


####################MAIN####################


if __name__ == "__main__":

    ## sampling class
    class Sampling(layers.Layer):

        def call(self, inputs):
            z_mean, z_log_var = inputs
            batch = tf.shape(z_mean)[0]
            print("Batch used in the Sampling function")
            print(batch)
            dim = tf.shape(z_mean)[1]
            epsilon = tf.random.normal(shape=(batch, dim))
            return z_mean + tf.exp(0.5 * z_log_var) * epsilon


    latent_dim = 1024


    ## encoder
    encoder_inputs = keras.Input(shape=(64, 64, 3))
    x = layers.Conv2D(32, 4, activation="relu", strides=2, padding="same")(encoder_inputs)
    x = layers.Conv2D(32, 3, activation="relu", padding="same")(x)
    x = layers.Conv2D(64, 4, activation="relu", strides=2, padding="same")(x)
    x = layers.Conv2D(64, 3, activation="relu", padding="same")(x)
    x = layers.Conv2D(128, 4, activation="relu", strides=2, padding="same")(x)
    x = layers.Conv2D(128, 3, activation="relu", padding="same")(x)
    x = layers.Conv2D(256, 4, activation="relu", strides=2, padding="same")(x)
    x = layers.Conv2D(256, 3, activation="relu", padding="same")(x)
    x = layers.Flatten()(x)
    x = layers.Dense(latent_dim, activation="relu")(x)
    z_mean = layers.Dense(latent_dim, name="z_mean")(x)
    z_log_var = layers.Dense(latent_dim, name="z_log_var")(x)
    z = Sampling()([z_mean, z_log_var])
    encoder = keras.Model(encoder_inputs, [z_mean, z_log_var, z], name="encoder")
    encoder.summary()

    ## decoder
    latent_inputs = keras.Input(shape=(latent_dim,))
    x = layers.Dense(4 * 4 * 256, activation="relu")(latent_inputs)
    x = layers.Reshape((4, 4, 256))(x)
    x = layers.Conv2DTranspose(256, 4, activation="relu", strides=2, padding="same")(x)
    x = layers.Conv2DTranspose(128, 4, activation="relu",strides=2, padding="same")(x)
    x = layers.Conv2DTranspose(128, 3, activation="relu", padding="same")(x)
    x = layers.Conv2DTranspose(64, 4, activation="relu", strides=2, padding="same")(x)
    x = layers.Conv2DTranspose(64, 3, activation="relu", padding="same")(x)
    x = layers.Conv2DTranspose(32, 4, activation="relu", strides=2, padding="same")(x)
    x = layers.Conv2DTranspose(32, 3, activation="relu", padding="same")(x)
    decoder_outputs = layers.Conv2DTranspose(3, 3, activation="sigmoid", padding="same")(x)
    decoder = keras.Model(latent_inputs, decoder_outputs, name="decoder")
    decoder.summary()


    ## class vae
    @tf.keras.utils.register_keras_serializable()
    class VAE(keras.Model):
        def __init__(self, encoder, decoder, **kwargs):
            super().__init__(**kwargs)
            self.encoder = encoder
            self.decoder = decoder
            self.total_loss_tracker = keras.metrics.Mean(name="total_loss")
            self.reconstruction_loss_tracker = keras.metrics.Mean(
                name="reconstruction_loss"
            )
            self.kl_loss_tracker = keras.metrics.Mean(name="kl_loss")


        def get_config(self):
            #, "total_loss":self.total_loss_tracker,"reconstruction_loss" :self.reconstruction_loss_tracker, "kl_loss":self.kl_loss_tracker
            return {"encoder": self.encoder, "decoder":self.decoder}

        @property
        def metrics(self):
            return [
                self.total_loss_tracker,
                self.reconstruction_loss_tracker,
                self.kl_loss_tracker,
            ]

        def train_step(self, data):
            with tf.GradientTape() as tape:
                z_mean, z_log_var, z = self.encoder(data)
                reconstruction = self.decoder(z)
                reconstruction_loss = tf.reduce_mean(
                    tf.reduce_sum(
                        keras.losses.binary_crossentropy(data, reconstruction),
                        axis=(1, 2),
                    )
                )
                kl_loss = tf.reduce_sum(tf.square(tf.exp(z_log_var)) + tf.square(z_mean) - z_log_var - 0.5, axis=1)
                total_loss =reconstruction_loss + kl_loss/2
            grads = tape.gradient(total_loss, self.trainable_weights)
            self.optimizer.apply_gradients(zip(grads, self.trainable_weights))
            self.total_loss_tracker.update_state(total_loss)
            self.reconstruction_loss_tracker.update_state(reconstruction_loss)
            self.kl_loss_tracker.update_state(kl_loss)
            return {
                "loss": self.total_loss_tracker.result(),
                "reconstruction_loss": self.reconstruction_loss_tracker.result(),
                "kl_loss": self.kl_loss_tracker.result(),
            }
        def call(self, x):
            encoded = self.encoder(x)
            decoded = self.decoder(encoded)
            return decoded


    import pooch

    POOCH = pooch.create(
        # Use the default cache folder for the OS
        path=os.path.join(os.path.dirname(__file__),'..','saved_model'),
        # The remote data is on Github
        base_url="https://zenodo.org/records/10957695/files/felon_finder_vae.weights.h5?download=1",
        # The registry specifies the files that can be fetched
        registry={
            # The registry is a dict with file names and their SHA256 hashes
            "felon_finder_vae.weights.h5": "38595de4ea78d8a1ba21f7b1a3a3b3c7c1c4c862bf3b290c5cd9d2ebaccc16fa",
        },
    )

    vae_weights = POOCH.fetch("felon_finder_vae.weights.h5")

    ## load weights from the saved model
    vae = VAE(encoder, decoder)
    vae.load_weights(vae_weights)



    ### upload images from celebA for model testing
    data_dir=os.path.join(os.path.abspath(".."), 'img', 'faces')

    batch_size=128
    img_height= 64
    img_width= 64
    train_ds = tf.keras.utils.image_dataset_from_directory( data_dir,validation_split=0.2,subset="training",seed=123,image_size=(img_height, img_width),batch_size=batch_size, labels=None)

    x_train_list = list(train_ds)
    x_train=x_train_list[0]
    x_train=x_train.numpy()
    for element in x_train_list:
        element=element.numpy()
        x_train=np.concatenate([x_train, element], axis=0)
    x_train = x_train.astype("float32") / 255


    ## reconstruct the faces
    z_mean,_,x_encoded = vae.encoder(x_train[:20])


    x_1 = one_selection(x_encoded[5], 0, 2)


    x_decoded = vae.decoder(x_encoded)
    x_decoded2 = vae.decoder(x_1)

    plt.figure(figsize=(20, 8))

    plt.subplot(2, 4, 1)
    plt.title("selected")
    plt.imshow(x_decoded[5])
    plt.axis('off')


    for i in range(4):

        # display reconstruction
        bx = plt.subplot(2, 4, i + 5)
        plt.title("reconstructed")
        plt.imshow(x_decoded2[i])
        bx.get_xaxis().set_visible(False)
        bx.get_yaxis().set_visible(False)

    plt.suptitle('Une sélection')
    plt.show()

    x_2 = two_selections(x_encoded[7], x_encoded[11])

    x_decoded21 = vae.decoder(x_2)

    plt.figure(figsize=(20, 8))

    plt.subplot(2, 4, 1)
    plt.title("selected")
    plt.imshow(x_decoded[6])
    plt.axis('off')
    plt.subplot(2, 4, 2)
    plt.title("selected")
    plt.imshow(x_decoded[10])
    plt.axis('off')

    for i in range(4):

        # display reconstruction
        bx = plt.subplot(2, 4, i + 5)
        plt.title("reconstructed")
        plt.imshow(x_decoded21[i])
        bx.get_xaxis().set_visible(False)
        bx.get_yaxis().set_visible(False)

    plt.suptitle('2 sélections')
    plt.show()

    x_3 = multiple_selections( x_encoded[0], x_encoded[15], x_encoded[19])

    x_decoded22 = vae.decoder(x_3)

    plt.figure(figsize=(20, 8))

    plt.subplot(2, 4, 1)
    plt.title("selected")
    plt.imshow(x_decoded[3])
    plt.axis('off')
    plt.subplot(2, 4, 2)
    plt.title("selected")
    plt.imshow(x_decoded[0])
    plt.axis('off')
    plt.subplot(2, 4, 3)
    plt.title("selected")
    plt.imshow(x_decoded[15])
    plt.axis('off')
    plt.subplot(2, 4, 4)
    plt.title("selected")
    plt.imshow(x_decoded[19])
    plt.axis('off')

    for i in range(4):

        # display reconstruction
        bx = plt.subplot(2, 4, i + 5)
        plt.title("reconstructed")
        plt.imshow(x_decoded22[i])
        bx.get_xaxis().set_visible(False)
        bx.get_yaxis().set_visible(False)

    plt.suptitle('3 ou 4 sélections')
    plt.show()
