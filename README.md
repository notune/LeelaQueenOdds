
# LeelaQueenOdds
This repo contains the network used on the [LeelaQueenOdds Bot on Lichess](https://lichess.org/@/LeelaQueenOdds), which you can download [here](lqo_v2.pb.gz).

Moreover, it also contains a customizable script that can be used to generate games to train your own odds-network. It supports various engine parameters, node limiting, opening books in FEN format, and automatic Dropbox file uploads. I also provided the configs and resulting training data used for networks v1 and v2.

## Usage
Download the v2 network from [here](lqo_v2.pb.gz) and install it by following the instructions [here](https://lczero.org/play/quickstart/). Make sure to limit the node count of this network to a maximum of `1000` nodes or lower to avoid that the net searches for positions that a human will be unlikely to find, making it less effective at playing odds games. Based on some tests against `maia-2200` we set the node limit on the lichess bot to `800`.

## Training
Detailed instructions on how to train your own odds-network can be found [here](training/README.md).

## Acknowledgments
This project wouldn't be possible without the help from these people and projects:
- [The Leela Chess Zero Engine](https://github.com/LeelaChessZero/lc0)
- [Marcogio9](https://github.com/Marcogio9/) who made the initial [KnightOdds Bot](https://github.com/Marcogio9/LeelaKnightOdds), inspired me to train my own queen-odds-net, and helped me a lot by providing me both the right engine configs to create the games, as well as the right training config, and answering any questions I had to be able to finish this project
- [Naphthalin](https://github.com/Naphthalin) and [Hissha](https://www.chess.com/member/hissha) who answered any questions I had on the lichess discord server and helped me evaluate this network as well as find the right settings
- [Maia1900, the human-like chess network](https://github.com/CSSLab/maia-chess) used to create training data for this net
- [Maia2200 from CallOn84](https://github.com/CallOn84/LeelaNets) used for testing the network
- [python-chess](https://github.com/niklasf/python-chess) used for generating games with the script
- [Chris Whittington](https://github.com/ChrisWhittington/Chess-EPDs) for the Queen Odds opening book

## License 
This project is licensed under the **GNU AGPLv3** License, which you can read here: [LICENSE](LICENSE).
