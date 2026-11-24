import laserchicken as lc

# Load data
point_cloud = lc.load("../../testdata/AHN3.ply")

## Normalize data
# Adds the attribute 'normaiized_height' to the point cloud.
# Note that data is added to the given point cloud in place
lc.normalize(point_cloud)

## Filter points inside a polygon
polygon = (
    "POLYGON(( 131963.984125 549718.375000,"
    + " 132000.000125 549718.375000,"
    + " 132000.000125 549797.063000,"
    + " 131963.984125 549797.063000,"
    + " 131963.984125 549718.375000))"
)
point_cloud = lc.select_polygon(point_cloud, polygon)

## Filter points by attribute threshold
points_below_1_meter = lc.select_below(point_cloud, "normalized_height", 1)
points_above_1_meter = lc.select_above(point_cloud, "normalized_height", 1)

# Computer neighbors for every point in the point cloud. This means that the target point cloud should contain the same points as the environment point cloud. The target point cloud contains the point at which the neighbors should be calculated.
# The code below finds for every target point, the neighbors within a Spherical neighborhood with radius of 5 meters.
targets = point_cloud
volume = lc.build_volume("sphere", radius=5)
neighborhoods = lc.compute_neighborhoods(point_cloud, targets, volume)
## Calculate features
lc.compute_features(
    point_cloud, neighborhoods, targets, ["std_z", "mean_z", "slope"], volume
)
# We add 4 parameterized features.
lc.register_new_feature_extractor(
    lc.BandRatioFeatureExtractor(None, 1, data_key="normalized_height")
)
lc.register_new_feature_extractor(
    lc.BandRatioFeatureExtractor(1, 2, data_key="normalized_height")
)
lc.register_new_feature_extractor(
    lc.BandRatioFeatureExtractor(2, None, data_key="normalized_height")
)
lc.register_new_feature_extractor(lc.BandRatioFeatureExtractor(None, 0, data_key="z"))

# Print a list of all available feature names and notice the parameterized features we just registered, 'band_ratio_1<z<2'.
sorted(lc.list_feature_names())

## Recalculate neighbors and calculate the parameterized feature
# Neighbors is a generator and can only be iterated once. 
# We therefore recalculate them here. 
# If we would want to do multiple calculations without recalculating the neighbors, 
# we could copy the neighbors to a list. 
# This is not done by default because neighbors can quickly grow quite large so that available RAM unnecessarily becomes the bottle neck.
cylinder = lc.build_volume("infinite cylinder", radius=5)
neighborhoods = lc.compute_neighborhoods(point_cloud, targets, cylinder)
lc.compute_features(
    point_cloud, neighborhoods, targets, ["band_ratio_1_normalized_height_2"], cylinder
)

## Write result to ply file
lc.export(point_cloud, "my_output.ply")
