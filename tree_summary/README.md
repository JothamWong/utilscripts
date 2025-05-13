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
├── LICENSE
│   This file is a standard MIT License granting broad permissions for use and modification of the tree_summary utility while disclaiming any warranty.
├── README.md
│   This README file provides comprehensive documentation for the Flow-GRPO project, detailing setup, usage, reward model integration, hyperparameters, and acknowledgements, serving as a central guide for users and developers.
├── activities.txt
│   The activities.txt file lists common activities, likely used as examples or for testing in a tree summary or related functionality within the project.
├── activities_v0.txt
│   The file lists simple activities, likely used as examples or test data for a tree summarization script within the project.
├── aesthetic_scorer.py
│   This file defines an aesthetic scorer class that utilizes a pre-trained CLIP model and a custom MLP to predict aesthetic scores for images.
├── base.py
│   This file defines a configuration object using ml_collections to specify training parameters, sampling settings, prompt and reward functions, and other hyperparameters for a Stable Diffusion model.
├── deepspeed_zero1.yaml
│   This file configures a DeepSpeed training environment for local machines, enabling distributed training with ZeRO Stage 1 optimization.
├── deepspeed_zero2.yaml
│   This file configures a single-machine, 8-process DeepSpeed training run using ZeRO stage 2, enabling memory optimization for large model training.
├── deepspeed_zero3.yaml
│   This file configures a DeepSpeed training run using ZeRO-3 optimization for distributed training with 8 processes on a single machine, saving the model in 16-bit precision.
├── dgx.py
│   This file defines several configuration functions (get_config) for different training setups (pickscore, geneval, ocr, etc.) using the Stable Diffusion 3.5 medium model, likely for defining hyperparameters and training parameters for various tasks within a larger project.
├── ema.py
│   This file implements an Exponential Moving Average (EMA) module wrapper to track and update model parameters over time, facilitating a smoother and potentially more stable training process by maintaining a decaying average of previous weights.
├── geneval_filter_test.py
│   This script filters training metadata files by removing entries with prompts that appear in corresponding test metadata files, ensuring uniqueness between training and testing data for specific tasks.
├── imagenet_classes.txt
│   This file provides a comprehensive list of ImageNet classes, serving as a vocabulary for image recognition and categorization within the project, likely used for labeling, training, or evaluating image-related models.
├── imagereward_scorer.py
│   This file defines a class ImageRewardScorer that uses the ImageReward library to compute reward scores for a set of images based on given prompts, enabling evaluation or comparison of generated images.
├── main.sh
│   This bash script launches a distributed training job using Accelerate, configuring parameters like machine rank, number of machines, and IP address for a specific training run.
├── main1.sh
│   This script launches a training job on a multi-node cluster using Accelerate, configuring it as node 1 of 3 with specified rank, IP, and port, and utilizing a predefined configuration for training.
├── main2.sh
│   This script launches a training process using accelerate on a specific node (rank 2) within a 3-machine, 24-process distributed environment, using a pre-defined configuration file and a specified training script.
├── merge_genevaltask.py
│   This file merges and samples data from multiple Geneval task datasets based on specified weights, creating a combined training metadata file for downstream processing.
├── multi_gpu.yaml
│   This file configures a multi-GPU training environment locally using accelerate, specifying mixed precision and distributing the workload across 8 processes on a single machine.
├── multi_node.yaml
│   This file defines configuration settings for distributed training across multiple GPUs on a local machine, specifying network parameters, process counts, and mixed-precision settings.
├── ocr.py
│   This file defines an OcrScorer class that uses PaddleOCR to evaluate the accuracy of recognized text against provided prompts, calculating a reward based on Levenshtein distance and potentially using GPU acceleration.
├── pickscore_scorer.py
│   This file defines a PickScoreScorer class that utilizes a pre-trained CLIP model to calculate similarity scores between image and text prompts, enabling a pick score assessment for image-text pairs.
├── prompts.py
│   This file defines functions to generate diverse prompts for image generation by loading lines from text files and combining them with random choices and numerical transformations, offering metadata for questions and answers.
├── prpocess.py
│   This script processes a Hugging Face dataset, extracts unique captions with sufficient length, splits them into test and train sets, and saves them as text files for potential use in a downstream task or model training.
├── qwenvl.py
│   This file defines a QwenVLScorer class that uses the Qwen2.5-VL model to evaluate the aesthetic quality of images by generating text with scores based on a given prompt and returning a list of aesthetic quality scores.
├── rewards.py
│   This file defines and contains various reward calculation functions, including remote scoring and single-language reward models, which are used to evaluate generated images based on different metrics and weights during the training process.
├── sd3_pipeline_with_logprob.py
│   This file implements a Stable Diffusion 3 pipeline that incorporates the computation and tracking of log probabilities and KL divergence for advanced sampling and analysis.
├── sd3_sde_with_logprob.py
│   This file implements an SDE step with log probability calculation for flow matching Euler discrete scheduler, adapting a diffusion model approach to calculate the previous sample and log probability during the reverse diffusion process.
├── setup.py
│   This file (setup.py) defines the project's metadata, dependencies, and installation requirements using setuptools, enabling the creation of a Python package for the flow-grpo project.
├── simple_animals.txt
│   This file lists common animal names, likely used for simple classification tasks, dataset creation, or illustrative examples within the project.
├── simple_ocr_animals.txt
│   This file lists simple animal names likely used as training or testing data for OCR tasks within the project.
├── simple_ocr_animals_digit1.txt
│   The file contains a dataset of animal images, each holding a sign with a single digit from 0 to 8, likely for training or testing an OCR model.
├── simple_ocr_animals_digit3.txt
│   The file contains a repetitive sequence of animal images, each holding a sign displaying sequential digits, likely used for OCR training or validation data generation.
├── simple_ocr_animals_digit5.txt
│   The file contains a repetitive sequence of animal descriptions, each holding a sign with a five-digit number, likely serving as training or testing data for an OCR system focused on recognizing digits and associating them with animals.
├── stat_tracking.py
│   This file defines a PerPromptStatTracker class to calculate and track statistics (mean, standard deviation, advantages) for different prompts based on given rewards, and includes a main function for demonstration.
├── test.txt
│   This file (test.txt) contains a collection of diverse and detailed text prompts intended for image generation, likely used to test or demonstrate the capabilities of an AI art generation system or related utility.
├── test_metadata.jsonl
│   This file contains a JSON Lines dataset of image descriptions, used to test and evaluate the project's ability to generate captions or understand visual scenes based on object descriptions, positions, and colors.
├── train.txt
│   This file (train.txt) contains image descriptions used to train a text-to-image model, likely serving as the primary dataset for generating images based on textual prompts.
├── train_dreambooth_lora_sd3.py
│   This file contains functions for encoding text prompts into embeddings using CLIP and T5 models, likely for use in a Dreambooth or LoRA training pipeline involving text-to-image generation.
├── train_metadata.jsonl
│   This file contains training metadata for image generation, detailing object placement, colors, and counts to guide the creation of synthetic training data.
└── train_sd3.py
    This file (train_sd3.py) orchestrates the training process for a Stable Diffusion 3 model, handling data loading, loss calculation, optimization, and logging while interacting with other modules like the accelerator, optimizer, EMA, and pipeline components.
```