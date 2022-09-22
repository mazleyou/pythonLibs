import imgaug.augmenters as iaa

# augmentation properties
augmentation = iaa.Sequential([
    # 1. Flip
    iaa.Fliplr(0.5),
    iaa.Flipud(0.5),
    # 2. Affine
    iaa.Affine(translate_percent={"x": (-0.2, 0.2), "y": (-0.2, 0.2)},
               rotate=(-20, 20),
               scale=(0.5, 1.5)),
    # 3. Multiply
    iaa.Multiply((0.8, 1.2)),
    # 4. Linearcontrast
    iaa.LinearContrast((0.6, 1.4)),
    # Perform methods below only sometimes
    iaa.Sometimes(0.5,
                  # 5. GaussianBlur
                  iaa.GaussianBlur((0.0, 3.0))
                  )
])


def get_image(image):
    return augmentation(images=image)
