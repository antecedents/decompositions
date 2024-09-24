<br>

## Environments

### Remote Development

For this Python project/template, the remote development environment requires

* [Dockerfile](.devcontainer/Dockerfile)
* [requirements.txt](.devcontainer/requirements.txt)

An image is built via the command

```shell
docker build . --file .devcontainer/Dockerfile -t uncertainty
```

On success, the output of

```shell
docker images
```

should include

<br>

| repository   | tag    | image id | created  | size     |
|:-------------|:-------|:---------|:---------|:---------|
| uncertainty  | latest | $\ldots$ | $\ldots$ | $\ldots$ |


<br>

Subsequently, run a container, i.e., an instance, of the image `uncertainty` via:

<br>

```shell
docker run --rm -i -t -p 127.0.0.1:8000:8000 -w /app --mount
    type=bind,src="$(pwd)",target=/app uncertainty
```


<br>

Herein, `-p 8000:8000` maps the host port `8000` to container port `8000`.  Note, the container's working environment,
i.e., -w, must be inline with this project's top directory.  Additionally,

* --rm: [automatically remove container](https://docs.docker.com/engine/reference/commandline/run/#:~:text=a%20container%20exits-,%2D%2Drm,-Automatically%20remove%20the)
* -i: [interact](https://docs.docker.com/engine/reference/commandline/run/#:~:text=and%20reaps%20processes-,%2D%2Dinteractive,-%2C%20%2Di)
* -t: [tag](https://docs.docker.com/get-started/02_our_app/#:~:text=Finally%2C%20the-,%2Dt,-flag%20tags%20your)
* -p: [publish the container's port/s to the host](https://docs.docker.com/engine/reference/commandline/run/#:~:text=%2D%2Dpublish%20%2C-,%2Dp,-Publish%20a%20container%E2%80%99s)

<br>

Get the name of the running instance of ``uncertanty`` via:

```shell
docker ps --all
```

Never deploy a root container, study the production [Dockerfile](Dockerfile); cf. [/.devcontainer/Dockerfile](.devcontainer/Dockerfile)

<br>

### Remote Development & Integrated Development Environments

An IDE (integrated development environment) is a helpful remote development tool.  The **IntelliJ
IDEA** set up involves connecting to a machine's Docker [daemon](https://www.jetbrains.com/help/idea/docker.html#connect_to_docker), the steps are

<br>

> * **Settings** $\rightarrow$ **Build, Execution, Deployment** $\rightarrow$ **Docker** $\rightarrow$ **WSL:** {select the linux operating system}
> * **View** $\rightarrow$ **Tool Window** $\rightarrow$ **Services** <br>Within the **Containers** section connect to the running instance of interest, or ascertain connection to the running instance of interest.

<br>

**Visual Studio Code** has its container attachment instructions; study [Attach Container](https://code.visualstudio.com/docs/devcontainers/attach-container).


<br>
<br>

## Code Analysis

The GitHub Actions script [main.yml](.github/workflows/main.yml) conducts code analysis within a Cloud GitHub Workspace.  Depending on the script, code analysis may occur `on push` to any repository branch, or `on push` to a specific branch.

The sections herein outline remote code analysis.

<br>

### pylint

The directive

```shell
pylint --generate-rcfile > .pylintrc
```

generates the dotfile `.pylintrc` of the static code analyser [pylint](https://pylint.pycqa.org/en/latest/user_guide/checkers/features.html).  Analyse a directory via the command

```shell
python -m pylint --rcfile .pylintrc {directory}
```

The `.pylintrc` file of this template project has been **amended to adhere to team norms**, including

* Maximum number of characters on a single line.
  > max-line-length=127

* Maximum number of lines in a module.
  > max-module-lines=135


<br>


### pytest & pytest coverage

The directive patterns

```shell
python -m pytest tests/{directory.name}/...py
pytest --cov-report term-missing  --cov src/{directory.name}/...py tests/{directory.name}/...py
```

for test and test coverage, respectively.


<br>


### flake8

For code & complexity analysis.  A directive of the form

```bash
python -m flake8 --count --select=E9,F63,F7,F82 --show-source --statistics src/data
```

inspects issues in relation to logic (F7), syntax (Python E9, Flake F7), mathematical formulae symbols (F63), undefined variable names (F82).  Additionally

```shell
python -m flake8 --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics src/data
```

inspects complexity.

<br>
<br>

## References

* [Accident & Emergency](https://publichealthscotland.scot/our-areas-of-work/acute-and-emergency-services/urgent-and-unscheduled-care/accident-and-emergency/overview/#section-1)
* [Scottish Health and Social Care Open Data](https://www.opendata.nhs.scot/dataset)
  * [Weekly A&E Activity and Waiting Times](https://www.opendata.nhs.scot/dataset/weekly-accident-and-emergency-activity-and-waiting-times)
  * [Hospital Codes](https://www.opendata.nhs.scot/dataset/hospital-codes)
  * [Population Estimates](https://www.opendata.nhs.scot/dataset/population-estimates)
* [Assessment of Accident and Emergency (A&E) Activity Statistics in Scotland](https://osr.statisticsauthority.gov.uk/publication/assessment-of-accident-and-emergency-ae-activity-statistics-in-scotland/)

* [Notation: State Space Model, Kalman Filter](https://dismalpy.github.io/user/ssm/2-state_space_models.html)
* [<abbr title="Markov Chain Monte Carlo">MCMC</abbr> Convergence Diagnostic](https://search.r-project.org/CRAN/refmans/LaplacesDemon/html/Gelman.Diagnostic.html)
* [Convergence and efficiency diagnostics for Markov Chains](https://mc-stan.org/rstan/reference/Rhat.html)
* [Effective Sample Size (ESS) due to Autocorrelation](https://search.r-project.org/CRAN/refmans/LaplacesDemon/html/ESS.html)
* [<abbr title="Monte Carlo Standard Error">MCSE</abbr>: Equation & References](https://search.r-project.org/CRAN/refmans/LaplacesDemon/html/MCSE.html)

<br>
<br>

<br>
<br>

<br>
<br>

<br>
<br>
