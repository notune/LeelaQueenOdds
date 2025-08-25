
# LeelaQueenOdds
This repo contains the network used on the [LeelaQueenOdds Bot on Lichess](https://lichess.org/@/LeelaQueenOdds), which you can [download here lqo_v2.pb.gz](https://github.com/notune/LeelaQueenOdds/releases/download/v2/lqo_v2.pb.gz).

Moreover, it also contains a customizable script that can be used to generate games to train your own odds-network. It supports various engine parameters, node limiting, opening books in FEN format, and automatic Dropbox file uploads. I also provided the configs and resulting training data used for networks v1 and v2.

## Usage / Installation
Simplest way to play against LQO is on Lichess: https://lichess.org/@/LeelaQueenOdds

Disclaimer: Other use-cases such as analysis of normal chess positions, or even playing normal chess against the net is unlikely to work as intended as the net evaluates the queen-odds starting position as completely equal.

### Debian Linux (Ubuntu, Linux Mint, ...)
Execute the following commands:
```
sudo apt update
sudo apt upgrade
sudo apt install ninja-build meson
git clone -b search-contempt --recurse-submodules https://github.com/Naphthalin/lc0.git
./lc0/build.sh
wget -P lc0/build/release/ https://github.com/notune/LeelaQueenOdds/releases/download/v2/lqo_v2.pb.gz
```
the binary will then be located at lc0/build/release/lc0

### Windows
If you have an NVIDIA GPU copy [lc0_sc_cuda.exe](https://github.com/notune/LeelaQueenOdds/releases/download/v2/lc0_sc_cuda.exe) and [install-cuda_12_9.cmd](https://github.com/notune/LeelaQueenOdds/releases/download/v2/install-cuda_12_9.cmd) into a new folder and double-click the install-cuda file.

Otherwise download [lc0_win_sc_cpu.zip](https://github.com/notune/LeelaQueenOdds/releases/download/v2/lc0_win_sc_cpu.zip) and unpack the file.

Then download the LeelaQueenOdds net: [lqo_v2.pb.gz](https://github.com/notune/LeelaQueenOdds/releases/download/v2/lqo_v2.pb.gz) and copy it into the folder with lc0.exe.

### Settings

Use the following settings when playing against the net: (The most important settings are ScLimit and SwapColors, ScLimit has to be set when searching for more then 1k nodes, and SwapColor is the only way to make it play as Black with reasonable strength).

**When playing as Black (LQO plays White)**:
Node limit (configure in chess gui): 15000
```
WeightsFile: lqo_v2.pb.gz
ScLimit: 40
CPuct: 1.5
FpuValue: 0.4
DrawScore: -0.4
```
**When playing as White (LQO plays Black)**:
Node limit (configure in chess gui): 12000
```
WeightsFile: lqo_v2.pb.gz,
SwapColors: true
ScLimit: 32
CPuct: 1.5
FpuValue: 0.4
DrawScore: 0.6
```

## Training
Detailed instructions on how to train your own odds-network can be found [here](training/README.md).

## Acknowledgments
This project wouldn't be possible without the help from these people and projects:
- [The Leela Chess Zero Engine](https://github.com/LeelaChessZero/lc0)
- [Marcogio9](https://github.com/Marcogio9/) made the initial [KnightOdds Network](https://github.com/Marcogio9/LeelaKnightOdds), inspired me to train my own queen-odds-net, and helped me a lot by providing me both the right engine configs to create the games, as well as the right training config, and answering any questions I had to be able to finish this project
- [Naphthalin](https://github.com/Naphthalin) and [Hissha](https://www.chess.com/member/hissha) who answered any questions I had on the Leela Chess Zero discord server and helped me evaluate this network as well as find the right settings
- [Maia1900, the human-like chess network](https://github.com/CSSLab/maia-chess) used to create training data for this net
- [Maia2200 from CallOn84](https://github.com/CallOn84/LeelaNets) used for testing the network
- [python-chess](https://github.com/niklasf/python-chess) used for generating games with the script
- [Chris Whittington](https://github.com/ChrisWhittington/Chess-EPDs) for the Queen Odds opening book
- [amjshl](https://github.com/amjshl/lc0_v31_sc) implemented search contempt for lc0, which improves lqo's elo by another +200.
- [tiiber](https://github.com/dedekindcut) for sponsoring over 200$ in vast.ai compute for lqo_v3 (wip)

## License 
This project is licensed under the **GNU AGPLv3** License, which you can read here: [LICENSE](LICENSE).
