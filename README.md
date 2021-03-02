# masters_project_mpb
Simulation of photonic crystals using Meep / MPB.

## Recommended Configuration

Installation of *Meep* and *MPB* on Linux (tested on Ubuntu and Debian) using Anaconda or Miniconda Python distribution. From  [mpb.readthedocs.io](https://meep.readthedocs.io/en/latest/Installation/#conda-package):

> The **recommended** way to install PyMeep is using the [Conda](https://conda.io/docs/) package manager. The precompiled binaries run as *fast or faster* than the typical build from source, are simple to install, can be  upgraded easily, and take advantage of newer compilers and dependencies  than those available in typical systems

The following installation command was recommended at the time this repo was created.

```bash
conda create -n mp -c conda-forge pymeep
```

