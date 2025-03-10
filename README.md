# LightingInWhy3

The code, proofs, and simple payment test are packaged in a docker image to
simplify cross-platform proof verification without the need to set up the Why3
development environment.

Regarding proof verification, note that `why3 replay` reads the source code
(i.e., `*.mlw` files) to generate verification conditions and then it runs
transformations and the appropriate prover for each based on information in
`why3session.xml` and `why3shapes.gz`. Two python scripts are run:
`checkAllFilesHaveProof.py` verifies that whyML files and proofs correspond
1-to-1 (needed because why3 does not prove `*.mlw` files that appear in the
directory but not in `why3session.xml`), while `checkStatementProofConv.py`
verifies the Statement-Proof separation convention (explained at the beginning
of the module `closingWorksLemmas` in `honestPartyVsAdversary.mlw`).

The simple payment test is defined in `src/twoHonestParties.mlw` and checks the
liveness of a basic usage scenario: Two honest parties can open a channel and
use it to perform a payment.

## Setup

[Install docker](https://docs.docker.com/engine/install/).

If you want to avoid giving docker root access, [rootless
mode](https://docs.docker.com/engine/security/rootless/) is sufficient.
Furthermore, to increase your security, you can run the docker daemon with the
following options, or add them to the docker config file:
- `--icc=false`: disable inter-container communication
- `--userns-map`: remap container users to not match host users, so that even if
  a user escapes the container, they cannot run anything in the host

## Verify proofs and run simple payment test

Run from repository root:
```bash
docker build --tag proofs .
docker run --cap-drop all --security-opt=no-new-privileges --cpus=3 --memory=4g --rm proofs:latest
```

The first three flags add security (so you don't have to trust us):
- `--cap-drop`: drop all container capabilities
- `--security-opt=no-new-privileges`: block enabling new privileges from within
  the container

The next two flags set the maximum CPU cores and RAM that the container is
allowed to use. These resources should be enough to execute all tasks — users
should make sure that their system can provide them.

The last flag, `--rm`, removes resulting container after use.

**Important**: There is no option to fix the docker randomness, therefore proofs
might time out. Please rerun the container (`docker run ...`) if this happens.

Cleanup:
```bash
docker image rm proofs
```

## Recreate the proof tree

The proof tree are the transformations applied to the proof goals and are stored in the file `src/why3shapes.gz`.
Note that recreating the proof tree is only needed after modifying the code, as the released version of the repository comes equipped with an up-to-date proof tree.
In particular, recreating the proof tree is not required to replay the proofs.

Steps to recreate the proof tree:
1. Start the Why3 IDE (`./run.sh`).
1. Apply the Crush strategy to each top-level goal — this should handle most of the goals.
1. Each remaining goal is commented with a transformation in the .mlw file.
   Apply this transformation to each goal, removing possible nested splits introduced by Crush.
1. Unless instructed otherwise by the comments, apply Crush to each resulting goal after the transformation.

The Why3 IDE might prove a goal in multiple ways. Unfortunately this can make
replaying proofs unstable, as some ways can time out only in some proof runs.
To make the proof replays more stable after recreating the proof tree, follow
these extra steps:
1. Run `cleanProofTree.py` with Python, which keeps only one way to prove each
   goal (with a preference for transformations over provers, as the latter tend
   to reduce the subsequent work the provers need to do, thus making timeouts
   less likely).
1. Start the IDE (`./run.sh`) and rerun the proofs of all files with "Replay
   valid obsolete proofs" (keyboard shortcut "R"), which refreshes the
   `why3shapes.gz` file and removes warnings about "obsolete" proofs.

The proofs can be replayed outside Docker with `./replay.sh`.

## Run simple payment test without docker

Run `./test.sh` from the repository root. This script extracts executable ocaml code from `src/twoHonestParties.mlw`, compiles it and runs the result.

## Structure of the project
Below we list all relevant files (in a top-down order) together with
brief descriptions of their contents. For more information, please refer
to the comments at the beginning of each file:
1. `honestPartyVsAdversary.mlw` -- Definition of the security model. Definition and proof of funds security.
1. `twoHonestParties.mlw` -- Definition of the simple test for progress: two honest parties exchange messages with each other. It is only used in tests, and is not a part of the formal proof of funds security.
1. `honestPartyInteraction.mlw` -- Our provably secure implementation of an honest LN party. Proof that it satisfies the interface from `honestPartyInterface.mlw`.
1. `honestPartyType.mlw` -- The internal types and invariants used in our implementation of an honest LN Party.
1. `honestPartyInterface.mlw` -- Definition of an abstract interface for an LN client, including types, functions and properties. It is shown in `honestPartyVsAdversary.mlw` to guarantee funds security.
1. `gamma.mlw` -- Our modeling of Bitcoin. Definition of the evaluator function.
1. `signaturesFunctionality.mlw` -- Our modeling of signatures.
1. `basicTypes.mlw` -- Definitions of types (and basic functions about them) used throughout the project.
1. `listLibrary.mlw` -- Basic functions about lists and lemmas about them.
