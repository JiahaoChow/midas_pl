More Modalities
===============

MIDAS is designed to integrate RNA, ADT, and ATAC data. If you'd like to expand the model to support additional 
modalities, follow the instructions below.

Framework Overview
~~~~~~~~~~~~~~~~~~~

MIDAS is configured via the ``scmidas/model_config.toml`` file and primarily employs Multi-Layer Perceptrons (MLPs). 
Below are the key components of the MIDAS framework:

Key Components
-----------------------

1. **Data Encoder**: Encodes each modality into Gaussian-distributed latent features, including the means and log-transformed variances.
2. **Data Decoder**: Reconstructs counts for each modality using the joint latent features as input.
3. **Batch Indices Encoder**: Encodes batch indices for each modality into Gaussian-distributed latent features.
4. **Batch Indices Decoder**: Reconstructs batch indices for each modality using the joint latent features.
5. **Discriminator**: A group of classifiers that categorizes modality-specific latents and joint latents. Only the biological part of the latents is used for this classification.

.. Note:

   MIDAS currently supports MLP-based architectures. While more complex structures, such as convolutional neural networks (CNNs), are not yet supported, they can be incorporated with custom modifications.

Transformation and Distribution Functions
-----------------------------------------

MIDAS includes pre-defined transformation and distribution functions, which you can modify or extend for new modalities.

Transformation Functions
^^^^^^^^^^^^^^^^^^^^^^^^

- **binarize**

  - **Input Transformation**: Converts data into binary form.

  - **Output Transformation**: None

- **log1p**

  - **Input Transformation**: Apply ``log1p`` (log(x + 1)) transformation

  - **Output Transformation**: Apply the exponential function (``exp``)

.. note::
   Transformation functions specified during model configuration (e.g., ``transform`` parameter in ``configure_data_from_dir``) are applied only when retrieving items from the dataset (via ``get_item``). During the encoding and decoding process, both the transformation and its inverse are applied, ensuring data consistency between these stages.

Distribution Functions
^^^^^^^^^^^^^^^^^^^^^^

1. **POISSON**

   - **Loss Function**: Poisson loss

   - **Sampling**: Poisson sampling

   - **Activation**: None

2. **BERNOULLI**

   - **Loss Function**: Binary cross-entropy loss

   - **Sampling**: Bernoulli sampling

   - **Activation**: Sigmoid

The ``loss`` defines the reconstruction loss function, ``sampling`` defines how batch-corrected counts are calculated, and ``activation`` sets the output layer activation for the decoder.


Step 1: Extend the Framework
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To begin with, you should load the model configurations as follows:

.. code-block:: python

   from scmidas.config import load_config
   configs = load_config()

Data Encoder
------------

The data encoder transforms input data through modality-specific and shared layers to produce latent representations. Configure it as follows:

1. **Transformation Before Encoding**: Specify the transformation function to be applied before encoding.

   Example:

   .. code-block:: python
      
      configs['trsf_before_enc_mod'] = 'log1p'

.. attention::
      If the specified transformation is not registered, an error will occur. Refer to Registering Transformations for details.

2. **(Optional) Dimensionality Reduction Layer**: If the data is split into chunks, define the modality-specific layers for encoding each chunk individually before merging them.

   Example:

   .. code-block:: python
      
      configs['dims_before_enc_mod'] = [512, 128]  # First encode to 512 dimensions, then to 128
   
3. **(Optional) Shared Layer Configuration**: Define the architecture of the shared encoder layers.

   Example:

   .. code-block:: python
      
      configs['dims_shared_enc'] = [1024, 128]
   

Data Decoder
------------

The data decoder reconstructs original data from latent features. Configure the shared layers and dimensionality expansion layers as follows:

1. **(Optional) Shared Layer Setup**: Define the structure for the shared decoder layers.

   Example:

   .. code-block:: python
      
      configs['dims_shared_dec'] = [128, 1024]
   
2. **(Optional) Dimensionality Expansion Layer**: If the data is split into chunks, define the dimensionality expansion layers after the shared layers.

   Example:

   .. code-block:: python
      
      configs['dims_after_dec_mod'] = [128, 512]

3. **Output Distribution**: Set the output distribution for each modality.

   Example:

   .. code-block:: python
      
      configs['distribution_dec_mod'] = 'POISSON'

.. attention::
      If the specified distribution is not registered, an error will occur. Refer to Registering Distributions for guidance.

Reconstruction Loss Weight
--------------------------

Adjust the weight for reconstruction loss as needed:

.. code-block:: python

   configs['lam_recon_mod'] = 1  # Adjust as needed

.. (Optional) Batch Indices Encoder and Decoder
.. --------------------------------------------

.. Set up the batch indices encoder and decoder layers as follows:

.. 1. **Batch Indices Encoder Setup**:

..    .. code-block:: python
      
..       configs['dims_enc_s'] = [16, 16]
   
.. 2. **Batch Indices Decoder Setup**:

..    .. code-block:: python

..       configs['dims_dec_s'] = [16, 16]

Step 2: Register New Functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To add new functionalities, register transformation and distribution functions as follows:

.. Transformation:

Register New Transformation Functions
----------------------------------------

.. code-block:: python

   from scmidas.nn import transform_registry
   transform_registry.register(name, fn, inverse_fn)


.. Distribution:

Register New Distribution Functions
--------------------------------------

.. code-block:: python

   from scmidas.nn import distribution_registry
   distribution_registry.register(name, loss_fn, sampling_fn, activate_fn)


Call for Contributions
~~~~~~~~~~~~~~~~~~~~~~

We encourage you to contribute to MIDAS by submitting pull requests for new features, enhancements, or bug fixes. Contributions will be reviewed and, if suitable, integrated into the main repository. Thank you for helping us improve MIDAS!