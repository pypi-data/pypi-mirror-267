import os
os.environ["KERAS_BACKEND"] = "tensorflow"

import tensorflow as tf
import keras
from keras import layers

class Sampling(layers.Layer):
    """Sampling layer for VAE.
    
    This layer takes the mean and log variance of the latent space distribution
    as input and samples from the distribution to produce a latent vector.
    """

    def call(self, inputs):
        """Samples from the latent space distribution.

        Args:
            inputs (tuple): Tuple containing mean and log variance of the latent space distribution.

        Returns:
            tensor: Sampled latent vector.
        """
        z_mean, z_log_var = inputs
        batch = tf.shape(z_mean)[0]
        dim = tf.shape(z_mean)[1]
        epsilon = tf.random.normal(shape=(batch, dim))
        return z_mean + tf.exp(0.5 * z_log_var) * epsilon

@tf.keras.utils.register_keras_serializable()
class VAE(keras.Model):
    """Variational Autoencoder class."""

    def __init__(self, encoder, decoder, **kwargs):
        """Constructor for VAE class.

        Args:
            encoder (keras.Model): Encoder model.
            decoder (keras.Model): Decoder model.
            **kwargs: Additional arguments to be passed.
        """
        super().__init__(**kwargs)
        self.encoder = encoder
        self.decoder = decoder
        self.total_loss_tracker = keras.metrics.Mean(name="total_loss")
        self.reconstruction_loss_tracker = keras.metrics.Mean(
            name="reconstruction_loss"
        )
        self.kl_loss_tracker = keras.metrics.Mean(name="kl_loss")

    def get_config(self):
        """Returns the configuration of the VAE model."""
        return {"encoder": self.encoder, "decoder": self.decoder}

    @property
    def metrics(self):
        """Returns the list of metrics."""
        return [
            self.total_loss_tracker,
            self.reconstruction_loss_tracker,
            self.kl_loss_tracker,
        ]

    def train_step(self, data):
        """Performs a single training step.

        Args:
            data: Input data.

        Returns:
            dict: Dictionary containing loss values.
        """
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
            total_loss = reconstruction_loss + kl_loss/2
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
        """Call method for VAE model.

        Args:
            x: Input data.

        Returns:
            tensor: Decoded output.
        """
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded

def encoder_create(latent_dim=1024):
    """Creates an encoder model.

    Args:
        latent_dim (int): Dimensionality of the latent space.

    Returns:
        keras.Model: Encoder model.
    """
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
    return encoder

def decoder_create(latent_dim=1024):
    """Creates a decoder model.

    Args:
        latent_dim (int): Dimensionality of the latent space.

    Returns:
        keras.Model: Decoder model.
    """
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
    return decoder

if __name__ == '__main__':

    import matplotlib.pyplot as plt
    import numpy as np
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

    vae = VAE(encoder_create(), decoder_create())
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
    x_decoded = vae.decoder(x_encoded)

    plt.figure(figsize=(20, 4))
    for i in range(10):
        # display original
        ax = plt.subplot(2, 10, i + 1)
        plt.title("original")
        plt.imshow(x_train[i])
        plt.axis("off")
    
        # display reconstruction
        bx = plt.subplot(2, 10, i + 10 + 1)
        plt.title("reconstructed")
        plt.imshow(x_decoded[i])
        bx.get_xaxis().set_visible(False)
        bx.get_yaxis().set_visible(False)
    plt.show()