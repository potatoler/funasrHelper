# funasrHelper

Utilities and alternative scripts for [FunASR](https://github.com/modelscope/FunASR) model training.

This repo is originally created as a lifeline for those who lose their way in the TGU FunASR homework.

If my code helps you, please don't hesitate to give me a star.

## What are in this repo?

**Data processing tools** to satisfy funasr's requirement for training and evaluation data. [THCHS-30](https://www.openslr.org/18/) dataset is used as an example. You may need to change some of the code to use with your own dataset and I belive you can make it.

- `addNoise.py` is an alternative to THCHS-30's noise adding script.

- `processData.py` transfer .wav and .wav.trn files to a .scp file and a .txt file.

**Alternative shell scripts** which are a slightly modified version of those in the FunASR repo. I write some comments in the code as well as a minimal manual below to give a guide for the parameters. The FunASR doc literally tells nothing about how to set parameters.

- `finetune.sh` to finetune a model with your dataset.
- `infer_from_local.sh` for inference on your dataset.

**A fun toy** to evaluate the model.

- `calculate.py` to compare your model's prediction and the original audio script and calculate wer as well as some other figures.

## Data Preprocessing

There are two scripts for this section and they're nearly ready to go. All you have to do is specifying some variables in the scripts.

### Adding noise

| Variable in code | Description                        |
| ---------------- | ---------------------------------- |
| `data_dir`       | Directory of your clean audio data |
| `noise_file`     | Path to your noise data            |

**Usage:** Specify the variables in `addNoise.py` and run.

The script **only process wav files**, you need to modify the implement if your dataset audio is not in wav format. In THCHS-30, audio files have suffix .wav and transcript files have suffix .wav.trn, and this script can ignore the transcript file so you could feel free to use.

### Formatting your data

| Variable in code | Description                         |
| ---------------- | ----------------------------------- |
| `data_dir`       | Directory of your audio             |
| `output_dir`     | Directory to output formatted files |

**Usage:** Specify the variables in `processData.py` and run.

When training with local data, FunASR may ask you to use specific format of traning data. The [official training example](https://github.com/modelscope/FunASR/blob/main/examples/industrial_data_pretraining/paraformer/finetune.sh) shows that you need to format your data to an index of audio file (scp) and an list of texts like:

audio.scp

```
C21_517 train/C21_517.wav
C6_639 train/C6_639.wav
...
```

scripts.txt

```
C21_517 他 曾 为 ⽕药 仓库 研究 避雷 装置 为 国家 造 币 ⼚ 研究 减少 ⾦币 磨损 消耗 的 办法
C6_639 檀 野 麻⼦ 骂 笠 冈 窝囊 笠 冈 也 认为 ⾃⼰ 对 松 野 泰 造 之 死 负有 不可 推卸 的 责任
...
```

The scp and txt file are defaultly named "audio.scp" and "scripts.txt" as shown above. You can customize the file name by modifying variable `wav_scp_path` and `text_scp_path` in `processData.py` .

## Model Training and Inference

It's recommended to use **a full clone of the FunASR repo** rather than an installation via package managers to do this section. The shell scripts I provided are a modified version of the original scripts which are deep in the repo. Precisely, in `examples/industrial_data_pretraining/paraformer` if you finetune a  pre-trained paraformer model (like what I did).

Also in this section if you want to use the hyper-parameters the same as mine, you can directly go to the shell scripts without the manual below. I kept the comments from the ali-damo team and also left some comments there signed as `[potatoler]` .

### Training model with local datasets

| Variable                  | Description                                                  |
| ------------------------- | ------------------------------------------------------------ |
| `model_name_or_model_dir` | Use option 1 of the `finetune.sh` and specify a model name for auto-downloading or directory for a local model. |
| `scp_file_list`           | Sepecify the scp and txt file made in the last section, or you can rename those file and move to the path in the code. (the latter is recommended) |

> [!IMPORTANT]
>
> `scp_file_list` variable is considered as parameters passed to the scp2json tool. For train_data and val_data you need to separately specify this variable to match your training data and evaluation data.

For optinal variables you could take the [official doc](https://github.com/modelscope/FunASR/tree/main/examples/industrial_data_pretraining/paraformer#detailed-parameter-description) as a reference. Here are some additional info:

- `dataset_conf.batch_size` should be set together with `dataset_conf.batch_type`, as the latter is the unit of the former.
- Recklessly use a large number for `dataset_conf.num_workers` might slow the training speed.
- `train_conf.validate_interval` and `train_conf.save_checkpoint_interval` are counted by **steps** rather than epochs. The number of steps is related to the batch size you set.

- The training code save a checkpoint every epoch, and this is parallel with checkpoint save controlled by `train_conf.save_checkpoint_interval`. If you want the trainer to save less checkpoints you can simply modify the training code which is in `funasr/bin/train_ds.py` of the FunASR repo.

**Usage:** Specify the variables in `finetune.sh`, replace the original script and run.

### Model inference

| Variable                    | Description                                           |
| --------------------------- | ----------------------------------------------------- |
| `input`                     | Path to your test data scp.                           |
| `output_dir`                | Directory where model outputs its prediction.         |
| `workspace`                 | Directory of your FunASR repo clone.                  |
| `device`                    | Detailed in the comment.                              |
| `config`                    | File name of model config file, usually `config.yaml` |
| `config-path`               | Directory of model config file.                       |
| `init_param`                | Path to specific model checkpoint.                    |
| `tokenizer_conf.token_list` | Detailed in the comment.                              |
| `frontend_conf.cmvn_file`   | Detailed in the comment.                              |
| `batch_size`                | Batch size by sample.                                 |

Here are some tips:

- `workspace` can be automatically set to your shell working directory. To enable this function you would delete the workspace setting in **line 13**.

- A cuda device is not necessary for inference but recommended.

- To inference with your original pre-trained model parameters you could find the parameters in your model directory.
- `tokenizer_conf.token_list` and `frontend_conf.cmvn_file` path can be found in the model config file.

- `batch_size` is by sample (track), not token. Use a smaller value to avoid OOM.

**Usage:** Specify the variables in `infer_from_local.sh`, replace the original script and run.

## Evaluation

It is recommended to write your own evaluation code, as opinions on how to evaluate a model's performance might be different. The evaluation code I provided is considered as a prank or a toy. It mimic the evaluation system of the rhythm game [Arcaea](https://arcaea.lowiro.com/zh).

### Utilities

Though it's not recommended to use the toy code, some useful functions are exposed and could be imported as utilities to build your own code.

```python
remove_key_and_space(
    line: str,
    remove_space: bool = True
) -> str
```

Remove the key at the beginning of a line of the model's prediction file.

`line`: a string, the line to be processed

`remove_space`: a bool, whether to remove spaces in prediction content

return a string, the prediction content.

```python
compare_lines(
    pred_line: str,
    tag_line: str
) -> tuple[int, int]
```

Compare a raw prediction line with a raw audio script line.

`pred_line` and `tag_line`: two strings, two **raw** lines to compare

return a tuple, error counts and max length of the two line.

> [!WARNING]
>
> It may cause unexpected behaviors if not use RAW lines (with out key removing) for this function

### Performance Evaluation

| Variable        | Description                           |
| --------------- | ------------------------------------- |
| `pred_filename` | Path to your model's prediction file. |
| `tag_filename`  | Path to your evaluation text file.    |

Model's prediction on each track will be classified by word error rate on the track

| Class | wer             | Description                                          |
| ----- | --------------- | ---------------------------------------------------- |
| PURE  | $<10 \%$        | Pure prediction which is close to the original text. |
| FAR   | $>10\%\ ,<30\%$ | A prediciton far from the original text.             |
| LOST  | $>30\%$         | Bad prediction which loses original information.     |

Along with wer, some other figures are calculated to evaluate to model, including count of PURE, FAR, and LOST, and accept rate.

Accept rate is calculated as:

![acc](https://s2.loli.net/2025/04/11/aMDLviCj8gPnToQ.png)