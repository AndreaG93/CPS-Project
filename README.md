# CPS-Project A.A. 2020/2021 - Global Climate Change Data

Andrea Graziani - (0273395)

## Requirements

This application requires Python <code>3.x</code> and it depends on **Classic Jupyter Notebook**. In order to execute
this application, following python package **must** be installed:

1. <code>ipywidgets</code>
2. <code>numpy</code>
3. <code>pandas</code>
4. <code>matplotlib</code>
5. <code>notebook</code>
6. <code>requests</code>

On Ubuntu 21.04, you can install them, using following command:

```
pip3 install ipywidgets numpy pandas matplotlib notebook requests
```

While, on Windows 10:

```
pip install ipywidgets numpy pandas matplotlib notebook requests
```      

All required dataset files are already included inside <code>./data</code> directory. This dataset was downloaded from
[here](https://data.world/data-society/global-climate-change-data).

To properly display all  widgets belonging to ``ipywidgets`` package, we recommend the use of [Mozilla Firefox](https://www.mozilla.org/it/firefox/) (``v89.0``).  (Chromium-based Microsoft Edge and Google Chrome have some problems with ``ipywidgets``).

**Update 20-07-2021**

Due to Git LFS limitations on GitHub, all needed datasets were been removed from this repository. In order to use this application, you must donwload them from
[here](https://data.world/data-society/global-climate-change-data) and put them inside <code>./data</code> directory.

## How to run

To execute this program simply open <code>CPS.ipynb</code> file using the following command at the *Terminal* (Linux)
or *Command Prompt* (Windows):

```
git clone https://github.com/AndreaG93/CPS-Project
cd ./CPS-Project
jupyter notebook ./CPS.ipynb
```  

## Description

For a detailed description about this application, see the [Report](https://github.com/AndreaG93/CPS-Project/blob/main/report/Report.pdf)!.
