#!/usr/bin/env python3

import logging
import time

import crypten
import torch
from crypten.common import AverageMeter


def run_mpc_linear_svm(
    epochs=50, examples=50, features=100, lr=0.5, skip_plaintext=False
):
    # Set random seed for reproducibility
    torch.manual_seed(1)

    # Initialize x, y, w, b
    x = torch.randn(features, examples)
    w_true = torch.randn(1, features)
    b_true = torch.randn(1)
    y = w_true.matmul(x) + b_true
    y = y.sign()

    # Random initialization for linear svm
    w_init = torch.randn(1, features)
    b_init = torch.randn(1)

    if not skip_plaintext:
        logging.info("==================")
        logging.info("PyTorch Training")
        logging.info("==================")
        w = w_init
        b = b_init

        pt_time = AverageMeter()
        end = time.time()
        for i in range(epochs):
            logging.info("Epoch %d" % (i + 1))
            # Forward
            yhat = w.matmul(x) + b
            yhat = yhat.sign()

            yy = yhat * y

            # Accuracy
            accuracy = (yy == 1).float().mean()
            logging.info("--- Accuracy %.2f%%" % (accuracy.item() * 100))

            # Backward
            loss_grad = -y * (1 - yy) * 0.5

            b_grad = loss_grad.sum() * (1 / examples)
            w_grad = loss_grad.matmul(x.t()) * (1 / examples)

            # Update
            w = w - w_grad * lr
            b = b - b_grad * lr

            pt_time.update(time.time() - end)
            logging.info("    Time %.6f (%.6f)" % (pt_time.val, pt_time.avg))
            end = time.time()

        w_torch = w
        b_torch = b

    # Encrypt all the things!!!
    x = crypten.MPCTensor(x)
    y = crypten.MPCTensor(y)

    w = crypten.MPCTensor(w_init)
    b = crypten.MPCTensor(b_init)

    batch_time = AverageMeter()

    logging.info("==================")
    logging.info("CrypTen Training")
    logging.info("==================")
    end = time.time()
    for i in range(epochs):
        logging.info("Epoch %d" % (i + 1))

        # Forward
        yhat = w.matmul(x) + b
        yhat = yhat.sign()

        yy = yhat * y

        # Accuracy
        correct = (
            (yy + 1).mul(0.5).sum()
        )  # equivalent to (yy == 1).sum() w/o comparator
        logging.info(
            "--- Accuracy %.2f%%"
            % (correct.get_plain_text().float().div(examples).item() * 100)
        )

        # Backward
        loss_grad = -y * (1 - yy) * 0.5

        b_grad = loss_grad.sum() * (1 / examples)
        w_grad = loss_grad.matmul(x.t()) * (1 / examples)

        # Update
        w = w - w_grad * lr
        b = b - b_grad * lr

        batch_time.update(time.time() - end)
        logging.info("    Time %.6f (%.6f)" % (batch_time.val, batch_time.avg))
        end = time.time()

    if not skip_plaintext:
        logging.info("PyTorch Weights  :")
        logging.info(w_torch)
    logging.info("CrypTen Weights:")
    logging.info(w.get_plain_text())

    if not skip_plaintext:
        logging.info("PyTorch Bias  :")
        logging.info(b_torch)
    logging.info("CrypTen Bias:")
    logging.info(b.get_plain_text())