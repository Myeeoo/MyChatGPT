import tensorflow as tf
from tensorflow.keras import datasets, layers, models
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
def train_model(epochs, lr):
    # 加载MNIST数据集
    (train_images, train_labels), (test_images, test_labels) = datasets.mnist.load_data()

    # 归一化像素值
    train_images, test_images = train_images / 255.0, test_images / 255.0

    # 构建卷积神经网络
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dense(10)
    ])

    # 编译模型
    model.compile(optimizer=tf.keras.optimizers.Adam(lr=lr),
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])

    # 训练模型
    history = model.fit(train_images.reshape(-1, 28, 28, 1), train_labels, epochs=epochs,
                        validation_data=(test_images.reshape(-1, 28, 28, 1), test_labels))

    # 返回训练后的模型和训练结果
    return model, history.history
