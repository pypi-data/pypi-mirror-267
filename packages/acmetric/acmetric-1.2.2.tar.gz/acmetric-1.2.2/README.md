<a href='https://acmetric.com/' target='_blank'><img src='https://i.postimg.cc/ZnscgcFb/Acmetric-Social-3.jpg' height="100" border='0' alt='Acmetric-Social-3'/></a> 
# Introducing ACMetric package! :tada:
### Current version: `1.2.2`

:chart_with_upwards_trend: This package is created to help you use ACMetric's brand colors and build plots without hours of tuning. Enjoy!

## Installing on a local machine :computer:
Run this command in your local machine's terminal:
```bash
python3 -m pip install git+https://github.com/ACMetric/acmetric_package.git
```
<p align="right">Press here to copy :point_up_2: &ensp; </p>

>:heavy_exclamation_mark:If it doesn't work, run:
>```bash
>python3 -m pip install git+https://username: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@github.com/ACMetric/acmetric_package.git
>```
>
>:heavy_exclamation_mark:If the package is installed, but can't be imported, delete it (`pip unistall acmetric`) and run:
>```bash
>python3 -m pip install --upgrade pip setuptools wheel
>```
>and then repeat the installation procedure.
>
To update, run:
```bash
python3 -m pip install git+https://github.com/ACMetric/acmetric_package.git --upgrade
```

## Installing on Google Colab :orange_book:
Setting up in Google Colab is described [here](https://github.com/ACMetric/acmetric_package/blob/master/colab_setup.md).

## Importing :rocket:
I recommend importing it along with `matplotlib` and `seaborn`.

```python3
%matplotlib inline # display plots in the notebook right away
%config InlineBackend.figure_format='retina' # high resolution
import matplotlib.pyplot as plt
import seaborn as sns
import acmetric as ac
```

And it is ready to go! :sunglasses:

### :mag_right: You can find code examples here: [Jupyter](https://github.com/ACMetric/acmetric_package/blob/master/notebooks/acmetric_package_intro.ipynb) | [Google Colab](https://colab.research.google.com/drive/14eYxEthMcPohkTFC9CLhe-nzHbQDoEsu?usp=sharing)
***
## Some things you need to know :teacher:

 `ac.display_colors()` will show you a table with all the colors available and their names.

`ac.colors` module contains ACMetric colors, you can access them by writing `ac.colors.coral`, `ac.colors.sky_60`, etc.  

`ac.palette` is a `matplotlib` color palette. You can call it and choose a color you like by index, e.g. `ac.palette[3]`.

`ac.cmap` is a gradient colormap that can be used in `seaborn` heatmap and other plots.

Now 4 kinds of plots are available in the package: bar chart, pie chart, scatter plot and box plot. You can make them using `ac.bar`, `ac.pie`, `ac.scatter` and `ac.box`. All the possible parameters can be found in the docstring.

**Note:** it doesn't mean you can't build other kinds of plots. Just import `matplotlib` or `seaborn`, and all the plots you create will also be ACMetric branded!
