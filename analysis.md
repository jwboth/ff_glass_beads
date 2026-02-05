# Data and Image Analysis
Once calibrated, DarSIA can assist in various data analysis procedures. This list shows a complete overview of the general capabilities. Custom routines may be required to answer specific questions based on interpretations of the images, e.g., CO2 mass map or gas/aqueous segmented phases.

## The main run script
All analysis steps in this overview are controlled via the script `scripts/analysis.py` and different flags control which analysis routine is envoked.

## Config files
Again, the routines will require a config file to steer the analysis step in addition to common items already used during setup and calibration. In this overview, we will use an additional config file for the analysis steps, here referred to as `analysis.toml`, cleanly separated from the common and run-specific config files. This allows to again reuse the same analysis config file across different runs.

A central item for all steps is the `analysis.toml` file are the `[analysis.data.image_time_interval.TEXT]` sections, used to define the actual data to be analysed. This section is used across all presented analysis steps.

## Cropping raw images
For presentation purposes it is helpful to just geometrically process the raw images into the main ROI. This step is here referred to as 'cropping'. Use the flag `--cropping` to invoke cropping of the chosen images (see above):

```python
python scripts/analysis --cropping --config config_example/single/common.toml config_example/run/run_XYZ.toml config_example/single/analysis.toml
```
<button onclick="navigator.clipboard.writeText('python scripts/analysis --cropping --config config_example/single/common.toml config_example/run/run_XYZ.toml config_example/single/analysis.toml')">
Copy command
</button>


## Mass 
The calibrated mass analysis can be applied to batches of images and convert images to spatial mass maps. These will be stored as `npz` files in your common `results` folder. These files cannot be investigated visually but provide the basis for further analysis. Note that the step of converting an image to its mass interpretation is costly and thus should be considered to be performed only once for multiple analysis steps (detailed in the notebook on post-analysis).

```bash
python scripts/analysis --mass --config config_example/single/common.toml config_example/run/run_XYZ.toml config_example/single/analysis.toml
```
<button onclick="navigator.clipboard.writeText('python scripts/analysis --mass --config config_example/single/common.toml config_example/run/run_XYZ.toml config_example/single/analysis.toml')">
Copy command
</button>

It is possible to restrict the mass analysis to regions of interest (ROI). For this, in the config file, one can add as many sections `[analysis.mass.roi.TEXT]` with separate identifiers `TEXT` of the form:

```toml
[analysis.mass.roi.box2]
name = "Box 2"
corner_1 = [1.45, 0.0]
corner_2 = [2.745, 1.5]
```





## Segmentation
```bash
python scripts/analysis --segmentation --config config_example/single/common.toml config_example/run/run_XYZ.toml config_example/single/analysis.toml
```
<button onclick="navigator.clipboard.writeText('python scripts/analysis --segmentation --config config_example/single/common.toml config_example/run/run_XYZ.toml config_example/single/analysis.toml')">
Copy command
</button>