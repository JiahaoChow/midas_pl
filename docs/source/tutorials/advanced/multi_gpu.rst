Train with Multi-GPU
====================

To enable training on multiple GPUs, create a ``.py`` file and modify the ``strategy`` parameter to ``ddp`` (Distributed Data Parallel):

.. code-block:: python

    trainer = L.Trainer(
        devices='auto',                # Automatically use all available GPUs
        strategy='ddp'                 # Enable distributed training with DDP
    )

.. note::
    1. Set `devices=auto`` to utilize all available GPUs automatically. Alternatively, specify the exact number of GPUs by setting ``devices=n`` (for n GPUs).
    2. Use ``ddp`` for multi-GPU training on a single node.