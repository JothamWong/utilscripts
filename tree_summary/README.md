# Tree Summary

Simple Ollama wrapper + tree util that also summarizes what each file does
with respect to the entire project.

Logging is performed at the moment, but the output is intended to be piped from stdout
as you would any other unix utility.

## Notes/Possible improvements?

At the moment, the Ollama model could take awhile. A smaller model is pretty
useless, and a larger model takes a really long time. Improvement to streaming the
output could be made.

Perhaps a better approach would be to summarize each directory first, and then
pass that summary as the context to the contents of the file?

## Sample

I tried this script on https://github.com/yifan123/flow_grpo
with gemma3:12b and this was the output:

```
---Project Summaries: flow_grpo ---
├── config
│   ├── base.py
│   │   config/base.py defines a comprehensive configuration for training a Stable Diffusion model, specifying parameters for sampling, training, prompting, and reward functions, acting as a central hub for controlling various aspects of the project's behavior.
│   └── dgx.py
│       This file (config/dgx.py) defines configuration functions for different training scenarios (pickscore, geneval, pickscore, and general_ocr) using Stable Diffusion 3.5 medium, setting parameters for training and evaluation.
├── dataset
│   ├── geneval
│   │   ├── test_metadata.jsonl
│   │   │   This file (test_metadata.jsonl) provides structured data for generating image prompts based on object descriptions and relationships, likely to be used for testing or evaluating an image generation model.
│   │   └── train_metadata.jsonl
│   │       This file (train_metadata.jsonl) serves as a dataset providing structured metadata, including object descriptions and spatial relationships, for image generation tasks by detailing image content and scene composition.
│   ├── ocr
│   │   ├── test.txt
│   │   │   This file (dataset/ocr/test.txt) contains a collection of detailed descriptions of various scenes and objects, intended for use in testing or training an image generation or understanding model by providing textual prompts or labels.
│   │   └── train.txt
│   │       This file, train.txt, serves as a dataset of image descriptions used to train a model to generate textual descriptions of images, likely for tasks like image captioning or visual question answering.
│   ├── pickscore
│   │   ├── prpocess.py
│   │   │   This file processes the original Pick-A-Pic dataset, filters captions with at least 5 spaces, splits it into test and train sets, and saves the resulting datasets to text files.
│   │   ├── test.txt
│   │   │   This file (test.txt) contains a collection of diverse and complex text prompts intended to generate images, likely serving as a test set to evaluate the capabilities of an AI image generation model.
│   │   └── train.txt
│   │       This file, train.txt, contains the primary training data for the project, likely consisting of text prompts or descriptions paired with corresponding image identifiers, used to train a generative AI model to create images based on textual input.
│   ├── geneval_filter_test.py
│   │   This script filters training metadata by removing entries that have prompts present in the test metadata for specific GeneVAL tasks, ensuring no overlap between training and testing data.
│   └── merge_genevaltask.py
│       This script merges and samples data from multiple Geneval tasks based on specified weights to create a combined training dataset.
├── flow_grpo
│   ├── assets
│   │   ├── activities.txt
│   │   │   The activities.txt file contains a simple list of activity names, likely used for demonstration or as a data source within the flow_grpo project.
│   │   ├── activities_v0.txt
│   │   │   This file contains a list of simple activities likely used for data generation or demonstration within the flow_grpo project.
│   │   ├── imagenet_classes.txt
│   │   │   This file lists 1000 common object classes, serving as a vocabulary for image classification tasks within the project, likely used to label and categorize images for training or evaluation of a machine learning model.
│   │   ├── simple_animals.txt
│   │   │   This file lists common animal names, likely serving as a vocabulary or dataset for training or testing image generation or recognition models within the flow_grpo project.
│   │   ├── simple_ocr_animals.txt
│   │   │   This file contains a simple list of animal names likely used for testing or demonstrating OCR capabilities within the project.
│   │   ├── simple_ocr_animals_digit1.txt
│   │   │   This file contains descriptions of animals holding signs with digits from 0 to 8, likely serving as training or testing data for an OCR model focused on recognizing digits within images.
│   │   ├── simple_ocr_animals_digit3.txt
│   │   │   This file contains a dataset of animal descriptions paired with digit sequences, likely intended for training or testing an OCR model focused on recognizing digits displayed by animals.
│   │   └── simple_ocr_animals_digit5.txt
│   │       The file contains a repetitive sequence of animals holding signs displaying number sequences, likely serving as training or testing data for an OCR model focused on recognizing digits in images.
│   ├── diffusers_patch
│   │   ├── sd3_pipeline_with_logprob.py
│   │   │   This file implements a Stable Diffusion 3 pipeline that incorporates log-probability calculations and KL divergence tracking for enhanced sampling and analysis.
│   │   ├── sd3_sde_with_logprob.py
│   │   │   This file implements a modified SDE step with log probability calculation for flow matching, adapting a diffusion scheduler to propagate samples and compute log probabilities during the reverse diffusion process.
│   │   └── train_dreambooth_lora_sd3.py
│   │       This file contains functions for encoding prompts using various text encoders (CLIP and T5) to generate embeddings for image generation, likely within a Dreambooth LoRA training pipeline for Stable Diffusion.
│   ├── aesthetic_scorer.py
│   │   This file defines an AestheticScorer class that uses a pre-trained CLIP model and a custom MLP to predict aesthetic scores for images.
│   ├── ema.py
│   │   This file implements an Exponential Moving Average (EMA) module to track and update model parameters, likely used for stabilizing training or creating ensemble models.
│   ├── imagereward_scorer.py
│   │   This file defines an ImageRewardScorer class that uses the "ImageReward-v1.0" model to calculate image rewards based on provided prompts and images, likely for evaluating generated images.
│   ├── ocr.py
│   │   This file defines an OCR reward scorer using PaddleOCR to evaluate the accuracy of recognized text against provided prompts, calculating a reward based on Levenshtein distance and potentially utilizing GPU acceleration.
│   ├── pickscore_scorer.py
│   │   This file defines a PickScoreScorer class using Hugging Face Transformers to calculate similarity scores between text prompts and images using a pre-trained model, enabling evaluation of image-text alignment.
│   ├── prompts.py
│   │   This file defines various prompt generation functions, loading text from files to create diverse prompts for image generation tasks, often incorporating random elements and metadata for enhanced control and interactivity.
│   ├── qwenvl.py
│   │   This file defines a QwenVLScorer class that uses a Qwen2.5-VL model to evaluate the aesthetic quality of images based on a prompt and returns aesthetic scores.
│   ├── rewards.py
│   │   This file (flow_grpo/rewards.py) defines and implements various scoring functions, including image quality assessment, OCR, aesthetic evaluation, and unified reward scoring, to evaluate generated images based on different metrics, potentially interacting with image generation components and other evaluation modules within the larger project.
│   └── stat_tracking.py
│       This file implements a PerPromptStatTracker class to calculate and track statistics (mean, standard deviation, advantages) for individual prompts based on rewards, facilitating reward weighting and providing insights into prompt performance.
├── scripts
│   ├── accelerate_configs
│   │   ├── deepspeed_zero1.yaml
│   │   │   This file configures a local machine for distributed training using DeepSpeed with ZeRO Stage 1 optimization, utilizing 8 processes across a single machine.
│   │   ├── deepspeed_zero2.yaml
│   │   │   This file defines a DeepSpeed configuration for distributed training with mixed precision (FP16) using ZeRO stage 2, suitable for a single machine with 8 processes.
│   │   ├── deepspeed_zero3.yaml
│   │   │   This file configures a DeepSpeed training setup using ZeRO-3 optimization for distributed training across multiple machines, enabling memory efficiency and scalability.
│   │   ├── multi_gpu.yaml
│   │   │   This file configures a local multi-GPU training environment using accelerate, specifying parameters like mixed precision and the number of GPUs to utilize.
│   │   └── multi_node.yaml
│   │       This file defines configuration settings for distributed training across multiple machines using Accelerate, specifying parameters like IP addresses, ports, GPU usage, and mixed-precision settings to orchestrate the training process.
│   ├── multi_node
│   │   ├── main.sh
│   │   │   This script launches a distributed training job using Accelerate with parameters read from a configuration file, designed to be run on each node of a 3-machine, 24-process cluster.
│   │   ├── main1.sh
│   │   │   This script launches a training process on a multi-node setup using accelerate, configured with specific parameters for machine rank 1 and intended to be run on one of three nodes in the cluster.
│   │   └── main2.sh
│   │       This script launches a training process on a multi-node system, acting as a worker node (rank 2) with pre-defined environment variables and Accelerate configuration parameters for distributed training.
│   ├── single_node
│   │   └── main.sh
│   │       This script demonstrates how to launch a training script using accelerate with either a single GPU or multiple GPUs using a pre-configured multi_gpu.yaml configuration.
│   └── train_sd3.py
│       This script (scripts/train_sd3.py) orchestrates the training process for a Stable Diffusion 3 model, utilizing the accelerator for distributed training and managing optimization, logging, and EMA updates to refine the model's performance.
├── LICENSE
│   This file (LICENSE) grants broad usage permissions for the software under the MIT license, requiring only that the copyright notice and permission notice be included.
├── README.md
│   This README file provides a comprehensive guide to the Flow-GRPO project, detailing setup, usage, reward model configurations, hyperparameters, acknowledgements, and citation information for training flow matching models via online reinforcement learning.
└── setup.py
    This setup.py file defines the project's metadata, dependencies, and installation instructions, specifying the required Python packages for the "flow-grpo" project and enabling its distribution.
```