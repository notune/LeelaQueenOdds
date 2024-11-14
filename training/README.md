# How to train your own odds network
1. Install libraries with `pip install chess dropbox` (dropbox is optional)
2. Generate training data using the `generate_games.py` script in the `training` folder. Depending on your exact odds, you will have to make some adjustments to the `config_v0.json` file. The v0 file contains the exact configuration I used for the first version of this network. You will have to adjust the fen position or use an opening book, and adjust the settings such that you end up getting games with good variability and a win-rate of slightly more than 50%. I recommend generating 130k games for each of the iterations. Once you have the right configuration, start the script with:
```
python generate_games.py -c config_v0.json
```
3. Now convert the pgn into training-data using the [training-data tool](https://github.com/DanielUranga/trainingdata-tool).
4. Download the [base-network T82](https://storage.lczero.org/files/768x15x24h-t82-swa-7464000.pb.gz)
5. Install tensorflow for executing training code, for me it was tf-2.10. Make sure you have miniconda installed and run:
```
conda create -n tf_210 python=3.10
conda activate tf_210
conda install tensorflow-gpu==2.10.0
pip install tensorflow-addons==0.20.0
pip install pyyaml
```
this should install all the libraries including the right cuda and cudnn libraries. Then bind these libraries with:
```
conda install -c nvidia cuda-nvcc --yes
# Configure the XLA cuda directory
mkdir -p $CONDA_PREFIX/etc/conda/activate.d
printf 'export XLA_FLAGS=--xla_gpu_cuda_data_dir=$CONDA_PREFIX/lib/\n' >> $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
source $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
# Copy libdevice file to the required path
mkdir -p $CONDA_PREFIX/lib/nvvm/libdevice
cp $CONDA_PREFIX/lib/libdevice.10.bc $CONDA_PREFIX/lib/nvvm/libdevice/ 
```
then clone the training code and compile protobuf files:
```
git clone https://github.com/LeelaChessZero/lczero-training.git
cd lczero-training/libs
git clone https://github.com/LeelaChessZero/lczero-common.git
cd ..
./init.sh
```
and convert the base model for training:
```
python net_to_model.py --ignore-errors --cfg=training/768x15x24h-t80_lqo.yaml net/768x15x24h-t82-swa-7464000.pb.gz
```
edit the `input-path` of the yaml config, so that it points to your training-data generated earlier with the trainingdata-tool. and edit `path` to point to where the converted base model is. Make sure you see in console output that it gets loaded, otherwise it will train from scratch.
then start training with:
```
python train.py --cfg training/768x15x24h-t80_lqo.yaml
```
Once its done you should have `QUEEN_ODDS-swa-10000.pb.gz` file in your `path`. You should also have a non-swa version, but I recommend using that version.

Then repeat this process once but this time use the newly created network for generating games. I used the config_v1, but again, depending on your odds you might want to generate games against another opponent or with other settings. For the second training run, skip converting the net_to_model.py and, only change the data in the input-path, as it will then automatically resume training from your latest checkpoint.
