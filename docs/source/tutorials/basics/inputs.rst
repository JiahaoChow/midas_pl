Inputs of MIDAS
===============

This section explains how to prepare and load input data for MIDAS.
MIDAS requires two components as input: multi-modal data and masks. 
The data for each modality is stored separately, 
while the mask indicates the presence or absence of features, 
especially useful in multi-batch scenarios.

Mask
~~~~

- ``0``: Feature is missing.
- ``1``: Feature is present.
Each batch and modality has a corresponding CSV file with a shape of ``1 x m`` (1 row, m columns), 
including a header and an index column. If a mask file is missing, MIDAS assumes all features are present 
(defaulting the mask values to ``1``).

To specify a mask, provide the file paths as shown in the example below:

.. code-block:: python

    mask = [
        {'rna': 'batch_1_rna_mask.csv', 'adt': 'batch_1_adt_mask.csv'},
        {'rna': 'batch_2_rna_mask.csv', 'adt': 'batch_2_adt_mask.csv'},
        {'rna': 'batch_3_rna_mask.csv', 'adt': 'batch_3_adt_mask.csv'}
    ]

Data
~~~~

MIDAS supports three different input formats for data integration, 
each catering to different use cases. 

Initial Setup
^^^^^^^^^^^^^

Before diving into data formats, 
we first need to set up the environment and load the default configuration:

.. code-block:: python  

    from scmidas.model import MIDAS
    from scmidas.config import load_config

    # Settings for the model, such as the layer dimensions.
    configs = load_config()

Below are the details for each format:

Option 1: CSV per Modality and Batch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In this format, data for each modality is stored in CSV files. 
Each file represents a ``cell x feature`` matrix, 
where rows correspond to cells, and columns represent features. 
The file includes a header and an index column.

Step 1: Define Data Dimensions
------------------------------

First, we specify the dimensionality for each modality. 
In this example, ATAC data is split into multiple chunks during training 
based on the specified dimensions:

.. code-block:: python  

    # Dimensions per modality.
    # In this example, the ATAC data is split into chunks during training 
    # based on the specified dimensionality.
    dims_x = {
        'rna': [200],    # RNA data is represented as a cell x 200 matrix.
        'adt': [100],    # ADT data is represented as a cell x 100 matrix.
        'atac': [100, 200, 300, ..., 200]  # ATAC data is split into multiple chunks with varying dimensions
    }

.. note::

    For modalities in ``dims_x`` with more than one dimension (e.g., ATAC), 
    the data will be split into chunks based on these dimensions. 
    This can be particularly useful for high-dimensional data like ATAC-seq, 
    where splitting might occur based on features such as chromosomes.

Step 2: Load the Data
---------------------

Next, we provide the paths to the CSV files for each modality and batch:

.. code-block:: python  

    # Data for each modality and batch
    data = [
        {'rna': 'batch_1_rna.csv', 'adt': 'batch_1_adt.csv', 'atac': 'batch_1_atac.csv'},
        {'rna': 'batch_2_rna.csv', 'adt': 'batch_2_adt.csv', 'atac': 'batch_2_atac.csv'},
        {'rna': 'batch_3_rna.csv', 'adt': 'batch_3_adt.csv', 'atac': 'batch_3_atac.csv'}
    ]

Step 3: Specify Transformation Rules
------------------------------------

For certain modalities, 
you may want to apply transformations. 
In this example, we binarize the ATAC data and leave RNA and ADT data unchanged:

.. code-block:: python  

    # Transformation rules for some modalities
    transform = {'atac': 'binarize'}  # Binarize ATAC data, leave RNA and ADT unchanged

Step 4: Configure MIDAS
-----------------------

Finally, use the provided configuration to set up MIDAS:

.. code-block:: python    

    # Configure MIDAS with the data
    datasets, dims_s, s_joint, combs = MIDAS.configure_data_from_csv(data, mask, transform)
    model = MIDAS.configure_data(configs, datasets, dims_x, dims_s, s_joint, combs)

.. note::

    This format is efficient because it avoids re-fetching data, 
    making it suitable for datasets that can fit into memory. 
    If your dataset is too large to load entirely, consider **Option 2**, 
    which allows loading one sample at a time instead of the entire dataset.

Option 2: CSV per Cell
^^^^^^^^^^^^^^^^^^^^^^

In this format, data for each cell is stored in separate CSV files. 
Each file contains a ``1 x feature`` vector (one row, multiple columns), 
**without** a header or index column. This format is especially useful 
when data is split into individual files for each cell.

For each batch and modality, provide the directory paths where the data is stored:

.. code-block:: python

    # Directory paths for each modality and batch
    data = [
        {'rna': 'batch_1_rna_dir/', 'adt': 'batch_1_adt_dir/', 'atac': 'batch_1_atac_dir/'},
        {'rna': 'batch_2_rna_dir/', 'adt': 'batch_2_adt_dir/', 'atac': 'batch_2_atac_dir/'},
        {'rna': 'batch_3_rna_dir/', 'adt': 'batch_3_adt_dir/', 'atac': 'batch_3_atac_dir/'}
    ]

    # Configure MIDAS with the data
    datasets, dims_s, s_joint, combs = MIDAS.configure_data_from_csv(data, mask, transform)
    model = MIDAS.configure_data(configs, datasets, dims_x, dims_s, s_joint, combs)

.. tip::
    
    **Option 1** and **Option 2** can be combined for greater flexibility in handling your data.

Option 3: Directory Structure
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In this format, each batch is organized into subdirectories containing vec 
(data vectors) and mask files for each modality.

.. code-block:: plaintext

    ./dataset_path/
        batch_0/
            mask/
                mod1.csv
                mod2.csv
            vec/
                mod1/
                    0000.csv
                    0001.csv
                    ...
                mod2/
                    0000.csv
                    0001.csv
                    ...
        batch_1/
            ...

.. code-block:: python

    # Load dataset using the directory structure
    model = MIDAS.configure_data_from_dir(configs, dataset_path, transform)


Supported Input Modalities
~~~~~~~~~~~~~~~~~~~~~~~~~~

Currently, MIDAS supports the following modalities:

- **RNA**: RNA counts (integer values).
- **ADT**: Protein counts (integer values).
- **ATAC**: ATAC peaks (integer values, binarized during training).

For additional modalities or customization, refer to the configuration section.