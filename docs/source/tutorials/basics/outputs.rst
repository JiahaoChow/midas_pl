Outputs of MIDAS
================

In this section, we explain the outputs of MIDAS.

Infer with the Model
~~~~~~~~~~~~~~~~~~~~

After training, you can use the ``predict`` method to generate and save predictions. Here's the syntax:

.. code-block:: python

    model.predict(output_dir,   
            joint_latent=True,
            mod_latent=True,
            impute=True,
            batch_correct=True,
            translate=True,
            input=True)

- ``pred_dir``: The directory where prediction results will be saved.
- ``joint_latent``: Whether to calculate and save joint latent representations (combined features from all modalities).
- ``mod_latent``: Whether to calculate and save modality-specific latent representations (features for each individual modality).
- ``impute``: Whether to perform data imputation, filling in missing or incomplete data.
- ``batch_correct``: Whether to apply batch correction to the data to reduce batch effects.
- ``translate``: Whether to perform modality translation (i.e., transforming data between different modalities).
- ``input`` : Whether to save the original input data. Note that if you’ve configured any transformations (e.g., ``binarize``), the saved input data may differ from the original data in the file.

Fetch Outputs
~~~~~~~~~~~~~

To retrieve and load the predicted outputs, you can use the `load_predicted` function from the ``scmidas.utils`` module. Here's how to do it:

.. code-block:: python

    from scmidas.utils import load_predicted
    load_predicted( output_dir, 
                    model.s_joint, 
                    model.combs, 
                    model.mods, 
                    joint_latent=True, 
                    mod_latend=True, 
                    impute=True, 
                    batch_correct=True, 
                    translate=True, 
                    input=True)

