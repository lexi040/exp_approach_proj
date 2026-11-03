## Refactored Ternus Experiment 

## Directory Structure

```text
exp_approach_proj/
|── data #not in repo
|── events #not in repo
├── scripts/
│   └── Ternus.py       
├── tests/
│   └── test_exp.py  #automated unit tests using pytest
├── environment.yml  #conda environment specification
├── setup.sh         #automated environment installation
├── run_tests.sh     #automated test runner script
└── README.md        #project documentation

## Environment Setup
1. Clone the repository and navigate to the root directory.
2. Run the automated setup script:
   ```bash
   chmod +x setup.sh
   ./setup.sh
3. Run scripts/Ternus.py to start the experiment 
    ```bash
    GDK_BACKEND=x11 python3 scripts/Ternus.py
    *(on my machine)my Linux distro defaults to Wayland as display server instead of X11, pygame attempts to query GNOME settings schemas assuming that an X11 server is active => schema errors, force run app with the X11 compatibility backend
4. Run unit tests using:
    ```bash
    chmod +x run_tests.sh
    ./run_tests.sh

## References

1. **Roth, J., Wallis, T. S. A., Duan, Y., Mahner, F. P., Kaniuth, P., & Hebart, M. N.** (2025). Ten principles for reliable, efficient, and adaptable coding in psychology and cognitive neuroscience. *Communications Psychology*, 3(1), 62. https://doi.org/10.1038/s44271-025-00236-3

2. **Wilkinson, M. D., Dumontier, M., Aalbersberg, I. J., Appleton, G., Axton, M., Baak, A., Blomberg, N., et al.** (2016). The FAIR Guiding Principles for scientific data management and stewardship. *Scientific Data*, 3(1), 160018. https://doi.org/10.1038/sdata.2016.18