# Copyright FunASR (https://github.com/alibaba-damo-academy/FunASR). All Rights Reserved.
#  MIT License  (https://opensource.org/licenses/MIT)

# method2, inference from local model

# for more input type, please ref to readme.md
input="path to your evaluate scp file"
output_dir="./outputs/eval"

workspace=`pwd`
# [potatoler] I strongly recommend you NOT to use the above workspace!
# [potatoler] Set your own workspace like:
workspace="where you clone the FunASR repo"

# download model
# local_path_root=${workspace}/modelscope_models
# mkdir -p ${local_path_root}
# local_path=${local_path_root}/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch
# git lfs clone https://www.modelscope.cn/damo/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch.git ${local_path}

device="cuda:0" # "cuda:0" for gpu0, "cuda:1" for gpu1, "cpu"

config="config.yaml"

# [potatoler] the inference script is set as "funasr.bin.inference" to use a downloaded funasr package
# [potatoler] if you want to use an edited script in the repo, please set it like following:
python ${workspace}/FunASR/funasr/bin/inference.py \ 
--config-path "DIR to your model config" \
--config-name "${config}" \
++init_param="should be a model.pt file" \
++tokenizer_conf.token_list="check in your model config file" \
++frontend_conf.cmvn_file="check in your model config file" \
++input="${input}" \
++output_dir="${output_dir}" \
++device="${device}" \
++batch_size=512 \
# [potatoler] the indefence script defaultly use 4 thread
# [potatoler] I DO NOT recommend to use more thread for inference, as it will rather slow down the speed
# [potatoler] if you do want to use more thread, please set it like following:
# ++ncpu=28 \