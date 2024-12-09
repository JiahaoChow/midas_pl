import argparse
import lightning as L
from .src.model import MIDAS
from lightning.pytorch import loggers as pl_loggers
from lightning.pytorch.callbacks import model_checkpoint
import toml
import os
import torch
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--gpus', type=int, default=1, help='Number of GPUs to use')
    parser.add_argument('--precision', type=int, default=32, help='Precision for training')
    parser.add_argument('--num_nodes', type=int, default=1, help='Number of nodes')
    parser.add_argument('--task_name', type=str, default="version1", help='')
    parser.add_argument('--log_dir', type=str, default="./logs/", help='')
    parser.add_argument('--ckpt_dir', type=str, default="./ckpt/", help='')
    parser.add_argument('--filename', type=str, default="./checkpoint-{epoch}", help='')
    parser.add_argument('--every_n_epochs', type=int, default=1, help='')
    parser.add_argument('--save_top_k', type=int, default=5, help='')
    parser.add_argument('--n_epoch', type=int, default=500, help='')
    parser.add_argument('--batch_size', type=int, default=256, help='')
    parser.add_argument('--logging', type=bool, default=True, help='')
    parser.add_argument('--log_every_n_steps', type=int, default=10, help='')
    parser.add_argument('--load_ckpt', type=str, default="last_model.ckpt", help='')
    parser.add_argument('--action', type=str, default="train", help='')

    return parser.parse_args()

def main():

    data_path = "/opt/data/private/zjh/code/midas_pl/immune_cells_143s/"
    args = parse_args()
    strategy="ddp" if args.gpus > 1 else "auto"
    tb_logger = pl_loggers.TensorBoardLogger(save_dir=args.log_dir, version=args.task_name)
    model = MIDAS.configure_data_from_dir(data_path, strategy)
    if os.path.exists(args.load_ckpt):
        model.load_checkpoint(args.load_ckpt)
    if args.action == "train":
        trainer = L.Trainer(
            use_distributed_sampler=False, 
            accelerator="auto",
            devices=args.gpus,
            precision=args.precision,
            strategy=strategy,
            num_nodes=args.num_nodes,
            max_epochs = args.n_epoch,
            logger=tb_logger if args.logging else None,
            log_every_n_steps=args.log_every_n_steps
            )
        trainer.fit(model=model)
    elif args.action == "pred":
        model.freeze()
        model.to("cuda:0")
        model.predict("./predict/"+args.task_name, joint_latent=True, mod_latent=False, impute=False, batch_correct=False, translate=False, 
            input=False)
        model.get_emb_umap("./predict/"+args.task_name, "./predict/"+args.task_name, save_fig=True)

if __name__ == '__main__':
    main()